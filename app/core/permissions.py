"""
Permissions - Capability Checks.

The Permissions module manages what actions agents are allowed to perform.
It implements a capability-based security model where actions are only
allowed if explicitly granted.

IMPORTANT:
- Default deny - if not explicitly allowed, deny
- Capabilities are scoped per session/task
- Log all permission checks for auditing

TODO:
- Implement role-based access control
- Add dynamic capability grants
- Support capability inheritance
- Implement capability revocation
"""

from enum import Enum
from typing import Any


class Capability(str, Enum):
    """
    Enumeration of all possible agent capabilities.

    Each capability represents a specific action type that an agent
    may request to perform.
    """

    # Navigation capabilities
    NAVIGATE_URL = "navigate_url"
    NAVIGATE_BACK = "navigate_back"
    NAVIGATE_FORWARD = "navigate_forward"
    REFRESH_PAGE = "refresh_page"

    # DOM capabilities
    READ_DOM = "read_dom"
    CLICK_ELEMENT = "click_element"
    TYPE_TEXT = "type_text"
    SCROLL_PAGE = "scroll_page"

    # Data capabilities
    EXTRACT_DATA = "extract_data"
    DOWNLOAD_FILE = "download_file"
    UPLOAD_FILE = "upload_file"

    # System capabilities
    EXECUTE_SCRIPT = "execute_script"
    CAPTURE_SCREENSHOT = "capture_screenshot"
    ACCESS_COOKIES = "access_cookies"


class PermissionDenied(Exception):
    """Raised when a capability check fails."""

    def __init__(self, capability: Capability, reason: str) -> None:
        super().__init__(f"Permission denied for {capability}: {reason}")
        self.capability = capability
        self.reason = reason


class PermissionChecker:
    """
    Manages capability checks for agent actions.

    The PermissionChecker maintains a set of granted capabilities
    per session and validates requests against them.
    """

    def __init__(self) -> None:
        """
        Initialize the PermissionChecker.

        TODO:
        - Load default capability sets
        - Configure capability scopes
        """
        # Session ID -> set of granted capabilities
        self._grants: dict[str, set[Capability]] = {}

        # Default capabilities for new sessions
        self._default_capabilities: set[Capability] = {
            Capability.NAVIGATE_URL,
            Capability.READ_DOM,
            Capability.CLICK_ELEMENT,
            Capability.TYPE_TEXT,
            Capability.SCROLL_PAGE,
            Capability.CAPTURE_SCREENSHOT,
        }

    def grant(self, session_id: str, capability: Capability) -> None:
        """
        Grant a capability to a session.

        Args:
            session_id: The session identifier.
            capability: The capability to grant.

        TODO:
        - Log capability grants for auditing
        - Validate capability is valid for session type
        """
        if session_id not in self._grants:
            self._grants[session_id] = self._default_capabilities.copy()
        self._grants[session_id].add(capability)

    def revoke(self, session_id: str, capability: Capability) -> None:
        """
        Revoke a capability from a session.

        Args:
            session_id: The session identifier.
            capability: The capability to revoke.

        TODO:
        - Log capability revocations for auditing
        """
        if session_id in self._grants:
            self._grants[session_id].discard(capability)

    def check(self, session_id: str, capability: Capability) -> bool:
        """
        Check if a session has a specific capability.

        Args:
            session_id: The session identifier.
            capability: The capability to check.

        Returns:
            bool: True if the capability is granted.

        TODO:
        - Log all permission checks
        - Support capability scoping
        """
        if session_id not in self._grants:
            # Initialize with defaults for new sessions
            self._grants[session_id] = self._default_capabilities.copy()

        return capability in self._grants[session_id]

    def require(self, session_id: str, capability: Capability) -> None:
        """
        Require a capability, raising an exception if not granted.

        Args:
            session_id: The session identifier.
            capability: The required capability.

        Raises:
            PermissionDenied: If the capability is not granted.
        """
        if not self.check(session_id, capability):
            raise PermissionDenied(
                capability, f"Session {session_id} does not have this capability"
            )

    def get_capabilities(self, session_id: str) -> set[Capability]:
        """
        Get all capabilities granted to a session.

        Args:
            session_id: The session identifier.

        Returns:
            Set of granted capabilities.
        """
        if session_id not in self._grants:
            self._grants[session_id] = self._default_capabilities.copy()
        return self._grants[session_id].copy()


# Singleton instance
_permission_checker: PermissionChecker | None = None


def get_permission_checker() -> PermissionChecker:
    """Get the PermissionChecker singleton."""
    global _permission_checker
    if _permission_checker is None:
        _permission_checker = PermissionChecker()
    return _permission_checker
