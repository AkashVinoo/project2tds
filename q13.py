from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Function to get the sum of numbers in the table using Selenium
def get_table_sum(url, driver):
    try:
        driver.get(url)
        logging.info(f'Accessing URL: {url}')
        time.sleep(2)  # Wait for JS to render
        logging.info(f'Current URL after loading: {driver.current_url}')
        table = driver.find_element(By.TAG_NAME, 'table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        total = 0
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            for cell in cells:
                try:
                    total += int(cell.text)
                except ValueError:
                    continue
        logging.info(f'Extracted data from {url}: {total}')
        return total
    except Exception as e:
        logging.error(f'Error processing {url}: {e}')
        return 0

def main():
    base_url = 'https://sanand0.github.io/tdsdata/js_table/?seed='
    total_sum = 0

    # Set up Selenium headless Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options)

    try:
        for seed in range(43, 53):
            url = f'{base_url}{seed}'
            print(f'Processing seed {seed}...')
            sum_for_seed = get_table_sum(url, driver)
            print(f'Sum for seed {seed}: {sum_for_seed}')
            total_sum += sum_for_seed
        print(f'\nTotal sum across all seeds: {total_sum}')
    finally:
        driver.quit()

if __name__ == '__main__':
    main() 