
import React from "react";
import { Persona } from "@/data/personas";
import { cn } from "@/lib/utils";

interface PersonaGlobuleProps {
  persona: Persona;
  isActive: boolean;
  onClick: () => void;
}

const PersonaGlobule: React.FC<PersonaGlobuleProps> = ({
  persona,
  isActive,
  onClick,
}) => {
  // Determine size class based on animation variation
  const sizeClass = "h-24 w-24 sm:h-28 sm:w-28";
  
  // Determine animation class to add variety
  const animationClass = React.useMemo(() => {
    const animations = [
      "animate-float",
      "animate-float-slow",
      "animate-float-fast",
    ];
    return animations[Math.floor(Math.random() * animations.length)];
  }, []);

  return (
    <div className={cn("globule", isActive && "scale-110")} onClick={onClick}>
      <div
        className={cn(
          "globule-bubble",
          sizeClass,
          animationClass,
          `bg-${persona.color}/20`,
          isActive && "ring-4",
          isActive ? `ring-${persona.color}` : "ring-transparent"
        )}
      >
        {persona.avatar ? (
          <img
            src={persona.avatar}
            alt={persona.name}
            className="h-full w-full object-cover rounded-full"
          />
        ) : (
          <span className="text-4xl">{persona.emoji}</span>
        )}
      </div>
      <div className="mt-3 text-center">
        <h3 className="font-semibold text-sm sm:text-base">{persona.name}</h3>
        <p className="text-xs sm:text-sm text-muted-foreground">{persona.role}</p>
      </div>
    </div>
  );
};

export default PersonaGlobule;
