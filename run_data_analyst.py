#!/usr/bin/env python3
"""
Data Analyst Agent Server Startup Script
"""

import uvicorn
from data_analyst_agent import app

if __name__ == "__main__":
    print("Starting Data Analyst Agent API...")
    print("API will be available at: http://localhost:8000")
    print("Health check: http://localhost:8000/health")
    print("API docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 