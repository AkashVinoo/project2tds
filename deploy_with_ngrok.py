#!/usr/bin/env python3
"""
Deploy Data Analyst Agent API with ngrok
"""

import subprocess
import time
import requests
import sys
import os

def check_ngrok():
    """Check if ngrok is installed"""
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ngrok is installed")
            return True
        else:
            print("❌ ngrok is not installed or not in PATH")
            return False
    except FileNotFoundError:
        print("❌ ngrok is not installed or not in PATH")
        print("Please install ngrok from https://ngrok.com/download")
        return False

def start_api_server():
    """Start the API server in background"""
    print("🚀 Starting Data Analyst Agent API server...")
    
    # Start the server in background
    process = subprocess.Popen([
        sys.executable, 'data_analyst_agent.py'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait a moment for server to start
    time.sleep(3)
    
    # Check if server is running
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            print("✅ API server is running on http://localhost:8000")
            return process
        else:
            print("❌ API server failed to start")
            return None
    except requests.exceptions.RequestException:
        print("❌ API server failed to start")
        return None

def start_ngrok():
    """Start ngrok tunnel"""
    print("🌐 Starting ngrok tunnel...")
    
    # Start ngrok in background
    ngrok_process = subprocess.Popen([
        'ngrok', 'http', '8000'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for ngrok to start
    time.sleep(5)
    
    # Get the public URL
    try:
        response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
        if response.status_code == 200:
            tunnels = response.json()
            if tunnels['tunnels']:
                public_url = tunnels['tunnels'][0]['public_url']
                print(f"✅ ngrok tunnel is running: {public_url}")
                return ngrok_process, public_url
            else:
                print("❌ No ngrok tunnels found")
                return ngrok_process, None
        else:
            print("❌ Failed to get ngrok tunnel info")
            return ngrok_process, None
    except requests.exceptions.RequestException:
        print("❌ Failed to get ngrok tunnel info")
        return ngrok_process, None

def main():
    print("🚀 Deploying Data Analyst Agent API with ngrok...")
    print("=" * 60)
    
    # Check if ngrok is installed
    if not check_ngrok():
        return
    
    # Start API server
    api_process = start_api_server()
    if not api_process:
        return
    
    # Start ngrok tunnel
    ngrok_process, public_url = start_ngrok()
    if not public_url:
        print("❌ Failed to start ngrok tunnel")
        api_process.terminate()
        return
    
    print("\n" + "=" * 60)
    print("🎉 Deployment successful!")
    print(f"📡 Public API URL: {public_url}/api/")
    print(f"🔍 Health check: {public_url}/health")
    print(f"📚 API docs: {public_url}/docs")
    print("\n📝 Usage example:")
    print(f'curl "{public_url}/api/" -F "@question.txt"')
    print("\n⏹️  Press Ctrl+C to stop the servers")
    print("=" * 60)
    
    try:
        # Keep the processes running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        api_process.terminate()
        ngrok_process.terminate()
        print("✅ Servers stopped")

if __name__ == "__main__":
    main() 