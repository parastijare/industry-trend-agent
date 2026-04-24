# Industry Trends Report
A multi-agent AI system that generates comprehensive industry trend reports using real-time web data and autonomous reasoning.

# Live Demo
https://industry-trend-agent-aoybvpumomadgkxbbq9giz.streamlit.app/

# What It Does

Enter any industry or sector and get a complete AI-powered trend analysis in under a minute:
- Fetches real-time data from across the web
- Identifies emerging trends, market movements, and innovations
- Extracts key insights using multiple AI agents
- Generates a structured, executive-level industry report
- Evaluates report quality using an independent AI judge

# Agent Pipeline
```
User Input (Industry)
        ↓
Tavily Search (Live Data)
        ↓
Agent 1: Trend Researcher
        ↓
Agent 2: Signal Extractor
        ↓
Agent 3: Report Writer
        ↓
Agent 4: LLM Evaluator
        ↓
Final Trend Report
```
# Tech Stack
- LLM: Llama 3 (via Groq LPU API)
- Search: Tavily Search API
- Frontend & Deployment: Streamlit
- Language: Python 3

# Agents Overview
| Agent | Role | Input | Output |
|------|------|------|--------|
| Trend Researcher | Collects and summarizes real-time industry data | Tavily search results | Structured research insights |
| Signal Extractor | Identifies key trends from analysis | Research summary | Top 5 trend signals (JSON format) |
| Report Writer | Generates a professional industry report | Research + signals | Complete structured report |
| LLM Evaluator | Evaluates report quality | Final report | Scores + feedback |

# Project Context
- Course: B.E. Electronics and Communication
- Semester: IV
- Domain: Agentic AI Systems


This project demonstrates the use of multi-agent architectures for solving real-world analytical problems by combining:

- Real-time data retrieval
- LLM-based reasoning
- Autonomous task decomposition
- Self-evaluation mechanisms
