# Extension Update: Fixed Dependency Management

## What Changed

**Previous Version (v1):**
- Used system Python directly: `python -m mcp_fred`
- ❌ Failed with `ModuleNotFoundError: No module named 'tiktoken'`
- Required manual pip installation of dependencies

**Current Version (v2):**
- Uses `uv` for dependency management: `uv run --directory ${__dirname} python -m mcp_fred`
- ✅ Automatically installs and manages dependencies
- ✅ Creates isolated environment per extension
- ✅ Much smaller extension size (59.7 KB vs 50+ MB for bundled venv)

## Key Benefits of uv

1. **Automatic Dependency Resolution**: Reads `pyproject.toml` and installs all required packages
2. **Isolated Environments**: Each extension gets its own environment, no conflicts
3. **Fast**: uv is written in Rust, 10-100x faster than pip
4. **Small Extension Size**: Dependencies cached globally, not bundled in .mcpb file
5. **Zero Configuration**: Just works once uv is installed

## How It Works

### Manifest Configuration

```json
{
  "command": "uv",
  "args": [
    "run",                    // Run command with uv
    "--directory",           // Set working directory
    "${__dirname}",          // Extension install directory
    "python",                // Execute Python
    "-m",                    // Run as module
    "mcp_fred"              // Module name
  ]
}
```

### What uv Does

1. Reads `pyproject.toml` in `${__dirname}`
2. Creates isolated virtual environment (cached)
3. Installs dependencies listed in `dependencies = [...]`:
   - fastapi>=0.100.0,<1.0.0
   - httpx>=0.24.0,<1.0.0
   - pydantic>=2.0.0,<3.0.0
   - python-dotenv>=1.0.0
   - tiktoken>=0.5.0,<1.0.0
4. Runs `python -m mcp_fred` in that environment

## Installation Requirements

Users need:
1. **Python 3.11+**: `python --version`
2. **uv**: `brew install uv` (macOS) or `pip install uv` (Windows/Linux)

Check installations:
```bash
python --version   # Should be 3.11 or higher
uv --version       # Should show uv version
```

## Testing the Updated Extension

### Step 1: Verify Requirements

```bash
# Check Python
python --version
# Output: Python 3.11.x or higher

# Check uv
uv --version
# Output: uv x.x.x
```

### Step 2: Uninstall Old Extension

1. Open Claude Desktop
2. Go to Settings → Extensions
3. Find "FRED Economic Data"
4. Click "Uninstall" or "Remove"
5. Restart Claude Desktop

### Step 3: Install Updated Extension

```bash
# From the mcp-fred directory
open mcp-fred.mcpb
```

Or double-click the file in Finder.

### Step 4: Configure Extension

When prompted:
1. **FRED API Key**: Enter your key from fred.stlouisfed.org
2. **Storage Directory**: Default `~/fred-data` or choose custom
3. **Output Format**: Default `csv` or choose `json`

Click **Install**.

### Step 5: Test Extension

1. Restart Claude Desktop
2. Open new conversation
3. Test commands:

```
What FRED tools do you have?
```

Expected response: Claude lists 11 FRED tools.

```
Get information about FRED category 125
```

Expected response: Category information or job created for large dataset.

### Step 6: Verify Logs (if needed)

If issues occur, check logs at:
- **macOS**: `~/Library/Application Support/Claude/logs/`
- **Windows**: `%APPDATA%\Claude\logs\`

Look for:
- ✅ `Server started and connected successfully`
- ✅ Tool initialization messages
- ❌ `ModuleNotFoundError` (should NOT appear now)
- ❌ `uv command not found` (install uv if this appears)

## Troubleshooting

### "uv command not found"

**Solution:**
```bash
# Install uv
brew install uv  # macOS
pip install uv   # Windows/Linux

# Verify
uv --version

# Restart Claude Desktop
```

### Still Getting Dependency Errors

**Solution:**
```bash
# Test uv can run the server manually
cd /path/to/mcp-fred
uv run python -m mcp_fred

# Should start the MCP server (Ctrl+C to stop)
```

### Extension Size Comparison

**With bundled venv (not used):** 50-100 MB
- Includes entire Python environment
- All dependencies copied into .mcpb
- Slow to install and update

**With uv (current approach):** 59.7 KB
- Only source code in .mcpb
- Dependencies managed by uv
- Fast to install and update
- Shared cache across extensions

## Files Changed

### manifest.json
```diff
- "command": "python",
- "args": ["-m", "mcp_fred"],
+ "command": "uv",
+ "args": ["run", "--directory", "${__dirname}", "python", "-m", "mcp_fred"],
```

### EXTENSION.md
- Added Requirements section
- Added uv installation instructions
- Added troubleshooting for uv

### README.md
- Added uv requirement to Option 1

## Success Criteria

✅ Extension installs without errors
✅ No ModuleNotFoundError in logs
✅ All 11 tools available in Claude
✅ Can query FRED data successfully
✅ Files save to configured directory

## Next Steps

1. **Test Installation**: Follow Step-by-Step testing above
2. **Report Issues**: If problems occur, check logs and report
3. **Document Success**: Confirm all tools working
4. **Create Release**: Once validated, create GitHub release with new .mcpb

---

**Build Date**: 2025-11-06
**Extension Version**: 0.1.0 (with uv support)
**Extension Size**: 59.7 KB
**Status**: Ready for Testing
