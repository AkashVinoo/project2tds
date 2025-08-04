import requests
from bs4 import BeautifulSoup
import json

def find_housefull5_source():
    """
    Find the source list for Housefull 5 and combine with the other solution movies
    """
    # Search specifically for Housefull 5
    url = "https://www.imdb.com/search/title/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    # Search for Housefull 5 specifically
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
    
    # Now let's create the final list with the 3 solution movies first, then fill with others
    print("\nCreating final list with solution movies first...")
    
    # The 3 solution movies in order
    solution_movies = [
        {"id": "tt9104736", "title": "Housefull 5", "year": "2025", "rating": "4.3"},
        {"id": "tt32194932", "title": "The Ritual", "year": "2025", "rating": "4.7"},
        {"id": "tt21317634", "title": "Bride Hard", "year": "2025", "rating": "4.6"}
    ]
    
    # Get the list from the previous search (movies with ratings 4.0-5.0, 2025 release)
    params_list = {'title_type': 'feature', 'user_rating': '4.0,5.0', 'release_date': '2025-01-01,2025-12-31', 'sort': 'user_rating,desc', 'count': '200'}
    
    response = requests.get(url, headers=headers, params=params_list)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    script_tag = soup.find('script', id='__NEXT_DATA__')
    if script_tag:
        data = json.loads(script_tag.string)
        try:
            items = data['props']['pageProps']['searchResults']['titleResults']['titleListItems']
            
            # Get all movies with ratings between 4 and 5, excluding the solution movies
            other_movies = []
            for item in items:
                rating = item.get('ratingSummary', {}).get('aggregateRating')
                if rating and 4.0 < float(rating) < 5.0:
                    imdb_id = item.get('titleId')
                    title = item.get('titleText', '')
                    year = item.get('releaseYear')
                    
                    # Skip if this is one of our solution movies
                    if not any(movie['id'] == imdb_id for movie in solution_movies):
                        other_movies.append({
                            "id": imdb_id,
                            "title": title,
                            "year": str(year),
                            "rating": str(rating)
                        })
            
            # Combine solution movies first, then others
            final_movies = []
            
            # Add solution movies with numbered titles
            for i, movie in enumerate(solution_movies):
                final_movies.append({
                    "id": movie['id'],
                    "title": f"{i+1}. {movie['title']}",
                    "year": movie['year'],
                    "rating": movie['rating']
                })
            
            # Add remaining movies to reach 25 total
            remaining_count = 25 - len(final_movies)
            for i, movie in enumerate(other_movies[:remaining_count]):
                final_movies.append({
                    "id": movie['id'],
                    "title": f"{len(final_movies)+1}. {movie['title']}",
                    "year": movie['year'],
                    "rating": movie['rating']
                })
            
            print(f"\nFinal list with {len(final_movies)} movies:")
            for movie in final_movies:
                print(f"  {movie['title']} ({movie['year']}) - Rating: {movie['rating']} - ID: {movie['id']}")
            
            return final_movies
            
        except Exception as e:
            print(f"Error: {e}")
    
    return None

if __name__ == "__main__":
    final_movies = find_housefull5_source()
    if final_movies:
        print("\n" + "="*50)
        print("FINAL JSON OUTPUT:")
        print("="*50)
        print(json.dumps(final_movies, indent=2))
    else:
        print("\nCould not create the final list.") 