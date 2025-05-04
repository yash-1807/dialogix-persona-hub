import { useState, useRef, useEffect } from "react";
import { useParams } from "react-router-dom";
import { personas } from "@/data/personas";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Separator } from "@/components/ui/separator";
import { Upload, Send, FileText, X, ChevronDown, ChevronUp, BrainCircuit } from "lucide-react";
import ChatMessage from "@/components/ChatMessage";

// Interface for NLP analysis results
interface NLPAnalysis {
  sentiment: {
    negative: number;
    neutral: number;
    positive: number;
    compound: number;
  };
  entities: Array<{
    text: string;
    label: string;
    start: number;
    end: number;
  }>;
  intents: Record<string, number>;
}

interface Message {
  id: string;
  content: string;
  role: "user" | "assistant";
  timestamp: Date;
  nlpAnalysis?: NLPAnalysis;
}

const Chat = () => {
  const { personaId } = useParams<{ personaId: string }>();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [fileContent, setFileContent] = useState<string>("");
  const [fileName, setFileName] = useState<string>("");
  const [showDebugInfo, setShowDebugInfo] = useState(false);
  const [lastNLPAnalysis, setLastNLPAnalysis] = useState<NLPAnalysis | null>(null);
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
    if ((!input.trim() && !fileContent) || isLoading) return;
    
    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content: input || (fileName ? `Analyzing file: ${fileName}` : ""),
      role: "user",
      timestamp: new Date(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);
    setIsTyping(true);
    
    try {
      // Prepare conversation history for API
      const conversationHistory = messages.map(msg => ({
        sender: msg.role === "user" ? "user" : "assistant",
        message: msg.content
      }));

      // First, get NLP analysis of the user's message for visualization
      // Using port 8001 for the dedicated NLP server
      const nlpResponse = await fetch("http://localhost:8001/api/nlp/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: input || `Please analyze this file: ${fileName}`,
          document: fileContent || undefined
        }),
      });

      if (nlpResponse.ok) {
        const nlpData = await nlpResponse.json();
        setLastNLPAnalysis(nlpData);
        
        // Update the user message with NLP analysis
        setMessages(prev => 
          prev.map(msg => 
            msg.id === userMessage.id 
              ? { ...msg, nlpAnalysis: nlpData } 
              : msg
          )
        );
      } else {
        console.error("Error fetching NLP analysis:", await nlpResponse.text());
      }

      // Make API call to backend for the persona response
      // Using port 8000 for the main server with personas
      const response = await fetch(`http://localhost:8000/api/personas/${persona.id}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_message: input || "Please analyze this file content.",
          conversation_history: conversationHistory,
          document_context: fileContent || undefined
        }),
      });

      if (!response.ok) {
        throw new Error(`API responded with status: ${response.status}`);
      }

      const data = await response.json();
      
      // Add response from API
      const responseMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: data.response,
        role: "assistant",
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, responseMessage]);
      
      // Clear file content after sending
      if (fileContent) {
        setFileContent("");
        setFileName("");
        setUploadedFile(null);
      }
    } catch (error) {
      console.error("Error communicating with API:", error);
      
      // Fallback to mock response if API fails
      const fallbackResponse: Message = {
        id: (Date.now() + 1).toString(),
        content: "I'm sorry, I'm having trouble connecting to my brain right now. Please try again later.",
        role: "assistant",
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, fallbackResponse]);
    } finally {
      setIsLoading(false);
      setIsTyping(false);
    }
  };
  
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      const file = files[0];
      setUploadedFile(file);
      setFileName(file.name);
      
      // Read file content as text
      const reader = new FileReader();
      reader.onload = (e) => {
        if (typeof e.target?.result === "string") {
          setFileContent(e.target.result);
          
          // Add upload notification as a user message
          const fileMessage: Message = {
            id: Date.now().toString(),
            content: `Uploaded file: ${file.name}`,
            role: "user",
            timestamp: new Date(),
          };
          
          setMessages(prev => [...prev, fileMessage]);
          
          // Automatically send file for analysis
          handleSendFileAnalysis(file.name, e.target.result);
        }
      };
      reader.readAsText(file);
    }
  };
  
  const handleSendFileAnalysis = async (filename: string, content: string) => {
    setIsLoading(true);
    setIsTyping(true);
    
    try {
      // Prepare conversation history for API
      const conversationHistory = messages.map(msg => ({
        sender: msg.role === "user" ? "user" : "assistant",
        message: msg.content
      }));

      // Make API call to backend with file content in document_context
      const response = await fetch(`http://localhost:8000/api/personas/${persona.id}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_message: `Please analyze this file: ${filename}`,
          conversation_history: conversationHistory,
          document_context: content
        }),
      });

      if (!response.ok) {
        throw new Error(`API responded with status: ${response.status}`);
      }

      const data = await response.json();
      
      // Add response from API
      const responseMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: data.response,
        role: "assistant",
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, responseMessage]);
    } catch (error) {
      console.error("Error communicating with API:", error);
      
      // Fallback to mock response if API fails
      const fallbackResponse: Message = {
        id: (Date.now() + 1).toString(),
        content: `I've received your file "${filename}". It appears to be ${content.length} characters long, but I'm having trouble analyzing it at the moment.`,
        role: "assistant",
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, fallbackResponse]);
    } finally {
      setIsLoading(false);
      setIsTyping(false);
      // Clear file content after analysis
      setFileContent("");
      setFileName("");
      setUploadedFile(null);
    }
  };
  
  const clearUploadedFile = () => {
    setUploadedFile(null);
    setFileContent("");
    setFileName("");
  };

  // Function to render the NLP analysis visualization
  const renderNLPDebugPanel = () => {
    if (!lastNLPAnalysis || !lastNLPAnalysis.sentiment || !lastNLPAnalysis.intents) {
      return (
        <div className="bg-slate-50 dark:bg-slate-900 border rounded-md p-4 mb-4 text-sm">
          <div className="flex justify-between items-center">
            <h3 className="font-bold flex items-center">
              <BrainCircuit className="h-4 w-4 mr-2" />
              NLP Analysis Not Available
            </h3>
          </div>
          <p className="text-xs mt-2">No NLP analysis data is available. Try sending a message first.</p>
        </div>
      );
    }
    
    // Get the primary intent (highest confidence) with null checks
    const intentEntries = Object.entries(lastNLPAnalysis.intents || {});
    const primaryIntent = intentEntries.length > 0 ? 
      intentEntries.sort((a, b) => b[1] - a[1])[0] : 
      ["unknown", 0];
      
    // Get sentiment classification with safety checks
    const compound = lastNLPAnalysis.sentiment?.compound || 0;
    let sentimentClass = "neutral";
    if (compound > 0.05) {
      sentimentClass = "positive";
    } else if (compound < -0.05) {
      sentimentClass = "negative";
    }
    
    // Safe values with fallbacks
    const negative = lastNLPAnalysis.sentiment?.negative || 0;
    const neutral = lastNLPAnalysis.sentiment?.neutral || 0;
    const positive = lastNLPAnalysis.sentiment?.positive || 0;
    
    return (
      <div className="bg-slate-50 dark:bg-slate-900 border rounded-md p-4 mb-4 text-sm">
        <div className="flex justify-between items-center mb-2">
          <h3 className="font-bold flex items-center">
            <BrainCircuit className="h-4 w-4 mr-2" />
            NLP Analysis Dashboard
          </h3>
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={() => setShowDebugInfo(!showDebugInfo)}
            className="h-6 p-0 w-6"
          >
            {showDebugInfo ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
          </Button>
        </div>
        
        {showDebugInfo && (
          <div className="space-y-3">
            <div>
              <h4 className="text-xs font-semibold mb-1">Sentiment Analysis</h4>
              <div className="flex gap-1 items-center">
                <div className="h-2 rounded-full bg-gray-200 flex-1">
                  <div 
                    className={`h-2 rounded-full ${
                      sentimentClass === "positive" ? "bg-green-500" : 
                      sentimentClass === "negative" ? "bg-red-500" : 
                      "bg-gray-400"
                    }`}
                    style={{ width: `${Math.abs(compound) * 100}%` }}
                  ></div>
                </div>
                <span className="text-xs w-16">
                  {sentimentClass === "positive" ? "Positive" : 
                   sentimentClass === "negative" ? "Negative" : 
                   "Neutral"} ({compound.toFixed(2)})
                </span>
              </div>
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>Negative: {negative.toFixed(2)}</span>
                <span>Neutral: {neutral.toFixed(2)}</span>
                <span>Positive: {positive.toFixed(2)}</span>
              </div>
            </div>
            
            <div>
              <h4 className="text-xs font-semibold mb-1">Intent Classification</h4>
              <div className="grid grid-cols-2 gap-1">
                {Object.entries(lastNLPAnalysis.intents || {})
                  .sort((a, b) => b[1] - a[1])
                  .slice(0, 4)
                  .map(([intent, confidence]) => (
                    <div key={intent} className="flex items-center gap-1">
                      <div className="h-2 rounded-full bg-gray-200 flex-1">
                        <div 
                          className="h-2 rounded-full bg-blue-500"
                          style={{ width: `${(confidence || 0) * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-xs w-24">{intent} ({((confidence || 0) * 100).toFixed(0)}%)</span>
                    </div>
                  ))
                }
              </div>
            </div>
            
            {lastNLPAnalysis.entities && lastNLPAnalysis.entities.length > 0 && (
              <div>
                <h4 className="text-xs font-semibold mb-1">Named Entities</h4>
                <div className="flex flex-wrap gap-1">
                  {lastNLPAnalysis.entities.map((entity, idx) => (
                    <span 
                      key={idx} 
                      className="text-xs px-2 py-0.5 rounded-full bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-100"
                    >
                      {entity.text} <span className="opacity-70">({entity.label})</span>
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="flex flex-col h-screen pt-16">
      {/* Chat header */}
      <div className="border-b p-4">
        <div className="container mx-auto flex items-center gap-3">
          <div className={`h-10 w-10 rounded-full bg-${persona.color}/20 flex items-center justify-center`}>
            <span className="text-xl">{persona.emoji}</span>
          </div>
          <div className="flex-1">
            <h2 className="font-semibold">{persona.name}</h2>
            <p className="text-sm text-muted-foreground">{persona.role}</p>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowDebugInfo(!showDebugInfo)}
          >
            {showDebugInfo ? "Hide NLP Analysis" : "Show NLP Analysis"}
          </Button>
        </div>
      </div>
      
      {/* Chat messages */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="container mx-auto max-w-4xl">
          {/* NLP Debug Panel */}
          {lastNLPAnalysis && renderNLPDebugPanel()}
          
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
          {uploadedFile && (
            <div className="flex items-center mb-2 p-2 bg-muted rounded">
              <FileText className="h-4 w-4 mr-2" />
              <span className="text-sm truncate flex-1">{uploadedFile.name}</span>
              <Button 
                variant="ghost" 
                size="icon" 
                className="h-6 w-6" 
                onClick={clearUploadedFile}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          )}
          
          <form onSubmit={handleSendMessage} className="flex gap-2">
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={fileContent ? "Add a message about the file or press Send to analyze..." : "Type your message..."}
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
                    accept=".txt,.md,.json,.csv,.html,.js,.ts,.py,.jsx,.tsx,.css"
                  />
                </label>
              </Button>
              <Button 
                type="submit" 
                size="icon" 
                className="h-9 w-9" 
                disabled={isLoading || (!input.trim() && !fileContent)}
              >
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
