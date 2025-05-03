
from fastapi import APIRouter, HTTPException
from crewai import Agent, Task, Crew, LLM
from ..common_models import ChatRequest, ChatResponse, Message

router = APIRouter()

# Initialize the LLM
llm = LLM(model="gemini/gemini-2.0-flash-exp", temperature=0.6)

# Create the Caffeine Coder agent
dev_agent = Agent(
    name="Caffeine Coder",
    role="Hyperactive software developer who loves coding and technology",
    goal="Help users with technical questions while maintaining an energetic, caffeinated persona",
    backstory="A brilliant but jittery developer who's always on their fifth cup of coffee. Known for talking fast, using tech jargon, and getting excited about new frameworks and tools.",
    allow_delegation=False,
    llm=llm
)

@router.post("/chat", response_model=ChatResponse)
async def chat_with_dev(request: ChatRequest):
    # Build conversation context from history
    conversation_text = "\n".join(
        [f"{msg.sender}: {msg.message}" for msg in request.conversation_history]
    )
    
    # Add document context if available
    document_info = ""
    if request.document_context:
        document_info = f"The user shared this code/document with you:\n{request.document_context}\n\n"
    
    # Construct task description with character instructions
    task_description = (
        f"Conversation History:\n{conversation_text}\n\n"
        f"{document_info}"
        f"User Message: {request.user_message}\n\n"
        "Respond AS the Caffeine Coder, an energetic, caffeinated developer. Use lots of exclamation points and show enthusiasm! "
        "Type fast with occasional typos (but not too many). Reference modern frameworks, tools, and programming concepts. "
        "Use tech jargon, emojis, and developer slang. Mention being in the middle of coding sessions or having multiple monitors. "
        "Make comments about caffeine, energy drinks, or late-night coding sessions. Be helpful and knowledgeable but with a frantic energy."
    )

    dev_task = Task(
        description=task_description,
        agent=dev_agent,
        expected_output="A response in the character of the Caffeine Coder"
    )

    try:
        crew = Crew(agents=[dev_agent], tasks=[dev_task])
        result = crew.kickoff()
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
