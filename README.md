# Dialogix Persona Hub

[![Dialogix Logo](public/placeholder.svg)](https://your-project-link-here.com) <!-- Replace with actual logo/link if available -->

**Dialogix Persona Hub** is a multi-persona conversational AI application featuring a dynamic frontend built with React/Vite/TypeScript and a robust backend powered by Python/FastAPI. Engage in conversations with a diverse cast of AI personas, each with a unique personality and conversational style. The project also includes an NLP analysis component for text insights.

## ✨ Features

- **Multi-Persona Chat:** Interact with various AI agents like Captain Grumblebeard, Master Serenity, Caffeine Coder, and more.
- **Dynamic Frontend:** Modern and responsive user interface built with React, Vite, TypeScript, Shadcn UI, and Tailwind CSS.
- **FastAPI Backend:** Efficient and scalable Python backend serving the personas and handling API requests.
- **NLP Analysis:** Integrated NLP tools (via a separate FastAPI service) to analyze text for sentiment, entities, and provide summaries (demonstration purposes).
- **Component-Based UI:** Leverages Shadcn UI for pre-built, accessible, and customizable components.
- **Type Safety:** Full TypeScript integration in the frontend for enhanced developer experience and code reliability.

## 🚀 Technologies Used

**Frontend:**

- **Framework:** React 18+
- **Build Tool:** Vite
- **Language:** TypeScript
- **UI Library:** Shadcn UI
- **Styling:** Tailwind CSS
- **Routing:** React Router DOM
- **State Management/Data Fetching:** TanStack Query (React Query)
- **Forms:** React Hook Form + Zod
- **Linting/Formatting:** ESLint

**Backend:**

- **Framework:** FastAPI
- **Language:** Python 3.10+
- **Server:** Uvicorn
- **Core Libraries:** Pydantic (Data Validation)
- **NLP (Example):** Basic text analysis utilities (details in `backend/nlp_utils/`)

## 🏗️ Project Structure

```
dialogix-persona-hub/
├── backend/             # Python FastAPI backend
│   ├── common_models.py # Pydantic models shared across backend
│   ├── main.py          # Main FastAPI app definition, persona routing
│   ├── nlp_server.py    # Separate FastAPI app for NLP analysis (optional)
│   ├── requirements.txt # Backend Python dependencies
│   ├── nlp_utils/       # NLP helper functions
│   └── persona_agents/  # Individual persona logic and API endpoints
├── public/              # Static assets served by Vite
├── src/                 # Frontend React/TypeScript source code
│   ├── components/      # Reusable UI components (including Shadcn UI)
│   ├── data/            # Static data (like persona definitions)
│   ├── hooks/           # Custom React hooks
│   ├── lib/             # Utility functions
│   ├── pages/           # Page-level components/views
│   ├── App.tsx          # Main application component
│   ├── main.tsx         # Frontend entry point
│   └── index.css        # Global styles
├── bun.lockb            # Bun lockfile (alternative package manager)
├── package.json         # Frontend dependencies and scripts
├── tsconfig.json        # TypeScript configuration
├── vite.config.ts       # Vite configuration
└── README.md            # This file
```

## ⚙️ Getting Started

### Prerequisites

- Node.js (v18 or later recommended) and npm (or Bun)
- Python (v3.10 or later recommended) and pip

### Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone <YOUR_REPOSITORY_URL>
   cd dialogix-persona-hub
   ```

2. **Setup Frontend:**

   ```bash
   # Navigate to the root directory if not already there
   npm install  # or bun install
   ```

3. **Setup Backend:**
   ```bash
   cd backend
   python -m venv venv  # Create a virtual environment (recommended)
   # Activate the virtual environment:
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   # source venv/bin/activate
   pip install -r requirements.txt
   cd ..
   ```

### Running the Application

1. **Start the Backend Server:**
   Open a terminal, navigate to the `backend` directory, and ensure your virtual environment is active.

   ```bash
   cd backend
   # Make sure venv is active
   uvicorn main:app --reload --port 8000
   ```

   The main API server will run on `http://127.0.0.1:8000`.

2. **Start the NLP Server (Optional):**
   Open _another_ terminal, navigate to the `backend` directory, and ensure your virtual environment is active.

   ```bash
   cd backend
   # Make sure venv is active
   uvicorn nlp_server:app --reload --port 8001
   ```

   The NLP server will run on `http://127.0.0.1:8001`.

3. **Start the Frontend Development Server:**
   Open _another_ terminal in the project's root directory.
   ```bash
   npm run dev # or bun run dev
   ```
   The frontend application will be available at `http://localhost:5173` (or another port specified by Vite).

## 🎭 Available Personas

The backend currently supports the following personas (accessible via `/api/personas` endpoint and individual chat endpoints):

- **Captain Grumblebeard:** Grumpy Pirate (`/api/personas/captain`)
- **Master Serenity:** Zen Monk (`/api/personas/zen`)
- **Caffeine Coder:** Energetic Developer (`/api/personas/dev`)
- **Chef Gusteau:** Culinary Expert (`/api/personas/chef`)
- **Professor Knowitall:** Academic Expert (`/api/personas/professor`)
- **Lyra Versecraft:** Poetic Soul (`/api/personas/poet`)
- **Sherlock Holmes:** Deductive Genius (`/api/personas/detective`)

## 🌐 API Endpoints

- **`GET /`**: Backend root status message.
- **`GET /api/personas`**: List available personas.
- **`POST /api/personas/{persona_id}/chat`**: Send a message to a specific persona.
- **`POST /api/nlp/analyze`**: Analyze text using the NLP service (requires `nlp_server.py` to be running).

_(Refer to the FastAPI backend code (`main.py`, `nlp_server.py`, and `persona_agents/`) for detailed request/response models.)_

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to improve the project.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` file for more information (if applicable - add a LICENSE file if needed).
