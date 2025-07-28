#!/usr/bin/env python3

# S3 Delete Markers Listing Tool
#
# Lists all delete markers in an S3 bucket with details including key, version ID, 
# last modified date, and owner.
#
# Usage:
#     python delete_markers.py bucket-name
#     python delete_markers.py bucket-name -p profile-name
#
# Required modules:
#     - boto3: AWS SDK for Python
#     - argparse: Command-line argument parsing
#     - sys: System-specific parameters and functions
#     - botocore.exceptions: AWS SDK exception handling

import boto3
import argparse
import sys
from botocore.exceptions import ClientError, NoCredentialsError

# Lists all delete markers in the specified S3 bucket and displays them in a formatted table
def list_delete_markers(bucket_name, profile_name=None):
    try:
        if profile_name:
            session = boto3.Session(profile_name=profile_name)
            s3_client = session.client('s3')
        else:
            s3_client = boto3.client('s3')
        
        paginator = s3_client.get_paginator('list_object_versions')
        page_iterator = paginator.paginate(Bucket=bucket_name)
        
        delete_markers = []
        
        for page in page_iterator:
            if 'DeleteMarkers' in page:
                for marker in page['DeleteMarkers']:
                    delete_markers.append({
                        'Key': marker['Key'],
                        'VersionId': marker['VersionId'],
                        'LastModified': marker['LastModified'],
                        'Owner': marker.get('Owner', {}).get('DisplayName', 'Unknown')
                    })
        
        if delete_markers:
            print(f"Found {len(delete_markers)} delete markers in bucket '{bucket_name}':\n")
            print(f"{'Key':<50} {'Version ID':<36} {'Last Modified':<20} {'Owner'}")
            print("-" * 120)
            
            for marker in delete_markers:
                print(f"{marker['Key']:<50} {marker['VersionId']:<36} {marker['LastModified'].strftime('%Y-%m-%d %H:%M:%S'):<20} {marker['Owner']}")
        else:
            print(f"No delete markers found in bucket '{bucket_name}'")
            
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

# Parses command line arguments and calls list_delete_markers function
def main():
    parser = argparse.ArgumentParser(description='List all delete markers in an S3 bucket')
    parser.add_argument('bucket_name', help='Name of the S3 bucket to scan for delete markers')
    parser.add_argument('-p', '--profile', help='AWS credential profile to use')
    
    args = parser.parse_args()
    
    list_delete_markers(args.bucket_name, args.profile)

if __name__ == '__main__':
    main()
