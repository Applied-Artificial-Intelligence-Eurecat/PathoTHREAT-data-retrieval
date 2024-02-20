import os, re

# Define the path to the directory containing the JSON files
directory_path = '../../data/text'

# Regular expression pattern to match the "context" parameter and its text content
pattern = re.compile(r'"context":\s*"(.*?)"(?=,|\s*\})', re.DOTALL)

# Loop through each file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.txt'):  # Check if the file is a .txt file
        file_path = os.path.join(directory_path, filename)

        # Read the file data
        with open(file_path, 'r') as file:
            file_data = file.read()

        # Search for the 'context' parameter and extract its value
        matches = pattern.search(file_data)
        if matches:
            context = matches.group(1)  # Extract the context text

        # Replace the file content with just the 'context' value
        with open(file_path, 'w') as file:
            file.write(context)

