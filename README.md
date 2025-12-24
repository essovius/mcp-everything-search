# Everything MCP Server

[![PyPI version](https://badge.fury.io/py/mcp-everything-search.svg)](https://badge.fury.io/py/mcp-everything-search)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An MCP (Model Context Protocol) server that integrates [Everything](https://www.voidtools.com/) file search with Claude Desktop. Search your entire Windows filesystem instantly from Claude.

## Features

- ⚡ **Instant search** - Leverages Everything's lightning-fast file indexing
- 🔍 **Multiple search modes** - Basic, filtered, regex, type-based, attribute-based
- 📁 **Folder operations** - Search within specific paths, find empty folders
- 📊 **Statistics** - Get file counts and total sizes without listing files
- 🕐 **Recent files** - Find recently modified files
- 📋 **Duplicate finder** - Locate files with the same name
- 💾 **Export** - Save results to txt, csv, json, and more

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

### Basic Search
| Tool | Description |
|------|-------------|
| `search_files` | Basic file search with wildcards (`*`, `?`), sorting options |
| `search_with_filters` | Search with extension, size, path filters, files/folders only |
| `search_regex` | Search using regular expressions |

### Specialized Search
| Tool | Description |
|------|-------------|
| `search_by_type` | Search by category: audio, video, image, document, executable, compressed, code |
| `search_folders` | Find only directories |
| `search_recent_files` | Find recently modified files |
| `search_duplicates` | Find files with the same name |
| `search_by_attributes` | Filter by hidden, system, read-only, compressed, encrypted |
| `search_empty_folders` | Find empty directories |
| `search_large_files` | Find files over a specified size |

### Utilities
| Tool | Description |
|------|-------------|
| `search_with_details` | Search with detailed output (size, dates) |
| `get_result_count` | Get count of matches without listing (fast) |
| `get_total_size` | Get total size of all matching files |
| `open_file_location` | Open containing folder in Explorer |
| `get_file_info` | Get file size, dates, and details |
| `export_search_results` | Export to txt, csv, json, m3u, m3u8, tsv, efu |

## Example Queries

Ask Claude things like:

- "Find all Python files in D:\Projects"
- "Search for PDF files larger than 10mb"
- "Find images modified in the last 3 days"
- "Look for duplicate files named config.json"
- "Find all video files in my Downloads folder"
- "Search for files matching regex `test_.*\.py$`"
- "Find empty folders in D:\Archive"
- "What's the total size of all MP3 files?"
- "How many JavaScript files are in this project?"
- "Find hidden files in C:\Windows"
- "Export all log files to a CSV"

## Sort Options

Many tools support `sort_by` parameter:
- `name`, `path`, `size`, `extension`
- `date-modified`, `date-created`, `date-accessed`
- Add `-descending` for reverse order (e.g., `size-descending`)

## Development

```bash
# Clone the repo
git clone https://github.com/essovius/mcp-everything-search.git
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
