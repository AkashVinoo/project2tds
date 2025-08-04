import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

def count_files_recursive(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    count = 0
    for link in soup.find_all('a', href=True):
        href = link['href']
        # Skip parent directory links
        if href in ('../', './'):
            continue
        full_url = urljoin(url, href)
        if href.endswith('/'):
            # It's a directory, recurse into it
            count += count_files_recursive(full_url)
        elif href.endswith('.html'):
            filename = href.split('/')[-1]
            first_letter = filename[0].upper()
            if 'J' <= first_letter <= 'W':
                print(full_url)
                count += 1
    return count

if __name__ == "__main__":
    root_url = "https://sanand0.github.io/tdsdata/crawl_html/"
    print("HTML files starting with letters J through W:")
    result = count_files_recursive(root_url)
    print(f"\nNumber of HTML files starting with letters J through W: {result}") 