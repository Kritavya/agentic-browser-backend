"""
Agent State Models.

Models for tracking agent and task state during execution.
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Possible task statuses."""

    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentState(BaseModel):
    """
    Current state of an agent during task execution.

    Tracks what the agent is doing and any intermediate results.
    """

    agent_name: str = Field(..., description="Name of the agent")
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        description="Current agent status",
    )
    current_action: str | None = Field(
        None,
        description="What the agent is currently doing",
    )
    progress: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Progress from 0 to 1",
    )
    started_at: datetime | None = Field(
        None,
        description="When this agent started",
    )
    completed_at: datetime | None = Field(
        None,
        description="When this agent completed",
    )
    result: Any = Field(None, description="Agent result if completed")
    error: str | None = Field(None, description="Error if failed")


class TaskState(BaseModel):
    """
    Complete state of a task.

    Includes the overall task status and states of all involved agents.
    """

    task_id: str = Field(..., description="Unique task identifier")
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        description="Overall task status",
    )
    description: str = Field(..., description="Task description")
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Task creation time",
    )
    started_at: datetime | None = Field(
        None,
        description="When task execution started",
    )
    completed_at: datetime | None = Field(
        None,
        description="When task completed",
    )
    agent_states: dict[str, AgentState] = Field(
        default_factory=dict,
        description="State of each agent involved",
    )
    result: Any = Field(None, description="Final task result")
    error: str | None = Field(None, description="Error if failed")

    def update_agent(self, agent_name: str, **kwargs: Any) -> None:
        """
        Update the state of a specific agent.

        Args:
            agent_name: Name of the agent to update.
            **kwargs: State attributes to update.
        """
        if agent_name not in self.agent_states:
            self.agent_states[agent_name] = AgentState(agent_name=agent_name)

        for key, value in kwargs.items():
            if hasattr(self.agent_states[agent_name], key):
                setattr(self.agent_states[agent_name], key, value)

    def mark_running(self) -> None:
        """Mark task as running."""
        self.status = TaskStatus.RUNNING
        self.started_at = datetime.utcnow()

    def mark_completed(self, result: Any = None) -> None:
        """Mark task as completed."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        self.result = result

    def mark_failed(self, error: str) -> None:
        """Mark task as failed."""
        self.status = TaskStatus.FAILED
        self.completed_at = datetime.utcnow()
        self.error = error
