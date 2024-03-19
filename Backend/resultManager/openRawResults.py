import subprocess
import sys
import os

# Path to your Excel file
excel_file_path = "/result/yesbackpage-florida-2024-02-23_21-25-01/RAW-yesbackpage-florida-2024-02-23_21-25-01.xlsx"

# Making sure the path is absolute
absolute_path = os.path.abspath(excel_file_path)

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
subprocess.run(cmd, check=True, shell=sys.platform.startswith('win32'))