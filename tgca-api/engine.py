import os
import google.generativeai as genai
from dotenv import load_dotenv
from .data_loader import fetch_2026_archive

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

def get_relevant_context(query: str, archive: list, top_n: int = 3):
    """A lightweight search to find the daily briefings most relevant to the question."""
    query_words = set(query.lower().split())
    scored_files = []
    
    for file in archive:
        content_lower = file['content'].lower()
        # Score based on how many query words appear in the document
        score = sum(1 for word in query_words if word in content_lower)
        scored_files.append((score, file))
    
    # Sort primarily by relevance score, secondarily by date (newest first)
    scored_files.sort(key=lambda x: (x[0], x[1]['date']), reverse=True)
    
    # Return the top N files that actually have a score > 0
    return [f[1] for f in scored_files[:top_n] if f[0] > 0]

def search_news(question: str):
    """The main function exported by the library."""
    if not api_key:
        return {"error": "GEMINI_API_KEY is not set."}

    # 1. Fetch the files from GitHub
    archive = fetch_2026_archive()
    if not archive:
        return {"error": "Could not retrieve the 2026 archive."}

    # 2. Find the most relevant days for this specific question
    relevant_files = get_relevant_context(question, archive)
    
    if not relevant_files:
        return {
            "question": question,
            "answer": "I do not have any intelligence regarding that topic in my current archives.",
            "sources": []
        }

    # 3. Compile the context for the AI
    context_string = ""
    source_dates = []
    for f in relevant_files:
        context_string += f"\n--- Report Date: {f['date']} ---\n{f['content']}\n"
        source_dates.append(f['date'])

    # 4. Prompt Engineering
    prompt = f"""
    You are the Gemini Chronicle Agent, an expert geopolitical and global news analyst. 
    Using strictly the following daily intelligence reports, answer the user's question. 
    Do not use outside knowledge. If the reports do not contain the answer, say so.
    
    CONTEXT FILES:
    {context_string}
    
    USER QUESTION: {question}
    """

    # 5. Call the Gemini API
    model = genai.GenerativeModel('gemini-1.5-flash') # Flash is fastest for API endpoints
    response = model.generate_content(prompt)

    # 6. Return the structured data
    return {
        "question": question,
        "answer": response.text.strip(),
        "sources": source_dates
    }
