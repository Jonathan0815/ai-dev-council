# AI Dev Council — Your Local AI Software Company

**The first 100% local, GPU-accelerated AI dev team** — runs completely offline on your Intel Arc B580.

No OpenAI · No cloud · No paid APIs · 100% open-source

### Features
- Multi-agent council (PM, Coder, QA)
- Direct Ollama integration (llama3.1, qwen2.5-coder, etc.)
- FastAPI backend + Streamlit dashboard
- Self-upgrading capable

### Startup (Bazzite + Arc B580)

```bash
# 1. Start Ollama (GPU engine)
podman compose -f ~/ollama-intel-arc/compose.yml up -d

# 2. Start the council
distrobox enter ai-python
cd ~/ai-crew
nohup python app_dev_crew.py > crew.log 2>&1 &

# 3. Start the dashboard
streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0
Open http://localhost:8501
Shutdown
Bashpkill -f app_dev_crew.py
pkill -f streamlit
podman compose -f ~/ollama-intel-arc/compose.yml down
Change Model (edit app_dev_crew.py)
Pythonllm = OllamaLLM(model="qwen2.5-coder:14b-instruct-q4_K_M")  # best coder
# or
llm = OllamaLLM(model="llama3.1:8b")  # fast & good
Your GPU is now your software company.
Built by Jonathan0815 — November 20, 2025
