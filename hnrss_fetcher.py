import requests
import xml.etree.ElementTree as ET
from typing import Optional
import urllib.parse

def get_latest_cybersecurity_post() -> Optional[str]:
    """
    Fetch the latest Hacker News post about Cybersecurity with minimum 75 points.
    
    Returns:
        Optional[str]: URL of the latest post or None if not found
    """
    # Encode the search term
    search_term = urllib.parse.quote("Cybersecurity")
    
    # HNRSS API URL with search for Cybersecurity and minimum 75 points
    url = f"https://hnrss.org/newest?q={search_term}&points=75"
    
    print(f"Fetching from URL: {url}")
    
    try:
        # Make the request
        response = requests.get(url)
        response.raise_for_status()
        
        print(f"Response status code: {response.status_code}")
        print(f"Response content type: {response.headers.get('content-type', 'unknown')}")
        
        # Parse the XML response
        root = ET.fromstring(response.content)
        
        # Find all items
        items = root.findall('.//item')
        print(f"Found {len(items)} items")
        
        if not items:
            print("No posts found matching the criteria")
            return None
            
        # Get the link from the first item
        latest_post = items[0]
        link = latest_post.find('link')
        
        if link is not None:
            return link.text
        else:
            print("No link found in the post")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        print(f"Response content: {response.text[:500]}...")  # Print first 500 chars of response
        return None

def main():
    # Get the latest post
    post_url = get_latest_cybersecurity_post()
    
    if post_url:
        print(f"\nLatest Cybersecurity post with 75+ points:")
        print(post_url)
    else:
        print("Could not find a matching post")

if __name__ == "__main__":
    main() 