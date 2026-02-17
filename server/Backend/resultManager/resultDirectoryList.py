import os
import json


def list_folders_in_directory_to_json(directory_path):
    # List all entries in the specified directory
    entries = os.listdir(directory_path)

    # Filter out files, keeping only directories
    folders = [entry for entry in entries if os.path.isdir(os.path.join(directory_path, entry))]

    # Convert the list of folders to a JSON formatted string
    folders_json = json.dumps(folders, indent=4)

    return folders_json


if __name__ == "__main__":
    import sys
    directory_path = sys.argv[1] if len(sys.argv) > 1 else "/result"
    folders_json = list_folders_in_directory_to_json(directory_path)
    print(folders_json)
