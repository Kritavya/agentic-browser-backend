"""
Request Models.

Pydantic models for API request validation.
All incoming API requests should use these models for validation.
"""

from typing import Any

from pydantic import BaseModel, Field


class AgentRunRequest(BaseModel):
    """
    Request to run an agent task.

    This is the main request model for the /agent/run endpoint.
    """

    task: str = Field(
        ...,
        description="Natural language description of the task to execute",
        examples=["Navigate to google.com and search for 'python'"],
    )
    session_id: str | None = Field(
        None,
        description="Optional existing session ID to use",
    )
    config: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional configuration overrides",
    )
    timeout_ms: int = Field(
        default=60000,
        ge=1000,
        le=300000,
        description="Task timeout in milliseconds",
    )


class NavigateRequest(BaseModel):
    """Request to navigate to a URL."""

    url: str = Field(..., description="URL to navigate to")
    session_id: str | None = Field(None, description="Session ID")
    wait_until: str = Field(
        default="load",
        description="When to consider navigation complete",
    )


class ClickRequest(BaseModel):
    """Request to click an element."""

    selector: str = Field(..., description="Element selector")
    session_id: str = Field(..., description="Session ID")
    selector_type: str = Field(
        default="css",
        description="Selector type (css, xpath, text)",
    )


class TypeRequest(BaseModel):
    """Request to type text into an element."""

    selector: str = Field(..., description="Element selector")
    text: str = Field(..., description="Text to type")
    session_id: str = Field(..., description="Session ID")
    clear_first: bool = Field(
        default=False,
        description="Clear existing text before typing",
    )


class ExtractRequest(BaseModel):
    """Request to extract data from page."""

    session_id: str = Field(..., description="Session ID")
    extraction_type: str = Field(
        default="text",
        description="Type of extraction (text, table, links, structured)",
    )
    selector: str | None = Field(
        None,
        description="Optional selector to scope extraction",
    )
    schema: dict[str, Any] | None = Field(
        None,
        description="Optional schema for structured extraction",
    )


class SearchRequest(BaseModel):
    """Request to perform a web search."""

    query: str = Field(..., description="Search query")
    session_id: str | None = Field(None, description="Session ID")
    engine: str = Field(
        default="google",
        description="Search engine to use",
    )
    result_count: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of results to return",
    )


class SummarizeRequest(BaseModel):
    """Request to summarize content."""

    session_id: str = Field(..., description="Session ID")
    max_length: int = Field(
        default=500,
        ge=50,
        le=5000,
        description="Maximum summary length in characters",
    )
    format: str = Field(
        default="paragraph",
        description="Summary format (paragraph, bullets, json)",
    )
