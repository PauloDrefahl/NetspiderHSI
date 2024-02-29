'''
    ---------------------------------
    libraries
    ---------------------------------
'''

import re

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# ---- libraries ----
import pandas as pd
import os
from datetime import datetime
from shutil import copy2
from PyPDF2 import PdfMerger
import openpyxl
from openpyxl.utils import get_column_letter
pdf_merger = PdfMerger()

'''
    ---------------------------------
    Inputs for files to append and directory to save
    ---------------------------------
'''

results_directory = 'C:\\Users\\kskos\\PycharmProjects\\HSI_Back_Test3\\result'

'''
    ---------------------------------
    selected folders to process
    ---------------------------------
'''


selected_folder = 'yesbackpage-florida-2024-02-24_04-51-07'

'''
    ---------------------------------
    creating diagram folder and file names
    ---------------------------------
'''

selected_result_folder_path = os.path.join(results_directory, selected_folder)

# Create the new screenshot folder in the new folder directory
new_diagram_folder_path = os.path.join(selected_result_folder_path, 'diagrams')

# Adding a print statement to debug
print(f"Creating directory: {new_diagram_folder_path}")

# Use try-except block to catch any errors during directory creation
try:
    os.makedirs(new_diagram_folder_path, exist_ok=True)  # Make sure this line is executed without errors
    print("Directory created successfully or already exists.")
except Exception as e:
    print(f"Error creating directory: {e}")

# When saving a plot, specify the full path

plot_filename_keywords_vs_location = os.path.join(new_diagram_folder_path, 'keywords-vs-location.png')
plot_filename_location_vs_payment = os.path.join(new_diagram_folder_path, 'location-vs-payment.png')  # Corrected filename
plot_filename_location_vs_socialMedia = os.path.join(new_diagram_folder_path, 'location-vs-socialMedia.png')
plot_filename_keyword_frequency = os.path.join(new_diagram_folder_path, 'keyword-frequency.png')
'''
    ---------------------------------
    reading data
    ---------------------------------
'''

dataframes = []

# The spreadsheet file has the same name as the folder with a .xlsx extension
spreadsheet_name = 'CLEAN-' + selected_folder + '.xlsx'
file_path = os.path.join(selected_result_folder_path, spreadsheet_name)
if os.path.exists(file_path):
    df = pd.read_excel(file_path)
    dataframes.append(df)

'''
    ---------------------------------
    preprocessing
    ---------------------------------
'''
print(df.columns)

postId_column = 'Post-identifier'
link_column = 'Link'
city_column = 'Inputted City / Region'
specified_location_column = 'Specified Location'
timeline_column = 'Timeline'  # replace with your actual column name
contacts_column = 'Contacts'
personal_info_column = 'Personal Info'
overall_desc_column = 'Overall Description'
payment_methods_column = 'Payment-methods'
socialMedia_found_column = 'Social-media-found'
keywords_found_column = 'Keywords-found'
number_of_keywords_found_column = 'Number-of-keywords-found'

#df.replace(['N/A', "('N/A',)"], np.nan, inplace=True)

# For columns where 'N/A' means the data should be ignored, drop those cells.
# Assuming 'Timeline' is one such column, you would drop 'N/A' only from 'Timeline'
# but keep the rest of the row intact.
#df[timeline_column] = df[timeline_column].replace(['N/A', "('N/A',)", 'Posted on: N/A'], np.nan)

# Assuming 'text_column' contains the text with the dates


# Extract the date using a regular expression
#df[timeline_column] = df[timeline_column].str.extract(pattern)

# Convert the extracted date to a datetime object
#df[timeline_column] = pd.to_datetime(df[timeline_column], format='%d %B, %Y %H:%M')



# You can do this for other columns as needed.
# df['OtherColumn'] = df['OtherColumn'].replace(['N/A', "('N/A',)"], np.nan)

# Then, if you want to drop rows where all elements are np.nan you can use:
#df.dropna(how='all', inplace=True)

# Or if you want to drop rows where any element is np.nan you can use:
#df.dropna(how='any', inplace=True)

# Convert date columns to datetime format if not already and it's not 'N/A'
# Note: You need to ensure 'date_column' does not contain 'N/A' before converting.
#df[timeline_column] = pd.to_datetime(df[timeline_column], errors='coerce')
print(df[timeline_column])
print(df[city_column])
'''
    ---------------------------------
    corelations
    ---------------------------------
'''

# location vs timeline
plt.figure(figsize=(10, 8))  # Increase figure size
sns.lineplot(x=timeline_column, y=city_column, hue=city_column, data=df)
plt.title('Location vs. Timeline')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels
plt.tight_layout()  # Adjust layout to fit the figure and labels

# Optional: Change the size of the legend or relocate it
plt.legend(title='City', bbox_to_anchor=(1.05, 1), loc='upper left')

# Saving the plot with a higher resolution
#plt.savefig(plot_filename_keywords_vs_location, dpi=300)  # Save the plot with higher DPI for better quality
plt.show()

# location vs payment
sns.barplot(x=city_column, y=payment_methods_column, data=df)
plt.title('Location vs. Payment')
plt.xticks(rotation=45)  # Rotate labels if they overlap
#plt.savefig(plot_filename_location_vs_payment)  # Save the plot
plt.show()

# location vs social media
sns.countplot(x=city_column, hue=socialMedia_found_column, data=df)
plt.title('Location vs. Social Media Presence')
plt.xticks(rotation=45)
#plt.savefig(plot_filename_location_vs_socialMedia)  # Save the plot
plt.show()

# keyword frequency
# Set the figure size to make it larger
plt.figure(figsize=(12, 8))

# Calculate keyword frequencies and keep the top N for a cleaner plot
top_n = 20  # Adjust based on how many you wish to display
keyword_counts = df[keywords_found_column].value_counts().head(top_n)

# Create the bar plot
keyword_counts.plot(kind='bar')

plt.title('Top 20 Keyword Frequencies')
plt.xticks(rotation=45, ha='right')  # Rotate labels for better readability
plt.xlabel('Keywords')  # Optional: label the x-axis
plt.ylabel('Frequency')  # Optional: label the y-axis

# Adjust font size for x and y ticks if necessary
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels

# Optionally, save the plot with a higher resolution
#plt.savefig(plot_filename_keyword_frequency, dpi=300)

plt.show()

# keyword vs location

# keyword vs timeline

#  # posts vs timeline

#  # posts vs region

#  # of keywords found vs region

#  # of keywords found vs timeline


