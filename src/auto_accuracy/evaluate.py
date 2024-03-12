'''
The objective of this script is to implement a 
Voting system that automatically evaluates the 
accuracy between any results file and its correctly 
labelled answers.
'''
import json
import box
import yaml
import glob
from collections import Counter
from langchain_community.llms import LlamaCpp
from dotenv import find_dotenv, load_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Llegir carpeta models, tots arxius acabats amb gguf.
files_ending_with_gguf = glob.glob('models/*gguf')

# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))

model = 'mistral-7b-instruct-v0.2.Q8_0'

# Prompt used by each model
prompt="""
I will provide two text strings below. Do these two strings have the same contextual information?
After your analysis, respond with 'yes' if they share the same context, or 'no' if they do not.

String 1: {candidate}
String 2: {reference}

Answer only yes or no. Further wording is useless.

The answer is:
"""

# Carregar un a un model bucle for
def load_model(model_name):
    # Local Llamacpp model
    return LlamaCpp(
        model_path=model_name,
        n_gpu_layers=100,
        temperature=0.01,
        max_tokens=5,
        n_batch=1024,
        n_ctx=2500,
        verbose=False,
        use_mlock=True,
        streaming=False,
        seed=42
    )


def count_strings_with_yes_no(string_list):
    # Initialize a counter for strings containing "yes" or "no"
    ycount = 0
    ncount = 0

    # Iterate through each string in the list
    for s in string_list:
        # Check if "yes" or "no" is in the string (case-insensitive)
        if "yes" in s.lower() and "no" not in s.lower():
            ycount += 1
        elif "no" in s.lower() and "yes" not in s.lower():
            ncount += 1

    return 1 if ycount > ncount else 0


def democracy(votes):
    # Transpose matrix
    transposed_matrix = [list(row) for row in zip(*votes)]
    
    # Count elements in each list of the transposed matrix
    votes_count = [count_strings_with_yes_no(row) for row in transposed_matrix]

    return votes_count

def model_evaluation(references, candidates):
    votes = []
    # Extracting scores
    for model_name in files_ending_with_gguf:
        model_votes = []
        with open('results/logs.txt', 'a') as file:
            file.write('========\n')
            file.write('Loading model: '+model_name)
        llm = load_model(model_name)
        # for each reference and candidate, predict
        for reference, candidate in zip(references, candidates):
            #Reducing string to approchimatelly <2000 tokens
            vote = llm(prompt.format(candidate=candidate[:10000], reference=reference))
            model_votes.append(vote)
            with open('results/logs.txt', 'a') as file:
                file.write('\nModel votes: '+ vote)
        del llm
        votes.append(model_votes)
    decisions = democracy(votes)
    total_correct = sum(decisions)  # Sum of 1s
    total_predictions = len(decisions)  # Total number of predictions
    accuracy = total_correct / total_predictions
    return accuracy

def evaluate(current_scores):
    # Llegir json de results i de data.
    with open('results/results-'+model+'.json', 'r') as file:
        predicted_answers = json.load(file)
    with open('data/real_answers.json', 'r') as file:
        correct_answers = json.load(file)

    # Preparar el array de candidate i response.
    references = [[] for _ in range(23)]
    candidates = [[] for _ in range(23)]
    # iterating each document to format the predict - test into a correct format.
    for i in range(len(predicted_answers)):
        for z in range(23):
            # Extract empty strings, so that scorers can work well.
            if correct_answers[i]['answers'][z] != "":
                references[z].append(predicted_answers[i]['responses'][z])
                candidates[z].append(correct_answers[i]['answers'][z])

    for z in range(23):
        # Extracting scores
        accuracy = model_evaluation(references[z], candidates[z])
        current_scores[z]['voting_accuracy'] = accuracy

    return current_scores


if __name__ == "__main__":
    with open('results/scores-'+model+'.json', 'r') as file:
        current_scores = json.load(file)
    
    scoring = evaluate(current_scores)
    
    with open('results/scores-'+model+'.json', 'w') as file:
        json.dump(scoring, file, indent=4)
