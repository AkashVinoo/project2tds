import requests
from bs4 import BeautifulSoup
import json

def find_housefull5():
    """
    Specifically search for Housefull 5 and understand the rating structure
    """
    url = "https://www.imdb.com/search/title/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    # Search specifically for Housefull 5
    params = {'title': 'Housefull 5', 'count': '10'}
    
    print("Searching specifically for Housefull 5...")
    response = requests.get(url, headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    script_tag = soup.find('script', id='__NEXT_DATA__')
    if script_tag:
        data = json.loads(script_tag.string)
        try:
            items = data['props']['pageProps']['searchResults']['titleResults']['titleListItems']
            print(f"Found {len(items)} results")
            
            for item in items:
                title = item.get('titleText', '')
                rating = item.get('ratingSummary', {}).get('aggregateRating')
                year = item.get('releaseYear')
                imdb_id = item.get('titleId')
                
                print(f"Title: {title}")
                print(f"Year: {year}")
                print(f"Rating: {rating}")
                print(f"ID: {imdb_id}")
                print("---")
                
        except Exception as e:
            print(f"Error parsing results: {e}")
    else:
        print("Could not find embedded JSON data")

if __name__ == "__main__":
    find_housefull5() 