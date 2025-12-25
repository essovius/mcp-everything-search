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
ES_INSTANCE = os.environ.get("EVERYTHING_INSTANCE", "")


def run_es_command(args: list[str]) -> tuple[bool, str]:
    """Run es.exe with given arguments and return output."""
    try:
        cmd = [ES_PATH]
        if ES_INSTANCE:
            cmd.extend(["-instance", ES_INSTANCE])
        cmd.extend(args)
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30,
            encoding='utf-8', errors='replace'
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, result.stderr.strip() or "No results found"
    except subprocess.TimeoutExpired:
        return False, "Search timed out"
    except FileNotFoundError:
        return False, f"es.exe not found at {ES_PATH}. Install from https://github.com/voidtools/es"
    except Exception as e:
        return False, str(e)


def format_file_list(output: str, count_msg: str = "") -> str:
    """Format file list output."""
    if not output:
        return "No results found."
    files = [f for f in output.split('\n') if f.strip()]
    prefix = f"Found {len(files)} results" if not count_msg else count_msg
    return f"{prefix}:\n" + "\n".join(files)


def format_size(size_bytes: int) -> str:
    """Format bytes to human readable size."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    elif size_bytes < 1024 * 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024 * 1024):.2f} TB"


# =============================================================================
# BASIC SEARCH TOOLS
# =============================================================================

@mcp.tool()
def search_files(
    query: str, max_results: int = 50, match_case: bool = False,
    match_whole_word: bool = False, match_path: bool = False, sort_by: str = ""
) -> str:
    """
    Search for files and folders using Everything.
    
    Args:
        query: Search query (supports wildcards * and ?)
        max_results: Maximum number of results (default 50)
        match_case: Enable case-sensitive search
        match_whole_word: Match whole words only
        match_path: Search in full path instead of filename only
        sort_by: Sort by: name, path, size, extension, date-modified, date-created, date-accessed
    """
    args = ["-n", str(max_results)]
    if match_case: args.append("-case")
    if match_whole_word: args.append("-whole-word")
    if match_path: args.append("-match-path")
    if sort_by: args.extend(["-sort", sort_by])
    args.append(query)
    
    success, output = run_es_command(args)
    return format_file_list(output) if success else f"Search error: {output}"


@mcp.tool()
def search_with_filters(
    query: str = "", extension: str = "", folder_path: str = "",
    min_size: str = "", max_size: str = "", max_results: int = 50,
    match_case: bool = False, files_only: bool = False,
    folders_only: bool = False, sort_by: str = ""
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
        match_case: Enable case-sensitive search
        files_only: Return only files, not folders
        folders_only: Return only folders, not files
        sort_by: Sort by: name, path, size, extension, date-modified, date-created
    """
    args = ["-n", str(max_results)]
    if match_case: args.append("-case")
    if files_only: args.append("/a-d")
    if folders_only: args.append("/ad")
    if folder_path: args.extend(["-path", folder_path])
    if sort_by: args.extend(["-sort", sort_by])
    
    search_parts = []
    if query: search_parts.append(query)
    if extension: search_parts.append(f"ext:{extension.lstrip('.')}")
    if min_size: search_parts.append(f"size:>={min_size}")
    if max_size: search_parts.append(f"size:<={max_size}")
    
    if not search_parts and not folder_path:
        return "Error: Please provide at least one search parameter"
    if search_parts: args.append(" ".join(search_parts))
    
    success, output = run_es_command(args)
    return format_file_list(output) if success else f"Search error: {output}"


@mcp.tool()
def search_regex(
    pattern: str, folder_path: str = "", max_results: int = 50, match_case: bool = False
) -> str:
    """
    Search using regular expressions.
    
    Args:
        pattern: Regular expression pattern
        folder_path: Limit search to specific folder path (optional)
        max_results: Maximum number of results (default 50)
        match_case: Enable case-sensitive search
    """
    args = ["-n", str(max_results)]
    if match_case: args.append("-case")
    if folder_path: args.extend(["-path", folder_path])
    args.extend(["-regex", pattern])  # pattern must come right after -regex
    
    success, output = run_es_command(args)
    return format_file_list(output) if success else f"Search error: {output}"


