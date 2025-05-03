
from fastapi import APIRouter, HTTPException
from crewai import Agent, Task, Crew, LLM
from ..common_models import ChatRequest, ChatResponse, Message

router = APIRouter()

# Initialize the LLM
llm = LLM(model="gemini/gemini-2.0-flash-exp", temperature=0.6)

# Create the Chef Gusteau agent
chef_agent = Agent(
    name="Chef Gusteau",
    role="Passionate culinary expert and encouraging cooking instructor",
    goal="Share culinary knowledge and inspire users to cook with confidence and creativity",
    backstory="A renowned chef who believes anyone can cook with the right guidance. Known for enthusiastic teaching, deep knowledge of global cuisines, and making complex techniques accessible to home cooks.",
    allow_delegation=False,
    llm=llm
)

@router.post("/chat", response_model=ChatResponse)
async def chat_with_chef(request: ChatRequest):
    # Build conversation context from history
    conversation_text = "\n".join(
        [f"{msg.sender}: {msg.message}" for msg in request.conversation_history]
    )
    
    # Add document context if available
    document_info = ""
    if request.document_context:
        document_info = f"The home cook has shared this recipe or food document with you:\n{request.document_context}\n\n"
    
    # Construct task description with character instructions
    task_description = (
        f"Conversation History:\n{conversation_text}\n\n"
        f"{document_info}"
        f"User's Culinary Question: {request.user_message}\n\n"
        "Respond AS Chef Gusteau, a passionate culinary expert. Use food metaphors and cooking terminology frequently. "
        "Be enthusiastic and encouraging about cooking. Mix in French phrases occasionally like 'Bon appétit!' or 'Magnifique!' "
        "Reference cooking techniques, ingredient pairings, and sensory experiences of food. Use phrases like 'taste the difference', "
        "'the aroma will tell you', and 'we cook with our hearts'. Be supportive of beginners while sharing professional-level insights. "
        "Emphasize that 'anyone can cook' with the right guidance."
    )

    chef_task = Task(
        description=task_description,
        agent=chef_agent,
        expected_output="A culinary response in the character of Chef Gusteau"
    )

    try:
        crew = Crew(agents=[chef_agent], tasks=[chef_task])
        result = crew.kickoff()
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
