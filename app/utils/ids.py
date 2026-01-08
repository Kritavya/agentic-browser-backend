"""
ID Generation Utilities.

Provides functions for generating unique identifiers.
Uses UUIDs with optional prefixes for readability.

TODO:
- Add ULID support for sortable IDs
- Consider using nanoid for shorter IDs
"""

import uuid
from datetime import datetime


def generate_id(prefix: str = "") -> str:
    """
    Generate a unique identifier.

    Args:
        prefix: Optional prefix for the ID.

    Returns:
        Unique identifier string.

    Examples:
        >>> generate_id()
        'a1b2c3d4-e5f6-...'
        >>> generate_id("task")
        'task_a1b2c3d4-e5f6-...'
    """
    uid = str(uuid.uuid4())
    if prefix:
        return f"{prefix}_{uid}"
    return uid


def generate_short_id(length: int = 8) -> str:
    """
    Generate a short unique identifier.

    Less unique than full UUID but more readable.
    Suitable for session IDs and similar use cases.

    Args:
        length: Length of the ID (default 8).

    Returns:
        Short unique identifier.
    """
    return str(uuid.uuid4())[:length]


def generate_timestamp_id(prefix: str = "") -> str:
    """
    Generate a timestamp-based sortable identifier.

    Format: prefix_YYYYMMDDHHMMSS_uuid8

    Args:
        prefix: Optional prefix.

    Returns:
        Timestamp-based identifier.
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    short_uuid = generate_short_id()
    if prefix:
        return f"{prefix}_{timestamp}_{short_uuid}"
    return f"{timestamp}_{short_uuid}"
