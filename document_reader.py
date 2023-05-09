# Import PyPDF2 library for reading PDF files

import PyPDF2

# Function to read the content of a PDF file
def read_pdf_content(file_path):
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        content = ""
        for page_num in range(pdf_reader.numPages):
            content += pdf_reader.getPage(page_num).extractText()
    
    return content

# Function to save the content of a PDF file to the database
def save_pdf_content_to_db(file_path, db):
    content = read_pdf_content(file_path)
    
    document_id = db.documents.insert_one({'content': content}).inserted_id
    return document_id