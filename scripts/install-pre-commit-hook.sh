#!/usr/bin/env bash
# Install pre-commit hook for MCP-FRED development

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
HOOK_SOURCE="$SCRIPT_DIR/pre-commit-hook.sh"
HOOK_DEST="$REPO_ROOT/.git/hooks/pre-commit"

echo "🔧 Installing pre-commit hook..."
echo

# Check if .git directory exists
if [ ! -d "$REPO_ROOT/.git" ]; then
    echo "❌ Error: .git directory not found"
    echo "   Are you in a git repository?"
    exit 1
fi

# Check if hook source exists
if [ ! -f "$HOOK_SOURCE" ]; then
    echo "❌ Error: Hook source not found at $HOOK_SOURCE"
    exit 1
fi

# Backup existing hook if present
if [ -f "$HOOK_DEST" ]; then
    echo "📦 Backing up existing pre-commit hook..."
    mv "$HOOK_DEST" "$HOOK_DEST.backup.$(date +%s)"
    echo "   Backup saved"
fi

# Copy hook
echo "📋 Installing pre-commit hook..."
cp "$HOOK_SOURCE" "$HOOK_DEST"
chmod +x "$HOOK_DEST"

echo
echo "✅ Pre-commit hook installed successfully!"
echo
echo "The hook will run before each commit and check:"
echo "  • Code formatting (ruff format)"
echo "  • Linting (ruff check)"
echo "  • Tests (pytest)"
echo "  • Code coverage (80% threshold)"
echo
echo "To uninstall: rm $HOOK_DEST"
echo
