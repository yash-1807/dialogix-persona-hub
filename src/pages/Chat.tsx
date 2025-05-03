
import { useState, useRef, useEffect } from "react";
import { useParams } from "react-router-dom";
import { personas } from "@/data/personas";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Separator } from "@/components/ui/separator";
import { Upload, Send } from "lucide-react";
import ChatMessage from "@/components/ChatMessage";

interface Message {
  id: string;
  content: string;
  role: "user" | "assistant";
  timestamp: Date;
}

const Chat = () => {
  const { personaId } = useParams<{ personaId: string }>();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const persona = personas.find(p => p.id === personaId) || personas[0];
  
  // Add welcome message when chat loads
  useEffect(() => {
    if (messages.length === 0) {
      const welcomeMsg = getWelcomeMessage(persona.id);
      setMessages([
        {
          id: "welcome",
          content: welcomeMsg,
          role: "assistant",
          timestamp: new Date(),
        },
      ]);
    }
  }, [persona.id]);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const getWelcomeMessage = (id: string) => {
    switch (id) {
      case "captain":
        return "Arr! What brings ye to me ship, landlubber? Speak up before I make ye walk the plank!";
      case "zen":
        return "Welcome, seeker. The path to wisdom begins with a single step. What brings you to this moment?";
      case "dev":
        return "Hey there! *sips coffee* What are we building today? I've got like 17 tabs open and I'm READY TO CODE!";
      case "chef":
        return "Bonjour! Welcome to my virtual kitchen. What delicious creation shall we discuss today?";
      case "professor":
        return "Ah, a new student! I'm delighted to engage in scholarly discourse. What subject shall we explore?";
      case "poet":
        return "Upon this digital page, two souls shall meet. What verses stir within your heart, dear friend?";
      case "detective":
        return "Interesting... *adjusts magnifying glass* I observe you've come seeking answers. The game is afoot!";
      default:
        return "Hello! How can I assist you today?";
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    
    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      role: "user",
      timestamp: new Date(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);
    setIsTyping(true);
    
    // Simulate API call to backend
    setTimeout(() => {
      // This will be replaced with actual API call
      const responseMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: generateMockResponse(input, persona.id),
        role: "assistant",
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, responseMessage]);
      setIsLoading(false);
      setIsTyping(false);
    }, 1500);
  };
  
  const generateMockResponse = (message: string, personaId: string) => {
    // Later, this will be replaced with real API responses
    const responses: Record<string, string[]> = {
      captain: [
        "Arr! That be a fine question, matey!",
        "Blimey! Ye speak like a true landlubber!",
        "By Davy Jones' locker! I've sailed the seven seas and never heard such nonsense!",
      ],
      zen: [
        "The answer you seek is within the question itself.",
        "Consider the bamboo: flexible yet unbreakable. This is the way of wisdom.",
        "The river flows without effort. Your mind should be the same.",
      ],
      dev: [
        "OMG! Let me refactor that for you real quick! *types furiously*",
        "Have you tried turning it off and on again? Just kidding, let's debug this!",
        "That's a feature, not a bug! But seriously, I can help optimize that.",
      ],
    };
    
    const defaultResponses = [
      "That's a fascinating perspective. Let me think about that.",
      "I understand what you're asking. Here's my thought...",
      "Interesting question! From my perspective...",
    ];
    
    const personaResponses = responses[personaId] || defaultResponses;
    return personaResponses[Math.floor(Math.random() * personaResponses.length)];
  };
  
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    // Placeholder for file upload functionality
    // This will be implemented when connecting to the backend
    const files = e.target.files;
    if (files && files.length > 0) {
      const file = files[0];
      setMessages(prev => [
        ...prev,
        {
          id: Date.now().toString(),
          content: `Uploaded file: ${file.name}`,
          role: "user",
          timestamp: new Date(),
        },
      ]);
      
      // Mock response for file upload
      setTimeout(() => {
        setMessages(prev => [
          ...prev,
          {
            id: (Date.now() + 1).toString(),
            content: `I've received your file "${file.name}". What would you like me to do with it?`,
            role: "assistant",
            timestamp: new Date(),
          },
        ]);
      }, 1000);
    }
  };

  return (
    <div className="flex flex-col h-screen pt-16">
      {/* Chat header */}
      <div className="border-b p-4">
        <div className="container mx-auto flex items-center gap-3">
          <div className={`h-10 w-10 rounded-full bg-${persona.color}/20 flex items-center justify-center`}>
            <span className="text-xl">{persona.emoji}</span>
          </div>
          <div>
            <h2 className="font-semibold">{persona.name}</h2>
            <p className="text-sm text-muted-foreground">{persona.role}</p>
          </div>
        </div>
      </div>
      
      {/* Chat messages */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="container mx-auto max-w-4xl">
          {messages.map((msg) => (
            <ChatMessage 
              key={msg.id} 
              message={msg} 
              persona={persona}
            />
          ))}
          {isTyping && (
            <div className="chat-bubble chat-bubble-ai max-w-[60%]">
              <div className="flex gap-1">
                <span className="animate-pulse">●</span>
                <span className="animate-pulse delay-100">●</span>
                <span className="animate-pulse delay-200">●</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>
      
      {/* Input area */}
      <div className="border-t p-4">
        <div className="container mx-auto max-w-4xl">
          <form onSubmit={handleSendMessage} className="flex gap-2">
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="resize-none min-h-[3rem]"
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSendMessage(e);
                }
              }}
            />
            <div className="flex flex-col gap-2">
              <Button type="button" variant="outline" size="icon" className="h-9 w-9">
                <label className="cursor-pointer w-full h-full flex items-center justify-center">
                  <Upload className="h-4 w-4" />
                  <input 
                    type="file" 
                    className="hidden"
                    onChange={handleFileUpload}
                  />
                </label>
              </Button>
              <Button type="submit" size="icon" className="h-9 w-9" disabled={isLoading || !input.trim()}>
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Chat;
