import pypdf
import io

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """PDF Bytes se Text Extract karta hai."""
    try:
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        extracted_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
        return extracted_text.strip()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""