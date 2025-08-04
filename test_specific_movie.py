import requests
from bs4 import BeautifulSoup
import json

def test_specific_movie():
    """
    Test script to search for "Housefull 5" and understand IMDb's data structure
    """
    # Search for the specific movie
    url = "https://www.imdb.com/search/title/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    # Try different search parameters
    params_list = [
        {'title': 'Housefull 5', 'count': '10'},
        {'title_type': 'feature', 'user_rating': '4.0,5.0', 'sort': 'user_rating,desc', 'count': '200'},
        {'title_type': 'feature', 'user_rating': '4.1,4.9', 'sort': 'user_rating,desc', 'count': '100'},
    ]
    
    for i, params in enumerate(params_list):
        print(f"\n=== Test {i+1} ===")
        print(f"Parameters: {params}")
        
        try:
            response = requests.get(url, headers=headers, params=params)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the embedded JSON data
            script_tag = soup.find('script', id='__NEXT_DATA__')
            if not script_tag:
                print('Could not find embedded JSON data.')
                continue
                
            data = json.loads(script_tag.string)
            
            # Try to get movie list
            try:
                items = data['props']['pageProps']['searchResults']['titleResults']['titleListItems']
                print(f"Found {len(items)} movies")
                
                # Look for Housefull 5 specifically
                for item in items:
                    title = item.get('titleText', '')
                    rating = item.get('ratingSummary', {}).get('aggregateRating')
                    year = item.get('releaseYear')
                    
                    if 'housefull' in title.lower() or '5' in title:
                        print(f"Found: {title} ({year}) - Rating: {rating}")
                    
                    # Also print any movie with rating between 4 and 5
                    if rating and 4.0 < float(rating) < 5.0:
                        print(f"Movie in range: {title} ({year}) - Rating: {rating}")
                        
            except Exception as e:
                print(f'Could not parse movie list: {e}')
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_specific_movie() 