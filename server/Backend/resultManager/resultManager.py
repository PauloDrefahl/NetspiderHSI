import json
import logging
import webbrowser
import os
import sys
import subprocess
from Backend.resultManager.makeDiagramsBetter import DataAnalyzer

from flask import jsonify

logger = logging.getLogger(__name__)


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
        try:
            if not os.path.exists('folders.json'):
                self.update_folders_json()

            with open('folders.json', 'r') as f:
                folders = json.load(f)
            return folders
        except FileNotFoundError:
            logger.debug("folders.json not found, creating")
            self.update_folders_json()
            return self.get_folders()
        except Exception as e:
            logger.error("Error getting folders: %s", str(e))
            return {"error": str(e)}, 500

    def update_folders_json(self):
        try:
            all_entries = os.listdir(self.results_directory)
            all_folders = [e for e in all_entries if os.path.isdir(os.path.join(self.results_directory, e))]
            all_folders.sort()
            with open('folders.json', 'w') as f:
                json.dump(all_folders, f, indent=2)
        except Exception as e:
            logger.error("Error updating folders list: %s", e)

    def view_pdf(self, kwargs):
        relative_path = kwargs['pdf_path']
        absolute_path = os.path.abspath(os.path.join(self.results_directory, relative_path))
        try:
            # Open the PDF file in the default application
            webbrowser.open('file://' + absolute_path)
            return 0
        except Exception as e:
            logger.error("Error opening PDF: %s", e)
            return 1

    def view_ss_dir(self, kwargs):
        relative_path = kwargs['ss_path']
        absolute_path = os.path.abspath(os.path.join(self.results_directory, relative_path))

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
        relative_path = kwargs['raw_path']
        absolute_path = os.path.abspath(os.path.join(self.results_directory, relative_path))

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
            logger.error("Error opening raw data: %s", e)

    def view_clean_data(self, kwargs):
        relative_path = kwargs['clean_path']
        absolute_path = os.path.abspath(os.path.join(self.results_directory, relative_path))

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
            logger.error("Error opening clean data: %s", e)

    def make_diagrams(self, relative_path):
        diagramMaker = DataAnalyzer(self.results_directory, relative_path)
        diagramMaker.read_data()
        diagramMaker.preprocess_data()
        diagramMaker.plot_keyword_frequency()
        diagramMaker.plot_keywords_vs_location()
        diagramMaker.plot_posts_vs_region()

    def view_diagram_dir(self, kwargs):
        # Extract the relative path from the kwargs dictionary
        relative_path = kwargs.get('diagram_path')
        if not relative_path:
            logger.error("No diagram path provided")
            return

        absolute_path = os.path.abspath(os.path.join(self.results_directory, relative_path, "diagrams"))

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
            logger.error("Error opening diagram directory: %s", e)
