import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import string

def deep_explore():
    """
    Deep exploration to find alphabetized folders
    """
    base_url = "https://sanand0.github.io/tdsdata/crawl_html/"
    
    # Try different possible URL patterns
    possible_patterns = [
        base_url,
        base_url + "a/",
        base_url + "j/",
        base_url + "k/",
        base_url + "l/",
        base_url + "m/",
        base_url + "n/",
        base_url + "o/",
        base_url + "p/",
        base_url + "q/",
        base_url + "r/",
        base_url + "s/",
        base_url + "t/",
        base_url + "u/",
        base_url + "v/",
        base_url + "w/",
        base_url + "x/",
        base_url + "y/",
        base_url + "z/"
    ]
    
    total_html_files = 0
    j_to_w_files = []
    
    for pattern in possible_patterns:
        try:
            print(f"Checking: {pattern}")
            response = requests.get(pattern, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a', href=True)
                
                html_files = [link for link in links if link['href'].endswith('.html')]
                
                if html_files:
                    print(f"  Found {len(html_files)} HTML files")
                    total_html_files += len(html_files)
                    
                    for link in html_files:
                        filename = link['href']
                        if filename and filename[0].upper() in 'JKLMNOPQRSTUVW':
                            j_to_w_files.append(filename)
                            print(f"    J-W file: {filename}")
                else:
                    print("  No HTML files found")
            else:
                print(f"  Status code: {response.status_code}")
                
        except Exception as e:
            print(f"  Error: {e}")
    
    print(f"\nTotal HTML files found: {total_html_files}")
    print(f"HTML files beginning with J-W: {len(j_to_w_files)}")
    
    # Also try to check if there's a different base URL
    print("\nTrying alternative base URLs...")
    alt_base = "https://sanand0.github.io/tdsdata/"
    
    try:
        response = requests.get(alt_base, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            print(f"Found {len(links)} links at {alt_base}")
            
            for link in links:
                href = link['href']
                text = link.get_text(strip=True)
                print(f"  {text} -> {href}")
                
    except Exception as e:
        print(f"Error with alternative base: {e}")
    
    return len(j_to_w_files)

if __name__ == "__main__":
    count = deep_explore()
    print(f"\nFinal count: {count} HTML files begin with letters J to W") 