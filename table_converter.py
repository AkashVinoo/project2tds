from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time

def extract_numbers_from_text(text):
    # Find all numbers in the text, including decimals and negative numbers
    numbers = re.findall(r'-?\d*\.?\d+', text)
    return [float(num) for num in numbers]

def process_all_tables(url, driver):
    try:
        driver.get(url)
        # Wait for at least one table to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        time.sleep(1)
        
        tables = driver.find_elements(By.TAG_NAME, "table")
        total = 0
        print(f"\nProcessing ALL tables at {url}:")
        for table_idx, table in enumerate(tables):
            print(f"  Table {table_idx+1}:")
            cells = table.find_elements(By.CSS_SELECTOR, "td, th")
            for cell in cells:
                cell_text = cell.text.strip()
                if cell_text:
                    numbers = extract_numbers_from_text(cell_text)
                    if numbers:
                        print(f"    Cell text: '{cell_text}' -> Numbers: {numbers}")
                        total += sum(numbers)
        return total
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return 0

def main():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    try:
        urls = [
            "https://sanand0.github.io/tdsdata/js_table/?seed=43",
            "https://sanand0.github.io/tdsdata/js_table/?seed=44",
            "https://sanand0.github.io/tdsdata/js_table/?seed=45",
            "https://sanand0.github.io/tdsdata/js_table/?seed=46",
            "https://sanand0.github.io/tdsdata/js_table/?seed=47",
            "https://sanand0.github.io/tdsdata/js_table/?seed=48",
            "https://sanand0.github.io/tdsdata/js_table/?seed=49",
            "https://sanand0.github.io/tdsdata/js_table/?seed=50",
            "https://sanand0.github.io/tdsdata/js_table/?seed=51",
            "https://sanand0.github.io/tdsdata/js_table/?seed=52"
        ]
        total_sum = 0
        for url in urls:
            table_sum = process_all_tables(url, driver)
            total_sum += table_sum
            print(f"Sum for all tables on this page: {table_sum}")
        print(f"\nTotal sum across all tables on all pages: {total_sum}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main() 