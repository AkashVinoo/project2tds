from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import json
import re
import duckdb
import os
from typing import List, Dict, Any, Optional
import asyncio
import aiohttp
from datetime import datetime
import logging
from io import StringIO

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom JSON encoder to handle numpy types
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.Series):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

app = FastAPI(title="Data Analyst Agent", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataAnalystAgent:
    def __init__(self):
        self.session = None
    
    async def get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close_session(self):
        if self.session:
            await self.session.close()
            self.session = None
    
    def extract_urls_from_text(self, text: str) -> List[str]:
        """Extract URLs from text using regex"""
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        return re.findall(url_pattern, text)
    
    def extract_questions_from_text(self, text: str) -> List[str]:
        """Extract numbered questions from text"""
        # Look for numbered questions (1., 2., etc.)
        question_pattern = r'\d+\.\s*([^?\n]+[?])'
        questions = re.findall(question_pattern, text, re.IGNORECASE | re.MULTILINE)
        
        # Also look for questions without numbers
        general_question_pattern = r'([A-Z][^.!?]*[?])'
        general_questions = re.findall(general_question_pattern, text)
        
        return questions + general_questions
    
    def scrape_data_from_url(self, url: str) -> pd.DataFrame:
        """Generic data scraping from any URL"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Try to read tables from the page
            try:
                tables = pd.read_html(StringIO(response.text))
                if tables:
                    df = tables[0]  # Take the first table
                    # Clean column names
                    df.columns = [str(col).strip() for col in df.columns]
                    return df
            except Exception as e:
                logger.warning(f"Could not read tables from {url}: {e}")
            
            # If no tables found, try to extract structured data
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for JSON-LD structured data
            json_ld_scripts = soup.find_all('script', type='application/ld+json')
            for script in json_ld_scripts:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, list) and data:
                        # Convert to DataFrame
                        df = pd.json_normalize(data)
                        return df
                except:
                    continue
            
            # If still no data, return empty DataFrame
            return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"Error scraping data from {url}: {e}")
            return pd.DataFrame()
    
    def clean_numeric_column(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Clean numeric columns by removing non-numeric characters"""
        if column in df.columns:
            df[column] = df[column].astype(str).str.replace(r'[^\d.]', '', regex=True)
            df[column] = pd.to_numeric(df[column], errors='coerce')
        return df
    
    def analyze_question(self, df: pd.DataFrame, question: str) -> Any:
        """Generic question analysis"""
        question_lower = question.lower()
        
        try:
            # Count questions
            if any(word in question_lower for word in ['how many', 'count', 'number of']):
                return self.handle_count_question(df, question)
            
            # Correlation questions
            elif 'correlation' in question_lower:
                return self.handle_correlation_question(df, question)
            
            # Earliest/latest questions
            elif any(word in question_lower for word in ['earliest', 'latest', 'first', 'last']):
                return self.handle_temporal_question(df, question)
            
            # Statistical questions
            elif any(word in question_lower for word in ['average', 'mean', 'median', 'sum', 'total']):
                return self.handle_statistical_question(df, question)
            
            # Regression questions
            elif 'regression' in question_lower or 'slope' in question_lower:
                return self.handle_regression_question(df, question)
            
            # Default: return descriptive statistics
            else:
                return self.handle_descriptive_question(df, question)
                
        except Exception as e:
            logger.error(f"Error analyzing question '{question}': {e}")
            return f"Error analyzing question: {str(e)}"
    
    def handle_count_question(self, df: pd.DataFrame, question: str) -> int:
        """Handle count-based questions"""
        question_lower = question.lower()
        
        # Create a copy to avoid modifying original
        df_work = df.copy()
        
        # Extract conditions from question
        conditions = []
        
        # Look for monetary amounts
        money_pattern = r'\$([\d,]+)\s*(bn|billion|m|million|k|thousand)?'
        money_matches = re.findall(money_pattern, question_lower)
        for amount, unit in money_matches:
            amount = float(amount.replace(',', ''))
            if unit in ['bn', 'billion']:
                amount *= 1e9
            elif unit in ['m', 'million']:
                amount *= 1e6
            elif unit in ['k', 'thousand']:
                amount *= 1e3
            
            # Find the column that might contain this data
            for col in df_work.columns:
                if any(word in col.lower() for word in ['gross', 'revenue', 'amount', 'price', 'cost']):
                    # Clean the column first
                    df_work = self.clean_numeric_column(df_work, col)
                    # Create condition mask
                    mask = df_work[col] >= amount
                    conditions.append(mask)
                    break
        
        # Look for year conditions
        year_pattern = r'(before|after|in)\s*(\d{4})'
        year_matches = re.findall(year_pattern, question_lower)
        for time_word, year in year_matches:
            year = int(year)
            # Find year column
            for col in df_work.columns:
                if 'year' in col.lower():
                    # Clean the column first
                    df_work = self.clean_numeric_column(df_work, col)
                    # Create condition mask
                    if time_word == 'before':
                        mask = df_work[col] < year
                    elif time_word == 'after':
                        mask = df_work[col] > year
                    else:
                        mask = df_work[col] == year
                    conditions.append(mask)
                    break
        
        # Apply conditions
        if conditions:
            # Combine all conditions with AND
            final_mask = conditions[0]
            for condition in conditions[1:]:
                final_mask = final_mask & condition
            return int(final_mask.sum())
        else:
            return len(df_work)
    
    def handle_correlation_question(self, df: pd.DataFrame, question: str) -> float:
        """Handle correlation questions"""
        # Create a copy to avoid modifying original
        df_work = df.copy()
        
        # Extract column names from question
        words = question.lower().split()
        columns = []
        
        for word in words:
            for col in df_work.columns:
                if word in col.lower():
                    columns.append(col)
                    break
        
        if len(columns) >= 2:
            # Clean numeric columns
            for col in columns:
                df_work = self.clean_numeric_column(df_work, col)
            
            # Drop rows with NaN values in both columns
            df_clean = df_work[columns].dropna()
            
            if len(df_clean) < 2:
                return 0.0
            
            # Calculate correlation
            correlation = df_clean[columns[0]].corr(df_clean[columns[1]])
            return float(correlation) if not pd.isna(correlation) else 0.0
        else:
            return 0.0
    
    def handle_temporal_question(self, df: pd.DataFrame, question: str) -> str:
        """Handle temporal questions (earliest, latest, etc.)"""
        # Create a copy to avoid modifying original
        df_work = df.copy()
        question_lower = question.lower()
        
        # Find the target column (usually title or name)
        target_col = None
        for col in df_work.columns:
            if any(word in col.lower() for word in ['title', 'name', 'film', 'movie']):
                target_col = col
                break
        
        if not target_col:
            return "Target column not found"
        
        # Find date/time column
        date_col = None
        for col in df_work.columns:
            if any(word in col.lower() for word in ['year', 'date', 'time']):
                date_col = col
                break
        
        if not date_col:
            return "Date column not found"
        
        # Clean date column
        df_work = self.clean_numeric_column(df_work, date_col)
        
        # Drop rows with NaN values in date column
        df_clean = df_work.dropna(subset=[date_col])
        
        if len(df_clean) == 0:
            return "No valid data found"
        
        # Find earliest/latest
        if 'earliest' in question_lower or 'first' in question_lower:
            idx = df_clean[date_col].idxmin()
        else:
            idx = df_clean[date_col].idxmax()
        
        if pd.isna(idx):
            return "No valid data found"
        
        return str(df_clean.loc[idx, target_col])
    
    def handle_statistical_question(self, df: pd.DataFrame, question: str) -> float:
        """Handle statistical questions"""
        question_lower = question.lower()
        
        # Find numeric column
        numeric_col = None
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                numeric_col = col
                break
        
        if not numeric_col:
            return 0.0
        
        # Calculate appropriate statistic
        if 'average' in question_lower or 'mean' in question_lower:
            return float(df[numeric_col].mean())
        elif 'median' in question_lower:
            return float(df[numeric_col].median())
        elif 'sum' in question_lower or 'total' in question_lower:
            return float(df[numeric_col].sum())
        else:
            return float(df[numeric_col].mean())
    
    def handle_regression_question(self, df: pd.DataFrame, question: str) -> float:
        """Handle regression questions"""
        # Extract column names
        words = question.lower().split()
        columns = []
        
        for word in words:
            for col in df.columns:
                if word in col.lower():
                    columns.append(col)
                    break
        
        if len(columns) >= 2:
            # Clean numeric columns
            for col in columns:
                df = self.clean_numeric_column(df, col)
            
            # Calculate regression slope
            x = df[columns[0]].dropna()
            y = df[columns[1]].dropna()
            
            if len(x) > 1 and len(y) > 1:
                # Align the data
                common_idx = x.index.intersection(y.index)
                x = x[common_idx]
                y = y[common_idx]
                
                if len(x) > 1:
                    slope = np.polyfit(x, y, 1)[0]
                    return float(slope)
        
        return 0.0
    
    def handle_descriptive_question(self, df: pd.DataFrame, question: str) -> str:
        """Handle descriptive questions"""
        # Return basic info about the dataset
        return f"Dataset has {len(df)} rows and {len(df.columns)} columns"
    
    def create_visualization(self, df: pd.DataFrame, question: str) -> str:
        """Create visualizations based on question"""
        question_lower = question.lower()
        
        try:
            # Extract column names for plotting
            columns = []
            for col in df.columns:
                if any(word in question_lower for word in col.lower().split()):
                    columns.append(col)
            
            if len(columns) < 2:
                # Use first two numeric columns
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                if len(numeric_cols) >= 2:
                    columns = numeric_cols[:2]
                else:
                    return "Insufficient numeric data for plotting"
            
            x_col, y_col = columns[0], columns[1]
            
            # Clean data
            df_clean = df.copy()
            df_clean = self.clean_numeric_column(df_clean, x_col)
            df_clean = self.clean_numeric_column(df_clean, y_col)
            
            # Remove NaN values
            df_clean = df_clean.dropna(subset=[x_col, y_col])
            
            if len(df_clean) == 0:
                return "No valid data for plotting"
            
            # Create plot
            plt.figure(figsize=(10, 6))
            plt.scatter(df_clean[x_col], df_clean[y_col], alpha=0.6)
            
            # Add regression line if requested
            if 'regression' in question_lower or 'trend' in question_lower:
                if len(df_clean) > 1:
                    z = np.polyfit(df_clean[x_col], df_clean[y_col], 1)
                    p = np.poly1d(z)
                    plt.plot(df_clean[x_col], p(df_clean[x_col]), "r--", alpha=0.8)
            
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.title(f'{x_col} vs {y_col}')
            plt.grid(True, alpha=0.3)
            
            # Save to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return f"data:image/png;base64,{image_base64}"
            
        except Exception as e:
            logger.error(f"Error creating visualization: {e}")
            return f"Error creating plot: {str(e)}"
    
    def query_duckdb_s3(self, query: str) -> pd.DataFrame:
        """Query data from S3 using DuckDB"""
        try:
            # Initialize DuckDB
            con = duckdb.connect(':memory:')
            
            # Install and load required extensions
            con.execute("INSTALL httpfs")
            con.execute("LOAD httpfs")
            con.execute("INSTALL parquet")
            con.execute("LOAD parquet")
            
            # Execute query
            result = con.execute(query)
            df = result.df()
            
            con.close()
            return df
            
        except Exception as e:
            logger.error(f"Error querying DuckDB: {e}")
            raise

# Global agent instance
agent = DataAnalystAgent()

@app.post("/api/")
async def analyze_data_task(file: UploadFile = File(...)):
    """Main endpoint for data analysis tasks"""
    try:
        # Read the question file
        content = await file.read()
        question_text = content.decode('utf-8')
        
        logger.info(f"Received question: {question_text[:200]}...")
        
        # Extract URLs from the question
        urls = agent.extract_urls_from_text(question_text)
        
        # Extract questions from the text
        questions = agent.extract_questions_from_text(question_text)
        
        # Determine if this is a DuckDB/S3 query
        if any(word in question_text.lower() for word in ['duckdb', 's3://', 'parquet', 'sql']):
            # Handle DuckDB/S3 analysis
            return await handle_duckdb_analysis(question_text, questions)
        
        # Handle web scraping analysis
        elif urls:
            return await handle_web_analysis(urls, questions, question_text)
        
        # Generic analysis
        else:
            return JSONResponse(content=["Analysis type not recognized"])
    
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def handle_web_analysis(urls: List[str], questions: List[str], question_text: str) -> JSONResponse:
    """Handle web scraping analysis"""
    results = []
    
    # Scrape data from the first URL
    if urls:
        df = agent.scrape_data_from_url(urls[0])
        
        if not df.empty:
            # Analyze each question
            for question in questions:
                result = agent.analyze_question(df, question)
                results.append(result)
            
            # Check if visualization is requested
            if any(word in question_text.lower() for word in ['plot', 'scatterplot', 'graph', 'chart', 'visualization']):
                plot_data = agent.create_visualization(df, question_text)
                results.append(plot_data)
        else:
            results = ["No data found from the provided URL"]
    
    # Ensure results are JSON serializable
    return JSONResponse(content=json.loads(json.dumps(results, cls=NumpyEncoder)))

async def handle_duckdb_analysis(question_text: str, questions: List[str]) -> JSONResponse:
    """Handle DuckDB/S3 analysis"""
    results = {}
    
    # Extract SQL queries from the question text
    sql_pattern = r'```sql\s*(.*?)\s*```'
    sql_matches = re.findall(sql_pattern, question_text, re.DOTALL | re.IGNORECASE)
    
    # If no SQL found, try to construct queries from questions
    if not sql_matches:
        for question in questions:
            try:
                # Construct a simple query based on the question
                if 'count' in question.lower() or 'how many' in question.lower():
                    query = """
                    SELECT COUNT(*) as count
                    FROM read_parquet('s3://indian-high-court-judgments/metadata/parquet/year=*/court=*/bench=*/metadata.parquet?s3_region=ap-south-1')
                    """
                else:
                    query = """
                    SELECT *
                    FROM read_parquet('s3://indian-high-court-judgments/metadata/parquet/year=*/court=*/bench=*/metadata.parquet?s3_region=ap-south-1')
                    LIMIT 100
                    """
                
                df = agent.query_duckdb_s3(query)
                if not df.empty:
                    result = agent.analyze_question(df, question)
                    results[question] = result
                else:
                    results[question] = "No data found"
                    
            except Exception as e:
                results[question] = f"Error: {str(e)}"
    
    # Handle visualization requests
    if any(word in question_text.lower() for word in ['plot', 'scatterplot', 'graph', 'chart']):
        try:
            # Get some data for visualization
            query = """
            SELECT year, COUNT(*) as case_count
            FROM read_parquet('s3://indian-high-court-judgments/metadata/parquet/year=*/court=*/bench=*/metadata.parquet?s3_region=ap-south-1')
            WHERE year BETWEEN 2019 AND 2022
            GROUP BY year
            ORDER BY year
            """
            df = agent.query_duckdb_s3(query)
            if not df.empty:
                plot_data = agent.create_visualization(df, question_text)
                results["Visualization"] = plot_data
        except Exception as e:
            results["Visualization"] = f"Error creating plot: {str(e)}"
    
    return JSONResponse(content=results)

@app.on_event("shutdown")
async def shutdown_event():
    await agent.close_session()

@app.get("/")
async def root():
    return {"message": "Data Analyst Agent API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 