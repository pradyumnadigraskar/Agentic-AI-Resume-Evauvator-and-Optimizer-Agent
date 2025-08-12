from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.ocr_utils import extract_text_from_pdf
from app.ats_score import calculate_ats_score
from app.resume_optimizer import optimize_resume
import shutil
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process/")
async def process_resume(
    request: Request,
    resume_file: UploadFile,
    job_description: str = Form(...)
):
    file_path = f"temp_{resume_file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume_file.file, buffer)

    # Extract original resume text
    original_text = extract_text_from_pdf(file_path)
    original_score = calculate_ats_score(original_text, job_description)

    # Get optimized resume
    optimized_text = optimize_resume(original_text, job_description)
    optimized_score = calculate_ats_score(optimized_text, job_description)

    # Save optimized resume for download
    output_path = os.path.join(BASE_DIR, "static", "optimized_resume.txt")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(optimized_text)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "original_text": original_text,
        "original_score": original_score,
        "optimized_text": optimized_text,
        "optimized_score": optimized_score,
        "download_link": "/static/optimized_resume.txt"
    })
