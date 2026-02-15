
import os
from dotenv import load_dotenv

# Load env
load_dotenv()
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
NVIDIA_BASE_URL = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")

# Force Env Vars for CrewAI/LiteLLM logic
os.environ["OPENAI_API_KEY"] = NVIDIA_API_KEY
os.environ["OPENAI_API_BASE"] = NVIDIA_BASE_URL
os.environ["OPENAI_MODEL_NAME"] = "openai/moonshotai/kimi-k2.5" # Use a valid model

from crewai import Agent, Task, Crew, Process
from callbacks import AgentEventBridge

bridge = AgentEventBridge()

def step_callback(step_output):
    print(f"\n[DEBUG] Step Callback received: {type(step_output)}")
    # Print attributes to find where agent name is hiding
    # Try expected attributes
    if hasattr(step_output, 'agent'):
        print(f"[DEBUG] .agent: {step_output.agent}")
    if hasattr(step_output, 'agent_role'):
        print(f"[DEBUG] .agent_role: {step_output.agent_role}")
    if hasattr(step_output, 'acting_agent'):
        print(f"[DEBUG] .acting_agent: {step_output.acting_agent}")
    
    # Dump all dir keys that don't start with _
    keys = [k for k in dir(step_output) if not k.startswith('_')]
    print(f"[DEBUG] Available keys: {keys}")

    bridge.step_callback(step_output)

def task_callback(task_output):
    print(f"\n[DEBUG] Task Callback received")
    bridge.task_callback(task_output)

# Create a simple agent that mimics "Human Signal Expert" role
agent = Agent(
    role="Human Signal Expert",
    goal="Test callbacks",
    backstory="Testing",
    llm="openai/moonshotai/kimi-k2.5",
    allow_delegation=False
)

task = Task(
    description="Return the word 'Detected'",
    expected_output="Detected",
    agent=agent
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    process=Process.sequential,
    step_callback=step_callback,
    task_callback=task_callback
)

print("Starting Crew...")
try:
    crew.kickoff()
except Exception as e:
    print(f"Crew failed: {e}")

print("\n--- Events captured in Bridge ---")
while not bridge.event_queue.empty():
    print(bridge.event_queue.get())
