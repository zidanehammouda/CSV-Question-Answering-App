prompt_template = """df is a dataframe about {description}. df has these columns: {columns}. Write python code that answers this question: Print {question}
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