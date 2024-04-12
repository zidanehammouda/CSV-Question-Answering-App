from transformers import AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv 
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
load_dotenv()



app = Flask(__name__)


model = {
    "tokenizer": AutoTokenizer.from_pretrained("deepseek-ai/deepseek-coder-7b-instruct-v1.5"),
    "model": AutoModelForCausalLM.from_pretrained("deepseek-ai/deepseek-coder-7b-instruct-v1.5")
}


device = "cuda"


def generate_response(prompt):
    try:
        coder_model_prompt = [
            {"role": "user", "content": prompt}
        ]
        encodeds = model["tokenizer"].apply_chat_template(coder_model_prompt, return_tensors="pt")

        model_inputs = encodeds.to(device)
        model['model'].to(device)

        generated_ids = model['model'].generate(model_inputs, max_new_tokens=500, do_sample=False, temperature=0.1, repetition_penalty=1)
        decoded = model["tokenizer"].batch_decode(generated_ids)
        return decoded[0].split('[/INST]')[-1].split('</s>')[0]
    except Exception as e:
        return {'error':'An error happened when trying to generate a response'}


@app.route('/generate', methods=['POST'])
def handle_request():
    data = request.json  # Get JSON data from request
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    response = generate_response(prompt)
    return jsonify({'response': response})

# Run the app
if __name__ == '__main__':
    app.run(debug=False, port=5000)


    
