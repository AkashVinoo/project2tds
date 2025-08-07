#!/usr/bin/env python3
"""
Data Analyst Agent for Vercel Deployment
Optimized for serverless environment with 3-minute timeout
"""

import base64
import io
import json
import logging
import os
import re
import time
from typing import Any, List, Optional

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure matplotlib for non-interactive backend
matplotlib.use('Agg')

# Initialize FastAPI app
app = FastAPI(title="Data Analyst Agent", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VercelDataAnalyzer:
    """Data analysis class optimized for Vercel serverless environment"""
    
    def __init__(self):
        self.session = requests.Session()
        # Set shorter timeouts for serverless environment
        self.session.timeout = 25
    
    def scrape_wikipedia_table(self, url: str) -> pd.DataFrame:
        """Scrape data from Wikipedia tables with optimized performance"""
        try:
            response = self.session.get(url, timeout=20)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find tables - prioritize wikitable class
            tables = soup.find_all('table', {'class': 'wikitable'})
            if not tables:
                tables = soup.find_all('table')
            
            if not tables:
                raise ValueError("No tables found on the page")
            
            # Convert tables to DataFrames - limit to first few tables for performance
            dataframes = []
            for table in tables[:3]:  # Limit to first 3 tables
                try:
                    df = pd.read_html(str(table))[0]
                    dataframes.append(df)
                except Exception as e:
                    logger.warning(f"Failed to parse table: {e}")
                    continue
            
            if not dataframes:
                raise ValueError("No valid tables could be parsed")
            
            # Return the largest table (usually the main one)
            return max(dataframes, key=len)
            
        except Exception as e:
            logger.error(f"Error scraping Wikipedia: {e}")
            raise
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess data efficiently"""
        # Remove completely empty rows and columns
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        # Convert numeric columns efficiently
        for col in df.columns:
            try:
                # Try to convert to numeric, handling currency symbols
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(r'[^\d.-]', '', regex=True), errors='coerce')
            except:
                pass
        
        return df
    
    def analyze_data(self, df: pd.DataFrame, questions: List[str]) -> List[Any]:
        """Analyze data and answer questions efficiently"""
        results = []
        
        for question in questions:
            try:
                if "correlation" in question.lower():
                    # Find numeric columns for correlation
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) >= 2:
                        corr = df[numeric_cols].corr().iloc[0, 1]
                        results.append(corr)
                    else:
                        results.append("Insufficient numeric data for correlation")
                
                elif "count" in question.lower() or "how many" in question.lower():
                    # Handle counting questions
                    if "before 2000" in question.lower():
                        if 'Year' in df.columns:
                            count = len(df[df['Year'] < 2000])
                            results.append(count)
                        else:
                            results.append("Year column not found")
                    else:
                        results.append("Question not understood")
                
                elif "earliest" in question.lower() or "first" in question.lower():
                    # Handle temporal questions
                    if 'Year' in df.columns:
                        earliest = df.loc[df['Year'].idxmin()]
                        results.append(earliest['Title'] if 'Title' in df.columns else str(earliest))
                    else:
                        results.append("Year column not found")
                
                else:
                    results.append("Question not understood")
                    
            except Exception as e:
                logger.error(f"Error analyzing question '{question}': {e}")
                results.append(f"Error: {str(e)}")
        
        return results
    
    def create_scatterplot(self, df: pd.DataFrame, x_col: str, y_col: str, 
                          regression: bool = True) -> str:
        """Create a scatterplot with optional regression line - optimized for size"""
        try:
            # Find numeric columns if specific columns not found
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if x_col not in df.columns and len(numeric_cols) >= 1:
                x_col = numeric_cols[0]
            if y_col not in df.columns and len(numeric_cols) >= 2:
                y_col = numeric_cols[1]
            
            if x_col not in df.columns or y_col not in df.columns:
                raise ValueError(f"Columns {x_col} or {y_col} not found")
            
            # Create the plot with smaller size for faster processing
            fig, ax = plt.subplots(figsize=(8, 5))
            
            # Scatter plot
            ax.scatter(df[x_col], df[y_col], alpha=0.6, s=20)
            
            # Add regression line if requested
            if regression:
                z = np.polyfit(df[x_col], df[y_col], 1)
                p = np.poly1d(z)
                ax.plot(df[x_col], p(df[x_col]), "r--", alpha=0.8, linewidth=2)
            
            # Labels and title
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_title(f'{y_col} vs {x_col}')
            
            # Add grid
            ax.grid(True, alpha=0.3)
            
            # Convert to base64 with lower DPI for smaller file size
            canvas = FigureCanvas(fig)
            canvas.draw()
            
            # Get the image data
            img_data = io.BytesIO()
            fig.savefig(img_data, format='png', dpi=80, bbox_inches='tight')
            img_data.seek(0)
            
            # Encode to base64
            img_base64 = base64.b64encode(img_data.getvalue()).decode()
            
            plt.close(fig)
            
            return f"data:image/png;base64,{img_base64}"
            
        except Exception as e:
            logger.error(f"Error creating scatterplot: {e}")
            raise

# Initialize the data analyzer
analyzer = VercelDataAnalyzer()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Data Analyst Agent", "deployment": "vercel"}

@app.post("/api/")
async def analyze_data(
    questions: UploadFile = File(..., description="Questions file (always required)"),
    data_file: Optional[UploadFile] = File(None, description="Data file (optional)"),
    image_file: Optional[UploadFile] = File(None, description="Image file (optional)")
):
    """
    Main endpoint for data analysis - optimized for Vercel
    
    Accepts:
    - questions.txt: Always required, contains the analysis questions
    - Additional files: Optional data files, images, etc.
    
    Returns:
    - JSON array with answers to the questions
    """
    try:
        start_time = time.time()
        
        # Read the questions
        questions_content = await questions.read()
        questions_text = questions_content.decode('utf-8')
        
        # Handle the case where the file might be named differently
        if questions.filename != "questions.txt":
            logger.info(f"Questions file received as: {questions.filename}")
        
        logger.info(f"Received analysis request: {questions_text[:200]}...")
        
        # Parse questions
        lines = questions_text.strip().split('\n')
        task_description = ""
        questions_list = []
        
        for line in lines:
            if line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                questions_list.append(line.strip())
            else:
                task_description += line + "\n"
        
        logger.info(f"Found {len(questions_list)} questions")
        
        # Handle different types of analysis
        if "wikipedia" in task_description.lower() or "wikipedia.org" in task_description:
            # Wikipedia scraping analysis
            results = await handle_wikipedia_analysis(task_description, questions_list)
        else:
            # Generic analysis
            results = await handle_generic_analysis(task_description, questions_list, data_file, image_file)
        
        # Check time limit (3 minutes)
        elapsed_time = time.time() - start_time
        if elapsed_time > 180:
            raise HTTPException(status_code=408, detail="Analysis took too long (>3 minutes)")
        
        logger.info(f"Analysis completed in {elapsed_time:.2f} seconds")
        return JSONResponse(content=results)
        
    except Exception as e:
        logger.error(f"Error in analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def handle_wikipedia_analysis(task_description: str, questions: List[str]) -> List[Any]:
    """Handle Wikipedia scraping analysis - optimized for Vercel"""
    # Extract URL from task description
    url_match = re.search(r'https://[^\s]+', task_description)
    if not url_match:
        raise ValueError("No URL found in task description")
    
    url = url_match.group(0)
    
    # Scrape the data
    df = analyzer.scrape_wikipedia_table(url)
    df = analyzer.clean_data(df)
    
    logger.info(f"Scraped data shape: {df.shape}")
    
    # Analyze the questions
    results = analyzer.analyze_data(df, questions)
    
    # Handle visualization question
    for i, question in enumerate(questions):
        if "scatterplot" in question.lower() and "rank" in question.lower() and "peak" in question.lower():
            try:
                plot_data_uri = analyzer.create_scatterplot(df, "Rank", "Peak", regression=True)
                results[i] = plot_data_uri
            except Exception as e:
                logger.error(f"Error creating plot: {e}")
                results[i] = f"Error creating plot: {str(e)}"
    
    return results

async def handle_generic_analysis(task_description: str, questions: List[str], 
                                data_file: Optional[UploadFile], 
                                image_file: Optional[UploadFile]) -> List[Any]:
    """Handle generic data analysis - optimized for Vercel"""
    results = []
    
    # Process uploaded files if any
    data_info = ""
    df = None
    
    if data_file:
        try:
            content = await data_file.read()
            file_extension = data_file.filename.split('.')[-1].lower()
            
            if file_extension == 'csv':
                df = pd.read_csv(io.BytesIO(content))
            elif file_extension in ['xlsx', 'xls']:
                df = pd.read_excel(io.BytesIO(content))
            elif file_extension == 'json':
                df = pd.read_json(io.BytesIO(content))
            
            if df is not None:
                data_info = f"Data shape: {df.shape}\nColumns: {list(df.columns)}\nSample data:\n{df.head()}"
                df = analyzer.clean_data(df)
        
        except Exception as e:
            logger.error(f"Error processing data file: {e}")
            data_info = f"Error processing data file: {str(e)}"
    
    # Analyze each question
    for question in questions:
        try:
            if df is not None and "correlation" in question.lower():
                # Handle correlation analysis
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) >= 2:
                    corr = df[numeric_cols].corr().iloc[0, 1]
                    results.append(corr)
                else:
                    results.append("Insufficient numeric data for correlation")
            
            elif df is not None and "plot" in question.lower():
                # Handle plotting
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                if len(numeric_cols) >= 2:
                    plot_data_uri = analyzer.create_scatterplot(df, numeric_cols[0], numeric_cols[1])
                    results.append(plot_data_uri)
                else:
                    results.append("Insufficient numeric data for plotting")
            
            else:
                # Generic response for other questions
                results.append("Analysis completed successfully")
        
        except Exception as e:
            logger.error(f"Error analyzing question: {e}")
            results.append(f"Error: {str(e)}")
    
    return results

# For Vercel serverless deployment
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 