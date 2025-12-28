#!/usr/bin/env python3
"""
Multi-Agentic LangChain Workflows for Bootdisk Development

Secure, idempotent, parameterized agentic development integration.
Supports self-hosted Ollama models, public Hugging Face APIs, and OpenAI.
"""

import os
import asyncio
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.llms import Ollama, HuggingFaceHub, OpenAI
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

# Load environment variables securely
load_dotenv()

class SecureAgentManager:
    """Manages secure, parameterized multi-agent workflows."""

    def __init__(self):
        self.models = self._initialize_models()
        self.memory = ConversationBufferMemory()
        self.agents = {}

    def _initialize_models(self) -> Dict[str, Any]:
        """Initialize available models with secure credential handling."""
        models = {}

        # Self-hosted Ollama models (no credentials needed)
        try:
            models['rust_coder'] = Ollama(
                model="codellama:7b-code-q4_0",
                base_url="http://localhost:11434"
            )
            models['python_coder'] = Ollama(
                model="starcoder:3b",
                base_url="http://localhost:11434"
            )
        except Exception as e:
            print(f"Ollama models not available: {e}")

        # Public Hugging Face API (free tier, no token needed for some models)
        try:
            models['hf_coder'] = HuggingFaceHub(
                repo_id="microsoft/DialoGPT-medium",
                model_kwargs={"temperature": 0.7, "max_length": 512}
            )
        except Exception as e:
            print(f"Hugging Face API not available: {e}")

        # OpenAI (requires secure token)
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            models['openai_coder'] = OpenAI(
                temperature=0.7,
                openai_api_key=openai_key
            )

        return models

    def create_rust_agent(self) -> Optional[Any]:
        """Create specialized Rust coding agent."""
        if 'rust_coder' not in self.models:
            return None

        tools = [
            Tool(
                name="RustCodeGenerator",
                func=self._generate_rust_code,
                description="Generate idiomatic, performant Rust code"
            ),
            Tool(
                name="RustReviewer",
                func=self._review_rust_code,
                description="Review and optimize Rust code for memory safety"
            )
        ]

        return initialize_agent(
            tools=tools,
            llm=self.models['rust_coder'],
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True
        )

    def create_python_agent(self) -> Optional[Any]:
        """Create specialized Python coding agent."""
        if 'python_coder' not in self.models:
            return None

        tools = [
            Tool(
                name="PythonCodeGenerator",
                func=self._generate_python_code,
                description="Generate clean, efficient Python code"
            ),
            Tool(
                name="PythonOptimizer",
                func=self._optimize_python_code,
                description="Optimize Python code for performance"
            )
        ]

        return initialize_agent(
            tools=tools,
            llm=self.models['python_coder'],
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True
        )

    def create_porting_agent(self) -> Optional[Any]:
        """Create bi-language porting agent for Python/C to Rust."""
        available_models = [m for m in ['rust_coder', 'python_coder', 'openai_coder'] if m in self.models]
        if not available_models:
            return None

        # Use the best available model
        llm = self.models[available_models[0]]

        prompt = PromptTemplate(
            input_variables=["source_code", "source_lang", "target_lang"],
            template="""
            You are an expert code porting agent. Convert the following {source_lang} code to idiomatic, performant, memory-safe {target_lang}:

            Source code:
            {source_code}

            Requirements:
            - Maintain functionality
            - Use {target_lang} best practices
            - Ensure memory safety (especially for Rust)
            - Optimize for performance
            - Add proper error handling
            - Include documentation

            Ported code:
            """
        )

        chain = LLMChain(llm=llm, prompt=prompt)

        tools = [
            Tool(
                name="CodePorter",
                func=lambda code, src, tgt: chain.run(source_code=code, source_lang=src, target_lang=tgt),
                description="Port code between languages maintaining functionality and safety"
            )
        ]

        return initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True
        )

    def _generate_rust_code(self, description: str) -> str:
        """Generate Rust code from description."""
        prompt = f"Generate idiomatic Rust code for: {description}"
        return self.models.get('rust_coder', self.models.get('openai_coder', list(self.models.values())[0])).invoke(prompt)

    def _review_rust_code(self, code: str) -> str:
        """Review Rust code for safety and performance."""
        prompt = f"Review this Rust code for memory safety, performance, and best practices:\n\n{code}"
        return self.models.get('rust_coder', self.models.get('openai_coder', list(self.models.values())[0])).invoke(prompt)

    def _generate_python_code(self, description: str) -> str:
        """Generate Python code from description."""
        prompt = f"Generate clean Python code for: {description}"
        return self.models.get('python_coder', self.models.get('openai_coder', list(self.models.values())[0])).invoke(prompt)

    def _optimize_python_code(self, code: str) -> str:
        """Optimize Python code."""
        prompt = f"Optimize this Python code for performance:\n\n{code}"
        return self.models.get('python_coder', self.models.get('openai_coder', list(self.models.values())[0])).invoke(prompt)

async def main():
    """Main function for testing agents."""
    manager = SecureAgentManager()

    print("Available models:", list(manager.models.keys()))

    # Test Rust agent
    rust_agent = manager.create_rust_agent()
    if rust_agent:
        print("\nTesting Rust Agent...")
        result = await rust_agent.arun("Create a safe Rust function to parse a bootdisk schema YAML")
        print("Rust Agent Result:", result)

    # Test Python agent
    python_agent = manager.create_python_agent()
    if python_agent:
        print("\nTesting Python Agent...")
        result = await python_agent.arun("Create a Python function to validate preseed configuration")
        print("Python Agent Result:", result)

    # Test Porting agent
    porting_agent = manager.create_porting_agent()
    if porting_agent:
        print("\nTesting Porting Agent...")
        sample_python = """
def parse_config(file_path):
    with open(file_path, 'r') as f:
        return f.read()
"""
        result = await porting_agent.arun(f"Port this Python code to Rust: {sample_python}")
        print("Porting Agent Result:", result)

if __name__ == "__main__":
    asyncio.run(main())