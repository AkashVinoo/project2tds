import json
import re
from bs4 import BeautifulSoup

# Read the HTML file
with open('imdb_raw.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Parse the HTML to find the __NEXT_DATA__ script tag
soup = BeautifulSoup(html, 'html.parser')
script_tag = soup.find('script', id='__NEXT_DATA__', type='application/json')

if not script_tag:
    print('Could not find the __NEXT_DATA__ script tag.')
    exit(1)

# Load the JSON data
try:
    data = json.loads(script_tag.string)
except Exception as e:
    print('Error parsing JSON:', e)
    exit(1)

# Navigate to the movie list
try:
    title_items = data['props']['pageProps']['searchResults']['titleResults']['titleListItems']
except KeyError:
    print('Could not find movie data in the JSON.')
    exit(1)

# Extract up to the first 25 movies with ratings between 4 and 5
movies = []
for item in title_items:
    rating = None
    if 'ratingSummary' in item and item['ratingSummary'] and 'aggregateRating' in item['ratingSummary']:
        rating = item['ratingSummary']['aggregateRating']
    if rating is not None and 4 <= rating <= 5:
        title_id = item.get('titleId', '')
        id_part = title_id[2:] if title_id.startswith('tt') else title_id
        title = item.get('titleText', item.get('originalTitleText', ''))
        year = item.get('releaseYear', '')
        movie = {
            'id': id_part,
            'title': title,
            'year': year,
            'rating': rating
        }
        movies.append(movie)
    if len(movies) == 25:
        break

print(json.dumps(movies, indent=2)) 