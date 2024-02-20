from bert_score import score
import re
'''
We want evaluate:
- Context relevance with precision, recall, f1. BERT used for that.
- When there should be no answer, does the LLM infer something from the context?
- Use a human, boolean evaluation to evaluate correct extraction.
'''


# Bert: compute similarity scores between generated text and reference text.
def evaluate_bert(references, candidates):
    #references = ["This is a reference sentence."]
    #candidates = ["This is a candidate sentence."]
    if len(references) == 0:
        return "No", "No", "No"
    P, R, F1 = score(candidates, references, lang='en')
    
    return str(P.mean().numpy()), str(R.mean().numpy()), str(F1.mean().numpy())


def evaluate_empty(references, candidates):
    # Detected problems. The model instead of returning "" always returns Not specified (or specify), not provide, not mention.
    correct = sum(1 for a, b in zip(references, candidates) if a == "" and b == "")
    if len(references) == 0:
        return "No empties"
    return correct/len(references)*100

def replace_not_specified_strings(input_string):
    pattern = re.compile(r'not\s+(specified|specify|provide|mention)', re.IGNORECASE)
    if pattern.search(input_string):
        return ""
    return input_string

def evaluate_registers(predicted_answers, correct_answers):
    '''
    PREDICTIONS FORMAT
    [
        {
        file_name: ...
        questions: [q, ...]
        responses: [response, ...]
        },
        ...
    ]
    ANSWERS FORMAT
    [
        {
        "title": ...
        "answers": [...]
        },
        ...
    ]
    PREDICT FORMAT
    [
    ["", "", "", ...],
    ...
    ]
    BLEU TEST FORMAT
    [  
    ["", "", "", ...],
    ...
    ]
    BERT TEST FORMAT
    [  
    ["", "", "", ...],
    ...
    ]
    '''
    references = [[] for _ in range(23)]
    candidates = [[] for _ in range(23)]
    empty_references = [[] for _ in range(23)]
    empty_candidates = [[] for _ in range(23)]
    # iterating each document to format the predict - test into a correct format.
    for i in range(len(predicted_answers)):
        for z in range(23):
            # Extract empty strings, so that scorers can work well.
            if correct_answers[i]['answers'][z] == "":
                empty_candidates[z].append(replace_not_specified_strings(predicted_answers[i]['responses'][z]))
                empty_references[z].append(correct_answers[i]['answers'][z])
            else:
                references[z].append(predicted_answers[i]['responses'][z])
                candidates[z].append(correct_answers[i]['answers'][z])

    scoring = []
    for z in range(23):
        # Extracting scores
        precision, recall, f1_score = evaluate_bert(references[z], candidates[z])
        empty_score = evaluate_empty(empty_references[z], empty_candidates[z])
        scoring.append({
            'Question': z+1, #Question id being evaluated
            'precision_bert': precision,
            'recall_bert': recall,
            'f1_score': f1_score,
            'empty_score': empty_score
        })
    
    return scoring
