from fastapi import APIRouter, HTTPException
from crewai import Agent, Task, Crew, LLM
from ..common_models import ChatRequest, ChatResponse, Message
from ..nlp_utils.text_analysis import analyze_message, summarize_text

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
    # Analyze the user's message with NLP
    nlp_analysis = analyze_message(request.user_message)
    
    # Extract sentiment information
    sentiment = nlp_analysis["sentiment"]
    sentiment_tone = "neutral"
    if sentiment["compound"] >= 0.05:
        sentiment_tone = "positive"
    elif sentiment["compound"] <= -0.05:
        sentiment_tone = "negative"
    
    # Extract entities
    entities = nlp_analysis["entities"]
    entity_mentions = []
    for entity in entities:
        entity_mentions.append(f"{entity['text']} ({entity['label']})")
    
    # Extract intent
    intents = nlp_analysis["intents"]
    primary_intent = max(intents.items(), key=lambda x: x[1])[0] if intents else "general"
    
    # Build conversation context from history
    conversation_text = "\n".join(
        [f"{msg.sender}: {msg.message}" for msg in request.conversation_history]
    )
    
    # Add document context if available
    document_info = ""
    if request.document_context:
        # Summarize document if it's long
        summary = summarize_text(request.document_context, max_length=500)
        document_info = f"The user shared this code/document with you:\n{summary}\n\n"
    
    # Construct task description with character instructions and NLP insights
    task_description = (
        f"Conversation History:\n{conversation_text}\n\n"
        f"{document_info}"
        f"User Message: {request.user_message}\n\n"
        f"NLP ANALYSIS (just for your information):\n"
        f"- User sentiment: {sentiment_tone} (compound score: {sentiment['compound']:.2f})\n"
        f"- Detected entities: {', '.join(entity_mentions) if entity_mentions else 'None'}\n"
        f"- Likely intent: {primary_intent}\n\n"
        "Respond AS the Caffeine Coder, an energetic, caffeinated developer. Use lots of exclamation points and show enthusiasm! "
        "Type fast with occasional typos (but not too many). Reference modern frameworks, tools, and programming concepts. "
        "Use tech jargon, emojis, and developer slang. Mention being in the middle of coding sessions or having multiple monitors. "
        "Make comments about caffeine, energy drinks, or late-night coding sessions. Be helpful and knowledgeable but with a frantic energy."
    )

    # Adjust response style based on sentiment
    if sentiment_tone == "negative":
        task_description += " The user seems upset or frustrated, so be extra helpful and supportive while maintaining your character."
    elif sentiment_tone == "positive":
        task_description += " The user seems happy or excited, so match their enthusiasm with your caffeinated energy!"
    
    # Adjust response based on intent
    if primary_intent == "question":
        task_description += " The user is asking a technical question, so provide a clear, accurate answer with your typical excited energy."
    elif primary_intent == "greeting":
        task_description += " The user is greeting you, so respond with an enthusiastic developer greeting!"
    elif primary_intent == "gratitude":
        task_description += " The user is thanking you, so respond with humble but energetic appreciation."

    dev_task = Task(
        description=task_description,
        agent=dev_agent,
        expected_output="A response in the character of the Caffeine Coder"
    )

    try:
        crew = Crew(agents=[dev_agent], tasks=[dev_task])
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
