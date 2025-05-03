
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

# Import all persona endpoints
from persona_agents.captain import router as captain_router
from persona_agents.zen import router as zen_router
from persona_agents.dev import router as dev_router
from persona_agents.chef import router as chef_router
from persona_agents.professor import router as professor_router
from persona_agents.poet import router as poet_router
from persona_agents.detective import router as detective_router

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

@app.get("/")
def read_root():
    return {"message": "Welcome to Dialogix API", "status": "online"}

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
