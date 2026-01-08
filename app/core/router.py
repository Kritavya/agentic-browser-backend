"""
Agent Router.

The Router is responsible for selecting the appropriate agent(s) for
a given task. It analyzes the task requirements and maps them to
available agent capabilities.

IMPORTANT:
- Do NOT hardcode agent references
- Use a registry pattern for agent discovery
- Support dynamic agent registration

TODO:
- Implement capability-based routing
- Add fallback agent selection
- Support multi-agent routing for complex tasks
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class AgentProtocol(Protocol):
    """
    Protocol defining the common interface for all agents.

    All agents must implement this protocol to be registered with the Router.
    """

    async def run(self, task: dict) -> dict:
        """Execute the agent's main task."""
        ...

    async def execute(self, action: str, params: dict) -> dict:
        """Execute a specific action."""
        ...

    @property
    def capabilities(self) -> list[str]:
        """List of capabilities this agent provides."""
        ...


class AgentRegistry:
    """
    Registry for agent discovery and lookup.

    Agents register themselves with their capabilities, and the router
    uses this registry to find appropriate agents for tasks.
    """

    def __init__(self) -> None:
        """Initialize empty agent registry."""
        self._agents: dict[str, AgentProtocol] = {}
        self._capabilities: dict[str, list[str]] = {}

    def register(self, name: str, agent: AgentProtocol) -> None:
        """
        Register an agent with the router.

        Args:
            name: Unique identifier for the agent.
            agent: The agent instance implementing AgentProtocol.

        TODO:
        - Validate agent implements required interface
        - Index capabilities for fast lookup
        """
        self._agents[name] = agent
        self._capabilities[name] = agent.capabilities

    def get(self, name: str) -> AgentProtocol | None:
        """
        Get an agent by name.

        Args:
            name: The agent identifier.

        Returns:
            The agent if found, None otherwise.
        """
        return self._agents.get(name)

    def find_by_capability(self, capability: str) -> list[str]:
        """
        Find agents that have a specific capability.

        Args:
            capability: The capability to search for.

        Returns:
            List of agent names that have this capability.

        TODO:
        - Implement fuzzy matching
        - Support capability hierarchies
        """
        return [
            name
            for name, caps in self._capabilities.items()
            if capability in caps
        ]


class Router:
    """
    Routes tasks to appropriate agents based on task analysis.
    """

    def __init__(self, registry: AgentRegistry | None = None) -> None:
        """
        Initialize the Router.

        Args:
            registry: Optional agent registry. Creates new one if not provided.
        """
        self.registry = registry or AgentRegistry()

    async def route(self, task: dict) -> list[str]:
        """
        Determine which agent(s) should handle a task.

        Analyzes the task description and requirements to select
        the most appropriate agent(s) for execution.

        Args:
            task: The task description and parameters.

        Returns:
            List of agent names that should handle this task.

        TODO:
        - Implement task analysis logic
        - Use LLM for complex routing decisions
        - Support task decomposition into sub-tasks
        """
        # Placeholder - return empty list until implemented
        return []

    async def get_agent(self, name: str) -> AgentProtocol | None:
        """
        Get an agent by name from the registry.

        Args:
            name: The agent identifier.

        Returns:
            The agent if found, None otherwise.
        """
        return self.registry.get(name)


# Singleton instance
_router: Router | None = None


def get_router() -> Router:
    """Get the Router singleton."""
    global _router
    if _router is None:
        _router = Router()
    return _router
