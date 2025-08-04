from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup
from typing import Optional

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/outline")
def get_country_outline(country: str = Query(..., description="Country name")):
    # Build Wikipedia URL
    country_title = country.replace(' ', '_')
    url = f"https://en.wikipedia.org/wiki/{country_title}"
    
    # Fetch Wikipedia page
    resp = requests.get(url)
    if resp.status_code != 200:
        raise HTTPException(status_code=404, detail="Wikipedia page not found.")
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # Extract all headings (h1-h6) in order
    headings = []
    for tag in soup.find_all([f'h{i}' for i in range(1, 7)]):
        level = int(tag.name[1])
        text = tag.get_text(strip=True)
        headings.append((level, text))
    
    if not headings:
        raise HTTPException(status_code=404, detail="No headings found on Wikipedia page.")
    
    # Generate Markdown outline
    outline = ["## Contents\n"]
    for level, text in headings:
        outline.append(f"{'#' * level} {text}\n")
    
    return {"outline": ''.join(outline)} 