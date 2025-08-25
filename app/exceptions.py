# app/exceptions.py

class ModerationError(Exception):
    """Base class for moderation-related errors."""


class LLMServiceError(ModerationError):
    """Raised when the LLM service (OpenAI/Gemini) fails."""


class NotificationError(ModerationError):
    """Raised when sending a notification fails."""


class DatabaseError(ModerationError):
    """Raised when a database operation fails."""
