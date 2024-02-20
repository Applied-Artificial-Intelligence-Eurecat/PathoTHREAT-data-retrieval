import json
import re

# Define the list of questions
questions = [
    "Date of Event: When did the contamination event occur?",
    "Event Location: Where did the contamination event take place?",
    "Event Description: Can you provide a summary of the contamination event?",
    "Initial Cause: What triggered the onset of the contamination event or outbreak?",
    "Contamination Source: What was identified as the origin of the contamination?",
    "Detection Method: How was the contamination event first discovered?",
    "Exposure and Hospitalization: How many individuals were exposed to the contaminant, and how many were hospitalized as a result?",
    "Illness Count: What was the number of people who fell ill due to the event?",
    "Attack Rate: What is the ratio of individuals who became ill to those who were exposed?",
    "Fatality Count: How many fatalities were associated with the contamination event?",
    "Pathogens Identified: What pathogens were found in the collected samples?",
    "Symptoms: What symptoms were associated with the contamination?",
    "Investigation Steps: What were the initial actions taken to investigate or inspect the event?",
    "Investigation Details: Can you describe the detailed investigation or inspection that was conducted?",
    "Case Definition: What is the case definition used for the cohort study?",
    "Risk Factors: Which risk factors were identified during the investigation?",
    "Event Duration: Over what period did the contamination event span?",
    "Mitigation Steps: What immediate actions were taken to mitigate the effects of the contamination (e.g., boil water advisory, stopping water supply, chlorination)?",
    "Event Monitoring: What types of water analyses were performed during the monitoring phase?",
    "Monitoring Results: What concentrations of contaminants were detected in the post-event analysis?",
    "Restoration Actions: What steps were taken to restore the system to normal operation?",
    "Prevention Measures: What measures have been implemented to prevent future contamination events?",
    "Demographics: What is the age range of the individuals affected by the event?"
]

# Load the real answers from the JSON file
with open('../../data/correct_answers_real.json', 'r') as json_file:
    real_answers_data = json.load(json_file)

# Read the content of the uploaded text file
file_path = '../../results/results.txt'
with open(file_path, 'r') as file:
    content = file.read()

# Split the content by file titles to separate papers
papers = re.split(r'^\d+.*\.txt', content, flags=re.MULTILINE)

# Gather the file titles
titles = re.findall(r'^\d+.*\.txt', content, re.MULTILINE)

# Remove the first element if it is empty (due to split)
if papers and not papers[0].strip():
    papers.pop(0)

# Function to parse answers from a given text
def parse_answers(text):
    # Split by the '=====' separator
    answers = re.split(r'={50}', text)
    # Remove whitespace and the 'Answer:' prompt
    answers = [re.sub(r'Answer:\s*', '', ans).strip() for ans in answers if ans.strip()]
    return answers

# Function to extract the numeric prefix from a string
def extract_numeric_prefix(s):
    match = re.match(r'^(\d+)', s)
    return match.group(1) if match else None

# Process each paper and extract the information
json_output = []

for i in range(len(papers)):
    # Split by lines and extract the first line as the file name
    lines = papers[i].strip().split('\n')
    file_name = titles[i]
    answers_text = '\n'.join(lines)  # Join the rest of the lines for further processing
    answers = parse_answers(answers_text)

    # Extract the real answers from the loaded JSON data
    real_answers = []
    for item in real_answers_data:
        if extract_numeric_prefix(item['title']) == extract_numeric_prefix(file_name):
            real_answers = item['answers']



    # Construct the JSON structure for the current paper
    paper_dict = {
        'PaperName': file_name,
        'Questions': questions,
        'Answers': answers,
        'RealAnswers': real_answers
    }
    json_output.append(paper_dict)

# Convert to JSON string for display
json_string = json.dumps(json_output, indent=2)

# Save the JSON to a file
output_json_path = '../../results/parsed_results.json'
with open(output_json_path, 'w') as json_file:
    json_file.write(json_string)

