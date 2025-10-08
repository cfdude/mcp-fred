# MCP-FRED Development Guide

**Complete setup guide for developers and AI agents working on MCP-FRED**

---

## Quick Links

- [CONTEXT.md](CONTEXT.md) - Project overview and current status
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture and design
- [API_MAPPING.md](API_MAPPING.md) - FRED API to tool mapping
- [TODO.md](TODO.md) - Development tasks
- [DEPENDENCIES.md](DEPENDENCIES.md) - Why each dependency was chosen

---

## Prerequisites

### Required Software

- **Python 3.11 or higher** (required for latest type hints and performance)
- **Git** with SSH commit signing configured
- **Text editor or IDE** (VS Code, PyCharm, etc.)

### Optional but Recommended

- **pyenv** for Python version management
- **virtual environment** tool (venv, virtualenv, or conda)
- **FRED API key** for integration testing (get from https://fred.stlouisfed.org/docs/api/api_key.html)

---

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/cfdude/mcp-fred.git
cd mcp-fred
```

### 2. Switch to Development Branch

```bash
git checkout dev
```

**Branch Strategy:**
- `main` - Production-ready releases only
- `dev` - Active development (work here)

### 3. Set Up Python Virtual Environment

#### Using venv (recommended):

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Verify Python version
python --version  # Should show Python 3.11+
```

#### Using pyenv + virtualenv:

```bash
# Install Python 3.11 if needed
pyenv install 3.11.9

# Create virtual environment
pyenv virtualenv 3.11.9 mcp-fred

# Activate
pyenv activate mcp-fred
```

### 4. Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# Verify installation
python -c "import fastapi, httpx, pydantic; print('Dependencies installed successfully')"
```

**See [DEPENDENCIES.md](DEPENDENCIES.md) for detailed explanation of each dependency.**

### 5. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your settings
# Required:
FRED_API_KEY=your_api_key_here

# Optional (defaults provided):
FRED_STORAGE_DIR=./fred-data
FRED_PROJECT_NAME=default
FRED_OUTPUT_FORMAT=csv
```

**Getting a FRED API Key:**
1. Visit https://fred.stlouisfed.org/
2. Create a free account
3. Go to https://fred.stlouisfed.org/docs/api/api_key.html
4. Request an API key (instant approval)

---

## Development Workflow

### Project Structure

After Phase 1 setup, the project structure will be:

```
mcp-fred/
├── src/
│   └── mcp_fred/           # Main package
│       ├── __init__.py
│       ├── server.py       # MCP server entry point
│       ├── config.py       # Configuration management
│       ├── api/            # FRED API client
│       ├── utils/          # Utilities (token estimation, file handling)
│       ├── tools/          # MCP tools (12 tools)
│       └── transports/     # STDIO and HTTP transports
├── tests/                  # Test suite
├── docs/                   # Documentation (you are here)
├── .env                    # Your local configuration (not committed)
├── .env.example            # Example configuration (committed)
├── pyproject.toml          # Ruff configuration
├── requirements.txt        # Python dependencies
└── pytest.ini              # Pytest configuration
```

### Running the Development Server

**STDIO Mode (Local - for Claude Desktop):**

```bash
# Run server via Python module
python -m mcp_fred

# Server will communicate via stdin/stdout
# Used by MCP clients like Claude Desktop
```

**HTTP Mode (Remote):**

```bash
# Run server with HTTP transport
python -m mcp_fred --transport http --host 0.0.0.0 --port 8000

# Access at http://localhost:8000/mcp
```

### Code Quality Tools

#### Ruff (Linting and Formatting)

```bash
# Check for linting issues
ruff check .

# Check specific file
ruff check src/mcp_fred/tools/series.py

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .

# Format specific file
ruff format src/mcp_fred/tools/series.py
```

**Ruff Configuration:** See `pyproject.toml`

#### Type Checking (Optional)

```bash
# Install mypy if desired
pip install mypy

# Run type checking
mypy src/mcp_fred/

# Type checking is optional but recommended
```

### Testing

#### Run All Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mcp_fred --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
```

#### Run Specific Tests

```bash
# Run tests for specific module
pytest tests/test_tools/test_series.py

# Run specific test function
pytest tests/test_tools/test_series.py::test_get_observations

# Run tests matching pattern
pytest -k "series"

# Run with verbose output
pytest -v

# Run with print statements visible
pytest -s
```

#### Testing Philosophy

- **Target**: 80% code coverage minimum
- **Focus**: Unit tests (primary), integration tests (as needed)
- **Mocking**: Mock FRED API responses (no real API calls in tests)
- **Fixtures**: Reusable test data in `tests/fixtures/`

**See testing sections in [TODO.md](TODO.md) → Phase 5 for detailed testing tasks.**

---

## Git Workflow

### Commit Message Convention

We use **conventional commits** for clear history:

```bash
# Format: <type>(<scope>): <description>

# Types:
feat(tools): add fred_series tool with observation support
fix(api): handle rate limit 429 responses correctly
docs(guide): add development workflow section
style(format): apply ruff formatting to all files
refactor(utils): simplify token estimation logic
test(series): add unit tests for large dataset handling
chore(deps): update tiktoken to v0.5.2
perf(worker): optimize background job processing
```

**Common types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code formatting (no logic change)
- `refactor`: Code restructuring (no behavior change)
- `test`: Adding or updating tests
- `chore`: Maintenance (deps, config, etc.)
- `perf`: Performance improvements

### Branch Strategy

```bash
# Always work on dev branch
git checkout dev

# Pull latest changes before starting work
git pull origin dev

# Make changes, then stage
git add src/mcp_fred/tools/series.py

# Commit with conventional message
git commit -m "feat(tools): implement fred_series tool"

# Push to remote
git push origin dev
```

### Before Committing

```bash
# 1. Run linter
ruff check .

# 2. Run formatter
ruff format .

# 3. Run tests
pytest

# 4. If all pass, commit
git add .
git commit -m "feat(scope): your message"
git push origin dev
```

---

## Common Development Tasks

### Adding a New MCP Tool

1. **Review documentation:**
   - Read [API_MAPPING.md](API_MAPPING.md) for endpoint mapping
   - Check [ARCHITECTURE.md → MCP Tool Design](ARCHITECTURE.md#mcp-tool-design)

2. **Create tool file:**
   ```bash
   # Example: creating fred_category tool
   touch src/mcp_fred/tools/category.py
   ```

3. **Implement tool pattern:**
   - Operation-based routing
   - Pydantic parameter validation
   - Output handling (auto/screen/file)
   - Error handling
   - Docstring with examples

4. **Register tool in server:**
   - Add to `src/mcp_fred/server.py`

5. **Write tests:**
   - Unit tests in `tests/test_tools/test_category.py`
   - Mock FRED API responses

6. **Run quality checks:**
   ```bash
   ruff check . && ruff format . && pytest
   ```

### Adding a New API Endpoint

1. **Review FRED API docs:**
   - Check [FRED_API_REFERENCE.md](FRED_API_REFERENCE.md)
   - Verify parameters and response format

2. **Create endpoint method:**
   ```bash
   # Edit appropriate file
   vim src/mcp_fred/api/endpoints/category.py
   ```

3. **Define Pydantic response model:**
   ```bash
   # Add to models
   vim src/mcp_fred/api/models/responses.py
   ```

4. **Write tests:**
   - Test with mocked responses
   - Test error handling

### Adding a New Utility

1. **Create utility module:**
   ```bash
   touch src/mcp_fred/utils/your_utility.py
   ```

2. **Implement with clear interface:**
   - Type hints for all functions
   - Comprehensive docstrings
   - Error handling

3. **Write unit tests:**
   ```bash
   touch tests/test_utils/test_your_utility.py
   ```

---

## Debugging

### Enable Debug Logging

```python
# Add to your code temporarily
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Run in Debug Mode

```bash
# Run with Python debugger
python -m pdb -m mcp_fred

# Or use your IDE's debugger
# VS Code: Set breakpoints and press F5
# PyCharm: Set breakpoints and Run > Debug
```

### Common Issues

#### Import Errors

```bash
# Ensure you're in virtual environment
which python  # Should show venv path

# Reinstall dependencies
pip install -r requirements.txt

# Check package is installed
pip show mcp-fred
```

#### FRED API Key Issues

```bash
# Verify .env file exists
cat .env | grep FRED_API_KEY

# Test API key directly
curl "https://api.stlouisfed.org/fred/series?series_id=GNPCA&api_key=YOUR_KEY&file_type=json"
```

#### File Permission Issues

```bash
# Check storage directory permissions
ls -la ./fred-data

# Create directory if missing
mkdir -p fred-data

# Set permissions
chmod 755 fred-data
```

---

## IDE Setup

### VS Code

**Recommended Extensions:**
- Python (Microsoft)
- Pylance (Microsoft)
- Ruff (Astral)

**Settings (`.vscode/settings.json`):**

```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": false,
  "ruff.enable": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": true,
    "source.organizeImports": true
  },
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff"
  }
}
```

### PyCharm

1. **Set Python Interpreter:**
   - File > Settings > Project > Python Interpreter
   - Select `venv/bin/python`

2. **Configure Ruff:**
   - Install Ruff plugin
   - Enable in Settings > Tools > Ruff

3. **Run Configurations:**
   - Create run config for `python -m mcp_fred`
   - Create test config for pytest

---

## Testing with MCP Clients

### Claude Desktop Configuration

**Config File Location:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**Configuration:**

```json
{
  "mcpServers": {
    "fred": {
      "command": "python",
      "args": ["-m", "mcp_fred"],
      "env": {
        "FRED_API_KEY": "your_api_key_here",
        "FRED_STORAGE_DIR": "/Users/username/Documents/fred-data"
      }
    }
  }
}
```

**Using Development Version:**

```json
{
  "mcpServers": {
    "fred-dev": {
      "command": "/path/to/mcp-fred/venv/bin/python",
      "args": ["-m", "mcp_fred"],
      "env": {
        "FRED_API_KEY": "your_api_key_here",
        "FRED_STORAGE_DIR": "/Users/username/Documents/fred-data-dev"
      }
    }
  }
}
```

### Testing HTTP Transport

```bash
# Start server
python -m mcp_fred --transport http --port 8000

# In another terminal, test with curl
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"list_tools","id":1}'
```

---

## Documentation Updates

### When to Update Documentation

**Always update documentation when:**
- Adding new features or tools
- Changing architecture or design decisions
- Modifying configuration options
- Adding dependencies
- Changing workflows or processes

**Which files to update:**
- `CHANGELOG.md` - All changes (follow semantic versioning)
- `ARCHITECTURE.md` - Design decisions, patterns
- `API_MAPPING.md` - New tools or endpoints
- `TODO.md` - Move completed tasks to PROGRESS.md
- `PROGRESS.md` - Completed phases and decisions

### Documentation Standards

Follow the standards in [TODO.md → Notes → Documentation Quality Standards](TODO.md#documentation-quality-standards):

- Accurate, complete, clear
- Consistent terminology
- Cross-referenced
- Navigable
- Self-contained (no external tools)

---

## Getting Help

### Documentation Resources

1. **Project Documentation:**
   - [CONTEXT.md](CONTEXT.md) - Start here
   - [ARCHITECTURE.md](ARCHITECTURE.md) - System design
   - [API_MAPPING.md](API_MAPPING.md) - Endpoint mappings
   - [DEPENDENCIES.md](DEPENDENCIES.md) - Dependency rationale

2. **External Documentation:**
   - [FRED API Docs](https://fred.stlouisfed.org/docs/api/fred/)
   - [MCP Specification](https://modelcontextprotocol.io/)
   - [FastAPI Docs](https://fastapi.tiangolo.com/)
   - [Ruff Docs](https://docs.astral.sh/ruff/)

### Issue Reporting

For bugs or issues with the project:
- Create an issue at https://github.com/cfdude/mcp-fred/issues
- Include error messages, steps to reproduce, environment info

---

## Development Phases

We're following an 8-phase development plan. See [TODO.md](TODO.md) for complete task lists.

**Current Phase:** Phase 1 - Project Setup & Infrastructure

**Completed Phases:**
- Phase 0.0 - 0.5: Planning, architecture, documentation

**Upcoming Phases:**
- Phase 2: Core API Client
- Phase 3: Large Data Handling Utilities
- Phase 4: MCP Tool Layer
- Phase 4: Transport Layer
- Phase 5: Testing
- Phase 6: Documentation & Polish
- Phase 7: Deployment & Release
- Phase 8: Future Enhancements

---

## Development Philosophy

### Code Quality

- **Type Hints**: Use everywhere possible
- **Docstrings**: Required for all public functions/classes
- **Error Handling**: Graceful handling with clear messages
- **Testing**: 80% coverage minimum, unit tests primary
- **Formatting**: Ruff auto-format before commits

### Architecture Principles

- **Separation of Concerns**: API client ≠ MCP tools ≠ utilities
- **Type Safety**: Pydantic for validation
- **User-Configurable**: Storage, formats, token limits
- **Conservative**: Err on side of file output vs context overflow
- **Async-First**: Background jobs for large datasets

### User Experience

- **Clear Messages**: Explain what's happening
- **Predictable**: Consistent response formats
- **Safe**: Path validation, no directory traversal
- **Organized**: Project-based storage
- **Fast**: Token estimation before large operations

---

**Last Updated:** 2025-10-08
**Document Version:** 1.0
