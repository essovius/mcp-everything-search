"""
Everything MCP Server
An MCP server that provides file search capabilities using Everything (voidtools)
"""

import subprocess
import os
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("everything-search")

# Path to es.exe
ES_PATH = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WindowsApps\es.exe")

# Optional: Set instance name for Everything beta (e.g., "1.5a")
# Leave empty for standard Everything installation
ES_INSTANCE = os.environ.get("EVERYTHING_INSTANCE", "")


def run_es_command(args: list[str]) -> tuple[bool, str]:
    """Run es.exe with given arguments and return output."""
    try:
        cmd = [ES_PATH]
        if ES_INSTANCE:
            cmd.extend(["-instance", ES_INSTANCE])
        cmd.extend(args)
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            encoding='utf-8',
            errors='replace'
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, result.stderr.strip() or "No results found"
    except subprocess.TimeoutExpired:
        return False, "Search timed out"
    except FileNotFoundError:
        return False, f"es.exe not found at {ES_PATH}"
    except Exception as e:
        return False, str(e)


@mcp.tool()
def search_files(
    query: str,
    max_results: int = 50,
    match_case: bool = False,
    match_whole_word: bool = False,
    match_path: bool = False
) -> str:
    """
    Search for files and folders using Everything.
    
    Args:
        query: Search query (supports wildcards * and ?)
        max_results: Maximum number of results to return (default 50)
        match_case: Enable case-sensitive search
        match_whole_word: Match whole words only
        match_path: Search in full path instead of filename only
    
    Returns:
        List of matching file paths
    """
    args = ["-n", str(max_results)]
    
    if match_case:
        args.append("-case")
    if match_whole_word:
        args.append("-whole-word")
    if match_path:
        args.append("-match-path")
    
    args.append(query)
    
    success, output = run_es_command(args)
    
    if success:
        files = output.split('\n') if output else []
        files = [f for f in files if f.strip()]
        return f"Found {len(files)} results:\n" + "\n".join(files)
    else:
        return f"Search error: {output}"


@mcp.tool()
def search_with_filters(
    query: str = "",
    extension: str = "",
    folder_path: str = "",
    min_size: str = "",
    max_size: str = "",
    max_results: int = 50
) -> str:
    """
    Search files with advanced filters.
    
    Args:
        query: Search query (optional if using other filters)
        extension: File extension filter (e.g., "py", "txt", "pdf")
        folder_path: Limit search to specific folder path
        min_size: Minimum file size (e.g., "1mb", "500kb", "1gb")
        max_size: Maximum file size (e.g., "10mb", "1gb")
        max_results: Maximum number of results (default 50)
    
    Returns:
        List of matching file paths
    """
    search_parts = []
    
    if query:
        search_parts.append(query)
    if extension:
        ext = extension.lstrip('.')
        search_parts.append(f"ext:{ext}")
    if folder_path:
        search_parts.append(f'"{folder_path}"')
    if min_size:
        search_parts.append(f"size:>={min_size}")
    if max_size:
        search_parts.append(f"size:<={max_size}")
    
    if not search_parts:
        return "Error: Please provide at least one search parameter"
    
    full_query = " ".join(search_parts)
    args = ["-n", str(max_results), full_query]
    
    success, output = run_es_command(args)
    
    if success:
        files = output.split('\n') if output else []
        files = [f for f in files if f.strip()]
        return f"Found {len(files)} results for '{full_query}':\n" + "\n".join(files)
    else:
        return f"Search error: {output}"


