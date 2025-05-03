
from pydantic import BaseModel
from typing import List, Optional

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
