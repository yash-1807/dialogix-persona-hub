import os
import sys
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional

# Add the current directory to the Python path so imports work correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import all persona endpoints
from backend.persona_agents.captain import router as captain_router
from backend.persona_agents.zen import router as zen_router
from backend.persona_agents.dev import router as dev_router
from backend.persona_agents.chef import router as chef_router
from backend.persona_agents.professor import router as professor_router
from backend.persona_agents.poet import router as poet_router
from backend.persona_agents.detective import router as detective_router

# Import NLP analysis utilities
from backend.nlp_utils.text_analysis import analyze_message, summarize_text

# Import common models
from backend.common_models import ChatRequest, ChatResponse, NLPAnalysisRequest, NLPAnalysisResponse

# Create NLP router
nlp_router = APIRouter()

app = FastAPI(
    title="Dialogix API",
    description="Multi-persona conversational AI service",
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

# Include all persona routers
app.include_router(captain_router, prefix="/api/personas/captain", tags=["Captain Grumblebeard"])
app.include_router(zen_router, prefix="/api/personas/zen", tags=["Master Serenity"])
app.include_router(dev_router, prefix="/api/personas/dev", tags=["Caffeine Coder"])
app.include_router(chef_router, prefix="/api/personas/chef", tags=["Chef Gusteau"])
app.include_router(professor_router, prefix="/api/personas/professor", tags=["Professor Knowitall"])
app.include_router(poet_router, prefix="/api/personas/poet", tags=["Lyra Versecraft"])
app.include_router(detective_router, prefix="/api/personas/detective", tags=["Sherlock Holmes"])

# Include NLP analysis router
app.include_router(nlp_router, prefix="/api/nlp", tags=["NLP Analysis"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Dialogix API", "status": "online"}

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
        raise HTTPException(status_code=500, detail=f"Error analyzing text: {str(e)}")

@app.get("/api/personas")
def get_personas():
    """Returns information about all available personas"""
    personas = [
        {
            "id": "captain",
            "name": "Captain Grumblebeard",
            "role": "Grumpy Pirate",
            "description": "A salty old sea dog with a flair for the dramatic and a disdain for landlubbers."
        },
        {
            "id": "zen",
            "name": "Master Serenity",
            "role": "Zen Monk",
            "description": "Find your center with this peaceful guide who speaks in koans and gentle wisdom."
        },
        {
            "id": "dev",
            "name": "Caffeine Coder",
            "role": "Energetic Developer",
            "description": "A hyperactive programmer who solves problems fast and talks even faster."
        },
        {
            "id": "chef",
            "name": "Chef Gusteau",
            "role": "Culinary Expert",
            "description": "A passionate chef who believes anyone can cook with the right guidance."
        },
        {
            "id": "professor",
            "name": "Professor Knowitall",
            "role": "Academic Expert",
            "description": "A scholarly type who provides detailed, citation-heavy explanations."
        },
        {
            "id": "poet",
            "name": "Lyra Versecraft",
            "role": "Poetic Soul",
            "description": "Expresses everything through beautiful, flowing verse and metaphor."
        },
        {
            "id": "detective",
            "name": "Sherlock Holmes",
            "role": "Deductive Genius",
            "description": "Observes the details others miss and makes surprising deductions."
        }
    ]
    return {"personas": personas}
