# 📚 Study Buddy — Multi-Agent AI Study Assistant

A modular multi-agent study companion that converts any topic or raw textbook text into structured study notes and an interactive quiz.

---

## 👥 The 4 Agents

| Agent | Role | Job Description |
|---|---|---|
| 🔍 **Topic Researcher** | Fact Extractor | Gathers 8–10 key verifiable facts (Topic or Text extraction mode) |
| 📝 **Notes Summarizer** | Educational Scribe | Formats facts into structured, exam-ready study notes |
| 🧠 **Quiz Generator** | Quizmaster | Generates challenging MCQs with 4 options & explanations in JSON |
| ⚖️ **Evaluator** | Strict Reviewer | Validates questions against notes (Score 1–10) and triggers retries on issues |

---

## 🏗️ Architecture & Evaluator Feedback Loop

```
               User Input (Topic or Chapter text)
                               │
                               ▼
                    [1. Topic Researcher]
                               │
                               ▼
                    [2. Notes Summarizer]
                               │
                               ▼
        ┌─────────── [3. Quiz Generator] ◄──────────────┐
        │                      │                        │
        │                      ▼                        │
        │               [4. Evaluator]                  │
        │                      │                        │
        │           Score >= 7?│                        │
        │           ┌──────────┴──────────┐             │
        │           ▼                     ▼             │
        │        [Passes]          [Score < 7]          │
        │           │               (Max 2 retries)     │
        │           │                     │             │
        │           │                     └─────────────┘
        │           │                    (passes feedback)
        │           ▼
        └─► Final Output: Notes + Interactive Quiz + Evaluator Verdict
```

---

## ⚡ Quick Start

### 1. Requirements

Dependencies are already installed. If running on another machine:
```bash
pip install -r requirements.txt
```

### 2. Configure Free API Key

Study Buddy supports **Groq** (Recommended - ultra fast) or **Google Gemini**.

- **Groq:** Get a free key at [console.groq.com/keys](https://console.groq.com/keys)
- **Gemini:** Get a free key at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

You can configure your key in **two ways**:
1. In the `.env` file:
   ```env
   GROQ_API_KEY=gsk_your_key_here
   ```
2. Or directly paste it into the **API Key** banner on the web interface (saves automatically)!

### 3. Start the Server

```bash
python -m uvicorn main:app --reload
```

Visit [http://localhost:8000](http://localhost:8000) in your browser.
API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Project Structure

```
study-buddy/
├── agents/
│   ├── __init__.py           # Agent exports
│   ├── researcher.py         # Agent 1: Topic / Text Researcher
│   ├── summarizer.py         # Agent 2: Notes Summarizer
│   ├── quiz_generator.py     # Agent 3: JSON MCQ Generator
│   └── evaluator.py          # Agent 4: Evaluator & Reviewer
├── static/
│   └── index.html            # Interactive web app
├── llm.py                    # Unified LLM provider (Groq / Gemini)
├── pipeline.py               # 4-agent orchestration & feedback loop
├── main.py                   # FastAPI backend (endpoints & UI)
├── requirements.txt          # Dependencies
├── .env.example              # Key templates
└── README.md                 # Documentation
```
