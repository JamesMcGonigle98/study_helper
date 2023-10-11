"""
Enter script name

Enter short description of the script
"""

__date__ = "2023-10-11"
__author__ = "JamesMcGonigle"



# %% --------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

from secret_key import openai_key, serpapi_key

# %% --------------------------------------------------------------------------
# Create the LLMs
# -----------------------------------------------------------------------------
llm = OpenAI(openai_api_key= openai_key)




# %% --------------------------------------------------------------------------
# Prompt Templates
# -----------------------------------------------------------------------------
prompt_template_starting = PromptTemplate(
    input_variables=['subject','qualification','subject_area'],
    template = "I am currently studying for my {qualification} {subject} exam. I want to revise {subject_area}."

)





