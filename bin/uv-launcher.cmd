@echo off
REM Cross-platform uv launcher for MCP-FRED extension (Windows)
REM Automatically uses the bundled Windows uv binary

setlocal enabledelayedexpansion

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"

REM Set the path to the Windows uv binary
set "UV_BIN=%SCRIPT_DIR%win32-x64\uv.exe"

REM Verify the binary exists
if not exist "%UV_BIN%" (
    echo Error: uv binary not found at: %UV_BIN% >&2
    exit /b 1
)

REM Execute uv with all passed arguments
"%UV_BIN%" %*
