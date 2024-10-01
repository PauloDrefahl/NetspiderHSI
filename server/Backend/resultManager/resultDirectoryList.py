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


# Specify the path to the directory you're interested in
directory_path = "/result"

# Get the folders in JSON format
folders_json = list_folders_in_directory_to_json(directory_path)

# Print the JSON string to the console
print(folders_json)

# Optionally, save the JSON string to a file
#with open("folders_list.json", "w") as json_file:
   # json_file.write(folders_json)
