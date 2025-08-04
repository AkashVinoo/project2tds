from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import io
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EMAIL = "24f2000935@ds.study.iitm.ac.in"
EXAM = "tds-2025-05-roe"

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()
    try:
        s = content.decode("utf-8")
    except UnicodeDecodeError:
        s = content.decode("latin1")
    delimiters = [',', ';', '\t', '|']
    for delim in delimiters:
        try:
            df = pd.read_csv(io.StringIO(s), delimiter=delim, engine='python', skipinitialspace=True)
            cols = [c.lower().replace(' ', '') for c in df.columns]
            cat_col = next((c for c in df.columns if 'category' in c.lower()), None)
            amt_col = next((c for c in df.columns if 'amount' in c.lower()), None)
            if cat_col and amt_col:
                # Clean category
                df[cat_col] = df[cat_col].astype(str).str.lower().str.replace(r'\s+', '', regex=True)
                # Clean amount
                def clean_amt(x):
                    if pd.isnull(x): return 0.0
                    x = str(x)
                    x = re.sub(r'[^0-9.\-]', '', x)
                    try: return float(x)
                    except: return 0.0
                df[amt_col] = df[amt_col].apply(clean_amt)
                # Filter for food
                food_mask = df[cat_col].str.contains('food', na=False)
                total = df.loc[food_mask, amt_col].sum()
                return {"answer": round(total, 2), "email": EMAIL, "exam": EXAM}
        except Exception:
            continue
    return {"answer": 0, "email": EMAIL, "exam": EXAM} 