# AI Dev Council

**Fully local, self-evolving AI software company** — powered by qwen2.5-coder:14b-instruct-q4_K_M on Ollama + Intel Arc B580.

No cloud. No OpenAI. No API keys. No limits.

This is not a chatbot.  
This is a **local AI dev team** that plans, codes, tests, and innovates on your GPU.

## Quick Start

```bash
git clone https://github.com/Jonathan0815/ai-dev-council.git
cd ai-dev-council
python -m venv ai-env && source ai-env/bin/activate
pip install streamlit crewai langchain-ollama openai
ollama pull qwen2.5-coder:14b-instruct-q4_K_M

# v1.7 (Streamlit UI)
streamlit run dashboard.py

# v2.0 (Pure Python UI)
python launcher.py  # → http://localhost:8000
