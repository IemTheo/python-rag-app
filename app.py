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
from rich-progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

# Pinecone, Google PaLM:
import google.generativeai as palm 
from pinecone import Pinecone, ServerlessSpec

console = Console()
SERVICE_ ACCOUNT_FILE = os. environ.get ("GOOGLE_DRIVE_SERVICE_ACCOUNT_FILE")
PINECONE_ API_KEY = os. environ.get ("PINECONE_API_KEY")
PINECONE_ENV = os. environ.get ("PINECONE_ENV") # e. g.
"us-west-2"
PINECONE_INDEX_NAME = os.environ.get ("PINECONE_INDEX_NAME", "company-files")
GOOGLE_GEMINI_API_KEY = 05. environ.get ("GOOGLE_GEMINI_API_ KEY")
GROQ_API_KEY = os. environ-get ("GROQ_API_KEY")
GOOGLE_DRIVE_FOLDER_ID = 05- environ.get ("GOOGLE_DRIVE_FOLDER_ID", "«YOUR_ FOLDER_ ID_ HERE»"*)
if not all(l
SERVICE_ACCOUNT_FILE, PINECONE_API_KEY, PINECONE_ENV, GOOGLE_GEMINI_API_KEY, GROO_API KEY, GOOGLE_DRIVE_FOLDER_ID
1):
console-print("[red]Error: Missing one or more required environment variables. l/red]*)
sys.exit (1)