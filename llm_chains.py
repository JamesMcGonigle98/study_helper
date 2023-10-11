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

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from secret_key import openai_key, serpapi_key

# %% --------------------------------------------------------------------------
# Create the LLMs
# -----------------------------------------------------------------------------
llm = OpenAI(openai_api_key= openai_key)
sentence_comparison_llm = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# %% --------------------------------------------------------------------------
# Prompt Templates
# -----------------------------------------------------------------------------
prompt_template_starting_qs = PromptTemplate(
    input_variables=['subject','qualification','subject_area'],
    template = "I am currently studying for my {qualification} {subject} exam. I want to revise {subject_area}. Give me 1 question of {qualification} standard to assess my knowledge. Return these questions as a comma seperated list please "

)

prompt_template_starting_as = PromptTemplate(
    input_variables=['question'],
    template = "For each of the following {question}, write the answers. Return these answers as a comma seperated list "
)


# %% --------------------------------------------------------------------------
# LLM Chain Functions 
# -----------------------------------------------------------------------------
def initial_questions(subject, qualification ,subject_area):

    initial_q_chain = LLMChain(llm=llm, prompt=prompt_template_starting_qs, output_key="question")

    initial_a_chain = LLMChain(llm=llm, prompt=prompt_template_starting_as, output_key="answer")

    chain = SequentialChain(
        chains = [initial_q_chain, initial_a_chain],
        input_variables=['subject','qualification','subject_area'],
        output_variables=['question','answer']
        )
    
    response = chain({'subject':subject,
                      'qualification':qualification,
                      'subject_area':subject_area}
                      )

    return response

# if __name__ == "__main__":
#     print(initial_questions("Maths","GCSE","Algebra")


def compare_sentences(sentence1, sentence2):

    sentences = [sentence1, sentence2]

    embeddings = sentence_comparison_llm.encode(sentences)

    embedding1 = embeddings[0]
    embedding2 = embeddings[1]

    similarity_score = cosine_similarity([embedding1], [embedding2])[0][0]

    return similarity_score

    



