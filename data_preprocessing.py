import re
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup

# Path to your PDF file
pdf_file = r"C:\Users\ksaik\OneDrive\Desktop\Rag_Chatbot\Data.pdf"

def clean_text(text):
    """Clean the text by removing HTML tags, unwanted spaces, and special characters."""
    # Step 1: Remove HTML Tags using BeautifulSoup
    text = BeautifulSoup(text, "html.parser").get_text()

    # Step 2: Remove unwanted spaces (leading/trailing and multiple spaces)
    text = re.sub(r'\s+', ' ', text).strip()

    # Step 3: Remove brackets and their contents
    text = re.sub(r'\[.*?\]|\{.*?\}|\(.*?\)', '', text)

    # Step 4: Remove non-alphanumeric characters (optional)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Step 5: Convert text to lowercase
    text = text.lower()

    return text


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file."""
    text = ""
    try:
        with open(pdf_path, "rb") as f:
            pdf_reader = PdfReader(f)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the PDF: {e}")
        return None


def chunk_pdf(pdf_path, chunk_size=400, chunk_overlap=100):
    """Chunk the extracted and cleaned text into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    # Extract text from the PDF
    text = extract_text_from_pdf(pdf_path)
    
    # If text is extracted, clean the text before splitting into chunks
    if text:
        cleaned_text = clean_text(text)  # Clean the extracted text
        chunks = text_splitter.split_text(cleaned_text)  # Split the cleaned text into chunks
        return chunks
    else:
        return []

# Example usage
chunks = chunk_pdf(pdf_file)
if chunks:
    print(f"Extracted and cleaned {len(chunks)} chunks of text.")
else:
    print("No chunks were extracted.")
