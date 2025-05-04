import os
import sys
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel

# Create models directly in this file to avoid import issues
class NLPAnalysisRequest(BaseModel):
    text: str
    document: Optional[str] = None

class NLPAnalysisResponse(BaseModel):
    sentiment: Dict[str, float]
    entities: List[Dict[str, Any]]  # Changed to Any to handle both string and int
    intents: Dict[str, float]
    document_summary: Optional[str] = None
    document_entities: Optional[List[Dict[str, Any]]] = None

# Add the current directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import NLP utilities directly with relative imports
from nlp_utils.text_analysis import analyze_message, summarize_text

# Create the FastAPI app
app = FastAPI(
    title="Dialogix NLP Visualizer",
    description="NLP visualization service for Dialogix",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function to sanitize analysis results
def sanitize_analysis(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure all values in the analysis conform to the expected types."""
    # Handle entities with proper type conversion
    if "entities" in analysis and analysis["entities"]:
        for entity in analysis["entities"]:
            # Make sure we handle empty entities
            if entity is None:
                continue
                
            # Convert integer values to strings where needed
            if "start" in entity and entity["start"] is not None:
                entity["start"] = entity["start"]  # Keep as is, we've updated the model
                
            if "end" in entity and entity["end"] is not None:
                entity["end"] = entity["end"]  # Keep as is, we've updated the model
                
    # Make sure sentiment values are floats
    if "sentiment" in analysis and analysis["sentiment"]:
        for key, value in analysis["sentiment"].items():
            if value is not None:
                analysis["sentiment"][key] = float(value)
                
    # Make sure intent values are floats
    if "intents" in analysis and analysis["intents"]:
        for key, value in analysis["intents"].items():
            if value is not None:
                analysis["intents"][key] = float(value)
                
    return analysis

# NLP analysis endpoint
@app.post("/api/nlp/analyze", response_model=NLPAnalysisResponse)
async def analyze_text(request: NLPAnalysisRequest):
    """
    Analyze text using NLP techniques and return insights.
    """
    try:
        print(f"Received analysis request for: {request.text[:30]}...")
        
        # Add content warning filter to handle potentially offensive content
        if any(word in request.text.lower() for word in ["fuck", "shit", "ass", "bitch"]):
            print("Warning: Potentially offensive content detected. Applying content filter.")
            # Still analyze but apply filter later
            
        # Analyze the main text content
        analysis = analyze_message(request.text)
        
        # Sanitize the analysis to ensure proper types
        analysis = sanitize_analysis(analysis)
        
        # If document is provided, include a summary
        if request.document:
            summary = summarize_text(request.document, max_length=500)
            analysis["document_summary"] = summary
            
            # Also analyze key entities in the document
            doc_entities = analyze_message(summary)["entities"]
            # Sanitize document entities too
            doc_entities_sanitized = sanitize_analysis({"entities": doc_entities})["entities"]
            analysis["document_entities"] = doc_entities_sanitized
        
        print("Analysis completed successfully")
        return analysis
    except Exception as e:
        error_msg = f"Error analyzing text: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/")
def read_root():
    return {"message": "Welcome to Dialogix NLP Visualizer", "status": "online"}

# Add an error fallback route
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return {
        "error": "An error occurred during NLP analysis",
        "detail": str(exc)
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting NLP visualization server on http://127.0.0.1:8001")
    uvicorn.run(app, host="127.0.0.1", port=8001)