FROM mcr.microsoft.com/devcontainers/rust:1-bullseye

# Install additional packages for AI/ML and development
RUN apt-get update && apt-get install -y \
    libssl-dev \
    pkg-config \
    xorriso \
    isolinux \
    python3-dev \
    build-essential \
    git \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Set up Python virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python packages for multi-agentic workflows
RUN pip install --upgrade pip && \
    pip install langchain langchain-openai langchain-community langchain-huggingface ollama openai tiktoken python-dotenv transformers && \
    pip install torch --index-url https://download.pytorch.org/whl/cpu

# Install Ollama for self-hosted models
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Install aider-chat for CLI agentic development
RUN pip install aider-chat

# Install Hugging Face CLI for public API access
RUN pip install huggingface_hub

# Create workspace directories
RUN mkdir -p /workspaces/bootdisk/.env /workspaces/bootdisk/agents

# Set up user
USER vscode

# Expose ports for development and AI services
EXPOSE 3000 8000 8080 11434

# Copy agent scripts
COPY .devcontainer/agents/ /workspaces/bootdisk/agents/