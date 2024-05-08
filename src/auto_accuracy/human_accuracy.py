
import pandas as pd
import numpy as np

def load_and_process_data(file_path):
    # Load data from the Excel file
    data = pd.read_excel(file_path, sheet_name='Sheet1', engine='pyxlsb').iloc[:, :5]

    # Remove rows with any empty cells
    data_cleaned = data.dropna(how='all').reset_index(drop=True)
    
    group_indices = []
    for i in range(23):
        local_indices = []
        for j in range(i,len(data_cleaned), 23):
            local_indices.append(j)
        group_indices.append(local_indices)


    # Initialize a dictionary to hold the ratios
    group_ratios = {}

    for group_i in group_indices: 
        # Get the subset of rows for each group
        group = data_cleaned.iloc[group_i]

        # Calculate the ratio of True (1.0) to False (0.0) in the "ANSWER" column
        true_count = group['ANSWER'].sum()
        total_count = len(group)
        
        # Avoid division by zero if total_count is 0
        if total_count > 0:
            ratio = true_count / total_count
        else:
            ratio = None
        
        # Store the ratio in the dictionary with the start row as the key
        group_ratios[group_i[0]] = ratio
    
    return group_ratios

# Path to the Excel file
file_path = '../../results/llama_human_eval.xlsb'

# Call the function to process the data
ratios = load_and_process_data(file_path)
print(ratios)
