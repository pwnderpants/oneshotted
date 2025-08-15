#!/usr/bin/env python3
# Dumps all files in an S3 bucket to a CSV file with pagination.
# Outputs last modified date, full path, and filename for each object.

import boto3
import csv
import sys
import argparse
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError


def dump_s3_inventory(bucket_name, output_file, profile_name=None, exclude_dirs=None, exclude_types=None):
    # Dump all S3 objects from bucket to CSV file with pagination
    try:
        
        if profile_name:
            session = boto3.Session(profile_name=profile_name)
            s3_client = session.client('s3')
        else:
            s3_client = boto3.client('s3')
        
        # Test bucket access
        s3_client.head_bucket(Bucket=bucket_name)

        # Open CSV file for writing
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write CSV headers
            writer.writerow(['Last Modified', 'Full Path', 'Filename'])
            
            # Initialize pagination variables
            continuation_token = None
            object_count = 0
            
            print(f"Starting inventory dump for bucket: {bucket_name}")
            
            while True:
                # Prepare list_objects_v2 parameters
                list_params = {
                    'Bucket': bucket_name,
                    'MaxKeys': 1000  # AWS recommended page size
                }
                
                # Add continuation token if we have one
                if continuation_token:
                    list_params['ContinuationToken'] = continuation_token
                
                # List objects with pagination
                response = s3_client.list_objects_v2(**list_params)
                
                # Check if we have any objects in this page
                if 'Contents' in response:
                    for obj in response['Contents']:
                        # Skip objects in excluded directories if specified
                        if exclude_dirs:
                            skip_object = False
                            for exclude_dir in exclude_dirs:
                                if obj['Key'].startswith(exclude_dir):
                                    skip_object = True
                                    break
                            if skip_object:
                                continue
                        
                        # Skip objects with excluded file types if specified
                        if exclude_types:
                            file_extension = '.' + obj['Key'].split('.')[-1].lower() if '.' in obj['Key'] else ''
                            if file_extension in exclude_types:
                                continue
                        
                        last_modified = obj['LastModified'].strftime('%Y-%m-%d %H:%M:%S UTC')
                        full_path = f"s3://{bucket_name}/{obj['Key']}"
                        filename = obj['Key'].split('/')[-1] if '/' in obj['Key'] else obj['Key']
                        
                        # Skip directory paths unless they represent empty directories
                        if not filename and obj['Key'].endswith('/'):
                            continue
                        
                        # Write to CSV
                        writer.writerow([last_modified, full_path, filename])
                        object_count += 1
                    
                    print(f"Processed {object_count} objects...")
                
                # Check if there are more objects to fetch
                if response.get('IsTruncated', False):
                    continuation_token = response['NextContinuationToken']
                else:
                    break
        
        print(f"Inventory dump completed. Total objects: {object_count}")
        print(f"Output saved to: {output_file}")
            
    except NoCredentialsError:
        print("Error: AWS credentials not found. Please configure your AWS credentials.")
        sys.exit(1)
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchBucket':
            print(f"Error: Bucket '{bucket_name}' does not exist.")
        elif error_code == 'AccessDenied':
            print(f"Error: Access denied to bucket '{bucket_name}'. Check your permissions.")
        else:
            print(f"Error: {e.response['Error']['Message']}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)


def main():
    # Main function to parse arguments and execute inventory dump
    parser = argparse.ArgumentParser(description='Dump S3 bucket inventory to CSV')
    parser.add_argument('bucket_name', help='Name of the S3 bucket to inventory')
    parser.add_argument('-o', '--output', 
                       help='Output CSV file name (default: {bucket_name}_inventory.csv)')
    parser.add_argument('-p', '--profile', help='AWS credential profile to use')
    parser.add_argument('--exclude-dirs', help='Comma-separated list of directory paths to exclude from inventory (e.g., logs/,temp/,cache/)')
    parser.add_argument('--exclude-types', help='Comma-separated list of file extensions to exclude (e.g., .jpg,.png,.pdf)')
    
    args = parser.parse_args()
    
    # Set default output filename to include bucket name if not specified
    if not args.output:
        args.output = f"{args.bucket_name}_inventory.csv"
    
    # Parse exclude_dirs into a set for efficient lookup
    exclude_dirs_set = None
    if args.exclude_dirs:
        exclude_dirs_set = set(dir_path.strip().rstrip('/') + '/' for dir_path in args.exclude_dirs.split(','))
    
    # Parse exclude_types into a set for efficient lookup
    exclude_types_set = None
    if args.exclude_types:
        exclude_types_set = set(ext.strip().lower() for ext in args.exclude_types.split(','))
        # Ensure extensions start with a dot
        exclude_types_set = {ext if ext.startswith('.') else f'.{ext}' for ext in exclude_types_set}
    
    dump_s3_inventory(args.bucket_name, args.output, args.profile, exclude_dirs_set, exclude_types_set)


if __name__ == '__main__':
    main()
