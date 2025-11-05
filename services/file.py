import os
from fastapi import UploadFile
from services.pdf_reader import extract_text

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def handle_file_upload(files: list[UploadFile]):
    file_analysis = []

    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save the file to disk
        with open(file_path, "wb") as f:
            contents = await file.read()
            f.write(contents)

        # Extract text from the file based on its type
        try:
            extracted_text = extract_text(file_path)
            analysis = {
                "filename": file.filename,
                "extracted_text": extracted_text[:1000]  # Preview first 1000 characters
            }
        except ValueError as e:
            analysis = {"error": str(e)}

        file_analysis.append(analysis)

    return file_analysis
