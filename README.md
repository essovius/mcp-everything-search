# Everything MCP Server

[![PyPI version](https://badge.fury.io/py/mcp-everything-search.svg)](https://badge.fury.io/py/mcp-everything-search)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An MCP (Model Context Protocol) server that integrates [Everything](https://www.voidtools.com/) file search with Claude Desktop. Search your entire Windows filesystem instantly from Claude.

![Demo](https://github.com/yourusername/mcp-everything-search/raw/main/demo.gif)

## Features

- ⚡ **Instant search** - Leverages Everything's lightning-fast file indexing
- 🔍 **Multiple search modes** - Basic search, filtered search, type-based search
- 📁 **File operations** - Get file info, open file locations
- 🕐 **Recent files** - Find recently modified files
- 📋 **Duplicate finder** - Locate files with the same name

## Prerequisites

1. **Windows** - Everything only runs on Windows
2. **[Everything](https://www.voidtools.com/)** must be installed and running
3. **es.exe** (Everything command-line) installed
   - Install from: https://github.com/voidtools/es
   - Must be in `%LOCALAPPDATA%\Microsoft\WindowsApps`

## Installation

### Using uvx (recommended)

```bash
uvx mcp-everything-search
```

### Using pip

```bash
pip install mcp-everything-search
```

## Configuration

Add this to your Claude Desktop config file:

**Location:** `%APPDATA%\Claude\claude_desktop_config.json`

### Using uvx

```json
{
  "mcpServers": {
    "everything-search": {
      "command": "uvx",
      "args": ["mcp-everything-search"]
    }
  }
}
```

### Using pip

```json
{
  "mcpServers": {
    "everything-search": {
      "command": "python",
      "args": ["-m", "mcp_everything_search"]
    }
  }
}
```

### Everything 1.5 Alpha Users

If you're using Everything 1.5 alpha, add the `EVERYTHING_INSTANCE` environment variable:

```json
{
  "mcpServers": {
    "everything-search": {
      "command": "uvx",
      "args": ["mcp-everything-search"],
      "env": {
        "EVERYTHING_INSTANCE": "1.5a"
      }
    }
  }
}
```

Then **restart Claude Desktop**.

## Available Tools

| Tool | Description |
|------|-------------|
| `search_files` | Basic file search with wildcards (`*`, `?`) |
| `search_with_filters` | Search with extension, size, and path filters |
| `search_by_type` | Search by category (audio, video, image, document, etc.) |
| `search_recent_files` | Find recently modified files |
| `search_duplicates` | Find files with the same name |
| `open_file_location` | Open containing folder in Explorer |
| `get_file_info` | Get file size, dates, and details |

## Example Queries

Ask Claude things like:

- "Find all Python files containing 'config'"
- "Search for PDF files larger than 10mb"
- "Find images modified in the last 3 days"
- "Look for duplicate files named config.json"
- "Find all video files in my Downloads folder"
- "Get info about C:\Users\Me\document.pdf"

## Development

```bash
# Clone the repo
git clone https://github.com/yourusername/mcp-everything-search.git
cd mcp-everything-search

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install in development mode
pip install -e .

# Run the server
python -m mcp_everything_search
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- [Everything](https://www.voidtools.com/) by voidtools
- [Model Context Protocol](https://modelcontextprotocol.io/) by Anthropic
