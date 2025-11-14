#!/usr/bin/env node
/**
 * Cross-platform uv launcher for MCP-FRED extension
 * Automatically detects platform and architecture to use the correct bundled uv binary
 */

const { spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// Get the directory where this script is located
const binDir = __dirname;

// Detect platform and architecture
const platform = process.platform;
const arch = process.arch;

let uvBinary;

if (platform === 'darwin') {
  // macOS
  if (arch === 'arm64') {
    uvBinary = path.join(binDir, 'darwin-arm64', 'uv');
  } else if (arch === 'x64') {
    uvBinary = path.join(binDir, 'darwin-x64', 'uv');
  } else {
    console.error(`Error: Unsupported macOS architecture: ${arch}`);
    process.exit(1);
  }
} else if (platform === 'linux') {
  // Linux
  if (arch === 'x64') {
    uvBinary = path.join(binDir, 'linux-x64', 'uv');
  } else {
    console.error(`Error: Unsupported Linux architecture: ${arch}`);
    process.exit(1);
  }
} else if (platform === 'win32') {
  // Windows
  uvBinary = path.join(binDir, 'win32-x64', 'uv.exe');
} else {
  console.error(`Error: Unsupported operating system: ${platform}`);
  process.exit(1);
}

// Verify the binary exists
if (!fs.existsSync(uvBinary)) {
  console.error(`Error: uv binary not found at: ${uvBinary}`);
  process.exit(1);
}

// Make it executable on Unix platforms
if (platform !== 'win32') {
  try {
    fs.chmodSync(uvBinary, 0o755);
  } catch (err) {
    // Ignore permission errors
  }
}

// Execute uv with all passed arguments
const result = spawnSync(uvBinary, process.argv.slice(2), {
  stdio: 'inherit',
  shell: false
});

process.exit(result.status || 0);