# =============================================================================
# SPECIALIZED SEARCH TOOLS
# =============================================================================

@mcp.tool()
def search_by_type(
    file_type: str, query: str = "", folder_path: str = "", max_results: int = 50
) -> str:
    """
    Search for specific file types.
    
    Args:
        file_type: Type: audio, video, image, document, executable, compressed, code
        query: Additional search query (optional)
        folder_path: Limit search to specific folder path (optional)
        max_results: Maximum number of results (default 50)
    """
    type_filters = {
        "audio": "ext:mp3;wav;flac;aac;ogg;wma;m4a;opus;aiff",
        "video": "ext:mp4;mkv;avi;mov;wmv;flv;webm;m4v;mpeg;mpg",
        "image": "ext:jpg;jpeg;png;gif;bmp;webp;svg;ico;tiff;raw;psd",
        "document": "ext:doc;docx;pdf;txt;rtf;odt;xls;xlsx;ppt;pptx;md;epub",
        "executable": "ext:exe;msi;bat;cmd;ps1;sh;com;scr",
        "compressed": "ext:zip;rar;7z;tar;gz;bz2;xz;iso;cab",
        "code": "ext:py;js;ts;c;cpp;h;hpp;java;cs;go;rs;rb;php;swift;kt;scala;r;sql;html;css;json;xml;yaml;yml"
    }
    
    if file_type.lower() not in type_filters:
        return f"Unknown file type '{file_type}'. Available: {', '.join(type_filters.keys())}"
    
    args = ["-n", str(max_results)]
    if folder_path: args.extend(["-path", folder_path])
    
    search_query = type_filters[file_type.lower()]
    if query: search_query = f"{query} {search_query}"
    args.append(search_query)
    
    success, output = run_es_command(args)
    return format_file_list(output, f"Found {file_type} files") if success else f"Search error: {output}"


@mcp.tool()
def search_folders(
    query: str = "", folder_path: str = "", max_results: int = 50, sort_by: str = ""
) -> str:
    """
    Search for folders/directories only.
    
    Args:
        query: Search query (optional)
        folder_path: Limit search to specific parent folder (optional)
        max_results: Maximum number of results (default 50)
        sort_by: Sort by: name, path, date-modified, date-created
    """
    args = ["-n", str(max_results), "/ad"]
    if folder_path: args.extend(["-path", folder_path])
    if sort_by: args.extend(["-sort", sort_by])
    if query: args.append(query)
    
    success, output = run_es_command(args)
    return format_file_list(output, "Found folders") if success else f"Search error: {output}"


@mcp.tool()
def search_recent_files(
    days: int = 7, query: str = "", folder_path: str = "",
    max_results: int = 50, files_only: bool = True
) -> str:
    """
    Search for recently modified files.
    
    Args:
        days: Files modified within this many days (default 7)
        query: Additional search query (optional)
        folder_path: Limit search to specific folder (optional)
        max_results: Maximum number of results (default 50)
        files_only: Return only files, not folders (default True)
    """
    args = ["-n", str(max_results), "-sort", "date-modified-descending"]
    if files_only: args.append("/a-d")
    if folder_path: args.extend(["-path", folder_path])
    
    search_query = f"dm:last{days}days"
    if query: search_query = f"{query} {search_query}"
    args.append(search_query)
    
    success, output = run_es_command(args)
    return format_file_list(output, f"Files modified in last {days} days") if success else f"Search error: {output}"


@mcp.tool()
def search_duplicates(filename: str, folder_path: str = "", max_results: int = 50) -> str:
    """
    Find files with the same name (potential duplicates).
    
    Args:
        filename: Exact filename to search for
        folder_path: Limit search to specific folder (optional)
        max_results: Maximum number of results (default 50)
    """
    args = ["-n", str(max_results), "-whole-word"]
    if folder_path: args.extend(["-path", folder_path])
    args.append(filename)
    
    success, output = run_es_command(args)
    if success:
        files = [f for f in output.split('\n') if f.strip()] if output else []
        if len(files) > 1:
            return f"Found {len(files)} files named '{filename}':\n" + "\n".join(files)
        elif len(files) == 1:
            return f"Only one file found named '{filename}':\n{files[0]}"
        else:
            return f"No files found named '{filename}'"
    return f"Search error: {output}"