@mcp.tool()
def search_by_type(
    file_type: str,
    query: str = "",
    max_results: int = 50
) -> str:
    """
    Search for specific file types.
    
    Args:
        file_type: Type of files to search. Options:
            - "audio" (mp3, wav, flac, etc.)
            - "video" (mp4, mkv, avi, etc.)
            - "image" (jpg, png, gif, etc.)
            - "document" (doc, pdf, txt, etc.)
            - "executable" (exe, msi, bat, etc.)
            - "compressed" (zip, rar, 7z, etc.)
        query: Additional search query (optional)
        max_results: Maximum number of results (default 50)
    
    Returns:
        List of matching file paths
    """
    type_filters = {
        "audio": "ext:mp3;wav;flac;aac;ogg;wma;m4a",
        "video": "ext:mp4;mkv;avi;mov;wmv;flv;webm",
        "image": "ext:jpg;jpeg;png;gif;bmp;webp;svg;ico",
        "document": "ext:doc;docx;pdf;txt;rtf;odt;xls;xlsx;ppt;pptx",
        "executable": "ext:exe;msi;bat;cmd;ps1;sh",
        "compressed": "ext:zip;rar;7z;tar;gz;bz2"
    }
    
    if file_type.lower() not in type_filters:
        return f"Unknown file type '{file_type}'. Available: {', '.join(type_filters.keys())}"
    
    search_query = type_filters[file_type.lower()]
    if query:
        search_query = f"{query} {search_query}"
    
    args = ["-n", str(max_results), search_query]
    success, output = run_es_command(args)
    
    if success:
        files = output.split('\n') if output else []
        files = [f for f in files if f.strip()]
        return f"Found {len(files)} {file_type} files:\n" + "\n".join(files)
    else:
        return f"Search error: {output}"


@mcp.tool()
def search_recent_files(
    days: int = 7,
    query: str = "",
    max_results: int = 50
) -> str:
    """
    Search for recently modified files.
    
    Args:
        days: Files modified within this many days (default 7)
        query: Additional search query (optional)
        max_results: Maximum number of results (default 50)
    
    Returns:
        List of recently modified files
    """
    search_query = f"dm:last{days}days"
    if query:
        search_query = f"{query} {search_query}"
    
    args = ["-n", str(max_results), "-sort", "dm", search_query]
    success, output = run_es_command(args)
    
    if success:
        files = output.split('\n') if output else []
        files = [f for f in files if f.strip()]
        return f"Found {len(files)} files modified in last {days} days:\n" + "\n".join(files)
    else:
        return f"Search error: {output}"


@mcp.tool()
def search_duplicates(
    filename: str,
    max_results: int = 50
) -> str:
    """
    Find files with the same name (potential duplicates).
    
    Args:
        filename: Exact filename to search for
        max_results: Maximum number of results (default 50)
    
    Returns:
        List of files with matching names
    """
    args = ["-n", str(max_results), "-whole-word", filename]
    success, output = run_es_command(args)
    
    if success:
        files = output.split('\n') if output else []
        files = [f for f in files if f.strip()]
        if len(files) > 1:
            return f"Found {len(files)} files named '{filename}':\n" + "\n".join(files)
        elif len(files) == 1:
            return f"Only one file found named '{filename}':\n{files[0]}"
        else:
            return f"No files found named '{filename}'"
    else:
        return f"Search error: {output}"


@mcp.tool()
def open_file_location(file_path: str) -> str:
    """
    Open the folder containing a file in Windows Explorer.
    
    Args:
        file_path: Full path to the file
    
    Returns:
        Success or error message
    """
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
    
    try:
        subprocess.run(["explorer", "/select,", file_path], check=True)
        return f"Opened folder containing: {file_path}"
    except Exception as e:
        return f"Error opening location: {e}"


@mcp.tool()
def get_file_info(file_path: str) -> str:
    """
    Get detailed information about a file.
    
    Args:
        file_path: Full path to the file
    
    Returns:
        File information (size, dates, etc.)
    """
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
    
    try:
        stat = os.stat(file_path)
        size_bytes = stat.st_size
        
        if size_bytes < 1024:
            size_str = f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            size_str = f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            size_str = f"{size_bytes / (1024 * 1024):.2f} MB"
        else:
            size_str = f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
        
        from datetime import datetime
        created = datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
        modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        accessed = datetime.fromtimestamp(stat.st_atime).strftime("%Y-%m-%d %H:%M:%S")
        
        is_dir = os.path.isdir(file_path)
        
        info = f"""Path: {file_path}
Type: {'Directory' if is_dir else 'File'}
Size: {size_str} ({size_bytes:,} bytes)
Created: {created}
Modified: {modified}
Accessed: {accessed}"""
        
        return info
    except Exception as e:
        return f"Error getting file info: {e}"


def main():
    """Entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
