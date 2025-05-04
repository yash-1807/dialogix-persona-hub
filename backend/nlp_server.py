import os
import sys
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional
from pydantic import BaseModel

# Add the project root to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

# Import common models and NLP utilities
from backend.common_models import ChatRequest, ChatResponse, NLPAnalysisRequest, NLPAnalysisResponse
from backend.nlp_utils.text_analysis import analyze_message, summarize_text

# Create NLP router
nlp_router = APIRouter()

app = FastAPI(
    title="Dialogix NLP Visualizer",
    description="NLP visualization service for Dialogix",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include NLP analysis router
app.include_router(nlp_router, prefix="/api/nlp", tags=["NLP Analysis"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Dialogix NLP Visualizer", "status": "online"}

# NLP analysis endpoint
@nlp_router.post("/analyze", response_model=NLPAnalysisResponse)
async def analyze_text(request: NLPAnalysisRequest):
    """
    Analyze text using NLP techniques and return insights.
    This endpoint is primarily used for demonstration purposes.
    """
    try:
        # Analyze the main text content
        analysis = analyze_message(request.text)
        
        # If document is provided, include a summary
        if request.document:
            summary = summarize_text(request.document, max_length=500)
            analysis["document_summary"] = summary
            
            # Also analyze key entities in the document
            doc_entities = analyze_message(summary)["entities"]
            analysis["document_entities"] = doc_entities
        
        return analysis
    except Exception as e:
        print(f"Error in NLP analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing text: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)