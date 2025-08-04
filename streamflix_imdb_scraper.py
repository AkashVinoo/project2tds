from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import json
import time
import re

def setup_driver():
    """Setup Chrome driver with appropriate options"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode for automation
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    return webdriver.Chrome(options=options)

def extract_movie_id(url):
    """Extract IMDb movie ID from URL"""
    match = re.search(r'/title/(tt\d+)/', url)
    return match.group(1) if match else None

def wait_for_element(driver, by, value, timeout=10):
    """Wait for element to be present on page"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        print(f"Timeout waiting for element: {value}")
        return None

def scrape_streamflix_movies():
    """
    Scrape IMDb movies with ratings between 4 and 5 for StreamFlix
    Returns up to 25 movies in the required JSON format
    """
    driver = setup_driver()
    movies = []
    
    try:
        print("Navigating to IMDb advanced search...")
        # Use IMDb's advanced search with rating filter between 4 and 5
        url = "https://www.imdb.com/search/title/?title_type=feature&user_rating=4.0,5.0&sort=user_rating,desc&count=50"
        driver.get(url)
        
        print("Waiting for page to load...")
        time.sleep(3)
        
        # Try different selectors for the movie list container
        selectors = [
            "div.lister-list",
            "ul.ipc-metadata-list",
            "div.sc-17bafbdb-2",
            "div[data-testid='results-section']"
        ]
        
        movie_list = None
        for selector in selectors:
            movie_list = wait_for_element(driver, By.CSS_SELECTOR, selector)
            if movie_list:
                print(f"Found movie list using selector: {selector}")
                break
                
        if not movie_list:
            print("Could not find movie list container")
            return movies
            
        # Try different selectors for movie items
        item_selectors = [
            "div.lister-item",
            "li.ipc-metadata-list-summary-item",
            "div.sc-17bafbdb-3",
            "li[data-testid='title']"
        ]
        
        movie_items = []
        for selector in item_selectors:
            movie_items = movie_list.find_elements(By.CSS_SELECTOR, selector)
            if movie_items:
                print(f"Found {len(movie_items)} movie items using selector: {selector}")
                break
                
        for index, item in enumerate(movie_items, 1):
            if len(movies) >= 25:  # Limit to 25 movies
                break
                
            try:
                print(f"Processing movie {index}...")
                
                # Extract title and ID
                title_selectors = [
                    "h3.lister-item-header a",
                    "h3.ipc-title__text a",
                    "a.ipc-title-link-wrapper",
                    "a[data-testid='title-link']"
                ]
                
                title_element = None
                for selector in title_selectors:
                    try:
                        title_element = item.find_element(By.CSS_SELECTOR, selector)
                        if title_element:
                            break
                    except NoSuchElementException:
                        continue
                
                if not title_element:
                    continue
                    
                title = title_element.text.strip()
                url = title_element.get_attribute("href")
                movie_id = extract_movie_id(url)
                
                if not movie_id or not title:
                    continue
                
                # Extract year
                year_selectors = [
                    "span.lister-item-year",
                    "span.ipc-metadata-list-summary-item__li",
                    "span.sc-17bafbdb-2",
                    "span[data-testid='title-year']"
                ]
                
                year = None
                for selector in year_selectors:
                    try:
                        year_element = item.find_element(By.CSS_SELECTOR, selector)
                        year_text = year_element.text.strip()
                        year_match = re.search(r'\d{4}', year_text)
                        if year_match:
                            year = year_match.group()
                            break
                    except NoSuchElementException:
                        continue
                
                # Extract rating
                rating_selectors = [
                    "div.ratings-imdb-rating strong",
                    "span.ipc-rating-star--imdb",
                    "span.sc-17bafbdb-2",
                    "span[data-testid='rating-value']"
                ]
                
                rating = None
                for selector in rating_selectors:
                    try:
                        rating_element = item.find_element(By.CSS_SELECTOR, selector)
                        rating_text = rating_element.text.strip()
                        # Handle different rating formats
                        if '/' in rating_text:
                            rating_text = rating_text.split('/')[0]
                        rating = float(rating_text)
                        break
                    except (NoSuchElementException, ValueError):
                        continue
                
                # Only include movies with ratings between 4 and 5
                if movie_id and title and year and rating and 4.0 <= rating <= 5.0:
                    movie_data = {
                        "id": movie_id,
                        "title": title,
                        "year": year,
                        "rating": str(rating)  # Convert to string as per requirements
                    }
                    movies.append(movie_data)
                    print(f"✓ Added: {title} ({year}) - Rating: {rating}")
                else:
                    print(f"✗ Skipped: {title} - Rating: {rating}")
                
            except (NoSuchElementException, StaleElementReferenceException) as e:
                print(f"Error processing movie: {str(e)}")
                continue
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()
        
    return movies

def save_movies_to_json(movies, filename="streamflix_movies.json"):
    """Save movies to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(movies, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(movies)} movies to {filename}")

def main():
    """Main function to run the StreamFlix IMDb scraper"""
    print("Starting StreamFlix IMDb movie scraper...")
    print("Searching for movies with ratings between 4.0 and 5.0...")
    
    movies = scrape_streamflix_movies()
    
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