"""
Bootdisk Agent API Clients
HTTP clients and API integrations for external services
"""

import aiohttp
import asyncio
from typing import Dict, List, Any, Optional, Union
import json
import logging
from dataclasses import dataclass
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


@dataclass
class APIResponse:
    """Standardized API response structure"""
    success: bool
    data: Any = None
    error: Optional[str] = None
    status_code: Optional[int] = None
    headers: Dict[str, str] = None

    def __post_init__(self):
        if self.headers is None:
            self.headers = {}


class BaseAPIClient:
    """Base class for API clients with common functionality"""

    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.session: Optional[aiohttp.ClientSession] = None
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    async def connect(self) -> None:
        """Establish connection to the API"""
        if self.session is None:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            self.session = aiohttp.ClientSession(
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
            self.logger.info("Connected to API")

    async def disconnect(self) -> None:
        """Close the API connection"""
        if self.session:
            await self.session.close()
            self.session = None
            self.logger.info("Disconnected from API")

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> APIResponse:
        """Make an HTTP request to the API"""
        if not self.session:
            return APIResponse(success=False, error="Not connected to API")

        url = urljoin(self.base_url + '/', endpoint.lstrip('/'))

        try:
            request_data = None
            if data:
                if method.upper() in ['POST', 'PUT', 'PATCH']:
                    request_data = json.dumps(data)
                    if not headers:
                        headers = {}
                    headers['Content-Type'] = 'application/json'
                else:
                    params = params or {}
                    params.update(data)

            self.logger.debug(f"Making {method} request to {url}")

            async with self.session.request(
                method=method,
                url=url,
                data=request_data,
                params=params,
                headers=headers
            ) as response:
                response_data = None
                try:
                    response_text = await response.text()
                    if response_text:
                        response_data = json.loads(response_text)
                except json.JSONDecodeError:
                    response_data = response_text

                if response.status >= 200 and response.status < 300:
                    return APIResponse(
                        success=True,
                        data=response_data,
                        status_code=response.status,
                        headers=dict(response.headers)
                    )
                else:
                    error_msg = response_data if isinstance(response_data, str) else str(response_data)
                    return APIResponse(
                        success=False,
                        error=f"HTTP {response.status}: {error_msg}",
                        status_code=response.status,
                        headers=dict(response.headers)
                    )

        except asyncio.TimeoutError:
            return APIResponse(success=False, error="Request timeout")
        except aiohttp.ClientError as e:
            return APIResponse(success=False, error=f"Client error: {e}")
        except Exception as e:
            return APIResponse(success=False, error=f"Unexpected error: {e}")


class OpenAIClient(BaseAPIClient):
    """Client for OpenAI API integration"""

    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1"):
        # Validate API key early to avoid hard-to-debug authentication errors
        if api_key is None or not str(api_key).strip():
            raise ValueError("OpenAI API key must be provided and cannot be empty.")
        super().__init__(base_url, api_key)

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> APIResponse:
        """Create a chat completion"""
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        if max_tokens:
            data["max_tokens"] = max_tokens

        return await self._make_request("POST", "/chat/completions", data)

    async def list_models(self) -> APIResponse:
        """List available models"""
        return await self._make_request("GET", "/models")


class OllamaClient(BaseAPIClient):
    """Client for Ollama API integration"""

    def __init__(self, base_url: str = "http://localhost:11434"):
        super().__init__(base_url)

    async def generate(
        self,
        model: str,
        prompt: str,
        stream: bool = False,
        options: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """Generate text using Ollama"""
        data = {
            "model": model,
            "prompt": prompt,
            "stream": stream
        }
        if options:
            data["options"] = options

        return await self._make_request("POST", "/api/generate", data)

    async def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        stream: bool = False
    ) -> APIResponse:
        """Chat with Ollama model"""
        data = {
            "model": model,
            "messages": messages,
            "stream": stream
        }

        return await self._make_request("POST", "/api/chat", data)

    async def list_models(self) -> APIResponse:
        """List available models"""
        return await self._make_request("GET", "/api/tags")


class HuggingFaceClient(BaseAPIClient):
    """Client for Hugging Face API integration"""

    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api-inference.huggingface.co"):
        super().__init__(base_url, api_key)

    async def text_generation(
        self,
        model: str,
        inputs: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """Generate text using Hugging Face model"""
        data = {
            "inputs": inputs
        }
        if parameters:
            data.update(parameters)

        endpoint = f"/models/{model}"
        return await self._make_request("POST", endpoint, data)


class GitHubClient(BaseAPIClient):
    """Client for GitHub API integration"""

    def __init__(self, token: str, base_url: str = "https://api.github.com"):
        super().__init__(base_url, token)

    async def get_repo(self, owner: str, repo: str) -> APIResponse:
        """Get repository information"""
        return await self._make_request("GET", f"/repos/{owner}/{repo}")

    async def create_issue(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str,
        labels: Optional[List[str]] = None
    ) -> APIResponse:
        """Create a new issue"""
        data = {
            "title": title,
            "body": body
        }
        if labels:
            data["labels"] = labels

        return await self._make_request("POST", f"/repos/{owner}/{repo}/issues", data)

    async def create_pull_request(
        self,
        owner: str,
        repo: str,
        title: str,
        head: str,
        base: str,
        body: str
    ) -> APIResponse:
        """Create a pull request"""
        data = {
            "title": title,
            "head": head,
            "base": base,
            "body": body
        }

        return await self._make_request("POST", f"/repos/{owner}/{repo}/pulls", data)


class APIClientManager:
    """Manager for multiple API clients"""

    def __init__(self):
        self.clients: Dict[str, BaseAPIClient] = {}
        self.logger = logging.getLogger(f"{__name__}.APIClientManager")

    def register_client(self, name: str, client: BaseAPIClient) -> None:
        """Register an API client"""
        self.clients[name] = client
        self.logger.info(f"Registered API client: {name}")

    def get_client(self, name: str) -> Optional[BaseAPIClient]:
        """Get a registered client"""
        return self.clients.get(name)

    async def connect_all(self) -> None:
        """Connect all registered clients"""
        for name, client in self.clients.items():
            try:
                await client.connect()
                self.logger.info(f"Connected client: {name}")
            except Exception as e:
                self.logger.error(f"Failed to connect client {name}: {e}")

    async def disconnect_all(self) -> None:
        """Disconnect all registered clients"""
        for name, client in self.clients.items():
            try:
                await client.disconnect()
                self.logger.info(f"Disconnected client: {name}")
            except Exception as e:
                self.logger.error(f"Failed to disconnect client {name}: {e}")

    async def __aenter__(self):
        await self.connect_all()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect_all()


# Convenience functions for common API operations
async def call_openai_chat(
    messages: List[Dict[str, str]],
    api_key: str,
    model: str = "gpt-4",
    temperature: float = 0.7
) -> APIResponse:
    """Convenience function for OpenAI chat completion"""
    async with OpenAIClient(api_key) as client:
        return await client.chat_completion(messages, model, temperature)


async def call_ollama_generate(
    model: str,
    prompt: str,
    base_url: str = "http://localhost:11434"
) -> APIResponse:
    """Convenience function for Ollama text generation"""
    async with OllamaClient(base_url) as client:
        return await client.generate(model, prompt)


async def call_github_create_issue(
    owner: str,
    repo: str,
    title: str,
    body: str,
    token: str,
    labels: Optional[List[str]] = None
) -> APIResponse:
    """Convenience function for creating GitHub issues"""
    async with GitHubClient(token) as client:
        return await client.create_issue(owner, repo, title, body, labels)</content>
<parameter name="filePath">/home/spooky/Documents/projects/bootdisk/agents/tools/api.py