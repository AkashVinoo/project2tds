from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pdfplumber
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

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()
    debug_rows = []
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        total_sum = 0.0
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for i, row in enumerate(table):
                    if not row:
                        continue
                    header = [str(c).strip().lower() if c else "" for c in row]
                    if "item" in header and "total" in header:
                        item_idx = header.index("item")
                        total_idx = header.index("total")
                        for data_row in table[i+1:]:
                            if not data_row or len(data_row) <= max(item_idx, total_idx):
                                continue
                            item = str(data_row[item_idx] or "").strip().lower()
                            total = str(data_row[total_idx] or "").strip()
                            if "contraption" in item:
                                num = re.sub(r"[^0-9.\-]", "", total.replace(",", ""))
                                try:
                                    val = float(num)
                                    total_sum += val
                                    debug_rows.append({"item": item, "total": total, "num": num, "val": val})
                                except Exception:
                                    debug_rows.append({"item": item, "total": total, "num": num, "val": "error"})
                        break
    return JSONResponse({"sum": round(total_sum, 2), "debug": debug_rows}) 