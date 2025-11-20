from crewai import Agent, Task, Crew
from langchain_ollama import OllamaLLM
from fastapi import FastAPI
from pydantic import BaseModel

llm = OllamaLLM(model="llama3.1:8b")  # or "qwen2.5-coder:14b-instruct-q4_K_M"

pm = Agent(role="Product Manager", goal="Create perfect specs", backstory="Senior PM", llm=llm, verbose=True)
coder = Agent(role="Senior Full-Stack Developer", goal="Write complete code", backstory="Expert coder", llm=llm, verbose=True)
reviewer = Agent(role="QA & Reviewer", goal="Find bugs and improve", backstory="Perfectionist", llm=llm, verbose=True)

t1 = Task(description="Research and write detailed spec for: {idea}", expected_output="spec.md", agent=pm)
t2 = Task(description="Write all code based on the spec", expected_output="Complete code", agent=coder, context=[t1])
t3 = Task(description="Review, test mentally, fix bugs, improve performance/security", expected_output="Final polished code", agent=reviewer, context=[t2])

crew = Crew(agents=[pm, coder, reviewer], tasks=[t1, t2, t3], verbose=True)

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
