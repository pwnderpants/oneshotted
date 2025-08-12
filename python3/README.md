
#### delete_markers.py
**AWS S3 Delete Markers Listing Tool**

Lists all delete markers in an S3 bucket with detailed information including key, version ID, last modified date, and owner.

- **Purpose**: Identify and analyze S3 delete markers for bucket management and cleanup
- **Dependencies**: `boto3`, `argparse`, `sys`, `botocore.exceptions`
- **Usage**: 
  ```bash
  python delete_markers.py bucket-name
  python delete_markers.py bucket-name -p profile-name
  ```
- **Features**:
  - AWS profile support
  - Formatted table output
  - Error handling for credentials, permissions, and bucket existence
  - Pagination support for large buckets

#### file_normie.py
**Filename Normalization Tool**

Normalizes filenames by replacing whitespace and special characters with underscores or dashes, and renames the actual files.

- **Purpose**: Clean up filenames to remove problematic characters and standardize naming
- **Dependencies**: Python standard library only (`argparse`, `re`, `os`, `sys`)
- **Usage**:
  ```bash
  # Single file
  python3 file_normie.py "my file name.txt"
  python3 file_normie.py -d "my file name.txt"  # Use dashes
  
  # Recursive processing
  python3 file_normie.py --recursive /path/to/folder
  python3 file_normie.py -r -d /path/to/folder  # Use dashes recursively
  ```
- **Features**:
  - Single file or recursive directory processing
  - Choice between underscores (default) or dashes as replacement characters
  - Duplicate filename protection
  - Comprehensive error handling and reporting

#### populate_files.py
**Random File Generator for Testing**

Generates random files with various sizes and optional subfolder structure for testing purposes.

- **Purpose**: Create test datasets with random content for filesystem testing, backup validation, or performance testing
- **Dependencies**: Python standard library only (`os`, `random`, `string`, `sys`, `time`, `optparse`)
- **Usage**:
  ```bash
  python3 populate_files.py [target_directory]
  python3 populate_files.py -n 50 --min-size 1000 --max-size 50000
  python3 populate_files.py --num-folders 5 --distribute-files /test/directory
  ```
- **Features**:
  - Configurable number of files and size ranges
  - Optional subfolder creation with configurable nesting depth
  - Random file distribution across subfolders
  - Progress animation and verbose output modes
  - Safety confirmation for current directory usage

## Requirements

- Python 3.x
- For `delete_markers.py`: AWS credentials configured and `boto3` library installed
- For other scripts: Python standard library (no additional installations required)

## Installation

1. Clone this repository
2. For AWS S3 script: Install boto3: `pip install boto3`
3. Make scripts executable: `chmod +x python3/*.py`
