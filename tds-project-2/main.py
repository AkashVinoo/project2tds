from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from app.agent import process_question_file
import uvicorn

app = FastAPI()

@app.post("/api/")
async def analyze(question_file: UploadFile = File(...), attachments: list[UploadFile] = File(default=[])):
    content = await question_file.read()
    answers = await process_question_file(content.decode(), attachments)
    return JSONResponse(content=answers)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
