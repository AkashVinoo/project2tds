import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json
from datetime import datetime
import string

class AggressiveSpider:
    def __init__(self, base_domain):
        self.base_domain = base_domain
        self.visited = set()
        self.html_files = []
        self.j_to_w_files = []
        self.stats = {
            'total_urls_visited': 0,
            'html_files_found': 0,
            'j_to_w_files_found': 0,
            'errors': 0,
            'start_time': datetime.now()
        }
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def try_url(self, url):
        """Try to access a URL and return response if successful"""
        if url in self.visited:
            return None
        
        self.visited.add(url)
        self.stats['total_urls_visited'] += 1
        
        try:
            print(f"[{self.stats['total_urls_visited']}] Trying: {url}")
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                return response
            else:
                print(f"  Status: {response.status_code}")
        except Exception as e:
            print(f"  Error: {e}")
            self.stats['errors'] += 1
        
        return None
    
    def crawl_directory(self, url):
        """Crawl a directory and extract all links"""
        response = self.try_url(url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        
        found_urls = []
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
            
            # Add to found URLs for further exploration
            if full_url.startswith(f"https://{self.base_domain}"):
                found_urls.append(full_url)
        
        return found_urls
    
    def explore_letter_directories(self):
        """Explore all possible letter directories"""
        print("Exploring letter directories...")
        
        for letter in string.ascii_lowercase:
            url = f"https://{self.base_domain}/tdsdata/crawl_html/{letter}/"
            self.crawl_directory(url)
            time.sleep(0.2)
    
    def explore_numeric_directories(self):
        """Explore numeric directories"""
        print("Exploring numeric directories...")
        
        for num in range(10):
            url = f"https://{self.base_domain}/tdsdata/crawl_html/{num}/"
            self.crawl_directory(url)
            time.sleep(0.2)
    
    def explore_common_directories(self):
        """Explore common directory names"""
        print("Exploring common directories...")
        
        common_dirs = [
            'files/', 'data/', 'html/', 'pages/', 'content/', 'docs/',
            'archive/', 'backup/', 'old/', 'new/', 'temp/', 'test/',
            'public/', 'private/', 'admin/', 'user/', 'download/',
            'images/', 'media/', 'assets/', 'static/', 'dynamic/'
        ]
        
        for dir_name in common_dirs:
            url = f"https://{self.base_domain}/tdsdata/crawl_html/{dir_name}"
            self.crawl_directory(url)
            time.sleep(0.2)
    
    def explore_parent_directories(self):
        """Explore parent directories"""
        print("Exploring parent directories...")
        
        parent_urls = [
            f"https://{self.base_domain}/tdsdata/",
            f"https://{self.base_domain}/",
            f"https://{self.base_domain}/tdsdata/crawl/",
            f"https://{self.base_domain}/tdsdata/html/",
        ]
        
        for url in parent_urls:
            self.crawl_directory(url)
            time.sleep(0.2)
    
    def run(self):
        """Run the aggressive spider"""
        print(f"Starting aggressive spider for domain: {self.base_domain}")
        print("=" * 80)
        
        # Start with the original URL
        start_url = f"https://{self.base_domain}/tdsdata/crawl_html/"
        self.crawl_directory(start_url)
        
        # Explore different patterns
        self.explore_letter_directories()
        self.explore_numeric_directories()
        self.explore_common_directories()
        self.explore_parent_directories()
        
        # Try some wildcard patterns
        print("Trying wildcard patterns...")
        wildcard_patterns = [
            f"https://{self.base_domain}/tdsdata/crawl_html/*/",
            f"https://{self.base_domain}/tdsdata/*/",
            f"https://{self.base_domain}/*/",
        ]
        
        for pattern in wildcard_patterns:
            # Try common variations
            for suffix in ['a/', 'b/', 'c/', 'j/', 'k/', 'l/', 'm/', 'n/', 'o/', 'p/', 'q/', 'r/', 's/', 't/', 'u/', 'v/', 'w/']:
                url = pattern.replace('*', suffix)
                self.crawl_directory(url)
                time.sleep(0.1)
        
        self.print_results()
    
    def print_results(self):
        """Print final results"""
        print("\n" + "=" * 80)
        print("AGGRESSIVE SPIDER COMPLETE")
        print("=" * 80)
        print(f"Total URLs visited: {self.stats['total_urls_visited']}")
        print(f"HTML files found: {len(self.html_files)}")
        print(f"J-W files found: {len(self.j_to_w_files)}")
        print(f"Errors encountered: {self.stats['errors']}")
        
        duration = datetime.now() - self.stats['start_time']
        print(f"Crawling duration: {duration}")
        
        print(f"\nAll HTML files found ({len(self.html_files)}):")
        for i, file_url in enumerate(sorted(self.html_files), 1):
            filename = urlparse(file_url).path.split('/')[-1]
            print(f"{i:3d}. {filename} -> {file_url}")
        
        print(f"\nHTML files beginning with J to W ({len(self.j_to_w_files)}):")
        for i, file_url in enumerate(sorted(self.j_to_w_files), 1):
            filename = urlparse(file_url).path.split('/')[-1]
            print(f"{i:3d}. {filename} -> {file_url}")
        
        print(f"\nFINAL COUNT: {len(self.j_to_w_files)} HTML files begin with letters J to W")
        
        # Save results
        results = {
            'stats': self.stats,
            'html_files': self.html_files,
            'j_to_w_files': self.j_to_w_files,
            'visited_urls': list(self.visited)
        }
        
        with open('aggressive_spider_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\nResults saved to: aggressive_spider_results.json")

def main():
    spider = AggressiveSpider("sanand0.github.io")
    spider.run()

if __name__ == "__main__":
    main() 