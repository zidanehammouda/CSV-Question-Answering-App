prompt_template_textual = """df is a dataframe that {description}. df has these columns: {columns}. Write a python code block that answers this question: {question}. Just write code and print results, no explanation should be given.
"""

prompt_template_visual = """df is a dataframe that {description}. df has these columns: {columns}. Write a python code block that answers this question: {question}. Just plot and save the results, no explanation should be given.
"""

description_template = """This is an example row of a given dataset titled {filename}.\n {example_row}. Complete this sentence with a maximum of 50 words: df is a dataframe about"""

suggestion_template = """This is an example row of a given dataset titled {filename}.\n {example_row}. Write 5 simple printing/visualizing questions about the dataset so I can solve it using code."""

libraries = """
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import seaborn as sns
from scipy import stats
"""