"""
Bootdisk Agent Tools
Integration tools and API clients for external services
"""

from .integration import ToolsIntegration
from .api import (
    BaseAPIClient,
    APIResponse,
    OpenAIClient,
    OllamaClient,
    HuggingFaceClient,
    GitHubClient,
    APIClientManager,
    call_openai_chat,
    call_ollama_generate,
    call_github_create_issue
)

__all__ = [
    # Tool integrations
    "ToolsIntegration",

    # API clients
    "BaseAPIClient",
    "APIResponse",
    "OpenAIClient",
    "OllamaClient",
    "HuggingFaceClient",
    "GitHubClient",
    "APIClientManager",

    # Convenience functions
    "call_openai_chat",
    "call_ollama_generate",
    "call_github_create_issue",
]