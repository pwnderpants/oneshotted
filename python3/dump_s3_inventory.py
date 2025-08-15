#!/usr/bin/env python3
# Dumps all files in an S3 bucket to a CSV file with pagination.
# Outputs last modified date, full path, and filename for each object.

import boto3
import csv
import sys
import argparse
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError


def dump_s3_inventory(bucket_name, output_file, profile_name=None, exclude_dir=None):
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
                        # Skip objects in excluded directory if specified
                        if exclude_dir and obj['Key'].startswith(exclude_dir.rstrip('/') + '/'):
                            continue
                        
                        last_modified = obj['LastModified'].strftime('%Y-%m-%d %H:%M:%S UTC')
                        full_path = f"s3://{bucket_name}/{obj['Key']}"
                        filename = obj['Key'].split('/')[-1] if '/' in obj['Key'] else obj['Key']
                        
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
    parser.add_argument('--exclude-dir', help='Directory path to exclude from inventory')
    
    args = parser.parse_args()
    
    # Set default output filename to include bucket name if not specified
    if not args.output:
        args.output = f"{args.bucket_name}_inventory.csv"
    
    dump_s3_inventory(args.bucket_name, args.output, args.profile, args.exclude_dir)


if __name__ == '__main__':
    main()
