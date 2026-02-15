
from crewai import Agent
from typing import Optional, Any
from pydantic import PrivateAttr

class VeritasAgent(Agent):
    """
    Custom Agent subclass to intercept task execution start
    and emit 'agent_start' events to the frontend.
    """
    _event_bridge: Optional[Any] = PrivateAttr(default=None)

    @property
    def event_bridge(self):
        return self._event_bridge

    @event_bridge.setter
    def event_bridge(self, value):
        self._event_bridge = value

    def execute_task(self, task, context=None, tools=None):
        # Emit start event if bridge is attached
        if self._event_bridge:
            # Map role to display name using bridge's internal mapping
            # or just pass role and let bridge handle it.
            self._event_bridge.notify_agent_start(self.role)

        return super().execute_task(task, context, tools)
