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
plot_filename_postNumber_vs_location = os.path.join(new_diagram_folder_path, 'posts-vs-location.png')
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

# Splitting the keywords into lists
# Splitting the 'Keywords-found' into lists and removing rows with 'service' as the only keyword
df['Keywords-found-list'] = df['Keywords-found'].apply(lambda x: x.split(',') if pd.notnull(x) and x.strip().lower() != 'service' else [])

# Splitting 'Social-media-found' into lists
df['Social-media-found-list'] = df['Social-media-found'].apply(lambda x: x.replace('\n', ',').split(',') if pd.notnull(x) else [])

# Exploding the DataFrame for keywords
df_exploded_keywords = df.explode('Keywords-found-list')

# Exploding the DataFrame for social media
df_exploded_social_media = df.explode('Social-media-found-list')

#df[payment_methods_column] = df[payment_methods_column].apply(lambda x: x.split(',') if pd.notnull(x) else [])

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
print(df[keywords_found_column])
print(df[socialMedia_found_column])
print(df[payment_methods_column])
'''
    ---------------------------------
    corelations
    ---------------------------------
'''

'''keyword vs location'''

location_keyword_counts = df_exploded_keywords.groupby(['Inputted City / Region', 'Keywords-found-list']).size().unstack(fill_value=0)

# You might want to focus on the top N keywords for clarity in the visualization
top_keywords = df_exploded_keywords['Keywords-found-list'].value_counts().head(10).index
filtered_location_keyword_counts = location_keyword_counts[top_keywords]

plt.figure(figsize=(12, 8))
sns.heatmap(filtered_location_keyword_counts, annot=True, cmap='viridis', fmt='g')
plt.title('Keywords Frequency by Location')
plt.xlabel('Keywords')
plt.ylabel('Inputted City / Region')
plt.xticks(rotation=45, ha='right')  # Rotate keywords for better visibility
plt.tight_layout()
plt.show()


'''posts vs region'''

# Counting the number of posts per location
posts_per_location = df.groupby('Inputted City / Region').size()

# Plotting the number of posts vs. location
plt.figure(figsize=(12, 8))
posts_per_location.sort_values(ascending=False).plot(kind='bar')  # Sort values for better visualization
plt.title('Number of Posts by Location')
plt.xlabel('Inputted City / Region')
plt.ylabel('Number of Posts')
plt.xticks(rotation=45, ha='right')  # Rotate location names for better visibility
plt.tight_layout()
plt.show()


'''keyword frequency'''

# Set the figure size to make it larger
plt.figure(figsize=(12, 8))

# Calculate keyword frequencies and keep the top N for a cleaner plot
top_n = 20  # Adjust based on how many you wish to display
keyword_counts = df_exploded_keywords['Keywords-found-list'].value_counts().head(20)  # Top 20 keywords

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


'''location vs payment'''

sns.barplot(x=city_column, y=payment_methods_column, data=df)
plt.title('Location vs. Payment')
plt.xticks(rotation=45)  # Rotate labels if they overlap
#plt.savefig(plot_filename_location_vs_payment)  # Save the plot
plt.show()


'''location vs social media'''

# Filter out empty strings which might have come from the split operation
df_exploded_social_media = df_exploded_social_media[df_exploded_social_media['Social-media-found-list'].str.strip() != '']

# Calculating social media presence by location
social_media_mapping = {
    'snap': 'Snapchat',
    'snapchat': 'Snapchat',
    'whatsapp': 'WhatsApp',
    'telegram': 'Telegram',
    # Add more mappings as needed
}

# Assuming 'Social-media-found-list' is the column after exploding and cleaning
df_exploded_social_media['Normalized Social Media'] = df_exploded_social_media['Social-media-found-list'].map(social_media_mapping).fillna(df_exploded_social_media['Social-media-found-list'])

## Aggregate data by location and normalized social media name
normalized_social_media_counts = df_exploded_social_media.groupby(['Inputted City / Region', 'Normalized Social Media']).size().unstack(fill_value=0)

# Plotting
normalized_social_media_counts.plot(kind='bar', stacked=True, figsize=(12, 8))
plt.title('Normalized Social Media Presence by Location')
plt.xlabel('Inputted City / Region')
plt.ylabel('Counts')
plt.xticks(rotation=45)
plt.legend(title='Social Media')
plt.tight_layout()
plt.show()


