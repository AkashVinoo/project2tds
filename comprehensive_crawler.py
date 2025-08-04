import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import re

def crawl_all_directories():
    """
    Crawl all directories and subdirectories to find HTML files
    """
    base_url = "https://sanand0.github.io/tdsdata/crawl_html/"
    
    try:
        print(f"Crawling {base_url}...")
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        
        # Find all directories and files
        directories = []
        files = []
        
        for link in links:
            href = link['href']
            if href.endswith('/'):
                directories.append(href)
            elif href.endswith('.html'):
                files.append(href)
        
        print(f"Found {len(directories)} directories and {len(files)} files on main page")
        
        # Collect all HTML files
        all_html_files = files.copy()
        
        # Crawl each directory
        for directory in directories:
            dir_url = urljoin(base_url, directory)
            print(f"Crawling directory: {dir_url}")
            
            try:
                dir_response = requests.get(dir_url, timeout=10)
                dir_response.raise_for_status()
                
                dir_soup = BeautifulSoup(dir_response.text, 'html.parser')
                dir_links = dir_soup.find_all('a', href=True)
                
                for link in dir_links:
                    href = link['href']
                    if href.endswith('.html'):
                        # Get full path
                        full_path = urljoin(dir_url, href)
                        all_html_files.append(full_path)
                
                time.sleep(0.5)  # Be respectful
                
            except Exception as e:
                print(f"Error crawling {dir_url}: {e}")
        
        print(f"\nTotal HTML files found: {len(all_html_files)}")
        
        # Count files that begin with letters J to W
        j_to_w_files = []
        for file_path in all_html_files:
            # Extract filename from path
            filename = urlparse(file_path).path.split('/')[-1]
            if filename and filename[0].upper() in 'JKLMNOPQRSTUVW':
                j_to_w_files.append(filename)
        
        print(f"\nHTML files beginning with letters J to W: {len(j_to_w_files)}")
        print("Files:")
        for file in sorted(j_to_w_files):
            print(f"  - {file}")
        
        return len(j_to_w_files)
        
    except Exception as e:
        print(f"Error: {e}")
        return 0

if __name__ == "__main__":
    count = crawl_all_directories()
    print(f"\nFinal count: {count} HTML files begin with letters J to W") 