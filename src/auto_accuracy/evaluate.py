'''
The objective of this script is to implement a 
Voting system that automatically evaluates the 
accuracy between any results file and its correctly 
labelled answers.
===============================================
Call this file from the project root.
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

# Prompt used by each model
prompt="""
I will provide two text strings below. 
Please analyze them and determine if they convey the same contextual information. 
It's important to consider their meanings, implications, and nuances rather than just the words used. 
After your analysis, respond with 'Yes' if they share the same context, or 'No' if they do not.

String 1: {candidate}
String 2: {reference}

Do these two strings have the same contextual information? Yes or No.
"""

# Carregar un a un model bucle for
def load_model(model_name):
    # Local Llamacpp model
    return LlamaCpp(
        model_path=model_name,
        n_gpu_layers=cfg.GPU_LAYERS,
        temperature=cfg.TEMPERATURE,
        max_tokens=cfg.MAX_NEW_TOKENS,
        n_batch=1024,
        n_ctx=cfg.CONTEXT_LENGTH,
        verbose=False,
        use_mlock=True,
        streaming=False,
        seed=42
    )

def democracy(votes):
    # Transpose matrix
    transposed_matrix = [list(row) for row in zip(*votes)]
    
    # Count elements in each list of the transposed matrix
    votes_count = [Counter(row) for row in transposed_matrix]

    counts = []
    # Display the counts for each list
    for counter in votes_count:
        counts.append(1 if counter['yes'] > counter['no'] else 0)

    return counts

def model_evaluation(references, candidates):
    votes = []
    # Extracting scores
    for model_name in files_ending_with_gguf:
        model_votes = []
        llm = load_model(model_name)
        # for each reference and candidate, predict
        for reference, candidate in zip(references, candidates):
            model_votes.append(llm(prompt.format(candidate=candidate, reference=reference)))
        del llm
        votes.append(model_votes)
    decisions = democracy(votes)
    total_correct = sum(decisions)  # Sum of 1s
    total_predictions = len(decisions)  # Total number of predictions
    accuracy = total_correct / total_predictions
    return accuracy

def evaluate():
    # Llegir json de results i de data.
    model = 'llama-2-7b-chat.Q4_0'
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

    scoring = []
    for z in range(23):
        # Extracting scores
        accuracy = model_evaluation(references[z], candidates[z])
        scoring.append({
            'Question': z+1, # Question id being evaluated
            'accuracy': accuracy
        })
