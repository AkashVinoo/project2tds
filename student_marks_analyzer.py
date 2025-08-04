import pandas as pd
import tabula
import os
from pathlib import Path

def extract_tables_with_groups(pdf_path):
    """Extract all tables from PDF and assign group numbers."""
    try:
        tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
        if not tables:
            print("No tables found in the PDF")
            return None
        all_tables = []
        for idx, table in enumerate(tables):
            table = table.copy()
            table['Group'] = idx + 1  # Group numbers start from 1
            all_tables.append(table)
        df = pd.concat(all_tables, ignore_index=True)
        return df
    except Exception as e:
        print(f"Error extracting tables from PDF: {str(e)}")
        return None

def clean_data(df):
    """Clean and prepare the data for analysis."""
    try:
        # Convert column names to string type
        df.columns = df.columns.astype(str)
        
        # Print full table structure
        print("\nFull table structure:")
        print(df.head(10).to_string())
        
        # Convert marks columns to numeric, handling any non-numeric values
        numeric_columns = ['Maths', 'Physics', 'English', 'Economics', 'Biology', 'Group']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
        
    except Exception as e:
        print(f"Error cleaning data: {str(e)}")
        return None

def calculate_total_english_marks(df):
    """Calculate total English marks for students meeting the criteria."""
    try:
        # Filter for groups 35-71 and Economics >= 79
        filtered_df = df[(df['Group'] >= 35) & (df['Group'] <= 71) & (df['Economics'] >= 79)]
        
        # Calculate total English marks for filtered students
        total_english_marks = filtered_df['English'].sum()
        
        # Print detailed information
        print("\nAnalysis Results:")
        print(f"Number of students meeting criteria: {len(filtered_df)}")
        print(f"Total English marks: {total_english_marks}")
        print("\nDetailed breakdown:")
        print(filtered_df[['Group', 'Economics', 'English']].to_string())
        
        return total_english_marks
        
    except Exception as e:
        print(f"Error calculating total marks: {str(e)}")
        return None

def main():
    # Get the Downloads folder path
    downloads_path = str(Path.home() / "Downloads")
    
    # Look for the specific file
    target_file = "q-extract-tables-from-pdf.pdf"
    pdf_path = os.path.join(downloads_path, target_file)
    
    if not os.path.exists(pdf_path):
        print(f"Error: Could not find file '{target_file}' in Downloads folder")
        return
        
    print(f"\nProcessing file: {target_file}")
    
    # Extract and process the data
    df = extract_tables_with_groups(pdf_path)
    if df is not None:
        print("\nExtracted table structure:")
        print(df.head())
        print("\nColumns found:", df.columns.tolist())
        
        df = clean_data(df)
        if df is not None:
            calculate_total_english_marks(df)

if __name__ == "__main__":
    main() 