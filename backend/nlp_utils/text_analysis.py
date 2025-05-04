import nltk
import spacy
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict, List, Tuple, Any, Optional
import re

# Download necessary NLTK resources on first run
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('punkt')
    nltk.download('vader_lexicon')

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # If model is not installed, we'll download a smaller one
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Initialize sentiment analyzer
try:
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sentiment_analyzer = SentimentIntensityAnalyzer()
except:
    sentiment_analyzer = None

# Common user intents in a chat context
INTENT_KEYWORDS = {
    "greeting": ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"],
    "farewell": ["goodbye", "bye", "see you", "farewell", "later", "take care"],
    "gratitude": ["thanks", "thank you", "appreciate", "grateful"],
    "question": ["what", "why", "how", "when", "where", "who", "which", "can you", "could you"],
    "request": ["please", "can you", "could you", "would you", "help", "assist"],
    "opinion": ["think", "believe", "opinion", "feel about", "thoughts on"],
    "agreement": ["yes", "yeah", "agree", "correct", "right", "okay", "sure"],
    "disagreement": ["no", "nope", "disagree", "incorrect", "wrong", "not really"],
    "confusion": ["confused", "don't understand", "unclear", "what do you mean", "explain"]
}

def analyze_sentiment(text: str) -> Dict[str, float]:
    """
    Analyze the sentiment of a piece of text.
    Returns a dictionary with sentiment scores: negative, neutral, positive, and compound.
    """
    if not sentiment_analyzer:
        return {"negative": 0.0, "neutral": 0.5, "positive": 0.0, "compound": 0.0}
    
    scores = sentiment_analyzer.polarity_scores(text)
    return scores

def extract_entities(text: str) -> List[Dict[str, Any]]:
    """
    Extract named entities from text.
    Returns a list of dictionaries with entity text, label, and start/end positions.
    """
    doc = nlp(text)
    entities = []
    
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char
        })
    
    return entities

def identify_intent(text: str) -> Dict[str, float]:
    """
    Identify the likely intent of a message.
    Returns a dictionary mapping intent categories to confidence scores.
    """
    text = text.lower()
    intents = {}
    
    for intent, keywords in INTENT_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in text:
                # Add score based on keyword match
                score += 1
                # Add extra score for keywords at the beginning
                if re.search(r'^\s*' + re.escape(keyword), text):
                    score += 0.5
        
        if score > 0:
            # Normalize the score based on the number of keywords for this intent
            intents[intent] = min(1.0, score / (len(keywords) * 0.5))
    
    # If no intents were identified, use a fallback
    if not intents:
        intents["general"] = 1.0
        
    return intents

def summarize_text(text: str, max_length: int = 150) -> str:
    """
    Create a simple extractive summary of longer text.
    Uses TF-IDF to find the most important sentences.
    """
    if len(text) <= max_length:
        return text
        
    # Split into sentences
    sentences = nltk.sent_tokenize(text)
    
    # Skip summarization for very short texts
    if len(sentences) <= 3:
        return text
    
    # Create TF-IDF matrix
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(sentences)
    
    # Calculate sentence scores based on TF-IDF values
    sentence_scores = [sum(tfidf_matrix[i].toarray()[0]) for i in range(len(sentences))]
    
    # Get top sentences
    top_sentence_indices = sorted(range(len(sentence_scores)), 
                                key=lambda i: sentence_scores[i], 
                                reverse=True)[:3]
    top_sentence_indices = sorted(top_sentence_indices)  # Sort by position in text
    
    # Create summary
    summary = " ".join([sentences[i] for i in top_sentence_indices])
    return summary

def analyze_message(text: str) -> Dict[str, Any]:
    """
    Comprehensive analysis of a message, combining all NLP functions.
    Returns a dictionary with sentiment, entities, and intents.
    """
    result = {
        "sentiment": analyze_sentiment(text),
        "entities": extract_entities(text),
        "intents": identify_intent(text)
    }
    
    return result