import requests
from bs4 import BeautifulSoup
import json

def get_imdb_movies_with_solution_start():
    # User's provided movies (first 9)
    user_movies = [
        {"id": "tt9104736", "title": "1. Housefull 5", "year": "2025", "rating": "4.3"},
        {"id": "tt32194932", "title": "2. The Ritual", "year": "2025", "rating": "4.7"},
        {"id": "tt21317634", "title": "3. Bride Hard", "year": "2025", "rating": "4.6"},
        {"id": "tt26927452", "title": "4. Hurry Up Tomorrow", "year": "2025", "rating": "4.7"},
        {"id": "tt2322441", "title": "5. Fifty Shades of Grey", "year": "2015", "rating": "4.2"},
        {"id": "tt26787296", "title": "6. O Lado Bom de ser Traída", "year": "2023", "rating": "4.1"},
        {"id": "tt11057302", "title": "7. Madame Web", "year": "2024", "rating": "4.0"},
        {"id": "tt1273235", "title": "8. A Serbian Film", "year": "2010", "rating": "4.9"},
        {"id": "tt3605418", "title": "9. Knock Knock", "year": "2015", "rating": "4.9"}
    ]
    user_ids = set(m["id"] for m in user_movies)

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
        'count': '200',
    }
    response = requests.get(url, headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.find('script', id='__NEXT_DATA__')
    if not script_tag:
        print('Could not find embedded JSON data.')
        return []
    data = json.loads(script_tag.string)
    try:
        items = data['props']['pageProps']['searchResults']['titleResults']['titleListItems']
    except Exception as e:
        print('Could not parse movie list from JSON:', e)
        return []
    # Build the final list
    final_movies = user_movies.copy()
    for item in items:
        imdb_id = item.get('titleId')
        if imdb_id in user_ids:
            continue
        title = item.get('titleText')
        year = item.get('releaseYear')
        rating = item.get('ratingSummary', {}).get('aggregateRating')
        if rating is not None and 4.0 <= float(rating) <= 5.0:
            final_movies.append({
                "id": imdb_id,
                "title": f"{len(final_movies)+1}. {title}",
                "year": str(year),
                "rating": str(rating)
            })
        if len(final_movies) == 25:
            break
    print(json.dumps(final_movies, indent=2))
    return final_movies

if __name__ == "__main__":
    get_imdb_movies_with_solution_start() 