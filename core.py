import os
import json
import threading
import time
from openai import OpenAI

os.environ["OLLAMA_HOST"] = "host.docker.internal:11434"
os.environ["OPENAI_API_KEY"] = "sk-ollama"
client = OpenAI(base_url="http://host.docker.internal:11434/v1", api_key="sk-ollama")

PROJECT_ROOT = "council_projects"
os.makedirs(PROJECT_ROOT, exist_ok=True)

def get_project_dir(name):
    safe = "".join(c if c.isalnum() or c in " _-" else "_" for c in name)
    path = os.path.join(PROJECT_ROOT, safe or "default")
    os.makedirs(path, exist_ok=True)
    return path

def load_json(file, default=None):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def run_council(task, project="default"):
    dir_path = get_project_dir(project)
    log_file = os.path.join(dir_path, "logs.json")

    agents = [
        ("Project Manager", "Create a perfect plan."),
        ("Architect", "Design the full system."),
        ("Coder", "Write complete, flawless code."),
        ("Tester", "Test rigorously."),
        ("Reviewer", "Review for quality."),
        ("Innovator", "Add one killer feature.")
    ]

    logs = load_json(log_file, [])
    history = [f"User: {task}"]

    for name, prompt in agents:
        print(f"[{project}] {name} → working")
        messages = [{"role": "system", "content": prompt}]
        for msg in history:
            messages.append({"role": "user" if "User:" in msg else "assistant", "content": msg})

        response = client.chat.completions.create(
            model="qwen2.5-coder:14b-instruct-q4_K_M",
            messages=messages,
            temperature=0.15
        ).choices[0].message.content

        logs.append({"agent": name, "content": response, "time": time.strftime("%H:%M")})
        save_json(log_file, logs)
        history.append(f"{name}: {response}")
        print(f"[{project}] {name} → done")

    print(f"Council finished: {project}")
