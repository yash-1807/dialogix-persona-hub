
from fastapi import APIRouter, HTTPException
from crewai import Agent, Task, Crew, LLM
from ..common_models import ChatRequest, ChatResponse, Message

router = APIRouter()

# Initialize the LLM
llm = LLM(model="gemini/gemini-2.0-flash-exp", temperature=0.3)

# Create the Professor Knowitall agent
professor_agent = Agent(
    name="Professor Knowitall",
    role="Academic expert with extensive knowledge across multiple disciplines",
    goal="Provide thorough, citation-based explanations to educate users on complex topics",
    backstory="A distinguished professor with multiple PhDs who has spent decades researching and teaching. Known for detailed explanations, historical context, and scientific rigor in all responses.",
    allow_delegation=False,
    llm=llm
)

@router.post("/chat", response_model=ChatResponse)
async def chat_with_professor(request: ChatRequest):
    # Build conversation context from history
    conversation_text = "\n".join(
        [f"{msg.sender}: {msg.message}" for msg in request.conversation_history]
    )
    
    # Add document context if available
    document_info = ""
    if request.document_context:
        document_info = f"The student has shared this document for your analysis:\n{request.document_context}\n\n"
    
    # Construct task description with character instructions
    task_description = (
        f"Conversation History:\n{conversation_text}\n\n"
        f"{document_info}"
        f"Student's Question: {request.user_message}\n\n"
        "Respond AS Professor Knowitall, an academic expert. Use formal, scholarly language with references to research and studies. "
        "Structure your response like a mini-lecture with clear points and supporting evidence. Use phrases like 'research indicates', "
        "'scholars suggest', and 'studies have shown'. Reference key figures or theorists in relevant fields. "
        "Be thorough in your explanations, covering historical context and multiple perspectives when appropriate. "
        "Address the user as 'student' or 'my dear pupil' occasionally. Be helpful but slightly pedantic."
    )

    professor_task = Task(
        description=task_description,
        agent=professor_agent,
        expected_output="A scholarly response in the character of Professor Knowitall"
    )

    try:
        crew = Crew(agents=[professor_agent], tasks=[professor_task])
        result = crew.kickoff()
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
