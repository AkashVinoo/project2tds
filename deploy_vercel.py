#!/usr/bin/env python3
"""
Vercel Deployment Script for Data Analyst Agent
"""

import os
import subprocess
import sys
import json
from pathlib import Path

def check_vercel_cli():
    """Check if Vercel CLI is installed"""
    try:
        result = subprocess.run(['vercel', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Vercel CLI found: {result.stdout.strip()}")
            return True
        else:
            print("❌ Vercel CLI not found")
            return False
    except FileNotFoundError:
        print("❌ Vercel CLI not installed")
        return False

def install_vercel_cli():
    """Install Vercel CLI"""
    print("📦 Installing Vercel CLI...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'vercel'], check=True)
        print("✅ Vercel CLI installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Vercel CLI")
        return False

def create_vercel_project():
    """Create and configure Vercel project"""
    print("🚀 Setting up Vercel project...")
    
    # Check if .vercel directory exists
    if Path('.vercel').exists():
        print("✅ Vercel project already configured")
        return True
    
    try:
        # Initialize Vercel project
        subprocess.run(['vercel', '--yes'], check=True)
        print("✅ Vercel project initialized")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to initialize Vercel project")
        return False

def deploy_to_vercel():
    """Deploy the application to Vercel"""
    print("🚀 Deploying to Vercel...")
    
    try:
        # Deploy to Vercel
        result = subprocess.run(['vercel', '--prod'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Deployment successful!")
            
            # Extract the deployment URL
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if 'https://' in line and 'vercel.app' in line:
                    deployment_url = line.strip()
                    print(f"🌍 Your API is deployed at: {deployment_url}")
                    print(f"📊 API endpoint: {deployment_url}/api/")
                    print(f"🔍 Health check: {deployment_url}/health")
                    return deployment_url
            
            print("⚠️ Could not extract deployment URL from output")
            return None
        else:
            print(f"❌ Deployment failed: {result.stderr}")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        return None

def test_deployment(url):
    """Test the deployed API"""
    print(f"🧪 Testing deployed API at {url}...")
    
    try:
        import requests
        
        # Test health endpoint
        health_response = requests.get(f"{url}/health", timeout=10)
        if health_response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {health_response.status_code}")
            return False
        
        # Test API endpoint with sample data
        test_question = """
Scrape the list of highest grossing films from Wikipedia. It is at the URL:
https://en.wikipedia.org/wiki/List_of_highest-grossing_films

Answer the following questions and respond with a JSON array of strings containing the answer.

1. How many $2 bn movies were released before 2000?
2. Which is the earliest film that grossed over $1.5 bn?
3. What's the correlation between the Rank and Peak?
4. Draw a scatterplot of Rank and Peak along with a dotted red regression line through it.
   Return as a base-64 encoded data URI, `"data:image/png;base64,iVBORw0KG..."` under 100,000 bytes.
"""
        
        files = {"questions": ("questions.txt", test_question, "text/plain")}
        api_response = requests.post(f"{url}/api/", files=files, timeout=180)
        
        if api_response.status_code == 200:
            result = api_response.json()
            print("✅ API test passed!")
            print(f"Response: {result}")
            return True
        else:
            print(f"❌ API test failed: {api_response.status_code}")
            print(f"Error: {api_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main deployment function"""
    print("🎯 Vercel Deployment for Data Analyst Agent")
    print("=" * 60)
    
    # Check if Vercel CLI is installed
    if not check_vercel_cli():
        print("Installing Vercel CLI...")
        if not install_vercel_cli():
            print("❌ Failed to install Vercel CLI")
            print("Please install manually: npm i -g vercel")
            return
    
    # Create Vercel project
    if not create_vercel_project():
        print("❌ Failed to create Vercel project")
        return
    
    # Deploy to Vercel
    deployment_url = deploy_to_vercel()
    if not deployment_url:
        print("❌ Deployment failed")
        return
    
    # Test the deployment
    print("\n" + "=" * 60)
    if test_deployment(deployment_url):
        print("\n🎉 Deployment and testing completed successfully!")
        print(f"📋 Use this URL for your submission: {deployment_url}/api/")
    else:
        print("\n⚠️ Deployment completed but testing failed")
        print("Please check the logs and test manually")
    
    print("\n" + "=" * 60)
    print("📚 Next steps:")
    print("1. Create a GitHub repository")
    print("2. Push your code to GitHub")
    print("3. Submit your API endpoint URL")
    print("4. Monitor your Vercel dashboard for any issues")

if __name__ == "__main__":
    main()
