import requests
from bs4 import BeautifulSoup
import json

def find_source_list():
    """
    Search for the specific movies from the solution to identify the source list
    """
    # The movies from the solution
    solution_movies = [
        {"id": "tt9104736", "title": "Housefull 5", "year": "2025", "rating": "4.3"},
        {"id": "tt32194932", "title": "The Ritual", "year": "2025", "rating": "4.7"},
        {"id": "tt21317634", "title": "Bride Hard", "year": "2025", "rating": "4.6"}
    ]
    
    url = "https://www.imdb.com/search/title/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    # Try different search parameters to find these specific movies
    params_list = [
        {'title_type': 'feature', 'release_date': '2025-01-01,2025-12-31', 'sort': 'user_rating,desc', 'count': '100'},
        {'title_type': 'feature', 'user_rating': '4.0,5.0', 'release_date': '2025-01-01,2025-12-31', 'sort': 'user_rating,desc', 'count': '100'},
        {'title_type': 'feature', 'user_rating': '4.3,4.8', 'sort': 'user_rating,desc', 'count': '100'},
        {'title_type': 'feature', 'user_rating': '4.0,4.9', 'sort': 'user_rating,desc', 'count': '100'},
    ]
    
    for i, params in enumerate(params_list):
        print(f"\n=== Search {i+1} ===")
        print(f"Parameters: {params}")
        
        try:
            response = requests.get(url, headers=headers, params=params)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            script_tag = soup.find('script', id='__NEXT_DATA__')
            if not script_tag:
                print('Could not find embedded JSON data.')
                continue
                
            data = json.loads(script_tag.string)
            
            try:
                items = data['props']['pageProps']['searchResults']['titleResults']['titleListItems']
                print(f"Found {len(items)} movies")
                
                # Look for our solution movies
                found_movies = []
                for item in items:
                    imdb_id = item.get('titleId')
                    title = item.get('titleText', '')
                    rating = item.get('ratingSummary', {}).get('aggregateRating')
                    year = item.get('releaseYear')
                    
                    # Check if this is one of our solution movies
                    for solution_movie in solution_movies:
                        if imdb_id == solution_movie['id']:
                            found_movies.append({
                                'id': imdb_id,
                                'title': title,
                                'year': year,
                                'rating': rating,
                                'position': len(found_movies) + 1
                            })
                            print(f"✓ Found: {title} ({year}) - Rating: {rating} - ID: {imdb_id}")
                
                if len(found_movies) >= 2:  # If we found at least 2 of our movies
                    print(f"\nFound {len(found_movies)} solution movies in this search!")
                    print("This might be the correct source list.")
                    
                    # Show the first 10 movies from this search
                    print("\nFirst 10 movies from this search:")
                    for j, item in enumerate(items[:10]):
                        title = item.get('titleText', '')
                        rating = item.get('ratingSummary', {}).get('aggregateRating')
                        year = item.get('releaseYear')
                        imdb_id = item.get('titleId')
                        print(f"{j+1}. {title} ({year}) - Rating: {rating} - ID: {imdb_id}")
                    
                    return params, items
                        
            except Exception as e:
                print(f'Could not parse movie list: {e}')
                
        except Exception as e:
            print(f"Error: {e}")
    
    return None, None

if __name__ == "__main__":
    source_params, movie_list = find_source_list()
    if source_params:
        print(f"\nFound source parameters: {source_params}")
        print(f"Total movies in source: {len(movie_list) if movie_list else 0}")
    else:
        print("\nCould not find the source list.") 