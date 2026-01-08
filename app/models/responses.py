"""
Response Models.

Pydantic models for API responses.
All API responses should use these models for consistent structure.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class AgentResult(BaseModel):
    """
    Standard result from agent execution.

    All agents return this structure to ensure consistent handling.
    """

    success: bool = Field(..., description="Whether the operation succeeded")
    data: Any = Field(None, description="Result data if successful")
    error: str | None = Field(None, description="Error message if failed")
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata",
    )


class AgentRunResponse(BaseModel):
    """
    Response from the /agent/run endpoint.

    Contains task information and execution result.
    """

    task_id: str = Field(..., description="Unique identifier for the task")
    status: str = Field(
        ...,
        description="Task status (pending, running, completed, failed)",
    )
    message: str | None = Field(None, description="Human-readable status message")
    result: AgentResult | None = Field(
        None,
        description="Execution result if completed",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the task was created",
    )


class SessionResponse(BaseModel):
    """Response containing session information."""

    session_id: str = Field(..., description="Session identifier")
    status: str = Field(..., description="Session status")
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Session creation time",
    )
    page_url: str | None = Field(None, description="Current page URL")
    page_title: str | None = Field(None, description="Current page title")


class NavigationResponse(BaseModel):
    """Response from navigation operations."""

    success: bool = Field(..., description="Whether navigation succeeded")
    url: str = Field(..., description="Current URL after navigation")
    title: str | None = Field(None, description="Page title")
    status_code: int | None = Field(None, description="HTTP status code")


class ExtractionResponse(BaseModel):
    """Response from data extraction operations."""

    success: bool = Field(..., description="Whether extraction succeeded")
    data: Any = Field(None, description="Extracted data")
    extraction_type: str = Field(..., description="Type of extraction performed")
    element_count: int = Field(
        default=0,
        description="Number of elements extracted",
    )


class SearchResponse(BaseModel):
    """Response from search operations."""

    success: bool = Field(..., description="Whether search succeeded")
    query: str = Field(..., description="The search query")
    results: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Search results",
    )
    result_count: int = Field(default=0, description="Number of results")


class SummaryResponse(BaseModel):
    """Response from summarization operations."""

    success: bool = Field(..., description="Whether summarization succeeded")
    summary: str | None = Field(None, description="Generated summary")
    key_points: list[str] = Field(
        default_factory=list,
        description="Key points extracted",
    )
    word_count: int = Field(default=0, description="Summary word count")


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Machine-readable error code")
    details: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional error details",
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)
