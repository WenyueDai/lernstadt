
# Game Plan: *Lernstadt – A Narrative-Driven German Learning Game*

## 1. Title Page
**Title**: Lernstadt  
**Subtitle**: A narrative-driven German-learning game with reactive NPCs  
**Author**: Eva Dai  
**Date**: [2025-05-05]  

---

## 2. Abstract / Executive Summary
Lernstadt is an experimental prototype of a story-rich educational game designed to support German language learners through immersive, character-driven interaction. The game simulates a small, vibrant town inhabited by unique NPCs, each with their own personality, memory, relationships, and emotional states. These characters respond dynamically to the player, drawing on past conversations, rumors, levels of trust and suspicion, and even blog posts written by the player. This document outlines the design philosophy, implementation strategy, and educational goals that shape the project.

Beyond its educational purpose, Lernstadt is wrapped in an atmosphere of mystery. Hidden beneath the peaceful surface of this seemingly ordinary German town lies a deeper narrative, slowly revealed through subtle interactions and carefully crafted dialogues. The player’s conversations with NPCs are not isolated exchanges—they are part of a living, reactive community. What the player says, writes, or withholds can echo throughout the town. NPCs might share the player’s secrets with others, while the player can also overhear local gossip and piece together clues about the town and its inhabitants.

This dynamic social network turns language learning into a fully immersive experience, where every phrase and sentence holds potential consequences—making German practice meaningful, personal, and engaging.

---

## 3. Introduction
- **Motivation**: To create a language-learning game that feels more like a living world than a vocabulary test.
- **Target Audience**: German learners and horror-lover.
- **Goal**: Increase conversational confidence through contextual storytelling and reactive characters.

---

## 4. Narrative & World Design
- The game takes place in *Lernstadt*, a seemingly cozy yet secret fictional town.
- Players interact with locals (NPCs) over several days leading up to New Year.
- Each NPC has memory, mood, and social relationships.
- A subtle mystery unfolds as the player explores the town and builds trust.

---

## 5. Core Mechanics
- **Dialogue System**: Player speaks in German; NPCs respond via GPT prompts.
- **MBTI Personalities**: Each NPC uses MBTI types to vary tone and language.
- **Trust & Suspicion**: NPCs track trust/suspicion based on conversations.
- **Player Blog**: NPCs reference the player’s published thoughts in real time.
- **Escape Clues**: Optional mechanic to find hidden routes or truths.

---

## 6. Language Learning Design
- NPCs use simple German with repetition and structure.
- Blog entries provide vocabulary recall and context anchoring.
- NPCs assist if player input is low-quality German.
- Encourages “learning by doing” via sustained interaction.

---

## 7. Technical Implementation
- **Frontend**: Streamlit-based interface.
- **Storage**: JSON files for blog, NPC memory, and dialogue logs.
- **Prompting**: GPT instructions customized per NPC personality.
- **Time System**: Tracks day, time, and special dates (e.g. New Year’s Eve).

---

## 8. Design Challenges & Solutions
- **Challenge**: Preventing repetitive responses.
  - *Solution*: Use conversation memory and prompt variation.
- **Challenge**: Ambiguous or poor user input.
  - *Solution*: NPCs adaptively interpret or ask clarifying questions.
- **Challenge**: Retaining immersion without breaking language learning goals.

---

## 9. Playtesting & Feedback
- Early testers reported immersion and emotional attachment to NPCs.
- Some requested clearer learning feedback and grammar correction.
- Blog system well-received as a creative reflection tool.

---

## 10. Evaluation & Reflections
- Reactive narrative supports language engagement.
- Personality-based responses increase variety.
- Prototype shows promise but would benefit from voice input, richer visuals, and learning analytics.

---

## 11. Future Work / Expansion
- Add voice recognition and spoken input feedback.
- Long-term memory for NPCs across sessions.
- Mini-games for grammar drills in-character.
- Multiplayer or teacher-mode for guided sessions.

---

## 12. References / Inspiration
- GPT-based NPC simulation.

---

**Appendix**: