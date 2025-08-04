import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json
from collections import deque
import threading
from datetime import datetime

class ContinuousSpider:
    def __init__(self, start_url, max_depth=10, delay=0.5, max_urls=1000):
        self.start_url = start_url
        self.max_depth = max_depth
        self.delay = delay
        self.max_urls = max_urls
        
        # Tracking
        self.visited = set()
        self.queue = deque([(start_url, 0)])  # (url, depth)
        self.html_files = []
        self.j_to_w_files = []
        self.stats = {
            'total_urls_visited': 0,
            'html_files_found': 0,
            'j_to_w_files_found': 0,
            'errors': 0,
            'start_time': datetime.now(),
            'end_time': None
        }
        
        # Session for better performance
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def is_valid_url(self, url, base_domain):
        """Check if URL is valid and belongs to the same domain"""
        try:
            parsed = urlparse(url)
            return (parsed.scheme in ['http', 'https'] and 
                   parsed.netloc == base_domain and
                   not url.endswith('.pdf') and
                   not url.endswith('.jpg') and
                   not url.endswith('.png') and
                   not url.endswith('.gif') and
                   not url.endswith('.css') and
                   not url.endswith('.js'))
        except:
            return False
    
    def crawl_page(self, url, depth):
        """Crawl a single page and extract all links"""
        if url in self.visited or depth > self.max_depth:
            return []
        
        self.visited.add(url)
        self.stats['total_urls_visited'] += 1
        
        print(f"[{self.stats['total_urls_visited']}] Crawling: {url} (depth: {depth})")
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            
            new_urls = []
            for link in links:
                href = link['href']
                full_url = urljoin(url, href)
                
                # Check if it's an HTML file
                if full_url.endswith('.html'):
                    self.html_files.append(full_url)
                    self.stats['html_files_found'] += 1
                    
                    # Check if filename starts with J to W
                    filename = urlparse(full_url).path.split('/')[-1]
                    if filename and filename[0].upper() in 'JKLMNOPQRSTUVW':
                        self.j_to_w_files.append(full_url)
                        self.stats['j_to_w_files_found'] += 1
                        print(f"  ✓ Found J-W file: {filename}")
                
                # Add to queue if it's a valid URL we haven't seen
                elif (self.is_valid_url(full_url, urlparse(self.start_url).netloc) and 
                      full_url not in self.visited and
                      len(self.queue) < self.max_urls):
                    new_urls.append((full_url, depth + 1))
            
            return new_urls
            
        except Exception as e:
            print(f"  ✗ Error crawling {url}: {e}")
            self.stats['errors'] += 1
            return []
    
    def run(self):
        """Main crawling loop"""
        print(f"Starting continuous spider from: {self.start_url}")
        print(f"Max depth: {self.max_depth}, Delay: {self.delay}s, Max URLs: {self.max_urls}")
        print("-" * 80)
        
        base_domain = urlparse(self.start_url).netloc
        
        while self.queue and len(self.visited) < self.max_urls:
            url, depth = self.queue.popleft()
            
            if url in self.visited:
                continue
                
            new_urls = self.crawl_page(url, depth)
            
            # Add new URLs to queue
            for new_url, new_depth in new_urls:
                if new_url not in self.visited:
                    self.queue.append((new_url, new_depth))
            
            # Respectful delay
            time.sleep(self.delay)
            
            # Progress update
            if self.stats['total_urls_visited'] % 10 == 0:
                print(f"Progress: {self.stats['total_urls_visited']} URLs visited, "
                      f"{len(self.html_files)} HTML files, "
                      f"{len(self.j_to_w_files)} J-W files")
        
        self.stats['end_time'] = datetime.now()
        self.print_results()
    
    def print_results(self):
        """Print final results"""
        print("\n" + "=" * 80)
        print("CRAWLING COMPLETE")
        print("=" * 80)
        print(f"Total URLs visited: {self.stats['total_urls_visited']}")
        print(f"HTML files found: {len(self.html_files)}")
        print(f"J-W files found: {len(self.j_to_w_files)}")
        print(f"Errors encountered: {self.stats['errors']}")
        
        duration = self.stats['end_time'] - self.stats['start_time']
        print(f"Crawling duration: {duration}")
        
        print(f"\nHTML files beginning with J to W ({len(self.j_to_w_files)}):")
        for i, file_url in enumerate(sorted(self.j_to_w_files), 1):
            filename = urlparse(file_url).path.split('/')[-1]
            print(f"{i:3d}. {filename} -> {file_url}")
        
        print(f"\nFINAL COUNT: {len(self.j_to_w_files)} HTML files begin with letters J to W")
        
        # Save results to file
        results = {
            'stats': self.stats,
            'html_files': self.html_files,
            'j_to_w_files': self.j_to_w_files,
            'visited_urls': list(self.visited)
        }
        
        with open('spider_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\nResults saved to: spider_results.json")

def main():
    start_url = "https://sanand0.github.io/tdsdata/crawl_html/"
    
    spider = ContinuousSpider(
        start_url=start_url,
        max_depth=5,      # Maximum depth to crawl
        delay=0.3,        # Delay between requests
        max_urls=500      # Maximum URLs to visit
    )
    
    spider.run()

if __name__ == "__main__":
    main() 