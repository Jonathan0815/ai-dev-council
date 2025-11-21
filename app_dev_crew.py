from crewai import Agent, Task, Crew, Process, LLM
import json
from datetime import datetime
import os

LOG_FILE = "council_logs.json"

def log_message(agent: str, content: str, task: str = ""):
    entry = {
        "timestamp": datetime.now().isoformat(timespec='seconds'),
        "agent": agent,
        "content": content,
        "task": task or "unknown"
    }
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
    else:
        logs = []
    logs.append(entry)
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

llm = LLM(model="ollama/qwen2.5-coder:14b-instruct-q4_K_M",
          base_url="http://localhost:11434", temperature=0.1, timeout=180)

pm = Agent(role="Project Manager", goal="Break down tasks perfectly", backstory="Senior PM", llm=llm, verbose=True)
coder = Agent(role="Senior Developer", goal="Write clean working code", backstory="Full-stack expert", llm=llm, verbose=True)
tester = Agent(role="QA Engineer", goal="Find every bug", backstory="Never misses anything", llm=llm, verbose=True)

def run_council(user_task: str):
    log_message("PM", f"Planning task: {user_task}", user_task)
    t1 = Task(description=f"Plan this project: {user_task}", expected_output="Detailed plan", agent=pm)
    t2 = Task(description="Write complete working code", expected_output="Working code", agent=coder, context=[t1])
    t3 = Task(description="Test rigorously and report issues", expected_output="Test report", agent=tester, context=[t1,t2])
    
    crew = Crew(agents=[pm,coder,tester], tasks=[t1,t2,t3], process=Process.sequential, verbose=True)
    result = crew.kickoff()
    
    log_message("Council", "Task completed", user_task)
    log_message("Result", str(result)[:500] + ("..." if len(str(result))>500 else ""), user_task)
    return result
