"""
Veritas Swarm — SSE Callback Bridge
Pushes CrewAI execution events into an asyncio.Queue for SSE streaming.
"""

import json
import queue
import re


class AgentEventBridge:
    """
    Thread-safe bridge between synchronous CrewAI callbacks and
    the async SSE event stream.
    """

    def __init__(self):
        self.event_queue = queue.Queue()
        self._agent_order = [
            "Human Signal Expert",
            "Environmental Forensic Analyst",
            "Digital Artifact Investigator",
            "Audio-Visual Auditor",
            "Master Deepfake Verdict Agent",
        ]
        self._agent_names = {
            "Human Signal Expert": "Biometric Sentinel",
            "Environmental Forensic Analyst": "Physics Inspector",
            "Digital Artifact Investigator": "Signal Analyst",
            "Audio-Visual Auditor": "Sync Specialist",
            "Master Deepfake Verdict Agent": "Chief Justice",
        }
        self._started_agents = set()

    def _push(self, event_type: str, data: dict):
        self.event_queue.put(json.dumps({"type": event_type, **data}))

    def notify_agent_start(self, agent_role: str):
        """Public method called by VeritasAgent when it starts a task."""
        if agent_role not in self._started_agents:
            self._started_agents.add(agent_role)
            display_name = self._agent_names.get(agent_role, agent_role)

            if agent_role == "Master Deepfake Verdict Agent":
                self._push("master_start", {"status": "synthesizing"})
            else:
                self._push("agent_start", {
                    "agent": display_name,
                    "status": "analyzing",
                })

    def task_callback(self, task_output):
        """Called when a CrewAI task completes."""
        agent_role = getattr(task_output, "agent", None) or ""
        raw_output = getattr(task_output, "raw", "") or str(task_output)
        display_name = self._agent_names.get(str(agent_role), str(agent_role))

        if str(agent_role) == "Master Deepfake Verdict Agent":
            # Parse the master verdict
            verdict_data = self._parse_verdict(raw_output)
            self._push("verdict", verdict_data)
        else:
            self._push("agent_complete", {
                "agent": display_name,
                "findings": raw_output[:500],
            })

    def step_callback(self, step_output):
        """Called on each CrewAI agent step — used to detect agent starts."""
        # DEBUG: Print step_output structure to identify available attributes
        # print(f"[DEBUG] step_callback received: {type(step_output)} {dir(step_output)}")
        
        agent_role = ""
        
        # Try various attributes used in different CrewAI versions
        if hasattr(step_output, "agent"):
            agent_role = str(step_output.agent)
        elif hasattr(step_output, "agent_role"):
            agent_role = str(step_output.agent_role)
        elif hasattr(step_output, "acting_agent"): # Some versions
            agent_role = str(step_output.acting_agent)
        elif hasattr(step_output, "metadata") and isinstance(step_output.metadata, dict):
            agent_role = step_output.metadata.get("agent", "")
        
        # If still empty, try to parse from string representation (fallback)
        if not agent_role:
             s = str(step_output)
             # sometimes it's just the output string, which doesn't help. 
             # But if it's an object, str() might reveal something.
             pass

        if agent_role and agent_role not in self._started_agents:
            self._started_agents.add(agent_role)
            display_name = self._agent_names.get(agent_role, agent_role)

            if agent_role == "Master Deepfake Verdict Agent":
                self._push("master_start", {"status": "synthesizing"})
            else:
                self._push("agent_start", {
                    "agent": display_name,
                    "status": "analyzing",
                })

    def push_error(self, message: str):
        self._push("error", {"message": message})

    def push_done(self):
        self._push("done", {})

    def _parse_verdict(self, raw: str) -> dict:
        """Best-effort parse of the master verdict output."""
        score = 50
        confidence = "MEDIUM"
        findings = []
        laymans_brief = ""

        # Extract score
        score_match = re.search(r"VERDICT\s*SCORE\s*:\s*(\d+)", raw, re.IGNORECASE)
        if score_match:
            score = int(score_match.group(1))

        # Extract confidence
        conf_match = re.search(r"CONFIDENCE\s*:\s*(HIGH|MEDIUM|LOW)", raw, re.IGNORECASE)
        if conf_match:
            confidence = conf_match.group(1).upper()

        # Extract findings (bullet points)
        findings_section = re.search(
            r"KEY\s*FINDINGS\s*:?\s*(.*?)(?:LAYMAN|$)",
            raw,
            re.IGNORECASE | re.DOTALL,
        )
        if findings_section:
            bullets = re.findall(r"[•\-\*]\s*(.+)", findings_section.group(1))
            findings = [b.strip() for b in bullets if b.strip()]

        # Extract layman's brief
        layman_match = re.search(
            r"LAYMAN[''S]*\s*BRIEF\s*:?\s*(.*)",
            raw,
            re.IGNORECASE | re.DOTALL,
        )
        if layman_match:
            laymans_brief = layman_match.group(1).strip()

        return {
            "score": score,
            "confidence": confidence,
            "findings": findings,
            "laymans_brief": laymans_brief,
            "raw": raw,
        }
