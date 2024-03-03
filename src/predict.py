'''
===========================================
        Module: Util functions
===========================================
'''
import box
import yaml
from langchain.prompts import PromptTemplate
from src.prompts import qa_template


# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


def set_qa_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(template=qa_template,
                            input_variables=['context', 'question'])
    return prompt


def predict_query(context, questions, llm, qa_prompt):
    for q in questions:
        print(q)
        response = llm(
                    qa_prompt.format(
                        context=context, 
                        question=q)
                )
        print(f'\nAnswer: {response}')
        print('='*50)


def predict_all_files(txt_files_content, txt_files_names, questions, llm, qa_prompt):
    for i_text in range(len(txt_files_content)):
        print(txt_files_names[i_text])
        for q in questions:
            response = llm(
                qa_prompt.format(
                    context=txt_files_content[i_text], 
                    question=q)
            )
            print(f'\nAnswer: {response}')
            print('='*50)

import json

def predict_all_files(txt_files_content, txt_files_names, questions, llm, qa_prompt):
    results = []  # List to hold all results as JSON objects
    '''
    Expected output:
    [
     {
     file_name: ...
     questions: [q, ...]
     responses: [response, ...]
     },
    ...
    ]
    '''

    for i_text in range(len(txt_files_content)):
        print(txt_files_names[i_text])
        responses = []

        for q in questions:
            response = llm(
                qa_prompt.format(
                    context=txt_files_content[i_text], 
                    question=q)
            )
            responses.append(response)

        # Prepare a dictionary with the questions and responses
        result_dict = {
            "file_name": txt_files_names[i_text],
            "questions": questions,
            "responses": responses
        }

        # Add the dict object to the results list
        results.append(result_dict)  # Storing the dictionary directly

    return results
