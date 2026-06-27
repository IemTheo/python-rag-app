import os
import sys
# For a nicer console output (optional):
from rich.console import Console
from groq import Groq

try:
    from app import get_embedding, index, console, GROQ_API_KEY
except ImportError:
    print("Make sure 'app.py' is in the same folder and named appropriately.")
    sys.exit(1)

def main():
    console.rule("[bold magenta]Company Documents Chat [/]") 
    console.print("[bold green]Type 'exit' to quit. [/]\n")
    
    while True:
        query = console.input("[bold cyan] Your Question> [/]").strip()
        if query.lower() in ("exit","quit"):
            break
        answer = chat_agent(query)
        console.print(f"\n[bold yellow]Answer:[/] {answer}\n")


def chat_agent(query: str) -> str:
    system_message =(
    "You are a helpful HR assistant designed to answer employee questions based on company policies."
    "Retrieve relevant information from the provided internal documents and provide a concise, accurate answer."
    "If the answer cannot be found in the provided documents, say 'I cannot find the answer in the available resources."
    )
    
    # 1) Embed the user query
    query_embedding = get_embedding(query)
    if query_embedding is None:
        return "Error obtaining query embedding."
    
    # 2) Query Pinecone
    try:
        result = index.query (
        vector=query_embedding, 
        top_k=3, 
        include_metadata=True, 
        namespace="default"
        )
    except Exception as e:
        return f"Error querying Pinecone: {str(e)}"
    
    if not result or "matches" not in result or not result["matches"]: 
        return "I cannot find the answer in the available resources."
    
    # Combine top results into a single string for context
    matches = result["matches"]
    context = " ".join(match["metadata"].get("text", "") for match in matches)
    if not context.strip():
        return "I cannot find the answer in the available resources."
    
    return groq_chat(system_message, query, context)


def groq_chat(system_message: str, query: str, context: str) -> str:

    client = Groq(api_key=GROQ_API_KEY)
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"{system_message}\n\nContext: {context}"
                },
                {
                    "role": "user",
                    "content": query
            }
            ],
            model="llama-3.3-70b-versatile", 
            temperature=0.2, 
            max_tokens=512
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    main()

