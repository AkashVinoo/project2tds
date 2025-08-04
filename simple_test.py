#!/usr/bin/env python3
"""
Simple test for the API endpoint
"""

import requests

def test_simple_api():
    """Test the API with a simple request"""
    
    # Create a simple test question
    question_content = """
    This is a simple test question.
    """
    
    # Save question to file
    with open("simple_test_question.txt", "w") as f:
        f.write(question_content)
    
    # Test the API
    url = "http://localhost:8000/api/"
    
    try:
        with open("simple_test_question.txt", "rb") as f:
            files = {"file": ("question.txt", f, "text/plain")}
            response = requests.post(url, files=files)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ API test passed!")
            return True
        else:
            print("❌ API test failed!")
            return False
            
    except Exception as e:
        print(f"❌ API test failed with exception: {e}")
        return False

if __name__ == "__main__":
    test_simple_api() 