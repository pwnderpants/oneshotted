#!/usr/bin/env python3

# Script to generate random files with various sizes for testing purposes.

import os
import random
import string
import sys
import time
from optparse import OptionParser


# Generate random content of specified size in bytes
def generate_random_content(size_bytes):
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation + ' \n', k=size_bytes))


# Generate a random folder name.
def generate_random_folder_name():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(3, 8)))


# Create random subfolders with specified nesting depth.
def create_random_subfolders(base_directory, num_folders, max_depth):
    folders = [base_directory]
    
    for _ in range(num_folders):
        # Choose a random parent folder from existing folders
        parent_folder = random.choice(folders)
        
        # Calculate current depth
        depth = parent_folder.replace(base_directory, '').count(os.sep)
        
        # Only create subfolder if we haven't reached max depth
        if depth < max_depth:
            folder_name = generate_random_folder_name()
            new_folder = os.path.join(parent_folder, folder_name)
            os.makedirs(new_folder, exist_ok=True)
            folders.append(new_folder)
    
    return folders


# Create a single random file with random size within specified range.
def create_random_file(directory, file_index, min_size, max_size):
    size = random.randint(min_size, max_size)
    filename = f"random_file_{file_index:04d}.txt"
    filepath = os.path.join(directory, filename)
    
    content = generate_random_content(size)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    return filepath, size


# Choose a random directory from the available directories.
def choose_random_directory(directories):
    return random.choice(directories)


# Prompt user to confirm using current directory as target.
def confirm_current_directory_usage():
    current_dir = os.getcwd()
    print(f"\nWARNING: No target directory specified.")
    print(f"Files will be created in the current directory: {current_dir}")
    
    while True:
        response = input("Do you want to continue? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' or 'n'")


# Display a progress animation for non-verbose mode.
def show_progress_animation(current, total, message="Processing"):
    spinner_chars = ['|', '/', '-', '\\']
    spinner = spinner_chars[current % len(spinner_chars)]
    percentage = (current / total) * 100
    
    # Create progress bar
    bar_length = 20
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    
    # Clear line and show progress
    sys.stdout.write(f'\r{message} {spinner} [{bar}] {percentage:.1f}% ({current}/{total})')
    sys.stdout.flush()


# Main function to parse arguments and generate files.
def main():
    parser = OptionParser(usage="usage: %prog [options] [target_directory]")
    
    parser.add_option("-n", "--num-files", 
                      dest="num_files", 
                      type="int", 
                      default=10,
                      help="Number of files to generate (default: 10)")
    
    parser.add_option("--min-size", 
                      dest="min_size", 
                      type="int", 
                      default=100,
                      help="Minimum file size in bytes (default: 100)")
    
    parser.add_option("--max-size", 
                      dest="max_size", 
                      type="int", 
                      default=10000,
                      help="Maximum file size in bytes (default: 10000)")
    
    
    parser.add_option("-v", "--verbose", 
                      dest="verbose", 
                      action="store_true", 
                      default=False,
                      help="Enable verbose output")
    
    parser.add_option("--num-folders", 
                      dest="num_folders", 
                      type="int", 
                      default=0,
                      help="Number of random subfolders to create (default: 0)")
    
    parser.add_option("--max-depth", 
                      dest="max_depth", 
                      type="int", 
                      default=3,
                      help="Maximum nesting depth for subfolders (default: 3)")
    
    parser.add_option("--distribute-files", 
                      dest="distribute_files", 
                      action="store_true", 
                      default=False,
                      help="Distribute files randomly across subfolders")

    (options, args) = parser.parse_args()

    # Determine target directory
    if len(args) >= 1:
        # Use positional argument
        target_directory = args[0]
    else:
        # No directory specified, use current directory with confirmation
        if not confirm_current_directory_usage():
            print("Operation aborted.")
            sys.exit(0)
        target_directory = "."
    
    # Store the determined directory in options for consistency
    options.directory = target_directory

    # Validate arguments
    if options.min_size < 0:
        parser.error("Minimum size must be non-negative")
    
    if options.max_size < options.min_size:
        parser.error("Maximum size must be greater than or equal to minimum size")
    
    if options.num_files < 1:
        parser.error("Number of files must be at least 1")
    
    if options.num_folders < 0:
        parser.error("Number of folders must be non-negative")
    
    if options.max_depth < 1:
        parser.error("Maximum depth must be at least 1")

    # Create output directory if it doesn't exist
    os.makedirs(options.directory, exist_ok=True)

    print(f"Generating {options.num_files} files in '{options.directory}'")
    print(f"File size range: {options.min_size} - {options.max_size} bytes")
    
    # Create subfolders if requested
    available_directories = [options.directory]
    if options.num_folders > 0:
        print(f"Creating {options.num_folders} subfolders with max depth {options.max_depth}")
        available_directories = create_random_subfolders(
            options.directory, 
            options.num_folders, 
            options.max_depth
        )
        
        if options.verbose:
            for folder in available_directories[1:]:  # Skip base directory
                print(f"Created folder: {folder}")
    
    total_size = 0
    
    for i in range(options.num_files):
        # Show progress animation for non-verbose mode
        if not options.verbose:
            show_progress_animation(i + 1, options.num_files, "Creating files")
        
        # Choose directory for file placement
        if options.distribute_files and len(available_directories) > 1:
            target_directory = choose_random_directory(available_directories)
        else:
            target_directory = options.directory
        
        filepath, file_size = create_random_file(
            target_directory, 
            i + 1, 
            options.min_size, 
            options.max_size
        )
        total_size += file_size
        
        if options.verbose:
            print(f"Created: {filepath} ({file_size} bytes)")
        
        # Small delay for animation visibility
        if not options.verbose:
            time.sleep(0.05)
    
    # Clear progress line and show completion
    if not options.verbose:
        print()  # New line after progress bar
    
    print(f"\nGenerated {options.num_files} files")
    if options.num_folders > 0:
        print(f"Created {len(available_directories) - 1} subfolders")
    print(f"Total size: {total_size} bytes ({total_size / 1024:.2f} KB)")


if __name__ == "__main__":
    main()
