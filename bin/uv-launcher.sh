#!/usr/bin/env bash
# Cross-platform uv launcher for MCP-FRED extension
# Automatically detects platform and architecture to use the correct bundled uv binary

set -euo pipefail

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Detect platform and architecture
OS="$(uname -s)"
ARCH="$(uname -m)"

case "$OS" in
    Darwin)
        # macOS
        case "$ARCH" in
            arm64|aarch64)
                UV_BIN="$SCRIPT_DIR/darwin-arm64/uv"
                ;;
            x86_64)
                UV_BIN="$SCRIPT_DIR/darwin-x64/uv"
                ;;
            *)
                echo "Error: Unsupported macOS architecture: $ARCH" >&2
                exit 1
                ;;
        esac
        ;;
    Linux)
        # Linux
        case "$ARCH" in
            x86_64)
                UV_BIN="$SCRIPT_DIR/linux-x64/uv"
                ;;
            *)
                echo "Error: Unsupported Linux architecture: $ARCH" >&2
                exit 1
                ;;
        esac
        ;;
    MINGW*|MSYS*|CYGWIN*)
        # Windows (running in Git Bash or similar)
        UV_BIN="$SCRIPT_DIR/win32-x64/uv.exe"
        ;;
    *)
        echo "Error: Unsupported operating system: $OS" >&2
        exit 1
        ;;
esac

# Verify the binary exists
if [[ ! -f "$UV_BIN" ]]; then
    echo "Error: uv binary not found at: $UV_BIN" >&2
    exit 1
fi

# Ensure it's executable
chmod +x "$UV_BIN" 2>/dev/null || true

# Execute uv with all passed arguments
exec "$UV_BIN" "$@"
