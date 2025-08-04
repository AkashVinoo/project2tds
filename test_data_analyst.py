#!/usr/bin/env python3
"""
Test script for Data Analyst Agent API
"""

import requests
import json
import time

def test_wikipedia_analysis():
    """Test the Wikipedia highest grossing films analysis"""
    
    # Create test question file content
    question_content = """
Scrape the list of highest grossing films from Wikipedia. It is at the URL:
https://en.wikipedia.org/wiki/List_of_highest-grossing_films

Answer the following questions and respond with a JSON array of strings containing the answer.

1. How many $2 bn movies were released before 2000?
2. Which is the earliest film that grossed over $1.5 bn?
3. What's the correlation between the Rank and Peak?
4. Draw a scatterplot of Rank and Peak along with a dotted red regression line through it.
   Return as a base-64 encoded data URI, `"data:image/png;base64,iVBORw0KG..."` under 100,000 bytes.
"""
    
    # Save question to file
    with open("test_question.txt", "w") as f:
        f.write(question_content)
    
    # Test the API
    url = "http://localhost:8000/api/"
    
    try:
        with open("test_question.txt", "rb") as f:
            files = {"file": ("question.txt", f, "text/plain")}
            response = requests.post(url, files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Wikipedia analysis test passed!")
            print(f"Result: {result}")
            return True
        else:
            print(f"❌ Wikipedia analysis test failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Wikipedia analysis test failed with exception: {e}")
        return False

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Health check passed!")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed with exception: {e}")
        return False

def main():
    print("🧪 Testing Data Analyst Agent API...")
    print("=" * 50)
    
    # Test health check first
    if not test_health_check():
        print("❌ API is not running. Please start the server first.")
        return
    
    # Wait a moment for the server to be ready
    time.sleep(2)
    
    # Test Wikipedia analysis
    success = test_wikipedia_analysis()
    if not success:
        print("❌ Wikipedia analysis test failed")
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")

if __name__ == "__main__":
    main() 