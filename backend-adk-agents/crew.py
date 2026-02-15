"""
Veritas Swarm — Crew Orchestration
Wires agents + tasks into a single CrewAI Crew.
"""

from crewai import Crew, Process
from agents import create_agents
from tasks import create_tasks
from orchestrator import get_agents_for_file


class VeritasCrew:
    """
    Orchestrates the Veritas Swarm deepfake-detection pipeline.

    Usage:
        result = VeritasCrew("media/sample.jpg").run()
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def run(self, step_callback=None, task_callback=None, event_bridge=None):
        """Build the crew, kick it off, and return the final verdict."""

        # 1 — Create all agents
        all_agents = create_agents()
        
        # 2 — Select agents based on file type (orchestrator)
        selected_agents = get_agents_for_file(self.file_path, all_agents)

        # Inject event bridge into agents if provided
        if event_bridge:
            for agent in selected_agents.values():
                if hasattr(agent, "event_bridge"):
                    agent.event_bridge = event_bridge

        # 3 — Create tasks for selected agents only
        tasks = create_tasks(selected_agents, self.file_path)

        # 4 — Assemble the crew with selected agents
        crew_kwargs = dict(
            agents=list(selected_agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
        )
        if step_callback:
            crew_kwargs["step_callback"] = step_callback
        if task_callback:
            crew_kwargs["task_callback"] = task_callback

        crew = Crew(**crew_kwargs)

        # 4 — Kick off the swarm
        result = crew.kickoff()
        return result
