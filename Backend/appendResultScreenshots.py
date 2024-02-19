import os
import shutil

# Define the source directories and the target directory
source_directories = ['/path/to/source1', '/path/to/source2']
target_directory = '/path/to/target'

# Loop through each source directory
for source_dir in source_directories:
    # List all files in the current source directory
    for file_name in os.listdir(source_dir):
        # Check if the file is a PNG
        if file_name.lower().endswith('.png'):
            # Construct full file paths
            source_file = os.path.join(source_dir, file_name)
            target_file = os.path.join(target_directory, file_name)

            # Copy the file
            shutil.copy(source_file, target_file)
