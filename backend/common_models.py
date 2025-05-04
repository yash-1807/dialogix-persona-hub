from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Message(BaseModel):
    sender: str  # "user" or "ai"
    message: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    user_message: str
    conversation_history: List[Message]
    document_context: Optional[str] = None  # For uploaded document content

class ChatResponse(BaseModel):
    response: str

class NLPAnalysisRequest(BaseModel):
    text: str
    document: Optional[str] = None

class NLPAnalysisResponse(BaseModel):
    sentiment: Dict[str, float]
    entities: List[Dict[str, Any]]
    intents: Dict[str, float]
    document_summary: Optional[str] = None
    document_entities: Optional[List[Dict[str, Any]]] = None
