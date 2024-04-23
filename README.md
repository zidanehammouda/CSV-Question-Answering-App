
# CSV Question Answering App

CSV Question Answering App, as the name implies, is an application that leverages the capabilities of text-generation LLM deepseek-coder to answer questions and give insights about datasets and CSV files. The application gives you the freedom to ask any kind of question regarding your input dataset and It will give you responses. Questions could range from ‘Which country has the highest infection rates per capita?” to “What’s the distribution of COVID-19 cases by age group?” for the [COVID-19 dataset](https://www.kaggle.com/datasets/imdevskp/corona-virus-report/code).




## Run Locally

The app can be run using three different methods: Remote Model Inference, Local Model Inference, and API. To start, run the ./launch_app.sh file and select your preferred method. Detailed explanations of each method are provided below.

![alt text](https://i.imgur.com/DFGdZLn.png)

**Please note:** The first two methods require that your hardware be capable of running the model locally.

### Remote Model Inference:

In this method, the model is deployed on a local server, meaning it runs independently of the application. The application communicates with the server via HTTP requests to send input data and receive predictions. This setup allows for easy updates and debugging without needing to reload the model with each change. To use this method, run the shell script and select mode 1. Alternatively, you can manually enter the following commands:

```bash
    python3 src/model_server.py
    export method=server
    python3 src/Interface.py
```
This configuration deploys the model on a local server on port 5000 and launches the application interface on a different port.

### Local Model Inference:

Here, the machine learning model is loaded directly within the application, eliminating the need for network communications. To use this method, choose mode 2 when running the ./launch_app.sh shell script. Alternatively, you can set it up manually with:

```bash
    export method=local
    python3 src/Interface.py
```

### Through API:

This method utilizes the public DeepSeek model API, allowing you to make predictions without loading the model on your machine. You'll need an API key from the DeepSeek API, set as an environment variable in the .env file. Note that the DeepSeek API platform provides 10M free tokens upon account creation. To proceed, update the DEEPSEEK_API_KEY in your .env file, then run ./launch_app.sh and choose mode 3.


## Live version
If you prefer not to install and run the app manually, you can use the hosted version on Hugging Face Spaces. Follow [this](https://huggingface.co/spaces/zidanehammouda/CSV_Question_Answering_App) link to access it.


## Usage
Once the app is running and you have selected a dataset you're interested in exploring, simply upload the CSV file. The app will then utilize the OpenAI API (GPT3.5 model) to generate a description of the dataset and suggest example queries that you can pose to the main code generator model. Note that the description and suggestions are optional; you can manually provide the description to the model instead.

Below is an example demo of how the app works and how to use it: 


![alt text](https://i.imgur.com/dj1qnJF.gif)
## Documentation

This app consists of four main components:

**Interface:** Utilizes the Gradio UI, which serves as the interface between the user and the rest of the application's components.

**Main App Component:** Encapsulates most of the app’s workflow, including prompt formatting, code extraction, and code execution.

**Model:** Features the deepseek-coder model, which acts as the code generator for this app. (Further details are available in the next section)

**API Client:** Calls the GPT-3.5 model to generate a brief description of the input dataset and suggests example questions that could help explore and understand the dataset. (This component is optional and can be omitted if not needed. Its primary function is to provide descriptions and suggested queries for the coder model)

### High-level design
Below is the high-level design of the app and how the different components interact with each other to answer input questions. Step 2 which represents the calling of the GPT3.5 API is optional and depends on whether you choose to rely on the model to generate a description for you (as well as return suggested questions for the dataset) or you write it manually.
Note: Providing a description of the dataset is not mandatory for the model to function, but it is highly recommended as it offers valuable context that can enhance the accuracy and relevance of the model's responses.

![HL design](https://i.imgur.com/b8CcaLZ.jpeg)

### Activity Diagram (Low-level design)
Below is the activity diagram describing the flow of the answer generation and how the components interact to return a response.

![HL design](https://i.imgur.com/HpPjjf0.jpeg)

### Model Selection:

The choice of the model was not made arbitrarily; it was based on comparative results from tests conducted on four distinct datasets. Each dataset included a set of test cases—comprising questions and answers—where the Deepseek-coder model consistently demonstrated superior efficiency and performance. The models compared were:

* Deepseek-coder-7b-instruct-v1.5
* mistralai/Mistral-7B-Instruct-v0.2
* CodeLlama-7b-Instruct-hf

Note that the same hyperparameters were used during the evaluation of the models. 

#### Evaluation Data
Below are the four datasets used in the evaluation and comparison of the three models:

* **Titanic.csv:** This dataset includes passenger details from the Titanic, such as survival status, class, name, gender, age, number of siblings/spouses and parents/children aboard, and fare amount.

* **Onlinefoods.csv:** Contains data from an online food ordering platform, covering attributes like occupation, family size, and feedback collected over a certain period.

* **Hw_200.csv:** Provides height and weight for 200 individuals. Each record includes three values: index, height (in inches), and weight (in pounds).

* **Monthly_Counts_of_Deaths_by_Select_Causes__2014-2019.csv:** Features monthly counts of deaths in the United States by select causes from 2014 to 2019, including causes such as Alzheimer's, heart disease, accidents, and drug overdose.

Each dataset was accompanied by a set of test cases ranging from 10 to 14, totaling 52 test cases for all datasets together.

Example test cases for the Titanic dataset include:
>   
    Question: How many females are in the dataset? Answer: 314
    Question: What is the average age of the passengers? Answer: 29.471
    Question: How many passengers survived? Answer: 342
    Question: Who paid the highest fare? Answer: Miss. Anna Ward
    Question: What is the total amount of fare paid? Answer: $28,654.91
    Question: Who is the passenger with the highest number of siblings aboard?

Some test cases were generated by ChatGPT but were thoroughly reviewed and verified to ensure they were suitable for use as test cases.

#### Prompt evaluation and results:

Below are the prompts that were ultimately used to evaluate the models. These were selected after testing numerous other prompts, which helped identify the most effective ones for our purposes. The development of these prompts was an incremental process, with adjustments made gradually until the optimal configuration was achieved.

**Prompt 1:**
>
    df is a dataframe that {description}. df has these columns: {columns}. Without explaining, write in a Python code block the answer to this question: Print {question}
**Prompt 2:**
>
    Prompt 2: df is a dataframe that {description}. df has these columns: {columns}. Write in a Python code block the answer to this question: Print {question}. Just code, no explanation should be given.
**Prompt 3:**
>
    Prompt 3: df is a dataframe that {description}. df has these columns: {columns}. Write in a Python code block the answer to this question: {question}. Just write code and print results, no explanation should be given.

Prompt 2 is derived from Prompt 1 and was specifically designed to compel the models to return only code. Prompt 3, a derivative of Prompt 2, was introduced when it was observed that the models occasionally failed to print the results.


* **CodeLlama:** This model struggled with both Prompt 1 and Prompt 2. With Prompt 1, it tended to overexplain and included many non-code tokens. With Prompt 2, it often failed to print the results, which is crucial for displaying the response. Therefore, both Prompt 2 and Prompt 3 were evaluated, with Prompt 3 proving to be the most effective for this model.

* **Deepseek:** This model delivered consistent results with both Prompts 1 and 2, and showed a slight improvement with Prompt 3.

* **Mistral:** Performed better with Prompt 1 but had issues with forgetting to print results in some test cases when using Prompt 2. It exhibited the lowest accuracy with Prompt 3.

#### Results
In this next section, the results of the three models will be compared when every model uses its best prompt. (Codellama and Deepseek prompt 3 and Mistral prompt 1).

Deepseek had the best performance with 44 true answers and 8 false answers (85% accuracy). Following it is Mistral with 34 true answers and 18 false answers (65% accuracy) and then Codellama which had the worst results with only 22 true answers and 30 false answers (42% accuracy)

![HL design](https://i.imgur.com/Qyo2r2Z.png)
![HL design](https://i.imgur.com/MctuZVC.png)

The models' average inference time results range from 2.2 seconds to 3.8 with Codellama being the fastest with 2.27s inference time followed by Deepseek with 3.4s and Mistral with 3.78s. 

![HL design](https://i.imgur.com/6zwiyzv.png)

![HL design](https://i.imgur.com/DJ4gccE.png)

Because both efficiency and accuracy are important in this project Deepseek was chosen as the best coder model for this app.

Please note all comparing results and data are included in this project under the evaluation directory. 








## Contribution
Although the app heavily relies on the model code generator and its output, its success would not have been possible without significant efforts to refine and adjust the inputs before they are fed into the model. This ensures that the model provides the most accurate results possible. A major contribution to this project was the thorough evaluation of different models, utilizing a set of meticulously validated test cases to determine which model would best suit the application's needs. Equally important is the work done to extract relevant code from the model's response, converting it into a format suitable for the code executor. The seamless integration of these commands is what makes this application functional by leveraging the LLM code generator. Finally, a key contribution to this project is the engineering behind the app. This includes careful planning of its various components and comprehensive management of all potential scenarios, including unexpected behaviors. These efforts ensure robust and reliable performance of the whole application. 
## Limitations
While the model has shown strong performance compared to other options and consistently achieves good scores, it is not 100% accurate and occasionally makes errors. Currently, the app is limited to displaying results through prints or plots only. Supporting additional result formats could be a valuable improvement for future development.

Another significant limitation is that the app does not automatically process and return results for suggested questions; it merely displays these suggestions to the user. Implementing a feature that automatically runs suggested questions and analyzes the CSV file would not only enhance user interaction but also provide deeper insights and knowledge about the data. This capability could be developed in future iterations of the project.