@mcp.tool()
def search_by_attributes(
    query: str = "", hidden: bool = False, system: bool = False,
    read_only: bool = False, compressed: bool = False, encrypted: bool = False,
    folder_path: str = "", max_results: int = 50
) -> str:
    """
    Search files by Windows file attributes.
    
    Args:
        query: Additional search query (optional)
        hidden: Find hidden files
        system: Find system files
        read_only: Find read-only files
        compressed: Find compressed files
        encrypted: Find encrypted files
        folder_path: Limit search to specific folder (optional)
        max_results: Maximum number of results (default 50)
    """
    args = ["-n", str(max_results)]
    
    attribs = []
    if hidden: attribs.append("H")
    if system: attribs.append("S")
    if read_only: attribs.append("R")
    if compressed: attribs.append("C")
    if encrypted: attribs.append("E")
    
    if attribs: args.append(f"/a{''.join(attribs)}")
    if folder_path: args.extend(["-path", folder_path])
    if query: args.append(query)
    elif not attribs: return "Error: Please provide a query or select at least one attribute"
    
    success, output = run_es_command(args)
    return format_file_list(output) if success else f"Search error: {output}"


@mcp.tool()
def search_empty_folders(folder_path: str = "", max_results: int = 100) -> str:
    """
    Find empty folders.
    
    Args:
        folder_path: Limit search to specific folder (optional)
        max_results: Maximum number of results (default 100)
    """
    args = ["-n", str(max_results), "/ad"]
    if folder_path: args.extend(["-path", folder_path])
    args.append("empty:")
    
    success, output = run_es_command(args)
    return format_file_list(output, "Empty folders found") if success else f"Search error: {output}"


@mcp.tool()
def search_large_files(
    min_size: str = "100mb", folder_path: str = "", extension: str = "", max_results: int = 50
) -> str:
    """
    Find large files.
    
    Args:
        min_size: Minimum file size (e.g., "100mb", "1gb", "500kb"). Default: 100mb
        folder_path: Limit search to specific folder (optional)
        extension: File extension filter (optional)
        max_results: Maximum number of results (default 50)
    """
    args = ["-n", str(max_results), "-sort", "size-descending", "/a-d"]
    if folder_path: args.extend(["-path", folder_path])
    
    search_parts = [f"size:>={min_size}"]
    if extension: search_parts.append(f"ext:{extension.lstrip('.')}")
    args.append(" ".join(search_parts))
    
    success, output = run_es_command(args)
    return format_file_list(output, f"Files larger than {min_size}") if success else f"Search error: {output}"


# =============================================================================
# UTILITY TOOLS
# =============================================================================

@mcp.tool()
def get_result_count(query: str, folder_path: str = "", extension: str = "") -> str:
    """
    Get the count of matching files without listing them (fast).
    
    Args:
        query: Search query
        folder_path: Limit search to specific folder (optional)
        extension: File extension filter (optional)
    """
    args = ["-get-result-count"]
    if folder_path: args.extend(["-path", folder_path])
    
    search_parts = [query] if query and query != "*" else []
    if extension: search_parts.append(f"ext:{extension.lstrip('.')}")
    if search_parts: args.append(" ".join(search_parts))
    
    success, output = run_es_command(args)
    return f"Found {output.strip()} matching files" if success else f"Error: {output}"


@mcp.tool()
def get_total_size(query: str, folder_path: str = "", extension: str = "") -> str:
    """
    Get the total size of all matching files.
    
    Args:
        query: Search query
        folder_path: Limit search to specific folder (optional)
        extension: File extension filter (optional)
    """
    args = ["-get-total-size"]
    if folder_path: args.extend(["-path", folder_path])
    
    search_parts = [query] if query and query != "*" else []
    if extension: search_parts.append(f"ext:{extension.lstrip('.')}")
    if search_parts: args.append(" ".join(search_parts))
    
    success, output = run_es_command(args)
    if success:
        try:
            size_bytes = int(output.strip())
            return f"Total size: {format_size(size_bytes)} ({size_bytes:,} bytes)"
        except ValueError:
            return f"Total size: {output.strip()}"
    return f"Error: {output}"


