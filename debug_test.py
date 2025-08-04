#!/usr/bin/env python3
"""
Debug script to test Wikipedia scraping
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np

def test_wikipedia_scraping():
    """Test Wikipedia scraping directly"""
    
    url = "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        tables = pd.read_html(response.text)
        print(f"Found {len(tables)} tables")
        
        if len(tables) > 0:
            df = tables[0]
            print(f"Table shape: {df.shape}")
            print(f"Columns: {df.columns.tolist()}")
            print(f"First few rows:")
            print(df.head())
            
            # Test correlation
            if 'Rank' in df.columns and 'Peak' in df.columns:
                correlation = df['Rank'].corr(df['Peak'])
                print(f"Correlation: {correlation} (type: {type(correlation)})")
                
                # Test if it's JSON serializable
                import json
                try:
                    json.dumps(correlation)
                    print("✅ Correlation is JSON serializable")
                except Exception as e:
                    print(f"❌ Correlation is NOT JSON serializable: {e}")
            
            # Test count
            if 'Worldwide gross' in df.columns and 'Year' in df.columns:
                df['Worldwide gross'] = df['Worldwide gross'].astype(str)
                df['Worldwide gross'] = df['Worldwide gross'].str.replace('$', '').str.replace(',', '')
                df['Worldwide gross'] = pd.to_numeric(df['Worldwide gross'], errors='coerce')
                
                mask = (df['Worldwide gross'] >= 2000000000) & (df['Year'] < 2000)
                count = mask.sum()
                print(f"Count: {count} (type: {type(count)})")
                
                # Test if it's JSON serializable
                try:
                    json.dumps(count)
                    print("✅ Count is JSON serializable")
                except Exception as e:
                    print(f"❌ Count is NOT JSON serializable: {e}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_wikipedia_scraping() 