import os
import shutil

def group_files_by_prefix(directory):
    # Get all files in the directory
    files = os.listdir(directory)

    # Create a dictionary to store file groups
    file_groups = {}

    # Group files by prefix
    for filename in files:
        prefix = filename.split('_')[0]  # Assuming the prefix is before the first underscore
        if prefix not in file_groups:
            file_groups[prefix] = []
        file_groups[prefix].append(filename)

    # Create folders for each file group
    for prefix, filenames in file_groups.items():
        folder_name = os.path.join(directory, prefix)
        os.makedirs(folder_name, exist_ok=True)

        # Move files to respective folders
        for filename in filenames:
            source = os.path.join(directory, filename)
            destination = os.path.join(folder_name, filename)
            shutil.move(source, destination)

    print("Files grouped and moved successfully!")

# Provide the directory path where the files are located
directory_path = '/path/to/directory'

# Call the function to group and move files
group_files_by_prefix(directory_path)
import boto3
import os

def upload_directory(local_path, bucket_name, s3_path):
    s3_client = boto3.client('s3')
    for root, dirs, files in os.walk(local_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            s3_key = os.path.join(s3_path, os.path.relpath(local_file_path, local_path))
            s3_client.upload_file(local_file_path, bucket_name, s3_key)
            print(f"Uploaded {local_file_path} to s3://{bucket_name}/{s3_key}")

# Specify the local directory path you want to copy
local_directory = '/path/to/local/directory'

# Specify your S3 bucket name and the destination path in S3
bucket_name = 'your-s3-bucket-name'
s3_directory = 'path/to/s3/directory'

# Upload the directory to S3
upload_directory(local_directory, bucket_name, s3_directory)
import os
import pandas as pd

def convert_csv_to_parquet(csv_path):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_path)

    # Extract the file name without extension
    file_name = os.path.splitext(csv_path)[0]

    # Convert and save the DataFrame as Parquet
    parquet_path = file_name + '.parquet'
    df.to_parquet(parquet_path)
    print(f"Converted {csv_path} to {parquet_path}")

def convert_csvs_to_parquet(directory):
    # Iterate over all files and directories in the given directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file is a CSV
            if file.endswith('.csv'):
                # Get the full path of the CSV file
                csv_path = os.path.join(root, file)
                
                # Convert the CSV file to Parquet
                convert_csv_to_parquet(csv_path)

# Specify the directory where the CSV files are located
directory_path = '/path/to/csv/files'

# Convert all CSV files in the directory and its subdirectories to Parquet
convert_csvs_to_parquet(directory_path)
