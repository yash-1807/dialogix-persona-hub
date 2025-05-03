
# Dialogix Backend

This is the backend service for Dialogix, a multi-persona conversational AI platform.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once running, visit http://localhost:8000/docs for the Swagger UI documentation.

## Persona Endpoints

Each persona has its own endpoint at `/api/personas/{persona_id}/chat`:

- `/api/personas/captain/chat` - Captain Grumblebeard (Grumpy Pirate)
- `/api/personas/zen/chat` - Master Serenity (Zen Monk)
- `/api/personas/dev/chat` - Caffeine Coder (Energetic Developer)
- `/api/personas/chef/chat` - Chef Gusteau (Culinary Expert)
- `/api/personas/professor/chat` - Professor Knowitall (Academic Expert)
- `/api/personas/poet/chat` - Lyra Versecraft (Poetic Soul)
- `/api/personas/detective/chat` - Sherlock Holmes (Deductive Genius)

## API Documentation

- GET `/` - API health check
- GET `/api/personas` - List all available personas
- POST `/api/personas/{persona_id}/chat` - Chat with a specific persona

## Environment Variables

To configure the API, you can set the following environment variables:

- `PORT` - The port to run the server on (default: 8000)
- `MODEL_NAME` - The Gemini model to use (default: gemini-2.0-flash-exp)
- `GOOGLE_API_KEY` - Your Google API key for Gemini models
