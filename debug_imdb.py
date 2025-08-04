import requests
from bs4 import BeautifulSoup
import json

def debug_imdb_structure():
    """Debug IMDb HTML structure to understand the rating extraction issue"""
    
    url = "https://www.imdb.com/search/title/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    params = {
        'title_type': 'feature',
        'user_rating': '4.0,5.0',
        'sort': 'user_rating,desc',
        'count': '10'
    }
    
    try:
        print("Fetching IMDb search results...")
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        # Save the HTML for inspection
        with open('debug_imdb.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Saved HTML to debug_imdb.html")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the first movie item
        movie_items = soup.select('li.ipc-metadata-list-summary-item')
        
        if movie_items:
            first_item = movie_items[0]
            print("\nFirst movie item HTML structure:")
            print("="*50)
            print(first_item.prettify()[:2000])  # First 2000 chars
            
            # Try to find rating elements
            print("\nLooking for rating elements...")
            rating_elements = first_item.find_all(['span', 'div'], class_=lambda x: x and ('rating' in x.lower() or 'star' in x.lower()))
            print(f"Found {len(rating_elements)} potential rating elements:")
            
            for i, elem in enumerate(rating_elements):
                print(f"{i+1}. {elem.name} - class: {elem.get('class', [])} - text: '{elem.get_text(strip=True)}'")
            
            # Also look for any elements containing numbers that might be ratings
            all_text = first_item.get_text()
            import re
            rating_matches = re.findall(r'\d+\.\d+', all_text)
            print(f"\nAll decimal numbers found: {rating_matches}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    debug_imdb_structure() 