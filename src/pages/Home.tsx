
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { MessageCircle } from "lucide-react";
import PersonaGlobule from "@/components/PersonaGlobule";
import { personas } from "@/data/personas";

const Home = () => {
  const navigate = useNavigate();
  const [activePersona, setActivePersona] = useState<string | null>(null);
  
  const handlePersonaClick = (id: string) => {
    setActivePersona(id);
    
    // Navigate to chat with a slight delay for animation
    setTimeout(() => {
      navigate(`/chat/${id}`);
    }, 300);
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Hero section */}
      <section className="pt-28 pb-16 px-4 md:pt-32 md:pb-20">
        <div className="container mx-auto text-center">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-4 bg-gradient-to-r from-primary to-dialog-blue bg-clip-text text-transparent">
            Meet Your AI Personas
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-8">
            Chat with an eclectic cast of AI characters — each with their own unique personality, 
            memories, and expertise.
          </p>
          <Button size="lg" asChild>
            <a href="#personas">
              <MessageCircle className="mr-2 h-5 w-5" />
              Start Chatting
            </a>
          </Button>
        </div>
      </section>

      {/* Personas section */}
      <section id="personas" className="py-16 px-4 bg-muted/50">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold mb-2 text-center">Choose a Persona</h2>
          <p className="text-muted-foreground text-center mb-12 max-w-2xl mx-auto">
            Each persona has their own personality, memories, and way of communicating. 
            Click on one to start a conversation!
          </p>
          
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-x-4 gap-y-12">
            {personas.map((persona) => (
              <PersonaGlobule
                key={persona.id}
                persona={persona}
                isActive={activePersona === persona.id}
                onClick={() => handlePersonaClick(persona.id)}
              />
            ))}
          </div>
        </div>
      </section>

      {/* Features section */}
      <section className="py-16 px-4">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold mb-12 text-center">Features</h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-card p-6 rounded-lg shadow-sm border">
              <div className="h-12 w-12 rounded-full bg-primary/20 flex items-center justify-center mb-4">
                <MessageCircle className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Distinct Personalities</h3>
              <p className="text-muted-foreground">
                Each persona has their own unique voice, personality, and expertise.
              </p>
            </div>
            
            <div className="bg-card p-6 rounded-lg shadow-sm border">
              <div className="h-12 w-12 rounded-full bg-dialog-blue/20 flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-dialog-blue" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/>
                  <circle cx="12" cy="13" r="3"/>
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2">Memory & Context</h3>
              <p className="text-muted-foreground">
                Personas remember your conversations and maintain context over time.
              </p>
            </div>
            
            <div className="bg-card p-6 rounded-lg shadow-sm border">
              <div className="h-12 w-12 rounded-full bg-dialog-pink/20 flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-dialog-pink" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                  <polyline points="15 3 21 3 21 9"/>
                  <line x1="10" y1="14" x2="21" y2="3"/>
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2">Document Sharing</h3>
              <p className="text-muted-foreground">
                Share documents, images, and more with your AI personas for deeper interaction.
              </p>
            </div>
          </div>
        </div>
      </section>
      
      {/* Footer */}
      <footer className="bg-muted/30 py-8 px-4 mt-auto">
        <div className="container mx-auto text-center">
          <p className="text-muted-foreground">© 2023 Dialogix. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default Home;
