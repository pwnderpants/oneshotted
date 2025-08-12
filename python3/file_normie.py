#!/usr/bin/env python3

# This script normalizes filenames by replacing whitespace and special characters
# with underscores (default) or dashes, and renames the actual file(s).
#
# Usage:
#     Single file:
#         python3 file_normie.py "my file name.txt"
#         python3 file_normie.py -d "my file name.txt"
#
#     Recursive folder:
#         python3 file_normie.py --recursive /path/to/folder
#         python3 file_normie.py -r -d /path/to/folder
#
# Options:
#     -d, --dashes      Use dashes instead of underscores for replacement
#     -r, --recursive   Recursively rename all files in the given directory
#
# Dependencies:
#     Uses only Python standard library modules (argparse, re, os, sys).
#     No additional modules need to be installed.
#
# Examples:
#     Single file:
#         "my file name.txt"     -> Renamed to: "my_file_name.txt"
#         "weird@file#name.pdf"  -> Renamed to: "weird_file_name.pdf"
#     Recursive:
#         Processes all files in directory and subdirectories

import argparse
import re
import os
import sys

# Normalize filename by replacing special characters with underscores or dashes
def normalize_filename(filename, use_dashes=False):
    replacement_char = '-' if use_dashes else '_'
    
    base_name, extension = os.path.splitext(filename)
    
    normalized_base = re.sub(r'[^\w.-]', replacement_char, base_name)
    normalized_base = re.sub(r'[_-]+', replacement_char, normalized_base)
    normalized_base = normalized_base.strip(replacement_char)
    
    return normalized_base + extension

# Rename a single file with normalized filename, returns success status and message
def rename_single_file(filepath, use_dashes=False):
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    normalized = normalize_filename(filename, use_dashes)
    
    if normalized == filename:
        return False, f"File '{filepath}' is already normalized"
    
    new_filepath = os.path.join(directory, normalized)
    
    if os.path.exists(new_filepath):
        return False, f"Target file '{new_filepath}' already exists"
    
    try:
        os.rename(filepath, new_filepath)
        return True, f"Renamed '{filepath}' -> '{new_filepath}'"
    except OSError as e:
        return False, f"Error renaming '{filepath}': {e}"

# Recursively process all files in directory and subdirectories
def process_directory_recursive(directory, use_dashes=False):
    renamed_count = 0
    error_count = 0
    
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            success, message = rename_single_file(filepath, use_dashes)
            print(message)
            if success:
                renamed_count += 1
            else:
                error_count += 1
    
    print(f"\nSummary: {renamed_count} files renamed, {error_count} errors/skipped")

# Main function handling command-line arguments and program flow
def main():
    parser = argparse.ArgumentParser(description='Normalize filenames by replacing whitespace and special characters')
    parser.add_argument('path', help='The file or directory path to process')
    parser.add_argument('-d', '--dashes', action='store_true', 
                       help='Use dashes instead of underscores for replacement')
    parser.add_argument('-r', '--recursive', action='store_true',
                       help='Recursively process all files in the given directory')
    
    args = parser.parse_args()
    
    if not args.path:
        print("Error: Please provide a file or directory path", file=sys.stderr)
        sys.exit(1)
    
    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    if args.recursive:
        if not os.path.isdir(args.path):
            print(f"Error: --recursive requires a directory, but '{args.path}' is not a directory", file=sys.stderr)
            sys.exit(1)
        process_directory_recursive(args.path, args.dashes)
    else:
        if os.path.isdir(args.path):
            print(f"Error: '{args.path}' is a directory. Use --recursive to process directories", file=sys.stderr)
            sys.exit(1)
        success, message = rename_single_file(args.path, args.dashes)
        print(message)
        if not success:
            sys.exit(1)

if __name__ == '__main__':
    main()
