# Bundled UV Solution

## Overview

The MCP-FRED extension now bundles `uv` binaries directly within the extension package, eliminating the need for users to have `uv` installed in their system PATH. This solves compatibility issues across different platforms and installation methods.

## Problem Statement

Previously, the extension relied on `uv` being available in the system PATH. This caused issues because:

1. **Claude Desktop has a limited PATH** - It doesn't include common installation locations like:
   - `/opt/homebrew/bin` (macOS ARM - M1/M2/M3/M4)
   - `/usr/local/bin` (macOS Intel)
   - `~/.local/bin` (uv standalone installer)

2. **Cross-platform compatibility** - Different platforms and architectures install `uv` in different locations

3. **User experience** - Requiring users to manually install and configure `uv` in the PATH added friction

## Solution

The extension now includes:

### 1. Platform-Specific UV Binaries

Located in `bin/` directory:
- `bin/darwin-arm64/` - macOS ARM64 (M1/M2/M3/M4)
- `bin/darwin-x64/` - macOS Intel (x86_64)
- `bin/linux-x64/` - Linux x86_64
- `bin/win32-x64/` - Windows x86_64

### 2. Cross-Platform Launcher Scripts

**Unix/Linux/macOS**: `bin/uv-launcher.sh`
- Automatically detects OS and architecture
- Executes the appropriate bundled binary
- Handles errors gracefully

**Windows**: `bin/uv-launcher.cmd`
- Uses the bundled Windows binary
- Compatible with Windows command prompt and PowerShell

### 3. Automated Build Process

The `build-extension.sh` script now:
1. Checks if platform binaries exist
2. Downloads latest `uv` binaries from GitHub if missing
3. Packages everything into the `.mcpb` extension file

## Architecture

```
Extension Package (.mcpb)
├── bin/
│   ├── darwin-arm64/
│   │   ├── uv           (macOS ARM binary)
│   │   └── uvx
│   ├── darwin-x64/
│   │   ├── uv           (macOS Intel binary)
│   │   └── uvx
│   ├── linux-x64/
│   │   ├── uv           (Linux binary)
│   │   └── uvx
│   ├── win32-x64/
│   │   ├── uv.exe       (Windows binary)
│   │   ├── uvw.exe
│   │   └── uvx.exe
│   ├── uv-launcher.sh   (Unix launcher)
│   └── uv-launcher.cmd  (Windows launcher)
└── ...other extension files
```

## How It Works

1. **Extension Installation**: User installs the `.mcpb` extension which contains all platform binaries

2. **Runtime Execution**:
   - `manifest.json` specifies `command: "${__dirname}/bin/uv-launcher.sh"`
   - Launcher script detects platform and architecture
   - Launches the appropriate bundled `uv` binary
   - No system PATH required!

3. **Platform Detection**:
   ```bash
   OS="$(uname -s)"     # Darwin, Linux, MINGW64, etc.
   ARCH="$(uname -m)"   # arm64, x86_64, etc.
   ```

## Benefits

✅ **Zero System Dependencies** - No need to install `uv` separately
✅ **Cross-Platform** - Works on macOS (ARM & Intel), Linux, and Windows
✅ **Automatic Updates** - Build script always downloads latest `uv` release
✅ **Better UX** - Extension "just works" after installation
✅ **Version Control** - Binaries are in `.gitignore`, downloaded during build

## File Sizes

- Total extension package: ~78 MB
- Unpacked size: ~194 MB
- Individual platform binaries range from 17-57 MB

## Development Notes

### Building the Extension

```bash
./build-extension.sh
```

The script automatically:
1. Downloads missing platform binaries
2. Validates manifest
3. Packages everything into `.mcpb` file

### Version Control

Binaries are **not** committed to git:
- `.gitignore` excludes `bin/darwin-*/`, `bin/linux-*/`, `bin/win32-*/`
- Launcher scripts (`*.sh`, `*.cmd`) **are** committed
- Binaries are downloaded during the build process

### Updating UV Version

The build script always downloads the **latest** release from:
```
https://github.com/astral-sh/uv/releases/latest/download/
```

To use a specific version, modify the URLs in `build-extension.sh`:
```bash
DARWIN_ARM64_URL="https://github.com/astral-sh/uv/releases/download/0.9.9/uv-aarch64-apple-darwin.tar.gz"
```

## Testing

Test the launcher directly:
```bash
./bin/uv-launcher.sh --version
# Output: uv 0.9.9 (4fac4cb7e 2025-11-12)
```

Test with the extension:
1. Build: `./build-extension.sh`
2. Install: `open mcp-fred.mcpb`
3. Verify in Claude Desktop that the extension loads without errors

## Troubleshooting

### "uv binary not found" error

Check that binaries were downloaded:
```bash
ls -lh bin/*/uv*
```

If missing, run:
```bash
./build-extension.sh
```

### Permission denied

Ensure launcher is executable:
```bash
chmod +x bin/uv-launcher.sh
```

### Platform not detected

The launcher script logs errors to stderr. Check Claude Desktop logs for details.

## References

- [UV GitHub Repository](https://github.com/astral-sh/uv)
- [UV Standalone Installers](https://github.com/astral-sh/uv/releases)
- [Claude MCP Extension Documentation](https://docs.anthropic.com/claude/extensions)
