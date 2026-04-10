from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tgca_api.engine import search_news

app = FastAPI(
    title="TGCA Intelligence API",
    description="Real-time querying of the Gemini Chronicle Agent 2026 Archive",
    version="1.0.0"
)

# Crucial for allowing frontend JS to make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "TGCA API is live and listening."}

@app.get("/ask")
def ask_agent(query: str):
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required.")
        
    try:
        # Calls the actual engine
        result = search_news(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
