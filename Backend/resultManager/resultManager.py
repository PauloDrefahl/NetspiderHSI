import webbrowser
import os
import sys
import subprocess


class resultManager:
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

    def make_diagrams(self, kwargs):
        print("")

    def view_diagram_dir(self, kwargs):
        # Making sure the path is absolute
        # Making sure the path is absolute
        relative_path = kwargs['diagram_path']
        print(relative_path)
        full_path = self.results_directory + "\\" + relative_path

        absolute_path = os.path.abspath(full_path)
        print(absolute_path)

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
        try:
            subprocess.run(cmd, check=True, shell=sys.platform.startswith('win32'))
        except Exception as e:
            print(f"An error occurred: {e}")

    def debug_print(self):
        print("stored result directory",self.results_directory)
