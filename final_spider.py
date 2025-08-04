import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from collections import deque

class RelentlessSpider:
    def __init__(self, start_url):
        self.start_url = start_url
        self.base_domain = urlparse(start_url).netloc
        
        # Use a queue for breadth-first search
        self.queue = deque([start_url])
        
        # Use sets for efficient lookups of visited URLs and found files
        self.visited_urls = {start_url}
        self.found_html_files = set()

        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def is_valid_for_crawling(self, url):
        """Checks if a URL should be crawled."""
        try:
            parsed = urlparse(url)
            # Ensure it's on the same domain and not a link to an external site or a non-web page
            return parsed.netloc == self.base_domain and parsed.scheme in ['http', 'https']
        except (ValueError, AttributeError):
            return False

    def crawl(self):
        """Starts the relentless crawling process."""
        print(f"🚀 Starting relentless spider at: {self.start_url}")
        print("-" * 50)
        
        while self.queue:
            current_url = self.queue.popleft()
            print(f"Crawling: {current_url}")

            try:
                response = self.session.get(current_url, timeout=10)
                response.raise_for_status()
                time.sleep(0.1) # Be a good web citizen
            except requests.RequestException as e:
                print(f"  -> Failed to fetch {current_url}: {e}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all anchor tags with an href attribute
            for link in soup.find_all('a', href=True):
                href = link['href']
                
                # Construct the full, absolute URL
                absolute_url = urljoin(current_url, href)

                # Normalize URL to remove fragments
                absolute_url = urlparse(absolute_url)._replace(fragment="").geturl()

                # Check if we should process this link
                if self.is_valid_for_crawling(absolute_url) and absolute_url not in self.visited_urls:
                    self.visited_urls.add(absolute_url)
                    self.queue.append(absolute_url)
                    
                    # If it's an HTML file, add it to our collection
                    if absolute_url.endswith('.html'):
                        self.found_html_files.add(absolute_url)
                        print(f"  -> Found HTML file: {absolute_url.split('/')[-1]}")
        
        print("\n✅ Crawl complete. All reachable URLs visited.")

    def count_files_j_to_w(self):
        """Counts the found HTML files that start with letters J through W."""
        print("-" * 50)
        print("Analyzing results...")

        j_to_w_files = []
        for file_url in self.found_html_files:
            filename = file_url.split('/')[-1]
            if filename and filename[0].upper() in "JKLMNOPQRSTUVW":
                j_to_w_files.append(filename)
        
        print(f"\nTotal unique HTML files found: {len(self.found_html_files)}")
        print(f"Total files between J and W: {len(j_to_w_files)}")
        
        print("\nFiles found (J-W):")
        if j_to_w_files:
            for filename in sorted(j_to_w_files):
                print(f"  - {filename}")
        else:
            print("  - None")
            
        return len(j_to_w_files)

if __name__ == "__main__":
    spider = RelentlessSpider("https://sanand0.github.io/tdsdata/crawl_html/")
    spider.crawl()
    final_count = spider.count_files_j_to_w()
    print("-" * 50)
    print(f"\nFinal Answer: {final_count}") 