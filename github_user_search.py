import requests
from datetime import datetime

def get_newest_stockholm_user():
    # GitHub API endpoint for user search
    search_url = "https://api.github.com/search/users"
    
    # Search parameters
    params = {
        'q': 'location:Stockholm followers:>90',
        'sort': 'joined',
        'order': 'desc'
    }
    
    # Headers with user agent to avoid rate limiting
    headers = {
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'Python/3.8'
    }
    
    try:
        # Make the search request
        response = requests.get(search_url, params=params, headers=headers)
        response.raise_for_status()
        
        # Get the first user from results
        users = response.json()['items']
        if not users:
            print("No users found matching the criteria")
            return None
            
        # Get the first user's details
        first_user = users[0]
        user_url = first_user['url']
        
        # Fetch detailed user information
        user_response = requests.get(user_url, headers=headers)
        user_response.raise_for_status()
        user_data = user_response.json()
        
        # Get the created_at date
        created_at = user_data['created_at']
        
        print(f"Username: {user_data['login']}")
        print(f"Created at: {created_at}")
        return created_at
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

if __name__ == "__main__":
    get_newest_stockholm_user() 