import gradio as gr
import pandas as pd
from app import run, describe_file


def generate_description(uploaded_file):
    if uploaded_file is None:
        return "", "Please upload a CSV file"  # Clear the description and show a prompt
    df = pd.read_csv(uploaded_file)
    automatic_description = describe_file(df, uploaded_file.name)
    return automatic_description, ""  # Return the auto-generated description and clear any warning/message

def process_csv_question_and_description(uploaded_file, description, question):
    if uploaded_file is None:
        return "Please upload a CSV file."
    df = pd.read_csv(uploaded_file)
    df_columns = str(list(df.columns))
    namespace = {'df': df}
    
    # Use the provided description, assuming it could have been edited by the user
    response = run(namespace, description, df_columns, question)

    answer = response['execution']
    return answer

# Create the interface
with gr.Blocks() as app:
    gr.Markdown("## CSV Question Answering App")
    gr.Markdown("Upload a CSV file, and an automatic description will be generated. You can edit this description before asking your question.")
    
    with gr.Row():
        with gr.Column():  # Inputs column
            file_input = gr.File(label="Upload CSV File")
            description_input = gr.Textbox(label="Dataset Description", placeholder="The description will be generated here...")
            question_input = gr.Textbox(label="Type your question")
            submit_button = gr.Button("Submit")
        
        with gr.Column():  # Outputs column
            output = gr.Text(label="Answer")
            message = gr.Textbox(label="Message", visible=False)  # Used for displaying messages to the user, hidden by default
    
    file_input.change(fn=generate_description, inputs=[file_input], outputs=[description_input, message])
    submit_button.click(fn=process_csv_question_and_description, inputs=[file_input, description_input, question_input], outputs=output)

app.launch(debug=True)
