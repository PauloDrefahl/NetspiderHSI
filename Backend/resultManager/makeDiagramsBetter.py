import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class DataAnalyzer:
    def __init__(self, results_directory, selected_folder):

        # inputted directories
        self.results_directory = results_directory
        self.selected_folder = selected_folder

        print(self.results_directory + "\n")
        print(self.selected_folder + "\n")

        # the new diagram dir
        self.selected_result_folder_path = os.path.join(self.results_directory, self.selected_folder)
        self.new_diagram_folder_path = self.selected_result_folder_path + "\\diagrams"
        print(self.selected_result_folder_path + "\n")
        print(self.new_diagram_folder_path + "\n")


        # creates the directory
        self.create_diagrams_directory()
        self.df = None

        # Define column names as attributes for easy access
        self.postId_column = 'Post-identifier'
        self.link_column = 'Link'
        self.city_column = 'Inputted City / Region'
        self.specified_location_column = 'Specified Location'
        self.timeline_column = 'Timeline'  # replace with your actual column name
        self.contacts_column = 'Contacts'
        self.personal_info_column = 'Personal Info'
        self.overall_desc_column = 'Overall Description'
        self.payment_methods_column = 'Payment-methods'
        self.socialMedia_found_column = 'Social-media-found'
        self.keywords_found_column = 'Keywords-found'
        self.number_of_keywords_found_column = 'Number-of-keywords-found'

        # setting up preprocessing variables
        self.df_exploded_social_media = None
        self.df_exploded_keywords = None

    def create_diagrams_directory(self):
        try:
            os.makedirs(self.new_diagram_folder_path, exist_ok=True)
            print("Directory created successfully or already exists.")
        except Exception as e:
            print(f"Error creating directory: {e}")

    def read_data(self):
        spreadsheet_name = 'CLEAN-' + self.selected_folder + '.xlsx'
        file_path = self.selected_result_folder_path + "\\" + spreadsheet_name
        print("selected file path", file_path)
        if os.path.exists(file_path):
            self.df = pd.read_excel(file_path)
        else:
            print("Spreadsheet does not exist in the specified path.")

    def preprocess_data(self):
        if self.df is not None:
            self.df['Keywords-found-list'] = self.df[self.keywords_found_column].apply(
                lambda x: x.split(',') if pd.notnull(x) and x.strip().lower() != 'service' else [])
            self.df['Social-media-found-list'] = self.df[self.socialMedia_found_column].apply(
                lambda x: x.replace('\n', ',').split(',') if pd.notnull(x) else [])
            self.df_exploded_keywords = self.df.explode('Keywords-found-list')
            self.df_exploded_social_media = self.df.explode('Social-media-found-list')
        else:
            print("Data frame is empty. Ensure data is read correctly before preprocessing.")

    def plot_keywords_vs_location(self):
        if self.df_exploded_keywords is not None:
            print("Plotting keywords vs location.")
            location_keyword_counts = self.df_exploded_keywords.groupby(
                [self.city_column, 'Keywords-found-list']).size().unstack(fill_value=0)

            top_keywords = self.df_exploded_keywords['Keywords-found-list'].value_counts().head(10).index
            filtered_location_keyword_counts = location_keyword_counts[top_keywords]

            plt.figure(figsize=(12, 8))
            sns.heatmap(filtered_location_keyword_counts, annot=True, cmap='viridis', fmt='g')
            plt.title('Keywords Frequency by Location')
            plt.xlabel('Keywords')
            plt.ylabel('Inputted City / Region')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig(self.new_diagram_folder_path + '\\keywords-vs-location.png')
            plt.close()

    def plot_posts_vs_region(self):
        if self.df is not None:
            print("plotting posts vs region\n")
            posts_per_location = self.df.groupby(self.city_column).size()

            plt.figure(figsize=(12, 8))
            posts_per_location.sort_values(ascending=False).plot(kind='bar')
            plt.title('Number of Posts by Location')
            plt.xlabel('Inputted City / Region')
            plt.ylabel('Number of Posts')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            plt.savefig(self.new_diagram_folder_path + '\\posts-vs-location.png')
            plt.close()

    def plot_keyword_frequency(self):
        if self.df is not None:
            print("plotting the keyword freq")
            # Set the figure size to make it larger
            plt.figure(figsize=(12, 8))

            # Calculate keyword frequencies and keep the top N for a cleaner plot
            top_n = 20  # Adjust based on how many you wish to display
            keyword_counts = self.df_exploded_keywords['Keywords-found-list'].value_counts().head(20)  # Top 20 keywords

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

            plt.savefig(self.new_diagram_folder_path + '\\keyword-frequency.png', dpi=300)
            plt.show()

    def plot_location_vs_payment(self):
        if self.df is not None:
            sns.barplot(x=self.city_column, y=self.payment_methods_column, data=self.df)
            plt.title('Location vs. Payment')
            plt.xticks(rotation=45)  # Rotate labels if they overlap
            # plt.savefig(plot_filename_location_vs_payment)  # Save the plot
            plt.show()

    def plot_location_vs_social_media(self):
        if self.df is not None:
            # Filter out empty strings which might have come from the split operation
            df_exploded_social_media = self.df_exploded_social_media['Social-media-found-list'].str.strip() != ''

            # Calculating social media presence by location
            social_media_mapping = {
                'snap': 'Snapchat',
                'snapchat': 'Snapchat',
                'whatsapp': 'WhatsApp',
                'telegram': 'Telegram',
                # Add more mappings as needed
            }

            # Assuming 'Social-media-found-list' is the column after exploding and cleaning
            df_exploded_social_media['Normalized Social Media'] = df_exploded_social_media[
                'Social-media-found-list'].map(social_media_mapping).fillna(
                df_exploded_social_media['Social-media-found-list'])

            ## Aggregate data by location and normalized social media name
            normalized_social_media_counts = df_exploded_social_media.groupby(
                ['Inputted City / Region', 'Normalized Social Media']).size().unstack(fill_value=0)

            # Plotting
            normalized_social_media_counts.plot(kind='bar', stacked=True, figsize=(12, 8))
            plt.title('Normalized Social Media Presence by Location')
            plt.xlabel('Inputted City / Region')
            plt.ylabel('Counts')
            plt.xticks(rotation=45)
            plt.legend(title='Social Media')
            plt.tight_layout()
            plt.show()


# Usage
# results_directory = 'C:\\Users\\kskos\\PycharmProjects\\HSI_Back_Test3\\result'
# selected_folder = 'yesbackpage-florida-2024-02-24_04-51-07'
#
# analyzer = DataAnalyzer(results_directory, selected_folder)
#
# analyzer.read_data()
#
# analyzer.preprocess_data()
#
# analyzer.plot_keywords_vs_location()
#
# analyzer.plot_posts_vs_region()
#
# analyzer.plot_keyword_frequency()

#analyzer.plot_location_vs_social_media()
#analyzer.plot_location_vs_payment()

