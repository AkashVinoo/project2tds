from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import json
import time
import re

def setup_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Run in visible mode for manual CAPTCHA/login
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--start-maximized')
    return webdriver.Chrome(options=options)

def extract_movie_id(url):
    match = re.search(r'/title/(tt\d+)/', url)
    return match.group(1) if match else None

def wait_for_element(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        print(f"Timeout waiting for element: {value}")
        return None

def scrape_imdb_movies():
    driver = setup_driver()
    movies = []
    
    try:
        print("Navigating to IMDb...")
        url = "https://www.imdb.com/search/title/?title_type=feature&user_rating=4.1,4.9&sort=user_rating,desc&count=100"
        driver.get(url)
        
        # Verify we're on the correct page
        if "imdb.com/search/title" not in driver.current_url:
            print("Warning: Not on the expected IMDb search page. Current URL:", driver.current_url)
        
        print("\nIf you see a CAPTCHA or login page, please solve it in the opened browser window.")
        input("Press Enter here after the page has fully loaded and you see the movie list...")
        
        print("\nWaiting for page to load...")
        time.sleep(5)  # Give extra time for dynamic content to load
        
        print("\nLooking for movie list container...")
        # Try different possible selectors for the movie list
        selectors = [
            "div.lister-list",
            "ul.ipc-metadata-list",
            "div.sc-17bafbdb-2"
        ]
        
        movie_list = None
        for selector in selectors:
            movie_list = wait_for_element(driver, By.CSS_SELECTOR, selector)
            if movie_list:
                print(f"Found movie list using selector: {selector}")
                break
                
        if not movie_list:
            print("Could not find movie list container with any known selector")
            return movies
            
        print("Finding movie items...")
        # Try different possible selectors for movie items
        item_selectors = [
            "div.lister-item",
            "li.ipc-metadata-list-summary-item",
            "div.sc-17bafbdb-3"
        ]
        
        movie_items = []
        for selector in item_selectors:
            movie_items = movie_list.find_elements(By.CSS_SELECTOR, selector)
            if movie_items:
                print(f"Found movie items using selector: {selector}")
                break
                
        total_movies = len(movie_items)
        print(f"Found {total_movies} movies")
        
        for index, item in enumerate(movie_items, 1):
            try:
                print(f"\nProcessing movie {index}/{total_movies}...")
                
                # Try different possible selectors for title
                title_selectors = [
                    "h3.lister-item-header a",
                    "h3.ipc-title__text",
                    "a.ipc-title-link-wrapper"
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
                    print("Could not find title element")
                    continue
                    
                title = title_element.text.strip()
                url = title_element.get_attribute("href")
                movie_id = extract_movie_id(url)
                
                # Try different possible selectors for year
                year_selectors = [
                    "span.lister-item-year",
                    "span.ipc-metadata-list-summary-item__li",
                    "span.sc-17bafbdb-2"
                ]
                
                year = None
                for selector in year_selectors:
                    try:
                        year_element = item.find_element(By.CSS_SELECTOR, selector)
                        year_text = year_element.text.strip()
                        year_match = re.search(r'\d{4}', year_text)
                        if year_match:
                            year = int(year_match.group())
                            break
                    except (NoSuchElementException, ValueError):
                        continue
                
                # Try different possible selectors for rating
                rating_selectors = [
                    "div.ratings-imdb-rating strong",
                    "span.ipc-rating-star--imdb",
                    "span.sc-17bafbdb-2"
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
                
                # Only include movies with ratings between 4.1 and 4.9
                if movie_id and title and year and rating and 4.1 <= rating <= 4.9:
                    movie_data = {
                        "id": movie_id,
                        "title": title,
                        "year": year,
                        "rating": rating
                    }
                    movies.append(movie_data)
                    print(f"✓ Successfully extracted: {title} (Rating: {rating})")
                else:
                    print(f"✗ Skipped: {title} - Rating: {rating}")
                
            except (NoSuchElementException, StaleElementReferenceException) as e:
                print(f"Error extracting movie data: {str(e)}")
                continue
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()
        
    return movies

def save_movies_to_json(movies, filename="imdb_movies.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(movies, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(movies)} movies to {filename}")

if __name__ == "__main__":
    print("Starting IMDb movie scraper...")
    movies = scrape_imdb_movies()
    if movies:
        save_movies_to_json(movies)
    else:
        print("No movies were successfully scraped.") 