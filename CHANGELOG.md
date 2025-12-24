# Changelog

All notable changes to this project will be documented in this file.

## [0.1.1] - 2025-01-01

### Fixed
- `open_file_location` no longer reports false errors (Windows explorer.exe returns non-zero exit code even on success)

## [0.1.0] - 2025-01-01

### Added
- Initial release
- `search_files` - Basic file search with wildcards
- `search_with_filters` - Search with extension, size, and path filters
- `search_by_type` - Search by category (audio, video, image, document, executable, compressed)
- `search_recent_files` - Find recently modified files
- `search_duplicates` - Find files with the same name
- `open_file_location` - Open containing folder in Windows Explorer
- `get_file_info` - Get file size, dates, and details
- Support for Everything 1.5 alpha via `EVERYTHING_INSTANCE` environment variable
