"""
Memory Schema.

Pydantic models for memory storage.
Defines the structure of memory entries and sessions.

TODO:
- Add more entry types
- Support metadata attachments
- Add serialization helpers
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class MemoryEntry(BaseModel):
    """
    A single memory entry.

    Represents one piece of information stored in session memory,
    such as an action taken, an observation made, or a result received.
    """

    entry_type: str = Field(..., description="Type of memory entry")
    content: Any = Field(..., description="The memory content")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="When the entry was created"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Optional metadata"
    )


class SessionMemory(BaseModel):
    """
    Complete memory for a session.

    Contains all memory entries for a browsing session along with
    session-level metadata.
    """

    session_id: str = Field(..., description="Unique session identifier")
    entries: list[MemoryEntry] = Field(
        default_factory=list, description="List of memory entries"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Session creation time"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Session metadata"
    )

    def add_entry(self, entry_type: str, content: Any) -> MemoryEntry:
        """
        Add a new entry to the session.

        Args:
            entry_type: Type of the entry.
            content: Entry content.

        Returns:
            The created entry.
        """
        entry = MemoryEntry(entry_type=entry_type, content=content)
        self.entries.append(entry)
        return entry

    def get_recent(self, n: int = 10) -> list[MemoryEntry]:
        """
        Get the N most recent entries.

        Args:
            n: Number of entries to return.

        Returns:
            Most recent entries.
        """
        return self.entries[-n:]
