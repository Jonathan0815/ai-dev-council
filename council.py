import os
os.environ["OPENAI_API_KEY"] = "fake"  # tricks CrewAI

from crewai import Agent, Task, Crew
import ollama
from fastapi import FastAPI
from pydantic import BaseModel

class OllamaLLM:
    def __init__(self, model="llama3.1:8b"):
        self.model = model

    def __call__(self, prompt):
        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]

llm = OllamaLLM("llama3.1:8b")

ceo = Agent(role="CEO", goal="Decide what to build and upgrade the council itself", backstory="Visionary founder", llm=llm, verbose=True)
coder = Agent(role="Lead Engineer", goal="Write flawless code and fix dependency hell", backstory="10x developer", llm=llm, verbose=True)
qa = Agent(role="QA & Security", goal="Test everything, make it unbreakable", backstory="Perfectionist", llm=llm, verbose=True)
devops = Agent(role="DevOps Master", goal="Push to GitHub, write README, make it self-upgrading", backstory="GitHub legend", llm=llm, verbose=True)

tasks = [
    Task(description="Understand the idea and research", agent=ceo),
    Task(description="Write all code", agent=coder, context=[tasks[0]]),
    Task(description="Test and fix bugs", agent=qa, context=[tasks[0], tasks[1]]),
    Task(description="Create GitHub repo, push code, write perfect README + devcontainer", agent=devops, context=[tasks[0], tasks[1], tasks[2]])
]

crew = Crew(agents=[ceo, coder, qa, devops], tasks=tasks, verbose=2)

app = FastAPI()

class Idea(BaseModel):
    idea: str

@app.post("/build")
def build(idea: Idea):
    result = crew.kickoff(inputs={"idea": idea.idea})
    return {"result": str(result)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
