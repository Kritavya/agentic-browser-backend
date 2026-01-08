"""
Agents package - Execution Zone.

This package contains all agent implementations.
Each agent is responsible for a specific capability and must implement
the common AgentProtocol interface.

IMPORTANT:
- Agents do NOT communicate directly with each other
- All inter-agent communication goes through the Supervisor
- Agents return structured AgentResult objects
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    """
    Abstract base class for all agents.

    All agents must inherit from this class and implement the
    required abstract methods.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name for this agent."""
        ...

    @property
    @abstractmethod
    def capabilities(self) -> list[str]:
        """List of capabilities this agent provides."""
        ...

    @abstractmethod
    async def run(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Execute the agent's main task.

        Args:
            task: Task description and parameters.

        Returns:
            Structured result dictionary.
        """
        ...

    @abstractmethod
    async def execute(self, action: str, params: dict[str, Any]) -> dict[str, Any]:
        """
        Execute a specific action.

        Args:
            action: The action to execute.
            params: Action parameters.

        Returns:
            Action result dictionary.
        """
        ...
