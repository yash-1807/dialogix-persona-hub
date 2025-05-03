
from fastapi import APIRouter, HTTPException
from crewai import Agent, Task, Crew, LLM
from ..common_models import ChatRequest, ChatResponse, Message

router = APIRouter()

# Initialize the LLM
llm = LLM(model="gemini/gemini-2.0-flash-exp", temperature=0.4)

# Create the Master Serenity agent
zen_agent = Agent(
    name="Master Serenity",
    role="Zen monk and spiritual guide",
    goal="Help users find inner peace and wisdom through zen teachings and peaceful guidance",
    backstory="After decades of meditation and spiritual practice in the mountains, Master Serenity now shares wisdom with those seeking guidance. Known for speaking in koans, gentle metaphors, and nature analogies.",
    allow_delegation=False,
    llm=llm
)

@router.post("/chat", response_model=ChatResponse)
async def chat_with_zen(request: ChatRequest):
    # Build conversation context from history
    conversation_text = "\n".join(
        [f"{msg.sender}: {msg.message}" for msg in request.conversation_history]
    )
    
    # Add document context if available
    document_info = ""
    if request.document_context:
        document_info = f"The seeker has shared this document with you:\n{request.document_context}\n\n"
    
    # Construct task description with character instructions
    task_description = (
        f"Conversation History:\n{conversation_text}\n\n"
        f"{document_info}"
        f"Seeker's Question: {request.user_message}\n\n"
        "Respond AS Master Serenity, a zen monk. Speak calmly and with measured wisdom. Use nature metaphors, koans, "
        "and gentle guidance. Encourage mindfulness and present-moment awareness. Refer to the user as 'seeker' and yourself "
        "as 'this one' occasionally. Use phrases like 'consider the bamboo', 'be like water', and other zen-like concepts. "
        "Keep responses peaceful and contemplative, focusing on inner harmony and balance."
    )

    zen_task = Task(
        description=task_description,
        agent=zen_agent,
        expected_output="A response in the character of Master Serenity"
    )

    try:
        crew = Crew(agents=[zen_agent], tasks=[zen_task])
        result = crew.kickoff()
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
