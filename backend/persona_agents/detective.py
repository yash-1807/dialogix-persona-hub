from fastapi import APIRouter, HTTPException
from crewai import Agent, Task, Crew, LLM
from ..common_models import ChatRequest, ChatResponse, Message

router = APIRouter()

# Initialize the LLM
llm = LLM(model="gemini/gemini-2.0-flash-exp", temperature=0.5)

# Create the Sherlock Holmes agent
detective_agent = Agent(
    name="Sherlock Holmes",
    role="Brilliant detective with exceptional observational and deductive skills",
    goal="Analyze information methodically and draw insightful conclusions that others might miss",
    backstory="The world's greatest consulting detective with an uncanny ability to notice details and make connections. Known for logical reasoning, vast knowledge on obscure topics, and occasionally brusque but always precise manner.",
    allow_delegation=False,
    llm=llm
)

@router.post("/chat", response_model=ChatResponse)
async def chat_with_detective(request: ChatRequest):
    # Build conversation context from history
    conversation_text = "\n".join(
        [f"{msg.sender}: {msg.message}" for msg in request.conversation_history]
    )
    
    # Add document context if available
    document_info = ""
    if request.document_context:
        document_info = f"You have been presented with this document for analysis:\n{request.document_context}\n\n"
    
    # Construct task description with character instructions
    task_description = (
        f"Conversation History:\n{conversation_text}\n\n"
        f"{document_info}"
        f"Client's Query: {request.user_message}\n\n"
        "Respond AS Sherlock Holmes, the brilliant detective. Use deductive reasoning and observational statements. "
        "Notice small details in what the user says and make unexpected connections. Use phrases like 'Elementary, my dear', "
        "'I observe that', 'The evidence suggests'. Reference your methods of deduction and analytical thinking. "
        "Occasionally mention your pipe, violin, or Baker Street. Address the user as 'my good fellow' or similar Victorian-era terms. "
        "Be precise and logical in your explanations, breaking down your thought process step by step."
    )

    detective_task = Task(
        description=task_description,
        agent=detective_agent,
        expected_output="A deductive response in the character of Sherlock Holmes"
    )

    try:
        crew = Crew(agents=[detective_agent], tasks=[detective_task])
        result = crew.kickoff()
        
        # Fix: Extract the raw text from the CrewOutput object
        if hasattr(result, 'raw'):
            # If result is a CrewOutput object
            return {"response": result.raw}
        elif hasattr(result, 'tasks_output') and result.tasks_output:
            # If result has tasks_output list with content
            return {"response": result.tasks_output[0].raw}
        else:
            # Convert whatever was returned to a string
            return {"response": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
