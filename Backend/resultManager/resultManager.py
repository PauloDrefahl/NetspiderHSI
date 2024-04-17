import json
import webbrowser
import os
import sys
import subprocess
from Backend.resultManager.makeDiagramsBetter import DataAnalyzer

from flask import jsonify


class ResultManager:
    """
        Result Manager Class for seeing results.

        Attributes:
            results_directory: OpenAI client for accessing API.
            selected_folders:
        Functions:
            view_pdf: views selected pdf

    """
    def __init__(self, results_directory):
        self.results_directory = results_directory

        self.update_folders_json()

    def get_folders(self):
        print("Sending folder json to list component")

        try:
            if not os.path.exists('folders.json'):
                self.update_folders_json()

            with open('folders.json', 'r') as f:
                folders = json.load(f)
            return folders
        except FileNotFoundError:
            print("folders.json not found, creating a new one.")
            self.update_folders_json()
            return self.get_folders()
        except Exception as e:
            print(f"Error getting folders: {str(e)}")
            return {"error": str(e)}, 500

    def update_folders_json(self):
        print("Updating File list")
        try:
            print("Reading Directory")
            all_folders = []
            # Use os.walk to iterate through each directory and subdirectory
            # List everything in the directory
            all_entries = os.listdir(self.results_directory)
            # Filter to include only directories
            all_folders = [entry for entry in all_entries if os.path.isdir(os.path.join(self.results_directory, entry))]

            # Optionally, sort files alphabetically; adjust as needed
            all_folders.sort()

            print("Writing Directory into file")
            with open('folders.json', 'w') as f:
                json.dump(all_folders, f, indent=2)
            print("Folders list updated in folders.json")
        except Exception as e:
            print(f"Error updating the folders list: {e}")

    def view_pdf(self, kwargs):
        # Path to the directory you want to open
        # Making sure the path is absolute
        relative_path = kwargs['pdf_path']
        print("relative path", relative_path)

        print("result dir", self.results_directory)

        full_path = self.results_directory + "\\" + relative_path

        absolute_path = os.path.abspath(full_path)
        print("absolute path", absolute_path)
        try:
            # Open the PDF file in the default application
            webbrowser.open('file://' + absolute_path)
            return 0
        except Exception as e:
            print(f"An error occurred: {e}")
            return 1

    def view_ss_dir(self, kwargs):
        # Making sure the path is absolute
        relative_path = kwargs['ss_path']
        print(relative_path)
        full_path = self.results_directory + "\\" + relative_path

        absolute_path = os.path.abspath(full_path)
        print("open file path", absolute_path)

        # Determine the platform and construct the command
        if sys.platform.startswith('win32'):
            # Windows: 'explorer' opens File Explorer
            cmd = ['explorer', absolute_path]
        elif sys.platform.startswith('darwin'):
            # macOS: 'open' opens Finder
            cmd = ['open', absolute_path]
        elif sys.platform.startswith('linux'):
            # Linux: 'xdg-open' opens the default file manager
            cmd = ['xdg-open', absolute_path]
        else:
            raise OSError("Unsupported operating system")

        # Execute the command to open the directory
        subprocess.run(cmd, check=True, shell=sys.platform.startswith('win32'))

    def view_raw_data(self, kwargs):
        # Making sure the path is absolute
        # Making sure the path is absolute
        relative_path = kwargs['raw_path']
        print(relative_path)
        full_path = self.results_directory + "\\" + relative_path

        absolute_path = os.path.abspath(full_path)
        print(absolute_path)

        # Determine the platform and construct the command
        if sys.platform.startswith('win32'):
            # Windows
            cmd = ['start', absolute_path]
        elif sys.platform.startswith('darwin'):
            # macOS
            cmd = ['open', absolute_path]
        elif sys.platform.startswith('linux'):
            # Linux
            cmd = ['xdg-open', absolute_path]
        else:
            raise OSError("Unsupported operating system")

        # Execute the command to open the Excel file
        try:
            subprocess.run(cmd, check=True, shell=sys.platform.startswith('win32'))
        except Exception as e:
            print(f"An error occurred: {e}")

    def view_clean_data(self, kwargs):
        # Making sure the path is absolute
        # Making sure the path is absolute
        relative_path = kwargs['clean_path']
        full_path = self.results_directory + "\\" + relative_path

        absolute_path = os.path.abspath(full_path)
        print(absolute_path)

        # Determine the platform and construct the command
        if sys.platform.startswith('win32'):
            # Windows
            cmd = ['start', absolute_path]
        elif sys.platform.startswith('darwin'):
            # macOS
            cmd = ['open', absolute_path]
        elif sys.platform.startswith('linux'):
            # Linux
            cmd = ['xdg-open', absolute_path]
        else:
            raise OSError("Unsupported operating system")

        # Execute the command to open the Excel file
        try:
            subprocess.run(cmd, check=True, shell=sys.platform.startswith('win32'))
        except Exception as e:
            print(f"An error occurred: {e}")

    def make_diagrams(self, relative_path):
        print("Making Diagrams")
        diagramMaker = DataAnalyzer(self.results_directory, relative_path)

        diagramMaker.read_data()
        print("Read data from clean file\n")
        diagramMaker.preprocess_data()
        print("Preprocessed data\n")

        diagramMaker.plot_keyword_frequency()
        print("Plotted Keyword Frequency\n")
        diagramMaker.plot_keywords_vs_location()
        print("Plotted Keyword Frequency vs Location\n")
        diagramMaker.plot_posts_vs_region()
        print("Plotted Posts vs Region\n")
        print("Diagrams made\n")

    def view_diagram_dir(self, kwargs):
        # Extract the relative path from the kwargs dictionary
        relative_path = kwargs.get('diagram_path')
        if not relative_path:
            print("Error: No diagram path provided.")
            return  # Exit the function if no path is provided

        # Construct the full path by combining the results directory with the relative path
        full_path = os.path.join(self.results_directory, relative_path)

        # Convert to absolute path to ensure compatibility across different operations
        absolute_path = os.path.abspath(full_path)
        absolute_path = absolute_path + "\\diagrams"
        print("Attempting to open:", absolute_path)

        # Check if the path exists
        if not os.path.exists(absolute_path):
            self.make_diagrams(relative_path)

        # Determine the platform and construct the command to open the directory
        if sys.platform.startswith('win32'):
            # Windows: 'explorer' opens File Explorer
            cmd = ['explorer', absolute_path]
        elif sys.platform.startswith('darwin'):
            # macOS: 'open' opens Finder
            cmd = ['open', absolute_path]
        elif sys.platform.startswith('linux'):
            # Linux: 'xdg-open' opens the default file manager
            cmd = ['xdg-open', absolute_path]
        else:
            raise OSError("Unsupported operating system")

        # Execute the command to open the directory
        try:
            subprocess.run(cmd, check=True, shell=sys.platform.startswith('win32'))
        except Exception as e:
            print(f"An error occurred while trying to open the directory: {e}")

    def debug_print(self):
        print("stored result directory",self.results_directory)
