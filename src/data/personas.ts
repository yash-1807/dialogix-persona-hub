
export interface Persona {
  id: string;
  name: string;
  role: string;
  description: string;
  color: string;
  emoji: string;
  avatar?: string;
}

export const personas: Persona[] = [
  {
    id: "captain",
    name: "Captain Grumblebeard",
    role: "Grumpy Pirate",
    description: "A salty old sea dog with a flair for the dramatic and a disdain for landlubbers.",
    color: "dialog-blue",
    emoji: "🏴‍☠️"
  },
  {
    id: "zen",
    name: "Master Serenity",
    role: "Zen Monk",
    description: "Find your center with this peaceful guide who speaks in koans and gentle wisdom.",
    color: "dialog-green",
    emoji: "🧘"
  },
  {
    id: "dev",
    name: "Caffeine Coder",
    role: "Energetic Developer",
    description: "A hyperactive programmer who solves problems fast and talks even faster.",
    color: "primary",
    emoji: "👩‍💻"
  },
  {
    id: "chef",
    name: "Chef Gusteau",
    role: "Culinary Expert",
    description: "A passionate chef who believes anyone can cook with the right guidance.",
    color: "dialog-red",
    emoji: "👨‍🍳"
  },
  {
    id: "professor",
    name: "Professor Knowitall",
    role: "Academic Expert",
    description: "A scholarly type who provides detailed, citation-heavy explanations.",
    color: "dialog-orange",
    emoji: "🧠"
  },
  {
    id: "poet",
    name: "Lyra Versecraft",
    role: "Poetic Soul",
    description: "Expresses everything through beautiful, flowing verse and metaphor.",
    color: "dialog-pink", 
    emoji: "✒️"
  },
  {
    id: "detective",
    name: "Sherlock Holmes",
    role: "Deductive Genius",
    description: "Observes the details others miss and makes surprising deductions.",
    color: "dialog-cyan",
    emoji: "🔍"
  }
];
