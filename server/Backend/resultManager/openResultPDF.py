import webbrowser
import os

# Path to your PDF file
pdf_file_path = '/result/yesbackpage-florida-2024-02-23_21-25-01/screenshots/yesbackpage-florida-2024-02-23_21-25-01.pdf'

# Making sure the path is absolute
absolute_path = os.path.abspath(pdf_file_path)

# Open the PDF file in the default application
webbrowser.open('file://' + absolute_path)
