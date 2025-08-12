import subprocess

def optimize_resume(resume_text, job_description):
    prompt = f"""
You are an ATS optimization expert and professional resume writer.

Your goal:
Improve the candidate's resume so it matches the given job description as closely as possible, while keeping the same section order and basic formatting.

Steps to follow:
1. Identify key skills, tools, and responsibilities from the job description.
2. Compare them to the resume and add missing but relevant keywords naturally into existing sections.
3. Rephrase bullet points to mirror the language of the job description, without inventing false information.
4. Add recommended skills needed for provided Job Discription.
5. Also add recommended tools for provided Job Discription.
6. Maintain a clean, ATS-friendly format (no tables, graphics, icons, or unusual characters).
7. Keep the original structure (Sections: Summary/Profile, Skills, Experience, Education, Projects, Certifications, etc.).

Important rules:
- Do not change or invent company names, Experience , job titles, or dates.
- Do not remove strong achievements — instead, enhance them.
- Make sure all added content could realistically be true for someone in this field.

=== Resume ===
{resume_text}

=== Job Description ===
{job_description}

Return only the fully optimized resume text, ready for submission.
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "mistral:latest", prompt],
            capture_output=True,
            text=True,
            encoding="utf-8",        # ✅ Force UTF-8 decoding
            errors="replace",        # ✅ Replace problematic characters instead of crashing
            check=True
        )

        if not result.stdout:
            raise ValueError("Ollama returned no output.")

        # Remove unwanted console mode error lines
        clean_lines = [
            line for line in result.stdout.splitlines()
            if not line.lower().startswith("failed to get console mode")
        ]

        return "\n".join(clean_lines).strip()

    except FileNotFoundError:
        return "Error: 'ollama' command not found. Please install Ollama and ensure it's in your PATH."

    except subprocess.CalledProcessError as e:
        return f"Ollama error (code {e.returncode}): {e.stderr or 'No error message'}"

    except Exception as e:
        return f"Unexpected error: {str(e)}"
