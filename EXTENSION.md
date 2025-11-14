# MCP-FRED Claude Desktop Extension

**One-click installation for Claude Desktop**

## Overview

The MCP-FRED extension provides a streamlined way to install and configure the FRED economic data MCP server in Claude Desktop. Instead of manually editing configuration files and setting up Python environments, you can install the extension with a single click.

## Features

- **One-Click Installation**: Double-click the .mcpb file to install
- **Automatic Configuration**: Claude Desktop handles all setup
- **Secure API Key Storage**: Your FRED API key is encrypted using OS-level secure storage (Keychain on macOS, Credential Manager on Windows)
- **Easy Updates**: Install new versions the same way

## Requirements

Before installing the extension, you need:

1. **Python 3.11+** installed on your system
2. **uv** (Python package manager) - Install with:
   ```bash
   # macOS/Linux
   brew install uv

   # Windows
   pip install uv

   # Or using pipx
   pipx install uv
   ```

> **Why uv?** The extension uses `uv` to manage Python dependencies automatically. This keeps the extension small and ensures consistent dependency resolution. `uv` is much faster than pip and handles isolated environments seamlessly.

## Installation

### Step 1: Get a FRED API Key

If you don't have a FRED API key yet:

1. Visit [fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html)
2. Sign up for a free account
3. Request an API key (instant approval)
4. Save your API key - you'll need it in Step 3

### Step 2: Download the Extension

Download the latest `mcp-fred.mcpb` file from:
- [GitHub Releases](https://github.com/cfdude/mcp-fred/releases)
- Or build it yourself (see Building section below)

### Step 3: Install in Claude Desktop

**macOS:**
```bash
open mcp-fred.mcpb
```

**Windows:**
Double-click `mcp-fred.mcpb`

**Linux:**
```bash
xdg-open mcp-fred.mcpb
```

Claude Desktop will launch and prompt you to configure the extension.

### Step 4: Configure Settings

When prompted, enter:

1. **FRED API Key** (required):
   - Your FRED API key from Step 1
   - This is stored securely in your system's keychain

2. **Storage Directory** (optional):
   - Default: `~/fred-data`
   - Where FRED data files will be saved
   - Choose a location that's easy to access

3. **Output Format** (optional):
   - Default: `csv`
   - Options: `csv` or `json`
   - Data file format preference

Click **Install** and you're done!

### Step 5: Verify Installation

1. Restart Claude Desktop
2. Open a new conversation
3. Try asking: "What economic data tools do you have access to?"

Claude should respond with information about the FRED tools.

## Using the Extension

Once installed, you can ask Claude to:

### Get Economic Data
> "Get the latest GDP data from FRED"

### Search for Series
> "Search FRED for unemployment rate series"

### Create Projects
> "Create a new FRED project called 'economy-2024'"

### Large Datasets
> "Get all CPI observations since 1950 and save to my inflation-study project"

For large datasets, Claude will automatically create background jobs and save data to files.

## Configuration Options

After installation, you can modify settings in Claude Desktop:

**macOS:** Settings → Extensions → FRED Economic Data
**Windows:** Settings → Extensions → FRED Economic Data

Available settings:
- **FRED API Key**: Your API key (sensitive - encrypted)
- **Storage Directory**: Where data files are saved
- **Output Format**: csv or json

## Uninstallation

To remove the extension:

**macOS:** Settings → Extensions → FRED Economic Data → Remove
**Windows:** Settings → Extensions → FRED Economic Data → Uninstall

This removes the extension but preserves your data files.

## Available Tools

The extension provides 11 MCP tools:

### Data Retrieval
- `fred_category` - Category information and hierarchies
- `fred_release` - Economic data releases
- `fred_series` - Economic time series data
- `fred_source` - Data sources
- `fred_tag` - Tag-based search and filtering
- `fred_maps` - GeoFRED geographic data

### Project Management
- `fred_project_create` - Create project workspaces
- `fred_project_list` - List all projects

### Job Management
- `fred_job_status` - Check background job status
- `fred_job_list` - List recent jobs
- `fred_job_cancel` - Cancel running jobs

## Building from Source

If you want to build the extension yourself:

### Prerequisites
- Python 3.11+
- Node.js and npm
- `@anthropic-ai/mcpb` CLI tool

### Build Steps

```bash
# Clone the repository
git clone https://github.com/cfdude/mcp-fred.git
cd mcp-fred

# Install mcpb CLI globally
npm install -g @anthropic-ai/mcpb

# Build the extension
./build-extension.sh
```

This creates `mcp-fred.mcpb` which you can install following Step 3 above.

### Manual Packaging

```bash
# Validate manifest
mcpb validate manifest.json

# Pack extension
mcpb pack . mcp-fred.mcpb

# View extension info
mcpb info mcp-fred.mcpb
```

## Troubleshooting

### Extension Won't Install

**Problem:** Claude Desktop doesn't recognize the .mcpb file

**Solution:**
- Ensure you're using Claude Desktop version 1.0.0 or higher
- Try right-clicking the file → Open With → Claude

### API Key Error

**Problem:** "Invalid API key" error when using FRED tools

**Solution:**
- Verify your API key at [fred.stlouisfed.org](https://fred.stlouisfed.org)
- Go to Settings → Extensions → FRED Economic Data
- Re-enter your API key
- Restart Claude Desktop

### Python Not Found

**Problem:** "Python command not found" error

**Solution:**
- Ensure Python 3.11+ is installed: `python --version`
- macOS: `brew install python@3.11`
- Windows: Download from [python.org](https://www.python.org)
- Linux: `sudo apt install python3.11`

### uv Not Found

**Problem:** "uv command not found" or dependency errors

**Solution:**
- Install uv: `brew install uv` (macOS) or `pip install uv`
- Verify installation: `uv --version`
- Ensure uv is in your PATH
- Restart Claude Desktop after installing uv

### Data Files Not Saving

**Problem:** Can't find saved data files

**Solution:**
- Check your configured storage directory in Settings → Extensions
- Default location: `~/fred-data`
- Verify directory exists and is writable
- Check Claude Desktop logs for permission errors

## Technical Details

### Extension Structure

```
mcp-fred.mcpb (zip archive)
├── manifest.json           # Extension metadata and configuration
├── requirements.txt        # Python dependencies
├── src/                    # Source code
│   └── mcp_fred/
│       ├── __init__.py
│       ├── __main__.py
│       ├── config.py
│       ├── server.py
│       ├── api/            # FRED API client
│       ├── tools/          # MCP tool implementations
│       ├── utils/          # Utilities
│       └── transports/     # MCP transports
└── pyproject.toml          # Project metadata
```

### Security

- **API Key Storage**: Encrypted using OS-level secure storage
- **File Access**: Limited to configured storage directory
- **No Network Access**: Extension only communicates with FRED API
- **Open Source**: All code is auditable on GitHub

### Compatibility

- **Platforms**: macOS, Windows, Linux
- **Claude Desktop**: ≥1.0.0
- **Python**: ≥3.11
- **uv**: Latest version (dependency manager)

## Support

- **Issues**: [GitHub Issues](https://github.com/cfdude/mcp-fred/issues)
- **Documentation**: [README.md](README.md)
- **FRED API**: [fred.stlouisfed.org/docs/api](https://fred.stlouisfed.org/docs/api/fred/)

## License

MIT License - see [LICENSE](LICENSE) file for details

---

**Version**: 0.1.0
**Last Updated**: 2025-11-06
