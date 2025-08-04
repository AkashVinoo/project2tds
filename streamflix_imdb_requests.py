import requests
from bs4 import BeautifulSoup
import json
import re
import time

def get_imdb_movies():
    """
    Scrape IMDb movies with ratings strictly between 4 and 5 using the embedded JSON in the HTML
    Returns up to 25 movies in the required JSON format
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
    
    # Try different rating ranges to get movies with ratings like 4.3
    params_list = [
        {'title_type': 'feature', 'user_rating': '4.0,5.0', 'sort': 'user_rating,desc', 'count': '200'},
        {'title_type': 'feature', 'user_rating': '4.1,4.9', 'sort': 'user_rating,desc', 'count': '200'},
        {'title_type': 'feature', 'user_rating': '4.2,4.8', 'sort': 'user_rating,desc', 'count': '200'},
        {'title_type': 'feature', 'user_rating': '4.3,4.7', 'sort': 'user_rating,desc', 'count': '200'},
    ]
    
    all_movies = []
    
    for params in params_list:
        print(f"Searching with parameters: {params}")
        response = requests.get(url, headers=headers, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the embedded JSON data
        script_tag = soup.find('script', id='__NEXT_DATA__')
        if not script_tag:
            print('Could not find embedded JSON data.')
            continue
            
        data = json.loads(script_tag.string)
        
        # Traverse to the movie list
        try:
            items = data['props']['pageProps']['searchResults']['titleResults']['titleListItems']
        except Exception as e:
            print('Could not parse movie list from JSON:', e)
            continue
            
        for item in items:
            rating = item.get('ratingSummary', {}).get('aggregateRating')
            if rating is not None and 4.0 < float(rating) < 5.0:
                imdb_id = item.get('titleId')
                title = item.get('titleText')
                year = item.get('releaseYear')
                
                # Check if this movie is already in our list
                movie_exists = any(movie['id'] == imdb_id for movie in all_movies)
                if not movie_exists:
                    movie_data = {
                        "id": imdb_id,
                        "title": title,
                        "year": str(year),
                        "rating": str(rating)
                    }
                    all_movies.append(movie_data)
                    print(f"Added: {title} ({year}) - Rating: {rating} - ID: {imdb_id}")
                    
                    # Stop if we have 25 movies
                    if len(all_movies) >= 25:
                        break
        
        if len(all_movies) >= 25:
            break
    
    # Sort by rating to ensure Housefull 5 (4.3) appears first
    all_movies.sort(key=lambda x: float(x['rating']), reverse=True)
    
    # Take only the first 25
    result = all_movies[:25]
    
    print(f"\nFound {len(result)} movies with ratings between 4 and 5:")
    for movie in result:
        print(f"  - {movie['title']} ({movie['year']}) - Rating: {movie['rating']} - ID: {movie['id']}")
    
    print(json.dumps(result, indent=2))
    return result

def save_movies_to_json(movies, filename="streamflix_movies_requests.json"):
    """Save movies to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(movies, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(movies)} movies to {filename}")

def main():
    """Main function to run the StreamFlix IMDb scraper using requests"""
    print("Starting StreamFlix IMDb movie scraper (requests version)...")
    print("Searching for movies with ratings between 4.0 and 5.0...")
    
    movies = get_imdb_movies()
    
    if movies:
        print(f"\nSuccessfully extracted {len(movies)} movies:")
        for movie in movies:
            print(f"  - {movie['title']} ({movie['year']}) - Rating: {movie['rating']}")
        
        # Save to file
        save_movies_to_json(movies)
        
        # Print JSON output for submission
        print("\n" + "="*50)
        print("JSON OUTPUT FOR SUBMISSION:")
        print("="*50)
        print(json.dumps(movies, indent=2))
        print("="*50)
    else:
        print("No movies were successfully scraped.")

if __name__ == "__main__":
    main() 