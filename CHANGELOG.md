# Changelog

All notable changes to this project will be documented in this file.

## [0.2.1] - 2025-01-01

### Fixed
- `search_regex` - Pattern now correctly placed after `-regex` flag
- `get_total_size` - Fixed garbage output when using `*` wildcard

## [0.2.0] - 2025-01-01

### Added
- `search_regex` - Search using regular expressions
- `search_folders` - Find only directories
- `search_by_attributes` - Filter by hidden, system, read-only, compressed, encrypted
- `search_empty_folders` - Find empty directories
- `search_large_files` - Find files over a specified size
- `search_with_details` - Get detailed info (size, dates) in results
- `get_result_count` - Quick count without listing files
- `get_total_size` - Calculate total size of matching files
- `export_search_results` - Export to txt, csv, json, m3u, m3u8, tsv, efu
- `folder_path` parameter added to most search tools
- `sort_by` parameter for custom result ordering
- `files_only` and `folders_only` filters
- Added "code" file type category

### Fixed
- **BREAKING**: Fixed `folder_path` filter - now uses correct `-path` argument
- Improved error messages with installation hints

### Changed
- Complete rewrite for better organization
- All search tools now support folder path filtering

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
