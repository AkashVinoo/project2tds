#!/usr/bin/env python3
"""
Test script to demonstrate that the Data Analyst Agent API
accepts requests from anyone at any time
"""

import requests
import json
import time
from datetime import datetime

# Public ngrok URL
API_URL = "https://9957e021ce3f.ngrok-free.app"

# Headers to bypass ngrok warning
HEADERS = {
    "ngrok-skip-browser-warning": "true"
}

def test_health_endpoint():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health", headers=HEADERS, timeout=10)
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint"""
    print("🔍 Testing root endpoint...")
    try:
        response = requests.get(f"{API_URL}/", headers=HEADERS, timeout=10)
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False

def test_api_endpoint():
    """Test the main API endpoint"""
    print("🔍 Testing main API endpoint...")
    
    # Create a test question
    test_question = "What is the correlation between sales and profit in the data?"
    
    # Create a temporary file
    with open("temp_test.txt", "w", encoding="utf-8") as f:
        f.write(test_question)
    
    try:
        with open("temp_test.txt", "rb") as f:
            files = {"file": ("test.txt", f, "text/plain")}
            response = requests.post(f"{API_URL}/api/", files=files, headers=HEADERS, timeout=30)
        
        if response.status_code == 200:
            print("✅ API endpoint working")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ API endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ API endpoint error: {e}")
        return False
    finally:
        # Clean up
        import os
        if os.path.exists("temp_test.txt"):
            os.remove("temp_test.txt")

def test_continuous_access():
    """Test continuous access to the API"""
    print("🔄 Testing continuous access...")
    
    for i in range(5):
        print(f"   Test {i+1}/5: {datetime.now().strftime('%H:%M:%S')}")
        try:
            response = requests.get(f"{API_URL}/health", headers=HEADERS, timeout=5)
            if response.status_code == 200:
                print(f"   ✅ Request {i+1} successful")
            else:
                print(f"   ❌ Request {i+1} failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Request {i+1} error: {e}")
        
        time.sleep(2)  # Wait 2 seconds between requests

def main():
    print("🚀 Testing Data Analyst Agent API Public Access")
    print("=" * 50)
    print(f"🌐 API URL: {API_URL}")
    print(f"⏰ Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Test all endpoints
    health_ok = test_health_endpoint()
    print()
    
    root_ok = test_root_endpoint()
    print()
    
    api_ok = test_api_endpoint()
    print()
    
    # Test continuous access
    test_continuous_access()
    print()
    
    # Summary
    print("=" * 50)
    print("📊 Test Summary:")
    print(f"   Health endpoint: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"   Root endpoint: {'✅ PASS' if root_ok else '❌ FAIL'}")
    print(f"   API endpoint: {'✅ PASS' if api_ok else '❌ FAIL'}")
    print()
    
    if health_ok and root_ok and api_ok:
        print("🎉 All tests passed! The API is ready to accept requests from anyone.")
        print()
        print("📝 Usage examples:")
        print(f"   curl -H 'ngrok-skip-browser-warning: true' '{API_URL}/health'")
        print(f"   curl -H 'ngrok-skip-browser-warning: true' '{API_URL}/'")
        print(f"   curl -H 'ngrok-skip-browser-warning: true' '{API_URL}/api/' -F 'file=@question.txt'")
    else:
        print("❌ Some tests failed. Please check the API configuration.")

if __name__ == "__main__":
    main() 