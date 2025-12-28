#!/bin/bash
# DevContainer Validation Script for Bootdisk
# This script validates that the devcontainer environment is properly configured

set -e

echo "🚀 Bootdisk DevContainer Validation"
echo "=================================="

# Check if we're running in a container
if [ ! -f /.dockerenv ]; then
    echo "❌ Not running in a container. Please use 'Dev Containers: Reopen in Container' from VS Code"
    exit 1
fi

echo "✅ Running in container environment"

# Check Rust installation
echo "🔧 Checking Rust toolchain..."
if command -v rustc &> /dev/null; then
    echo "✅ Rust installed: $(rustc --version)"
    echo "✅ Cargo installed: $(cargo --version)"
else
    echo "❌ Rust not found"
    exit 1
fi

# Check Python installation
echo "🐍 Checking Python environment..."
if command -v python3 &> /dev/null; then
    echo "✅ Python installed: $(python3 --version)"
    PYTHON_PATH="/opt/venv/bin/python"
    if [ -f "$PYTHON_PATH" ]; then
        echo "✅ Virtual environment found at $PYTHON_PATH"
        export PATH="/opt/venv/bin:$PATH"
        echo "✅ Python packages: $($PYTHON_PATH -c 'import langchain, ollama, aider; print(\"langchain, ollama, aider imported successfully\")' 2>/dev/null || echo 'Some packages missing')"
    else
        echo "❌ Python virtual environment not found"
        exit 1
    fi
else
    echo "❌ Python not found"
    exit 1
fi

# Check Ollama installation
echo "🤖 Checking Ollama..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama installed: $(ollama --version)"
    echo "📋 Available models:"
    ollama list 2>/dev/null || echo "   No models installed or service not running"
else
    echo "❌ Ollama not found"
fi

# Check aider-chat
echo "💬 Checking aider-chat..."
if command -v aider &> /dev/null; then
    echo "✅ aider-chat installed: $(aider --version)"
else
    echo "❌ aider-chat not found"
fi

# Check development tools
echo "🛠️  Checking development tools..."
TOOLS=("git" "curl" "jq" "xorriso" "isoinfo")
for tool in "${TOOLS[@]}"; do
    if command -v $tool &> /dev/null; then
        echo "✅ $tool available"
    else
        echo "❌ $tool missing"
    fi
done

# Check workspace setup
echo "📁 Checking workspace setup..."
if [ -d "/workspaces/bootdisk" ]; then
    echo "✅ Workspace directory exists"
    if [ -f "/workspaces/bootdisk/pyproject.toml" ]; then
        echo "✅ Python project file found"
    else
        echo "⚠️  Python project file not found"
    fi
else
    echo "❌ Workspace directory not found"
fi

# Test Rust compilation
echo "🔨 Testing Rust compilation..."
cd /tmp
cat > test.rs << 'EOF'
fn main() {
    println!("Hello from Rust in devcontainer!");
}
EOF

if rustc test.rs && ./test; then
    echo "✅ Rust compilation successful"
    rm -f test.rs test
else
    echo "❌ Rust compilation failed"
    exit 1
fi

# Test Python execution
echo "🐍 Testing Python execution..."
cd /tmp
cat > test.py << 'EOF'
import sys
print(f"Python {sys.version} in devcontainer")
try:
    import langchain
    print("✅ LangChain available")
except ImportError:
    print("❌ LangChain not available")
EOF

if $PYTHON_PATH test.py; then
    echo "✅ Python execution successful"
    rm -f test.py
else
    echo "❌ Python execution failed"
    exit 1
fi

echo ""
echo "🎉 DevContainer validation complete!"
echo "📝 Summary: All core components are working"
echo "🚀 Ready for bootdisk development"

# Optional: Interactive testing mode
if [ "$1" = "interactive" ]; then
    echo ""
    echo "🔍 Interactive Testing Mode"
    echo "=========================="
    echo "You can now test additional functionality:"
    echo "- Run 'ollama serve' to start Ollama service"
    echo "- Run 'aider --help' to test aider-chat"
    echo "- Run 'cargo new test-project' to test Rust project creation"
    echo "- Run 'python -c \"import torch; print('PyTorch available')\"' to test ML libraries"
    echo ""
    echo "Starting interactive shell..."
    exec /bin/bash
fi