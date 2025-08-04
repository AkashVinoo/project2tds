import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def setup_driver():
    chromedriver_autoinstaller.install()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def extract_numbers_from_table(driver, url):
    driver.get(url)
    # Wait for at least one table to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "table"))
    )
    tables = driver.find_elements(By.TAG_NAME, "table")
    table_sums = []
    total = 0
    
    for table_idx, table in enumerate(tables):
        table_sum = 0
        print(f"\nTable {table_idx + 1} numbers:")
        print("-" * 50)
        
        # Get all cell values
        cells = table.find_elements(By.TAG_NAME, "td")
        row_numbers = []
        current_row = []
        
        for cell_idx, cell in enumerate(cells):
            numbers = re.findall(r'-?\d+', cell.text)
            cell_sum = sum(int(num) for num in numbers)
            table_sum += cell_sum
            
            # Print each number found
            if numbers:
                print(f"Cell {cell_idx + 1}: {numbers} = {cell_sum}")
                current_row.append(cell_sum)
            
            # Start new row after every 5 cells (assuming 5 columns)
            if (cell_idx + 1) % 5 == 0:
                row_sum = sum(current_row)
                print(f"Row sum: {row_sum}")
                print("-" * 30)
                row_numbers.append(row_sum)
                current_row = []
        
        table_sums.append(table_sum)
        total += table_sum
        print(f"\nTable {table_idx + 1} total: {table_sum}")
        print(f"Row sums: {row_numbers}")
        print("=" * 50)
    
    return total, table_sums

def main():
    base_url = "https://sanand0.github.io/tdsdata/js_table/?seed="
    seeds = range(43, 53)  # 43 to 52 inclusive
    driver = setup_driver()
    total_sum = 0
    all_table_sums = []
    
    try:
        for seed in seeds:
            url = f"{base_url}{seed}"
            print(f"\nProcessing seed {seed}...")
            print(f"URL: {url}")
            print("=" * 50)
            page_sum, table_sums = extract_numbers_from_table(driver, url)
            total_sum += page_sum
            all_table_sums.extend(table_sums)
            print(f"\nTotal for seed {seed}: {page_sum}")
            print("=" * 50)
        
        print("\nDetailed Summary:")
        print(f"Total number of tables processed: {len(all_table_sums)}")
        print(f"Total sum across all tables: {total_sum}")
        print("\nIndividual table sums:")
        for i, sum_val in enumerate(all_table_sums):
            print(f"Table {i+1}: {sum_val}")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    main() 