import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def count_html_files_in_directory(base_url, visited=None):
    if visited is None:
        visited = set()
    
    if base_url in visited:
        return 0
    
    visited.add(base_url)
    total_count = 0
    
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        
        print(f"\nChecking directory: {base_url}")
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        
        for link in links:
            href = link.get('href', '')
            text = link.get_text().strip()
            full_url = urljoin(base_url, href)
            
            print(f"Found: {text} ({full_url})")
            
            # If it's a directory (ends with /), recursively check it
            if href.endswith('/'):
                total_count += count_html_files_in_directory(full_url, visited)
            # If it's an HTML file and starts with J-W
            elif href.endswith('.html') and text and text[0].upper() in 'JKLMNOPQRSTUVW':
                total_count += 1
                print(f"Found matching file: {text}")
        
        return total_count
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {base_url}: {e}")
        return 0

def count_html_files():
    base_url = "https://sanand0.github.io/tdsdata/crawl_html/"
    total_count = count_html_files_in_directory(base_url)
    print(f"\nTotal HTML files between J and W: {total_count}")
    return total_count

if __name__ == "__main__":
    count_html_files() 