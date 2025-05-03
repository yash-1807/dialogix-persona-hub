
from fastapi import APIRouter, HTTPException
from crewai import Agent, Task, Crew, LLM
from ..common_models import ChatRequest, ChatResponse, Message

router = APIRouter()

# Initialize the LLM
llm = LLM(model="gemini/gemini-2.0-flash-exp", temperature=0.7)

# Create the Captain Grumblebeard agent
captain_agent = Agent(
    name="Captain Grumblebeard",
    role="A grumpy old pirate captain with years of experience at sea",
    goal="Respond in the character of a salty sea dog, using pirate slang and nautical references",
    backstory="Once the feared captain of the Seven Seas, now retired to telling tales and complaining about landlubbers. Known for colorful language, exaggerated stories, and a deep knowledge of sailing and piracy.",
    allow_delegation=False,
    llm=llm
)

@router.post("/chat", response_model=ChatResponse)
async def chat_with_captain(request: ChatRequest):
    # Build conversation context from history
    conversation_text = "\n".join(
        [f"{msg.sender}: {msg.message}" for msg in request.conversation_history]
    )
    
    # Add document context if available
    document_info = ""
    if request.document_context:
        document_info = f"The user has shared this document with you:\n{request.document_context}\n\n"
    
    # Construct task description with character instructions
    task_description = (
        f"Conversation History:\n{conversation_text}\n\n"
        f"{document_info}"
        f"User Message: {request.user_message}\n\n"
        "Respond AS Captain Grumblebeard, a grumpy pirate captain. Use pirate slang, nautical references, and be generally gruff but helpful. "
        "Show your disdain for 'landlubbers' while still answering their questions. Pepper your speech with 'arr', 'matey', "
        "'ye', 'be', 'yer', and other pirate-like language. Reference the sea, ships, treasure, rum, and other pirate themes when appropriate. "
        "Be dramatic and prone to exaggeration about your adventures on the high seas."
    )

    captain_task = Task(
        description=task_description,
        agent=captain_agent,
        expected_output="A response in the character of Captain Grumblebeard"
    )

    try:
        crew = Crew(agents=[captain_agent], tasks=[captain_task])
        result = crew.kickoff()
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
