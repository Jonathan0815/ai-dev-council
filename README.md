# AI Development Council — Fully Local 14B Edition

**Zero cloud. Zero API keys. Zero bullshit.**

Runs a full multi-agent dev team (Project Manager → Coder → QA) using **qwen2.5-coder:14b-instruct-q4_K_M** entirely on your GPU via Ollama + Intel Arc B580.

Tested and working on:
- Bazzite (Fedora Atomic Gaming)
- Distrobox (Ubuntu toolbox)
- Podman + Ollama with Intel GPU acceleration
- CrewAI + LiteLLM + localhost networking

### Features
- 100% offline
- 14 billion parameter coding model
- Self-documenting, self-testing, self-improving
- No OpenAI, no keys, no tracking
- Ready to evolve into its own framework

### How to Run (Copy-Paste)

```bash
# 1. Install Ollama with Intel GPU support
# 2. Pull the model
ollama pull qwen2.5-coder:14b-instruct-q4_K_M

# 3. Run the council
python council/main.py
Dashboard
Bashstreamlit run dashboard.py --server.port=8501
Future Goals (the council will build these itself)

Replace CrewAI with a dependency-free alternative
Add Researcher, Deployer, and Self-Modifier agents
Auto-commit improvements to this repo
Become fully autonomous

This council is now alive. Feed it tasks. Watch it grow.
