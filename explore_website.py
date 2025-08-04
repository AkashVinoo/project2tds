import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def explore_website():
    """
    Explore the website structure to understand how files are organized
    """
    base_url = "https://sanand0.github.io/tdsdata/crawl_html/"
    
    try:
        print(f"Exploring {base_url}...")
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Print the page title
        title = soup.find('title')
        if title:
            print(f"Page title: {title.get_text()}")
        
        # Find all links
        links = soup.find_all('a', href=True)
        
        print(f"\nFound {len(links)} links:")
        for i, link in enumerate(links):
            href = link['href']
            text = link.get_text(strip=True)
            print(f"{i+1}. {text} -> {href}")
        
        # Check if there are any directories
        directories = [link for link in links if link['href'].endswith('/')]
        print(f"\nDirectories found: {len(directories)}")
        
        # Check for HTML files
        html_files = [link for link in links if link['href'].endswith('.html')]
        print(f"HTML files found: {len(html_files)}")
        
        # Let's also check if there are any subdirectories with letter names
        letter_dirs = []
        for link in links:
            href = link['href']
            if href.endswith('/') and len(href) == 2:  # Single letter directories like "a/"
                letter_dirs.append(href)
        
        print(f"Single letter directories: {letter_dirs}")
        
        # If we find letter directories, explore them
        if letter_dirs:
            print("\nExploring letter directories...")
            for letter_dir in sorted(letter_dirs):
                if letter_dir[0].upper() in 'JKLMNOPQRSTUVW':
                    dir_url = urljoin(base_url, letter_dir)
                    print(f"\nChecking {dir_url}...")
                    
                    try:
                        dir_response = requests.get(dir_url, timeout=10)
                        dir_response.raise_for_status()
                        
                        dir_soup = BeautifulSoup(dir_response.text, 'html.parser')
                        dir_links = dir_soup.find_all('a', href=True)
                        
                        html_in_dir = [link for link in dir_links if link['href'].endswith('.html')]
                        print(f"  HTML files in {letter_dir}: {len(html_in_dir)}")
                        
                        for html_link in html_in_dir:
                            print(f"    - {html_link['href']}")
                            
                    except Exception as e:
                        print(f"  Error accessing {dir_url}: {e}")
        
    except Exception as e:
        print(f"Error exploring website: {e}")

if __name__ == "__main__":
    explore_website() 