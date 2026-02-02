import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

# Absolute path loading to prevent .env not found errors
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def optimize_resume(resume_text, job_description):
    if not api_key:
        return "Error: API Key missing. Check your .env file."

    # Using 1.5-flash for speed and reliability
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are an expert ATS (Applicant Tracking System) Optimizer. 
    Rewrite the resume below to align with the Job Description.
    
    CRITICAL RULES:
    1. Do NOT invent fake experience.
    2. Use strong action verbs and keywords from the JD.
    3. Maintain a clean, professional plain-text layout.
    4. Return ONLY the optimized text. No preamble, no conversational filler.

    === Resume ===
    {resume_text}
    
    === Job Description ===
    {job_description}
    """
    
    try:
        response = model.generate_content(prompt)
        if response and response.text:
            # Remove any accidental markdown code blocks
            return response.text.replace('```text', '').replace('```', '').strip()
        return "Gemini returned empty content. Try a shorter Job Description."
    except Exception as e:
        return f"Optimization failed: {str(e)}"