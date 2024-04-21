
import re
from dotenv import load_dotenv 
import requests
import json
import os
load_dotenv()
import io
import sys
from api_client import predict_deepseek,predict_gpt

if os.environ.get("method") =="local":
    from model import generate_response



from prompt_templates import prompt_template,description_template,suggestion_template,libraries


def describe_file(df,filename):
    first_row = df.iloc[0].to_dict()
    prompt = description_template.format(filename=filename,example_row=first_row)
    response = predict_gpt(prompt)
    return response

def suggest_questions(df,filename):
    example_row = dict(df.iloc[0])
    prompt = suggestion_template.format(filename=filename,example_row=example_row)
    response = predict_gpt(prompt)
    return response

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



def run(namespace,description,columns,question,method):
    prompt = prompt_template.format(description=description,columns=columns,question=question)

    if method == 'server':
        request = {
        'url' : os.environ.get("MODEL_URL"),
        'payload' : json.dumps({"prompt": prompt}),
        'headers' : {
        'Content-Type': 'application/json'
        }}
        full_response = requests.request("POST", request['url'], headers=request['headers'], data=request['payload']).json()["response"]
    
    elif method == 'local':
        full_response = generate_response(prompt)

    elif method == 'api':
        full_response = predict_deepseek(prompt)

    else:
        return {'execution': 'Wrong model method'}
    

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


