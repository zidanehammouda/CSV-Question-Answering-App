
import re
from dotenv import load_dotenv 
import requests
import json
import os
load_dotenv()

import io
import sys
from openai import OpenAI


device = "cuda"

client = OpenAI(api_key=os.environ.get("OPEN_API_KEY"))


prompt_template = """df is a dataframe about {description}. df has these columns: {columns}. Write python code that answers this question: Print {question}
"""
description_template = """This is an example row of a given dataset titled {filename}.\n {example_row}. Complete this sentence with a maximum of 50 words: df is a dataframe about"""

suggestion_template = """This is an example row of a given dataset titled {filename}.\n {example_row}. Write 5 simple printing/visualizing questions about the dataset so I can solve it using code."""

libraries = """
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

"""

def extract_code(text):
    try:
        matches = []
        pattern = r"```python(.*?)```"
        if text:
            matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            return {'error':False,'response':matches[0]}
        else:
            return {'error':True,'response':text}
    except Exception as e:
        return {'error':True,'response':e}
    
def execute(code,namespace):
    try:
        buffer = io.StringIO()
        sys.stdout = buffer
        exec(libraries+code,namespace)

        sys.stdout = sys.__stdout__

        return buffer.getvalue()

    except Exception as e:
        return f'Execution error: {e}'

def describe_file(df,filename):
    first_row = df.iloc[0].to_dict()
    prompt = description_template.format(filename=filename,example_row=first_row)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )
    text_response = response.choices[0].message.content
    return text_response

def run(namespace,description,columns,question):
    prompt = prompt_template.format(description=description,columns=columns,question=question)
    request = {
    'url' : os.environ.get("MODEL_URL"),
    'payload' : json.dumps({"prompt": prompt}),
    'headers' : {
    'Content-Type': 'application/json'
    }
}
    full_response = requests.request("POST", request['url'], headers=request['headers'], data=request['payload']).json()["response"]
    extracted_code = extract_code(full_response)
    execution = execute(extracted_code['response'],namespace)
    
    data = {
        'description':description,
        'question': question,
        'prompt':prompt,
        'full_response': full_response,
        'extracted_code': extracted_code,
        'execution': execution
    }

    with open("log.json", 'w') as file:
        json.dump(data, file, indent=4) 
    
    return data

def suggest_questions(df,filename):
    example_row = dict(df.iloc[0])
    prompt = suggestion_template.format(filename=filename,example_row=example_row)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
