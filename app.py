import os
import io
import json
import time
import sys
from datetime import datetime

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# For a nicer console output (optional) :
from rich.console import Console 
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

# Pinecone, Google PaLM:
import google.genai as genai 
from pinecone import Pinecone, ServerlessSpec

console = Console()



load_dotenv()

SERVICE_ACCOUNT_FILE = os. environ.get ("GOOGLE_DRIVE_SERVICE_ACCOUNT_FILE")
PINECONE_API_KEY = os. environ.get ("PINECONE_API_KEY")
PINECONE_ENV = os.environ.get ("PINECONE_ENV") # e. g. "us-west-2"
PINECONE_INDEX_NAME = os.environ.get ("PINECONE_INDEX_NAME")
GOOGLE_GEMINI_API_KEY = os.environ.get ("GOOGLE_GEMINI_API_KEY")
GROQ_API_KEY = os.environ.get ("GROQ_API_KEY")
GOOGLE_DRIVE_FOLDER_ID = os.environ.get ("GOOGLE_DRIVE_FOLDER_ID")

if not all([
    SERVICE_ACCOUNT_FILE, PINECONE_API_KEY, PINECONE_ENV,
    GOOGLE_GEMINI_API_KEY, GROQ_API_KEY, GOOGLE_DRIVE_FOLDER_ID
]):
    console.print("[red]Error: Missing one or more required environment variables. [/red]")
    sys.exit(1)



pc = Pinecone(api_key=PINECONE_API_KEY)
existing_indexes = [idx["name"] for idx in pc.list_indexes()]

if PINECONE_INDEX_NAME not in existing_indexes:
    console.print(f"[yellow]Index '{PINECONE_INDEX_NAME}' not found. Creating a new one... [/yellow]")
    # Adjust the 'dimension' here to match your chosen embedding model's dimension
    pc.create_index(
        name=PINECONE_INDEX_NAME, 
        dimension=3072, 
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=PINECONE_ENV)
    )

index = pc.Index(PINECONE_INDEX_NAME)

client = genai.Client(api_key=GOOGLE_GEMINI_API_KEY)

def get_embedding(text: str) -> list:
    """Use Google's Gemini to get an embedding for the given text."""
    try:
        # The new SDK takes the string directly via 'contents'
        response = client.models.embed_content(
            model="gemini-embedding-2", 
            contents=text
        )
        
        # The response is now an object. 
        # We access the list of embeddings, take the first one, and return its float values.
        if response.embeddings:
            return response.embeddings[0].values
            
    except Exception as e:
        # Catching the exception is the new standard way to handle failures here
        console.print(f"[red]Error obtaining embedding: {e}[/red]")
        
    return None

SCOPES = ['https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)





PROCESSED_FILES_PATH = "processed_files.json"
def load_processed_files():
    #Returns a dict with ( file_id: { modified: str, vectors: [vector_ids], name: str ), ...)
    if os.path.exists(PROCESSED_FILES_PATH):
        with open(PROCESSED_FILES_PATH, "r") as f:
            return json.load(f)
    return {}

def save_processed_files(processed):
    with open (PROCESSED_FILES_PATH, "w") as f:
        json.dump(processed, f, indent=2)



