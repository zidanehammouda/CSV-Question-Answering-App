from openai import OpenAI
import os
import requests
import json
from dotenv import load_dotenv 
load_dotenv()


gpt_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def predict_gpt(prompt):
    response = gpt_client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}])
    text_response = response.choices[0].message.content
    return text_response

def predict_deepseek(prompt):
    try:
        url = "https://api.deepseek.com/v1/chat/completions"

        payload = json.dumps({
        "messages":[{"role": "user", "content": prompt}],
        "model": "deepseek-coder",
        "frequency_penalty": 1,
        "max_tokens": 500,
        "presence_penalty": 0,
        "stop": None,
        "stream": False,
        "temperature": 0.1,
        "top_p": 1
        })
        os.environ.get("DEEPSEEK_API_KEY")
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {os.environ.get("DEEPSEEK_API_KEY")}'
        }

        response = requests.request("POST", url, headers=headers, data=payload).text
        response = json.loads(response)
        return response['choices'][0]['message']['content']

    except Exception as e:
        return {'error':True, 'response': e}