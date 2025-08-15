
#### dump_s3_inventory.py
**AWS S3 Bucket Inventory Export Tool**

Dumps all files in an S3 bucket to a CSV file with detailed information including last modified date, full S3 path, and filename.

- **Purpose**: Create comprehensive inventory exports of S3 bucket contents for auditing, backup verification, or migration planning
- **Dependencies**: `boto3`, `csv`, `argparse`, `sys`, `datetime`, `botocore.exceptions`
- **Usage**: 
  ```bash
  python dump_s3_inventory.py bucket-name
  python dump_s3_inventory.py bucket-name -o custom_output.csv
  python dump_s3_inventory.py bucket-name -p profile-name
  python dump_s3_inventory.py bucket-name --exclude-dir logs/
  ```
- **Features**:
  - AWS profile support
  - Custom output filename (defaults to `{bucket_name}_inventory.csv`)
  - Directory exclusion filtering
  - Pagination support for large buckets (1000 objects per page)
  - Comprehensive error handling for credentials, permissions, and bucket existence
  - CSV export with Last Modified, Full Path, and Filename columns

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

#### aws_file_name_cheker.py
**AWS S3 Filename Compatibility Validator**

Validates filenames and directory structures against AWS S3 object key naming rules and best practices.

- **Purpose**: Check files for S3 compatibility before upload to prevent issues with problematic characters, length limits, and naming conventions
- **Dependencies**: Python standard library only (`sys`, `argparse`, `pathlib`, `typing`, `json`)
- **Usage**:
  ```bash
  python3 aws_file_name_cheker.py /path/to/files
  python3 aws_file_name_cheker.py /path/to/files --no-recursive
  python3 aws_file_name_cheker.py /path/to/files --show-valid
  python3 aws_file_name_cheker.py /path/to/files --output report.txt
  python3 aws_file_name_cheker.py /path/to/files --json
  ```
- **Features**:
  - Validates against S3 object key length limits (1024 bytes)
  - Identifies problematic characters (non-printable, avoid chars, extended ASCII)
  - Flags characters requiring special handling (URL encoding recommended)
  - Detects trailing periods, relative path elements, and spaces
  - Recursive or non-recursive directory scanning
  - Detailed reporting with validation results and recommendations
  - JSON output format support
  - Exit codes for CI/CD integration (non-zero if invalid files found)

## Requirements

- Python 3.x
- For `delete_markers.py`: AWS credentials configured and `boto3` library installed
- For other scripts: Python standard library (no additional installations required)

## Installation

1. Clone this repository
2. For AWS S3 script: Install boto3: `pip install boto3`
3. Make scripts executable: `chmod +x python3/*.py`
