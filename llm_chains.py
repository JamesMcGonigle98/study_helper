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
# Prompt Templates Multi 
# -----------------------------------------------------------------------------
prompt_template_starting_qs_multi = PromptTemplate(
    input_variables=['subject','qualification','subject_area'],
    template = "I am currently studying for my {qualification} {subject} exam. I want to revise {subject_area}. Give me 1 question of {qualification} standard. This questions should have one correct answer. Return this question as a string and do not include the answer."

)

prompt_template_starting_ans_multi = PromptTemplate(
    input_variables=['question'],
    template = "{question}? Write 1 correct answer and 4 other plausible, yet incorrect answers. Return the answers in a comma seperate list. None of the answers should contain a comma. The first item in the list should be the correct answer and this should be a string. The last four items in the list should be incorrect answers. Do not include any other information apart from the 1 correct answer and the 4 incorrect answers"
)

# %% --------------------------------------------------------------------------
# Prompt Templates Writing 
# -----------------------------------------------------------------------------
prompt_template_starting_qs_writing = PromptTemplate(
    input_variables=['subject','qualification','subject_area'],
    template = "I am currently studying for my {qualification} {subject} exam. I want to revise {subject_area}. Give me 1 question of {qualification} standard. This questions should have one correct answer. Return this question as a string and do not include the answer."

)

prompt_template_starting_ans_writing = PromptTemplate(
    input_variables=['question'],
    template = "{question}? Return the answer as a string. Do not include any other information apart from the answer."
)


# %% --------------------------------------------------------------------------
# LLM Chain Functions 
# -----------------------------------------------------------------------------
def initial_questions_multi_choice(subject, qualification ,subject_area):

    initial_q_chain_multi = LLMChain(llm=llm, prompt=prompt_template_starting_qs_multi, output_key="question")

    initial_a_chain_multi = LLMChain(llm=llm, prompt=prompt_template_starting_ans_multi, output_key="answer")

    chain = SequentialChain(
        chains = [initial_q_chain_multi, initial_a_chain_multi],
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

def initial_questions_writing_answers(subject, qualification, subject_area):

    initial_q_chain_writing = LLMChain(llm=llm, prompt=prompt_template_starting_qs_writing, output_key="question")

    initial_a_chain_writing = LLMChain(llm=llm, prompt=prompt_template_starting_ans_writing, output_key="answer")

    chain = SequentialChain(
        chains = [initial_q_chain_writing, initial_a_chain_writing],
        input_variables=['subject','qualification','subject_area'],
        output_variables=['question','answer']
        )
    
    response = chain({'subject':subject,
                      'qualification':qualification,
                      'subject_area':subject_area}
                      )

    return response

def compare_sentences(sentence1, sentence2):

    sentences = [sentence1, sentence2]

    embeddings = sentence_comparison_llm.encode(sentences)

    embedding1 = embeddings[0]
    embedding2 = embeddings[1]

    similarity_score = cosine_similarity([embedding1], [embedding2])[0][0]

    return similarity_score

    



