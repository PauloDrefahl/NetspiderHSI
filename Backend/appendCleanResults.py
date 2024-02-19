import pandas as pd

# Paths to your CSV files
files = ['data_jan.csv', 'data_feb.csv', 'data_mar.csv']

# Read each CSV file into a list of DataFrames
dfs = [pd.read_csv(file) for file in files]

# Concatenate all DataFrames into a single DataFrame
combined_df = pd.concat(dfs, ignore_index=True)

# Save the combined DataFrame to a new CSV file
combined_df.to_csv('combined_data.csv', index=False)