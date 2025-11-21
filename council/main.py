from crewai import Agent, Task, Crew, Process, LLM

# THIS IS THE WINNING CONFIG — uses localhost + ollama/ prefix
llm = LLM(
    model="ollama/qwen2.5-coder:14b-instruct-q4_K_M",
    base_url="http://localhost:11434",   # ← proven working
    temperature=0.1,
    timeout=180                           # 3 minutes max per call (plenty)
)

# Agents
pm = Agent(role="Project Manager", goal="Break down tasks and plan perfectly", backstory="You are a senior PM.", llm=llm, verbose=True, allow_delegation=False)
coder = Agent(role="Senior Developer", goal="Write clean, working code", backstory="You are a full-stack expert.", llm=llm, verbose=True)
tester = Agent(role="QA Engineer", goal="Test rigorously and find edge cases", backstory="You never miss a bug.", llm=llm, verbose=True)

def run_council(user_task: str):
    task1 = Task(description=f"Plan this project: {user_task}", expected_output="Detailed plan", agent=pm)
    task2 = Task(description="Write the complete code based on the plan", expected_output="Working code", agent=coder, context=[task1])
    task3 = Task(description="Test the code thoroughly and report issues", expected_output="Test report", agent=tester, context=[task1, task2])

    crew = Crew(agents=[pm, coder, tester], tasks=[task1, task2, task3], process=Process.sequential, verbose=True)
    return crew.kickoff()

if __name__ == "__main__":
    print(run_council("Quick test: Build a Python script that prints 'Hello from the AI Council!'"))
