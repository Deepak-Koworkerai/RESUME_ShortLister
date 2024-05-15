import os
from PyPDF2 import PdfReader

def read_resumes(directory):
    resumes = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            with open(os.path.join(directory, filename), "rb") as file:
                pdf_reader = PdfReader(file)
                text = ""
                # Iterate through all pages and extract text
                for page in pdf_reader.pages:
                    text += page.extract_text()
                # Append filename and content as a dictionary
                resumes.append({filename: text})
    print(f'total number of resumes :{len(resumes)}\n\n')

    return resumes

