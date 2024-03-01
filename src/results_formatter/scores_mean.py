import json
from statistics import mean

# Given JSON data
with open('../../results/scores.json', 'r') as file:
    data = json.load(file)

# Convert JSON values to floats where necessary
for item in data:
    item['precision_bert'] = float(item['precision_bert']) if item['precision_bert']!='No' else None
    item['recall_bert'] = float(item['recall_bert']) if item['recall_bert']!='No' else None
    item['f1_score'] = float(item['f1_score']) if item['f1_score']!='No' else None
    item['empty_score'] = float(item['empty_score']) if item['empty_score']!='No empties' else None
print([item['recall_bert'] for item in data if item['recall_bert'] is not None])
# Calculate means, ignoring None values
precision_bert_mean = mean(item['precision_bert'] for item in data if item['precision_bert'] is not None)
recall_bert_mean = mean(item['recall_bert'] for item in data if item['recall_bert'] is not None)
f1_score_mean = mean(item['f1_score'] for item in data if item['f1_score'] is not None)
empty_score_mean = mean(item['empty_score'] for item in data if item['empty_score'] is not None)

print(f"Precision Bert Mean: {precision_bert_mean}")
print(f"Recall Bert Mean: {recall_bert_mean}")
print(f"F1 Score Mean: {f1_score_mean}")
print(f"Empty Score Mean: {empty_score_mean}")