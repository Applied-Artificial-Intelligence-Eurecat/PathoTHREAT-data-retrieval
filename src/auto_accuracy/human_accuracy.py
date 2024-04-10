import pandas as pd

# Path to your .xlsb file
file_path = '../../results/llama_human_eval.xlsb'

# Using pandas with the pyxlsb engine to read data
df = pd.read_excel(file_path, sheet_name='Sheet1', engine='pyxlsb')

# Extracting the "answers" column
answers_column = df['ANSWER']

# Counting the number of entries that are equal to 1
num_ones = answers_column[answers_column == 1].count()

# Calculating the total length of the "answers" column
total_entries = len(answers_column)

# Calculating the proportion of 1's
proportion_of_ones = num_ones / total_entries

print(f"Proportion of 1's in the 'answers' column: {proportion_of_ones}")