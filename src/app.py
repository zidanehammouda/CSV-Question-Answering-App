
import re
from dotenv import load_dotenv 
import requests
import json
import os

import io
import sys
from api_client import predict_deepseek,predict_gpt

load_dotenv()
if os.environ.get("method") =="local":
    from model import generate_response



from prompt_templates import prompt_template_textual,prompt_template_visual,description_template,suggestion_template,libraries


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
            return matches[0]
        else:
            raise Exception("Error extracting code: No match")
    except Exception as e:
        raise Exception("Error extracting code: ",e) from e
    
def execute(code,namespace):
    try:
        buffer = io.StringIO()
        sys.stdout = buffer
        exec(libraries+code,namespace)

        sys.stdout = sys.__stdout__

        return buffer.getvalue()

    except Exception as e:
        raise Exception("Error executing: ",e) from e



def run(namespace,description,columns,question,method):
    try:
        if question.lower().startswith('plot:'):
            prompt = prompt_template_visual.format(description=description,columns=columns,question=question)
        else:
            prompt = prompt_template_textual.format(description=description,columns=columns,question=question)
        full_response= None
        extracted_code= None
        execution= None
        error = None
        try:
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
            execution = execute(extracted_code,namespace)
        
        except Exception as e:
                error = e
        
        data = {   
            'question': question,
            'prompt':prompt,
            'full_response': full_response,
            'extracted_code': extracted_code,
            'execution': execution,
            'error': error
                }

        with open("log.json", 'w') as file:
            json.dump(data, file, indent=4) 
        
        return data

    except Exception as e:
        print(e)


