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
from langchain.chains import LLMChain, SequentialChain

from secret_key import openai_key, serpapi_key

# %% --------------------------------------------------------------------------
# Create the LLMs
# -----------------------------------------------------------------------------
llm = OpenAI(openai_api_key= openai_key)



# %% --------------------------------------------------------------------------
# Prompt Templates
# -----------------------------------------------------------------------------
prompt_template_starting_qs = PromptTemplate(
    input_variables=['subject','qualification','subject_area'],
    template = "I am currently studying for my {qualification} {subject} exam. I want to revise {subject_area}. Give me 5 questions of {qualification} standard to assess my knowledge. Return these questions as a comma seperated list please "

)

prompt_template_starting_as = PromptTemplate(
    input_variables=['5_questions','subject','qualification','subject_area'],
    template = "For each of the following {5_questions}, write the answers. Return these answers as a comma seperated list "
)


# %% --------------------------------------------------------------------------
# LLM Chain Functions 
# -----------------------------------------------------------------------------
def initial_questions(subject, qualification ,subject_area):

    initial_q_chain = LLMChain(llm=llm, prompt=prompt_template_starting_qs, output_key="5_questions")

    initial_a_chain = LLMChain(llm=llm, prompt=prompt_template_starting_as, output_key="5_answers")

    chain = SequentialChain(
        chains = [initial_q_chain, initial_a_chain],
        input_variables=['subject','qualification','subject_area'],
        output_variables=['5_questions','5_answers']
        )
    
    response = chain({'sucject':subject,
                      'qualification':qualification,
                      'subject_area':subject_area}
                      )

    return response





