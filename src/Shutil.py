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
