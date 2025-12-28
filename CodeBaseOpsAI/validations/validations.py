import logging
from typing import Final

from config import CONSTANTS

log = logging.getLogger(__name__)


class InvalidAgentName(ValueError):
    """Raised when an agent name fails validation."""


_ALLOWED_CHARS: Final[set[str]] = set(CONSTANTS["ALLOWED_CHARS_FOR_AGENT_NAME"])


def ensure_is_string(name: object) -> None:
    """
    Raise TypeError if `name` is not a str.
    """
    if not isinstance(name, str):
        raise TypeError("Agent name must be a string")


def has_valid_characters(name: str) -> str:
    """
    Ensure `name` contains only allowed characters (letters, digits, space, hyphen, underscore).
    Returns `name` if valid; otherwise raises InvalidAgentName.
    """
    # Note: iterate over characters and check membership in allowed set
    if any(ch not in _ALLOWED_CHARS for ch in name):
        raise InvalidAgentName("Agent name contains invalid characters")
    return name


def is_empty_or_whitespace(name: str) -> bool:
    """
    Return True if `name` is empty or consists only of whitespace.
    """
    return len(name.strip()) == 0


def validate_agent_name(agent_name: object) -> str:
    """
    Validate and normalize an agent name.

    Rules:
      - must be a string (TypeError otherwise)
      - trimmed value must be non-empty (InvalidAgentName otherwise)
      - length <= 64 after trimming (InvalidAgentName otherwise)
      - allowed characters only (InvalidAgentName otherwise)

    Returns:
      - the trimmed, validated name

    Raises:
      - TypeError for non-string input
      - InvalidAgentName for value-related violations
    """
    # 1) Type check
    ensure_is_string(agent_name)

    # At this point, mypy/pyright may still consider agent_name as object; cast via str()
    name = str(agent_name).strip()

    # 2) Empty check (after trimming)
    if is_empty_or_whitespace(name):
        raise InvalidAgentName("Agent name cannot be empty or only whitespace")

    # 3) Length check
    if len(name) > 64:
        raise InvalidAgentName("Agent name must be at most 64 characters")

    # 4) Character whitelist check
    has_valid_characters(name)

    return name
