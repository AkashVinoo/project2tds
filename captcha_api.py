from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pytesseract
import re
import io

# Set the tesseract executable path for Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = FastAPI()

# Add CORS middleware to allow all origins (for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EMAIL = "24f2000935@ds.study.iitm.ac.in"

@app.post("/captcha")
async def solve_captcha(file: UploadFile = File(...)):
    # Read image from upload
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert('L')
    # OCR
    text = pytesseract.image_to_string(image)
    # Find two 8-digit numbers and a multiplication sign
    match = re.search(r'(\d{8})\s*[xX*]\s*(\d{8})', text)
    if not match:
        return JSONResponse(status_code=400, content={"error": "Could not find multiplication task in image."})
    a, b = int(match.group(1)), int(match.group(2))
    answer = a * b
    return {"answer": answer, "email": EMAIL}

# To run: uvicorn captcha_api:app --reload 