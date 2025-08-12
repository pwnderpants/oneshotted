#!/usr/bin/env python3

import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

class S3FileNameValidator:
    # Validates file names against AWS S3 object key naming rules.
    
    # Characters that are safe to use in S3 object keys
    SAFE_CHARS = set('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!-_.*\'()')
    
    # Characters that require special handling (URL encoding recommended)
    SPECIAL_HANDLING = set('&$@=;/:+,?')
    
    # Characters to avoid (may cause issues with various tools/protocols)
    AVOID_CHARS = set('\\{}^%`]"> [~<#|')
    
    # Non-printable ASCII characters (0-31 and 127)
    NON_PRINTABLE = set(chr(i) for i in range(0, 32)) | {chr(127)}
    
    # Extended ASCII characters (128-255)
    EXTENDED_ASCII = set(chr(i) for i in range(128, 256))
    
    def __init__(self):
        self.issues = []
    
    def validate_filename(self, filename: str, filepath: Optional[str] = None) -> Dict[str, Any]:
        # Validate a filename against S3 object key rules.
        # 
        # Args:
        #     filename: The filename to validate
        #     filepath: Optional full path for context
        #     
        # Returns:
        #     Dictionary with validation results
        result = {
            'filename': filename,
            'filepath': filepath,
            'is_valid': True,
            'issues': [],
            'recommendations': []
        }
        
        # Check length (1024 bytes max)
        filename_bytes = filename.encode('utf-8')
        if len(filename_bytes) > 1024:
            result['is_valid'] = False
            result['issues'].append(f"Filename too long: {len(filename_bytes)} bytes (max 1024)")
        
        # Check for empty filename
        if not filename.strip():
            result['is_valid'] = False
            result['issues'].append("Empty filename")

            return result
        
        # Analyze characters
        problematic_chars = []
        special_chars = []
        avoid_chars = []
        non_printable_chars = []
        
        for char in filename:
            if char in self.NON_PRINTABLE:
                non_printable_chars.append(char)
                result['is_valid'] = False
            elif char in self.AVOID_CHARS:
                avoid_chars.append(char)
                result['is_valid'] = False
            elif char in self.SPECIAL_HANDLING:
                special_chars.append(char)
            elif char in self.EXTENDED_ASCII:
                # Extended ASCII might cause issues
                problematic_chars.append(char)
        
        # Report issues
        if non_printable_chars:
            unique_chars = list(set(non_printable_chars))
            result['issues'].append(f"Contains non-printable characters: {unique_chars}")
        
        if avoid_chars:
            unique_chars = list(set(avoid_chars))
            result['issues'].append(f"Contains characters that should be avoided: {unique_chars}")
        
        if special_chars:
            unique_chars = list(set(special_chars))
            result['recommendations'].append(f"Contains characters that may need URL encoding: {unique_chars}")
        
        if problematic_chars:
            unique_chars = list(set(problematic_chars))
            result['recommendations'].append(f"Contains extended ASCII characters that may cause issues: {unique_chars}")
        
        # Check for trailing periods (console limitation)
        if filename.endswith('.'):
            result['recommendations'].append("Filename ends with period - may be truncated in S3 console")
        
        # Check for relative path elements
        if '../' in filename or './' in filename:
            result['recommendations'].append("Contains relative path elements - ensure proper handling")
        
        # Check for spaces
        if ' ' in filename:
            result['recommendations'].append("Contains spaces - may need special handling in URLs")
        
        return result
    
    def scan_directory(self, directory: str, recursive: bool = True) -> List[Dict]:
        # Scan a directory for files and validate their names.
        # 
        # Args:
        #     directory: Directory to scan
        #     recursive: Whether to scan subdirectories
        #     
        # Returns:
        #     List of validation results

        results = []
        path = Path(directory)
        
        if not path.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        if not path.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {directory}")
        
        # Get all files
        pattern = "**/*" if recursive else "*"
        
        for file_path in path.glob(pattern):
            if file_path.is_file():
                # Create relative path for S3-like key
                relative_path = file_path.relative_to(path)
                s3_key = str(relative_path).replace('\\', '/')  # Normalize path separators
                
                result = self.validate_filename(s3_key, str(file_path))
                results.append(result)
        
        return results
    
    def generate_report(self, results: List[Dict], show_valid: bool = False) -> str:
        # Generate a formatted report of validation results.
        report = []
        
        total_files = len(results)
        valid_files = sum(1 for r in results if r['is_valid'] and not r['recommendations'])
        invalid_files = sum(1 for r in results if not r['is_valid'])
        files_with_warnings = sum(1 for r in results if r['is_valid'] and r['recommendations'])
        
        report.append("="*80)
        report.append("AWS S3 FILENAME VALIDATION REPORT")
        report.append("="*80)
        report.append(f"Total files scanned: {total_files}")
        report.append(f"Valid files: {valid_files}")
        report.append(f"Invalid files: {invalid_files}")
        report.append(f"Files with warnings: {files_with_warnings}")
        report.append("")
        
        # Show invalid files
        if invalid_files > 0:
            report.append("INVALID FILES:")
            report.append("-" * 40)
            for result in results:
                if not result['is_valid']:
                    report.append(f"❌ {result['filename']}")
                    if result['filepath']:
                        report.append(f"   Path: {result['filepath']}")
                    for issue in result['issues']:
                        report.append(f"   Issue: {issue}")
                    report.append("")
        
        # Show files with warnings
        if files_with_warnings > 0:
            report.append("FILES WITH WARNINGS:")
            report.append("-" * 40)
            for result in results:
                if result['is_valid'] and result['recommendations']:
                    report.append(f"⚠️  {result['filename']}")
                    if result['filepath']:
                        report.append(f"   Path: {result['filepath']}")
                    for rec in result['recommendations']:
                        report.append(f"   Warning: {rec}")
                    report.append("")
        
        # Show valid files if requested
        if show_valid and valid_files > 0:
            report.append("VALID FILES:")
            report.append("-" * 40)
            for result in results:
                if result['is_valid'] and not result['recommendations']:
                    report.append(f"✅ {result['filename']}")
                    if result['filepath']:
                        report.append(f"   Path: {result['filepath']}")
            report.append("")
        
        return '\n'.join(report)

def main():
    parser = argparse.ArgumentParser(
        description="Check filenames for AWS S3 compatibility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 aws_file_name_checker.py /path/to/files
  python3 aws_file_name_checker.py /path/to/files --no-recursive
  python3 aws_file_name_checker.py /path/to/files --show-valid
  python3 aws_file_name_checker.py /path/to/files --output report.txt
        """
    )
    
    parser.add_argument('directory', help='Directory to scan for files')
    parser.add_argument('--no-recursive', action='store_true', 
                       help='Do not scan subdirectories')
    parser.add_argument('--show-valid', action='store_true',
                       help='Show valid files in the report')
    parser.add_argument('--output', '-o', help='Output report to file')
    parser.add_argument('--json', action='store_true',
                       help='Output results in JSON format')
    
    args = parser.parse_args()
    
    try:
        validator = S3FileNameValidator()
        recursive = not args.no_recursive
        
        print(f"Scanning {'recursively' if recursive else 'non-recursively'}: {args.directory}")
        results = validator.scan_directory(args.directory, recursive)
        
        if args.json:
            import json
            output = json.dumps(results, indent=2, ensure_ascii=False)
        else:
            output = validator.generate_report(results, args.show_valid)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Report written to: {args.output}")
        else:
            print(output)
            
        # Exit with error code if there are invalid files
        invalid_count = sum(1 for r in results if not r['is_valid'])
        sys.exit(1 if invalid_count > 0 else 0)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
