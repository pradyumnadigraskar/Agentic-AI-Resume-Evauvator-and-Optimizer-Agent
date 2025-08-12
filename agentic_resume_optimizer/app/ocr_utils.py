import pytesseract
from pdf2image import convert_from_path

# Set your path to tesseract
pytesseract.pytesseract.tesseract_cmd = r"D:\exam study\Tesseract\tesrt\tesseract.exe"

def extract_text_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path)
    full_text = ""
    for page in pages:
        text = pytesseract.image_to_string(page)
        full_text += text + "\n"
    return full_text.strip()