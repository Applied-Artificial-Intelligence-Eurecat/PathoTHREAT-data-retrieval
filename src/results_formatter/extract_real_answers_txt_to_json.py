import re
import json

file_path = '../../results/answers.txt'

with open(file_path, 'r') as file:
    content = file.read()

# Define a pattern to match the titles, which start with a number followed by a period
title_pattern = re.compile(r'^\d+', re.MULTILINE)
answers_pattern = re.compile(r'answers\s*=\s*\[(.*?)\]', re.DOTALL)

def clean_answers(answers_text):
    # Remove the "answers = [" part and the closing "]" bracket, then split by comma
    answers_cleaned = answers_text[10:-1]  # This removes 'answers = [' at the start and ']' at the end
    # Use regex to split on commas while ignoring commas in quotes
    answers = re.split(r',(?!\s*")', answers_cleaned)
    # Remove leading and trailing quotes and spaces from each answer
    cleaned_answers = [ans.strip(' "\n') for ans in answers]
    return cleaned_answers

# Initialize an empty list to hold all papers with titles and answers
papers_data = []

# Extract titles and their corresponding sections
titles_matches = title_pattern.findall(content)
answers_matches = answers_pattern.findall(content)

# Process each title and its corresponding section
for title, answers in zip(titles_matches, answers_matches):
    # Extract and clean the answers
    # Find the start of the answers list until the start of the next title
    answers_list = [answer.strip(' "').replace('",', '').replace('"', '') for answer in answers.splitlines()]
    answers_list = ["" if item == "," else item for item in answers_list]
    papers_data.append({
        "title": title.strip(),
        "answers": answers_list
    })

# Convert the dictionary to JSON format
json_data = json.dumps(papers_data, indent=4)

# Define the JSON file path
json_file_path = '../../data/correct_answers_real.json'

# Write the JSON data to a file
with open(json_file_path, 'w') as json_file:
    json_file.write(json_data)# Convert the dictionary to JSON format
