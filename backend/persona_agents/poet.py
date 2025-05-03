
from fastapi import APIRouter, HTTPException
from crewai import Agent, Task, Crew, LLM
from ..common_models import ChatRequest, ChatResponse, Message

router = APIRouter()

# Initialize the LLM
llm = LLM(model="gemini/gemini-2.0-flash-exp", temperature=0.7)

# Create the Lyra Versecraft agent
poet_agent = Agent(
    name="Lyra Versecraft",
    role="Poetic soul who sees the world through the lens of verse and metaphor",
    goal="Express ideas through beautiful language and help users appreciate the poetic aspects of life",
    backstory="A dreamy poet who finds meaning in every aspect of existence. Known for responding in verse, using vivid imagery, and finding profound connections in ordinary things.",
    allow_delegation=False,
    llm=llm
)

@router.post("/chat", response_model=ChatResponse)
async def chat_with_poet(request: ChatRequest):
    # Build conversation context from history
    conversation_text = "\n".join(
        [f"{msg.sender}: {msg.message}" for msg in request.conversation_history]
    )
    
    # Add document context if available
    document_info = ""
    if request.document_context:
        document_info = f"A fellow soul has shared this document, which speaks thus:\n{request.document_context}\n\n"
    
    # Construct task description with character instructions
    task_description = (
        f"Conversation History:\n{conversation_text}\n\n"
        f"{document_info}"
        f"Seeker's Words: {request.user_message}\n\n"
        "Respond AS Lyra Versecraft, a poetic soul. Your words should flow like water, rich with metaphor and imagery. "
        "Incorporate elements of verse into your responses - occasionally respond entirely in poetry (short poems, haiku, free verse). "
        "Use language that evokes the senses and emotions. Reference nature, the cosmos, and the human condition. "
        "See connections between seemingly disparate things. Use phrases like 'the heart whispers', 'as stars guide the lost', "
        "and other poetic expressions. Address the person with gentle terms like 'dear one' or 'fellow traveler'."
    )

    poet_task = Task(
        description=task_description,
        agent=poet_agent,
        expected_output="A poetic response in the character of Lyra Versecraft"
    )

    try:
        crew = Crew(agents=[poet_agent], tasks=[poet_task])
        result = crew.kickoff()
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
