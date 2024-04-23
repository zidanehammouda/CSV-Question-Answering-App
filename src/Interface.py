import gradio as gr
import pandas as pd
from app import run, describe_file,suggest_questions
import os 
from PIL import Image
import logging
import sys
from dotenv import load_dotenv 
load_dotenv()

if not os.environ.get('method'):
    if len(sys.argv) > 1 and sys.argv[1] in ["server","api","local"] :
        os.environ['method'] = sys.argv[1]
    else:
        print("Please type a valid model method")
        sys.exit()

logging.basicConfig(level=logging.INFO)
logging.info(os.environ.get('method'))


def read_image():
    directory='./'
    image_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and (f.endswith('.png') or f.endswith('.jpg'))]
    if image_files:
        image_path = os.path.join(directory, image_files[0])
        try:
            image = Image.open(image_path)
            return image
        except Exception as e:
            print(f"Error {e}")
            return None
    return None

def delete_image():
    directory='./'
    image_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and (f.endswith('.png') or f.endswith('.jpg'))]
    if image_files:
        for image_file in image_files:
            image_path = os.path.join(directory, image_file)
            try:
                os.remove(image_path)
            except:
                return



def generate_description(uploaded_file):
    delete_image()
    if uploaded_file is None:
        return "", "Please upload a CSV file" 
    df = pd.read_csv(uploaded_file)
    automatic_description = describe_file(df, uploaded_file.name)
    suggestions = suggest_questions(df, uploaded_file.name)
    return automatic_description, "",suggestions 

def process_csv_question_and_description(uploaded_file, description, question):
    delete_image()
    if uploaded_file is None:
        return "Please upload a CSV file."
    df = pd.read_csv(uploaded_file)
    df_columns = str(list(df.columns))
    namespace = {'df': df}
    
    response = run(namespace, description, df_columns, question,os.environ.get("method"))
    image = read_image()

    # logging.basicConfig(level=logging.INFO)
    # logging.info("This is an info message")
    # logging.info(response)
    
    execution = response['execution']
    if execution != None:
        return execution,image
    else:
        return response['error'],image


with gr.Blocks(css=".file_container {max-height:150px} .file_container > button > div {display:flex;flex-direction:row}") as app:
    gr.Markdown("## CSV Question Answering App")
    gr.Markdown("Upload a CSV file, and an automatic description will be generated. You can edit this description before asking your question.")
    
    with gr.Row():
        with gr.Column(): 
            file_input = gr.File(label="Upload CSV File",elem_classes=['file_container'])
            description_input = gr.Textbox(label="Dataset Description", placeholder="The description will be generated here...")
            question_input = gr.Textbox(label="For better visualization results start your input with \"Plot:\"")
            submit_button = gr.Button("Submit")
            suggestions=gr.Text(label="Suggestions")
        with gr.Column():  
            output = gr.Text(label="Answer")
            image = gr.Image()
            message = gr.Textbox(label="Message", visible=False) 
    
    file_input.change(fn=generate_description, inputs=[file_input], outputs=[description_input, message,suggestions])
    submit_button.click(fn=process_csv_question_and_description, inputs=[file_input, description_input, question_input], outputs=[output,image])

app.launch(debug=True)
