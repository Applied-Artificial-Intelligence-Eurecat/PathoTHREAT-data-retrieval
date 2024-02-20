'''
===========================================
        Module: Prompts collection
===========================================
'''
# Note: Precise formatting of spacing and indentation of the prompt template is important for Llama-2-7B-Chat,
# as it is highly sensitive to whitespace changes. For example, it could have problems generating
# a summary from the pieces of context if the spacing is not done correctly

qa_template = """Use the following information to answer the user's question.
If the text does not contain the information, just say Not specified.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""
