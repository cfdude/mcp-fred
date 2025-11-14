#!/usr/bin/env bash
# Build script for MCP-FRED Claude Desktop Extension

set -euo pipefail

echo "🔨 Building MCP-FRED Extension..."
echo

# Check for mcpb
if ! command -v mcpb &> /dev/null; then
    echo "❌ Error: mcpb not found. Install with:"
    echo "   npm install -g @anthropic-ai/mcpb"
    exit 1
fi

# Check and download uv binaries if needed
echo "🔍 Checking for bundled uv binaries..."
BIN_DIR="bin"
DOWNLOAD_NEEDED=false

# Define platforms and their download URLs
PLATFORMS=("darwin-arm64" "darwin-x64" "linux-x64" "win32-x64")
DARWIN_ARM64_URL="https://github.com/astral-sh/uv/releases/latest/download/uv-aarch64-apple-darwin.tar.gz"
DARWIN_X64_URL="https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-apple-darwin.tar.gz"
LINUX_X64_URL="https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-unknown-linux-gnu.tar.gz"
WIN32_X64_URL="https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-pc-windows-msvc.zip"

# Check if binaries exist
for platform in "${PLATFORMS[@]}"; do
    if [[ "$platform" == "win32-x64" ]]; then
        binary="$BIN_DIR/$platform/uv.exe"
    else
        binary="$BIN_DIR/$platform/uv"
    fi

    if [[ ! -f "$binary" ]]; then
        DOWNLOAD_NEEDED=true
        break
    fi
done

if [[ "$DOWNLOAD_NEEDED" == "true" ]]; then
    echo "📥 Downloading uv binaries for all platforms..."
    mkdir -p "$BIN_DIR"/{darwin-arm64,darwin-x64,linux-x64,win32-x64}

    # Download darwin-arm64
    echo "  ↓ Downloading darwin-arm64..."
    curl -sL "$DARWIN_ARM64_URL" -o "$BIN_DIR/darwin-arm64.tar.gz"
    tar -xzf "$BIN_DIR/darwin-arm64.tar.gz" -C "$BIN_DIR/darwin-arm64" --strip-components=1
    rm "$BIN_DIR/darwin-arm64.tar.gz"
    chmod +x "$BIN_DIR/darwin-arm64/uv"

    # Download darwin-x64
    echo "  ↓ Downloading darwin-x64..."
    curl -sL "$DARWIN_X64_URL" -o "$BIN_DIR/darwin-x64.tar.gz"
    tar -xzf "$BIN_DIR/darwin-x64.tar.gz" -C "$BIN_DIR/darwin-x64" --strip-components=1
    rm "$BIN_DIR/darwin-x64.tar.gz"
    chmod +x "$BIN_DIR/darwin-x64/uv"

    # Download linux-x64
    echo "  ↓ Downloading linux-x64..."
    curl -sL "$LINUX_X64_URL" -o "$BIN_DIR/linux-x64.tar.gz"
    tar -xzf "$BIN_DIR/linux-x64.tar.gz" -C "$BIN_DIR/linux-x64" --strip-components=1
    rm "$BIN_DIR/linux-x64.tar.gz"
    chmod +x "$BIN_DIR/linux-x64/uv"

    # Download win32-x64
    echo "  ↓ Downloading win32-x64..."
    curl -sL "$WIN32_X64_URL" -o "$BIN_DIR/win32-x64.zip"
    unzip -q "$BIN_DIR/win32-x64.zip" -d "$BIN_DIR/win32-x64"
    rm "$BIN_DIR/win32-x64.zip"

    # Make launcher executable
    chmod +x "$BIN_DIR/uv-launcher.sh" 2>/dev/null || true

    echo "✅ All uv binaries downloaded successfully"
else
    echo "✓ All uv binaries present"
fi
echo

# Validate manifest
echo "✓ Validating manifest.json..."
if ! mcpb validate manifest.json; then
    echo "❌ Manifest validation failed!"
    exit 1
fi
echo

# Clean previous build
if [ -f "mcp-fred.mcpb" ]; then
    echo "🗑️  Removing previous build..."
    rm mcp-fred.mcpb
fi
echo

# Pack the extension
echo "📦 Packing extension..."
if mcpb pack . mcp-fred.mcpb; then
    echo
    echo "✅ Extension built successfully!"
    echo
    echo "📦 Output: mcp-fred.mcpb"

    # Show file info
    if command -v mcpb &> /dev/null; then
        echo
        echo "📋 Extension Info:"
        mcpb info mcp-fred.mcpb
    fi
else
    echo "❌ Packing failed!"
    exit 1
fi

echo
echo "🚀 To install in Claude Desktop:"
echo "   Double-click mcp-fred.mcpb"
echo "   or use: open mcp-fred.mcpb"
