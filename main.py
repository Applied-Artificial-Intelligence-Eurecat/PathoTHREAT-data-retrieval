import box
import timeit
import yaml
import json
import os
import sys
from dotenv import find_dotenv, load_dotenv
from src.predict import set_qa_prompt, predict_all_files, predict_query
from src.llm import build_llm
from src.evaluate import evaluate_registers

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))

with open('questions/questions.txt', 'r') as file:
    questions = [line.rstrip() for line in file]

def sort_key(filename):
    # Extract the prefix number (assuming the format is number_*)
    prefix_num = filename.split('_')[0]
    # Convert the prefix to integer for numeric sorting
    return int(prefix_num)

def read_txts():
    txt_files_content = []

    files = os.listdir('data/text/')
    sorted_files = sorted(files, key=sort_key)

    for filename in sorted_files:
        file_path = os.path.join('data/text/', filename)
        # Open and read the content of the txt file
        with open(file_path, 'r') as file:
            content = file.read()
            # Append content to the list
            txt_files_content.append(content)
    return txt_files_content, sorted_files

def read_correct_answers():
    with open('data/real_answers.json', 'r') as file:
        answers = json.load(file)
    return answers

def save_results(results, path):
    with open(path, 'w') as file:
        json.dump(results, file, indent=4)


def select_execution_mode():
    llm = build_llm()
    qa_prompt = set_qa_prompt()

    if len(sys.argv) > 1:
        # Context input
        context = sys.argv[1]
        print("Text input detected")
        start = timeit.default_timer()
        predict_query(context, questions, llm, qa_prompt)
        end = timeit.default_timer()
        print(f"Time to retrieve response: {end - start} seconds")
    else:
        print("Predicting saved files.")
        # No context input
        txt_files_content, txt_files_names = read_txts()
        results = predict_all_files(txt_files_content, txt_files_names, questions, llm, qa_prompt)

        # save results
        save_results(results, 'results/results-'+cfg.MODEL+'.json')
        print("Predictions done.\n ----- \n Evaluation starting.")
        with open('results/results-'+cfg.MODEL+'.json', 'r') as file:
            results = json.load(file)

        # evaluate
        answers = read_correct_answers()
        scores = evaluate_registers(results, answers)

        # save scores
        save_results(scores, 'results/scores-'+cfg.MODEL+'.json')
        print("Evaluation DONE")


if __name__ == "__main__":
    select_execution_mode()
