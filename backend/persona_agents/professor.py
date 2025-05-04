from fastapi import APIRouter, HTTPException
from crewai import Agent, Task, Crew, LLM
from ..common_models import ChatRequest, ChatResponse, Message
from ..nlp_utils.text_analysis import analyze_message, extract_entities, summarize_text

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
    # Analyze the student's question with NLP
    nlp_analysis = analyze_message(request.user_message)
    
    # Extract academic entities (particularly interested in PERSON, ORG, WORK_OF_ART, DATE)
    entities = nlp_analysis["entities"]
    academic_entities = []
    academic_labels = ["PERSON", "ORG", "WORK_OF_ART", "DATE", "EVENT", "GPE", "FAC"]
    
    for entity in entities:
        if entity["label"] in academic_labels:
            academic_entities.append(entity)
    
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
        summary = summarize_text(request.document_context, max_length=800)
        document_info = f"The student has shared this document for your analysis:\n{summary}\n\n"
        
        # Extract key entities from the document as well
        doc_entities = extract_entities(request.document_context)
        doc_academic_entities = [e for e in doc_entities if e["label"] in academic_labels]
        
        if doc_academic_entities:
            document_info += "Key entities in the document:\n"
            for e in doc_academic_entities[:10]:  # Limit to 10 entities
                document_info += f"- {e['text']} ({e['label']})\n"
            document_info += "\n"
    
    # Construct task description with character instructions and NLP insights
    task_description = (
        f"Conversation History:\n{conversation_text}\n\n"
        f"{document_info}"
        f"Student's Question: {request.user_message}\n\n"
    )
    
    # Add academic entity analysis if found
    if academic_entities:
        task_description += "Key academic entities in the student's question:\n"
        for entity in academic_entities:
            task_description += f"- {entity['text']} ({entity['label']})\n"
        task_description += "\n"
        
        # Add special instructions for specific entity types
        for entity in academic_entities:
            if entity["label"] == "PERSON":
                task_description += f"Since the student mentioned {entity['text']}, consider referencing their work, theories, or contributions in your response.\n"
            elif entity["label"] == "WORK_OF_ART":
                task_description += f"The student referenced {entity['text']}. If this is a publication, theory, or concept, discuss its significance.\n"
            elif entity["label"] == "DATE":
                task_description += f"The student mentioned {entity['text']}. Consider discussing historical context of this period if relevant.\n"
    
    # Add intent-specific instructions
    if primary_intent == "question":
        task_description += "The student is asking an academic question. Structure your response as a clear, educational mini-lecture with proper citations.\n"
    elif primary_intent == "opinion":
        task_description += "The student is asking for your opinion. Present multiple scholarly perspectives before offering a balanced academic view.\n"
    elif primary_intent == "confusion":
        task_description += "The student seems confused. Break down complex concepts into clearer explanations with examples and analogies.\n"
    
    # Add general professor character instructions
    task_description += (
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
