import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import time

def crawl_and_count_html_files():
    """
    Crawl https://sanand0.github.io/tdsdata/crawl_html/ and count HTML files
    that begin with letters from J to W
    """
    base_url = "https://sanand0.github.io/tdsdata/crawl_html/"
    
    try:
        # Fetch the main page
        print(f"Crawling {base_url}...")
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all links
        links = soup.find_all('a', href=True)
        
        html_files = []
        folders = []
        
        for link in links:
            href = link['href']
            text = link.get_text(strip=True)
            
            # Check if it's a folder (ends with /) or HTML file
            if href.endswith('/'):
                folders.append(href)
            elif href.endswith('.html'):
                html_files.append(href)
        
        print(f"Found {len(folders)} folders and {len(html_files)} HTML files on main page")
        
        # Now crawl each folder to find HTML files
        all_html_files = html_files.copy()  # Start with files from main page
        
        for folder in folders:
            folder_url = urljoin(base_url, folder)
            print(f"Crawling folder: {folder_url}")
            
            try:
                folder_response = requests.get(folder_url, timeout=10)
                folder_response.raise_for_status()
                
                folder_soup = BeautifulSoup(folder_response.text, 'html.parser')
                folder_links = folder_soup.find_all('a', href=True)
                
                for link in folder_links:
                    href = link['href']
                    if href.endswith('.html'):
                        # Get the full path
                        full_path = urljoin(folder_url, href)
                        all_html_files.append(full_path)
                
                # Be respectful with crawling speed
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error crawling folder {folder_url}: {e}")
        
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
        print(f"Error crawling website: {e}")
        return 0

if __name__ == "__main__":
    count = crawl_and_count_html_files()
    print(f"\nFinal count: {count} HTML files begin with letters J to W") 