# LexIQ Labs — Core Engine

LexIQ Labs is an **emotionally intelligent response orchestration engine** designed for fast-paced, high-stakes customer communication across **Support, Sales, and Customer Success**.

This repository contains the **core, headless logic** that powers LexIQ.  
It is intentionally UI-agnostic and deterministic by design.

> **EI > AI**  
> LexIQ does not decide *what* to say.  
> It ensures you never say the *wrong* thing.

---

## 🧠 What This Engine Does

LexIQ helps teams craft **human, psychologically sound responses** by combining:

- Empathy Telemetry (emotional understanding)
- User-declared intent
- God Mode psychology constraints
- Optional AI language refinement (Gemini)
- Predictive “Time Travel” simulations

The result is responses that feel:
- Natural
- Calm
- Intentional
- On-brand
- Safe to send

---

## 🧩 Core Philosophy

- **Not a chatbot**
- **Not an AI writer**
- **Not prompt engineering**

LexIQ is a **decision-support workspace**:
- Humans decide intent
- LexIQ enforces psychology
- AI assists with wording — optionally

---

## 🔄 High-Level Flow

Customer Message
↓
Empathy Telemetry (local, deterministic)
↓
Contextual Clarification Questions (optional)
↓
User Direction (free-text intent)
↓
Pain Point Matching (secondary signal)
↓
God Mode Prompt Selection
↓
Blender → Response Contract
↓
Gemini Refinement (optional)
↓
Final Response
↓
Time Travel Simulation (optional)

---

## 📁 Repository Structure

lexiq-labs-core/
├── blender.py # Composes the response contract
├── pain_point_matcher.py # Secondary signal for God Mode selection
├── empathy_telemetry.py # Local emotional analysis + insight
├── question_generator.py # Contextual clarification questions
├── response_contract.py # Enforces response structure & rules
├── gemini_refiner.py # Optional language refinement
├── voice_profile.py # One-time user writing style constraints
├── time_travel.py # Simulates likely next customer reply
├── response_history.py # Stores past responses per session
├── session_state.py # Session-level context & settings
├── validate_prompts.py # YAML validation utility
├── requirements.txt
├── .env.example
├── README.md
└── prompts/
├── god_mode_prompts.yaml
└── pain_points_library.yml

---

## 🧠 Key Concepts

### Empathy Telemetry
Lightweight, local analysis that detects:
- Emotional intensity
- Frustration signals
- Urgency patterns

Outputs a **human-readable insight**, not raw sentiment scores.

---

### Contextual Questions
When useful, LexIQ asks **1–2 dynamic clarification questions** to avoid:
- Back-and-forth
- Reopens
- Escalations

Questions are optional and generated per situation.

---

### User Direction (Intent)
Instead of buttons or presets, users state **how they want to handle the situation** in their own words.

This keeps responses:
- Organic
- Intentional
- Non-templated

---

### God Mode Prompts
God Mode prompts encode **psychological strategy**, not scripts.

They act as:
- Non-negotiable constraints
- Emotional safety rails
- Strategy governors

They are never rewritten by AI.

---

### Response Contract
Every response must subtly include:
1. Reconfirmation of the issue or goal
2. Acknowledgement of the customer
3. Clear solution or next steps
4. Assurance / ownership

This structure is enforced without sounding templated.

---

### Voice Profile
Users can optionally set a **one-time writing style profile** using:
- 3–5 past responses
- Or preference sliders

LexIQ adapts tone and style while preserving psychology.

---

### Time Travel
After a response is generated, LexIQ can simulate:
- A plausible next customer reply
- Emotional direction (improving / neutral / worsening)

This supports reflection, not automation.

---

## 🤖 Gemini Usage (Optional)

Gemini is used **only** for:
- Clarification question suggestions
- Language refinement
- Time Travel simulation

Gemini is **never** allowed to:
- Decide strategy
- Select psychology
- Invent policies or promises
- Override user intent

If no API key is present, LexIQ works fully without AI.

---

## 🔐 Environment Variables

Create a `.env` file (not committed):

GEMINI_API_KEY=AIzaSyApSJ9DE4ijGE3bnoEgF_grkdavp7iFKxU

See `.env.example` for reference.

---

## 🛡️ Design Guarantees

- Deterministic core logic
- Graceful fallbacks
- No dead ends
- No forced AI dependency
- Enterprise-safe behavior

---

## 🧭 What This Repo Is (and Is Not)

✅ Core orchestration engine  
✅ Psychological guardrails  
✅ AI-assisted refinement (optional)

❌ UI / frontend  
❌ Chatbot logic  
❌ Model training  
❌ Data storage backend  

---

## ✨ One-Line Summary

> **LexIQ Labs helps teams think through responses, then ensures they say them right — every time.**

---

For UI, API, or deployment layers, this repo should be consumed as a **read-only engine**.

If you are integrating this into another system, do **not** modify core files.