@mcp.tool()
def search_with_details(
    query: str, folder_path: str = "", extension: str = "", max_results: int = 50,
    sort_by: str = "date-modified-descending", files_only: bool = False, folders_only: bool = False
) -> str:
    """
    Search files and return detailed information (name, path, size, dates).
    
    Args:
        query: Search query
        folder_path: Limit search to specific folder (optional)
        extension: File extension filter (optional)
        max_results: Maximum number of results (default 50)
        sort_by: Sort by: name, path, size, date-modified[-descending], date-created[-descending]
        files_only: Return only files
        folders_only: Return only folders
    """
    args = ["-n", str(max_results), "-full-path-and-name", "-size", "-date-modified", "-date-created"]
    if sort_by: args.extend(["-sort", sort_by])
    if files_only: args.append("/a-d")
    if folders_only: args.append("/ad")
    if folder_path: args.extend(["-path", folder_path])
    
    search_parts = [query] if query else []
    if extension: search_parts.append(f"ext:{extension.lstrip('.')}")
    if search_parts: args.append(" ".join(search_parts))
    elif not folder_path: return "Error: Please provide a query, folder_path, or extension"
    
    success, output = run_es_command(args)
    return output if success and output else "No results found." if success else f"Search error: {output}"


@mcp.tool()
def open_file_location(file_path: str) -> str:
    """
    Open the folder containing a file in Windows Explorer.
    
    Args:
        file_path: Full path to the file
    """
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
    try:
        subprocess.run(["explorer", "/select,", file_path])
        return f"Opened folder containing: {file_path}"
    except Exception as e:
        return f"Error opening location: {e}"


@mcp.tool()
def get_file_info(file_path: str) -> str:
    """
    Get detailed information about a file.
    
    Args:
        file_path: Full path to the file
    """
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
    
    try:
        stat = os.stat(file_path)
        from datetime import datetime
        created = datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
        modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        accessed = datetime.fromtimestamp(stat.st_atime).strftime("%Y-%m-%d %H:%M:%S")
        is_dir = os.path.isdir(file_path)
        
        return f"""Path: {file_path}
Type: {'Directory' if is_dir else 'File'}
Size: {format_size(stat.st_size)} ({stat.st_size:,} bytes)
Created: {created}
Modified: {modified}
Accessed: {accessed}"""
    except Exception as e:
        return f"Error getting file info: {e}"


@mcp.tool()
def export_search_results(
    query: str, output_file: str, format: str = "txt", folder_path: str = "",
    extension: str = "", max_results: int = 1000, include_size: bool = False, include_dates: bool = False
) -> str:
    """
    Export search results to a file.
    
    Args:
        query: Search query
        output_file: Output file path (e.g., "C:/results.txt")
        format: Export format: txt, csv, json, m3u, m3u8, tsv, efu
        folder_path: Limit search to specific folder (optional)
        extension: File extension filter (optional)
        max_results: Maximum number of results (default 1000)
        include_size: Include file sizes in export
        include_dates: Include dates (created, modified) in export
    """
    valid_formats = ["txt", "csv", "json", "m3u", "m3u8", "tsv", "efu"]
    if format.lower() not in valid_formats:
        return f"Invalid format '{format}'. Valid formats: {', '.join(valid_formats)}"
    
    args = ["-n", str(max_results), f"-export-{format.lower()}", output_file]
    if include_size: args.append("-size")
    if include_dates: args.extend(["-date-created", "-date-modified"])
    if folder_path: args.extend(["-path", folder_path])
    
    search_parts = [query] if query else []
    if extension: search_parts.append(f"ext:{extension.lstrip('.')}")
    if search_parts: args.append(" ".join(search_parts))
    
    success, output = run_es_command(args)
    return f"Results exported to: {output_file}" if success else f"Export error: {output}"


# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    """Entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
