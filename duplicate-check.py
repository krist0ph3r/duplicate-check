import os
import hashlib
import sys
from typing import List, Tuple


def calculate_md5(file_path: str, block_size: int = 65536) -> str:
    """
    Calculates the MD5 checksum of a file.
    Reads the file in blocks to handle large files efficiently.
    """
    md5_hash = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(block_size), b""):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()
    except IOError as e:
        return f"ERROR: {e}"

def get_file_info(directory: str = '.') -> List[Tuple[str, int, str]]:
    """
    Traverses the specified directory, collects file paths, sizes, and MD5 sums.
    """
    file_info_list = []
    
    # Use os.walk to traverse the directory tree recursively
    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            # Use a try-except block to handle permission errors or files 
            # that might be deleted during traversal
            try:
                # Check if the path is actually a file (important for robustness)
                if os.path.isfile(file_path):
                    # Get file size
                    size = os.path.getsize(file_path)
                    
                    # Calculate MD5 sum
                    md5_sum = calculate_md5(file_path)
                    sys.stderr.write(file_path + "\n")
                    file_info_list.append((file_path, size, md5_sum))
            except Exception as e:
                # Add a record for files that couldn't be processed
                file_info_list.append((file_path, 0, f"ACCESS_ERROR: {e}"))
                
    return file_info_list

def display_file_info(info_list: List[Tuple[str, int, str]]):
    """
    Prints the collected file information in a formatted table.
    """
    if not info_list:
        print("No files found or directory is empty.")
        return

    # Print Data Rows
    for path, size, md5 in info_list:
        print(f"{md5}|{size}|{path}")

if __name__ == "__main__":
    # The script will start scanning from the current directory ('.')
    # You can change the starting directory here:
    # START_DIR = '/path/to/scan'
    START_DIR = '.'
    
    sys.stderr.write(f"Scanning directory: **{os.path.abspath(START_DIR)}**\n")
    
    file_data = get_file_info(START_DIR)
    display_file_info(file_data)
