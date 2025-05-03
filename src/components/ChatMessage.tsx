
import React from "react";
import { Persona } from "@/data/personas";
import { cn } from "@/lib/utils";
import { format } from "date-fns";

interface Message {
  id: string;
  content: string;
  role: "user" | "assistant";
  timestamp: Date;
}

interface ChatMessageProps {
  message: Message;
  persona: Persona;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, persona }) => {
  const isUser = message.role === "user";
  
  return (
    <div className={cn("mb-6", isUser ? "flex flex-row-reverse" : "flex")}>
      <div className={cn("flex flex-col max-w-[80%]", isUser ? "items-end" : "items-start")}>
        <div className="flex items-center gap-2 mb-1">
          {!isUser && (
            <div className={`h-8 w-8 rounded-full bg-${persona.color}/20 flex items-center justify-center text-sm`}>
              <span>{persona.emoji}</span>
            </div>
          )}
          <div className="text-xs text-muted-foreground">
            {isUser ? "You" : persona.name} • {format(new Date(message.timestamp), "h:mm a")}
          </div>
          {isUser && (
            <div className="h-8 w-8 rounded-full bg-primary/20 flex items-center justify-center text-sm">
              <span>👤</span>
            </div>
          )}
        </div>
        
        <div className={cn(
          "chat-bubble",
          isUser ? "chat-bubble-user" : "chat-bubble-ai",
          isUser ? `bg-primary text-primary-foreground` : `bg-muted`
        )}>
          {message.content}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;
