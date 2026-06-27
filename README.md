# Custom Llama RAG AI Agent (Chat with Your Documents)

A completely custom, code-based Retrieval-Augmented Generation (RAG) chatbot that allows you to "chat" with your private documents stored in Google Drive. By utilizing Python, Pinecone, Google Gemini (for embeddings), and **Llama** (via the Groq API), this project serves as a highly customizable alternative to paid no-code platforms like n8n. 

## 🌟 Features

*   **Automated Document Syncing:** Connects directly to a specific Google Drive folder to poll for new, updated, or deleted files.
*   **Smart Vectorization:** Downloads your Google Drive files, splits them into manageable chunks, and generates vector embeddings using Google Gemini.
*   **Efficient Vector Storage:** Automatically stores and manages document vectors within a Pinecone database. It uses a local `processed_files.json` tracker to seamlessly handle file updates and deletions without creating messy duplicates.
*   **Llama-Powered Chat:** Leverages a Llama model via the ultra-fast and free Groq API to provide customized, context-aware answers based strictly on your private data. *(Note: The original tutorial utilized DeepSeek, but this project is configured for Llama).*
*   **Rich Terminal Interface:** Provides a clean, colorful command-line UI for chatting using the Python `rich` library.

## 📋 Prerequisites

To run this project, you will need:
*   **Python 3:** Ensure you have Python 3 installed (via Homebrew for Mac/Linux or Chocolatey for Windows).
*   **API Keys:** You will need free API keys and credentials for:
    *   **Groq** (For the Llama model)
    *   **Google Cloud Console** (To enable Google Drive API and Gemini API, and to generate a Service Account JSON file)
    *   **Pinecone** (For the Vector Database)

## 🛠️ Installation & Setup

1. **Set up a Virtual Environment:**
   It is best practice to keep your dependencies isolated.
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   **

2. **Install Dependencies:**
   Install the required Python modules from your `requirements.txt`. (Required packages include `google-generativeai`, `google-api-python-client`, `pinecone`, `rich`, `requests`, `numpy`, `groq`, and `python-dotenv`).
   ```bash
   pip install -r requirements.txt
   ```
   **

3. **Configure Environment Variables:**
   Create a `.env` file in the root directory. This file will be hidden from source control to protect your API keys. Add the following variables:
   ```env
   GOOGLE_DRIVE_SERVICE_ACCOUNT_FILE="your_service_account.json"
   GOOGLE_DRIVE_FOLDER_ID="your_drive_folder_id"
   GROQ_API_KEY="your_groq_api_key"
   GOOGLE_GEMINI_API_KEY="your_gemini_api_key"
   PINECONE_API_KEY="your_pinecone_api_key"
   PINECONE_ENVIRONMENT="your_pinecone_region" # e.g., us-east-1
   PINECONE_INDEX_NAME="company_files"
   ```
   **

## 🚀 Usage

This application runs using two separate terminal instances: one to keep your vector database synchronized with your Google Drive, and another for the chat interface.

### 1. Start the Document Sync Service
Open a terminal, activate your virtual environment, and run the main application file:
```bash
python3 app.py
```
This script will initialize your Pinecone index, read your Google Drive folder, chunk the text, embed it via Gemini, and upload it to Pinecone. 

**Note:** The script runs on an automatic loop every hour (3600 seconds). If you update a document in Drive and want to sync it immediately, simply type `poll` in the terminal. Type `q` to quit the sync service.

### 2. Start the Chat Interface
Open a *second* terminal, activate your virtual environment, and start the chat application:
```bash
python3 interface.py
```
*(File may also be named `chat_interface.py` depending on your exact setup)*.

You can now start asking questions! The Llama model will embed your query, retrieve the top matching chunks of text from Pinecone, and formulate an answer based entirely on your Google Drive documents. 

## 🧠 Customizing the AI Persona
If you want the AI to act with a specific persona (for example, an "HR Assistant" or a "Restaurant Owner"), you can edit the **System Message** inside the chat interface code. You can also control how strictly the AI adheres to your documents versus its own general knowledge by adjusting the model's `temperature` settings.
