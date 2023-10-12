"""
Streamlit App for Study Help

A Streamlit App to help students with exam preparation
"""

__date__ = "2023-10-11"
__author__ = "JamesMcGonigle"



# %% --------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import streamlit as st
import types_of_questions

import random
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

import llm_chains

# %% --------------------------------------------------------------------------
# Multiple Choice
# -----------------------------------------------------------------------------
def multi_choice(subject, qualification ,subject_area): 

    response = initial_questions_multi_choice(subject, qualification ,subject_area)   

    question = response['question']
    
    answer = response['answer'].strip().split(",")

    correct_answer = answer[0]

    shuffled_answers = random.sample(answer, len(answer))

    st.write(f"{question}?")

    # Update session state when selectbox changes
    option = st.selectbox('Answer',
            ("Choose an answer",) + tuple(shuffled_answers),
            index=0,  # Default index
            on_change=None,  # Optional: function to run on change
            args=()  # Optional: arguments for on_change function
            )
    
    if option == correct_answer:
        st.write("Correct!")
    elif option == "Choose an answer":
        st.write("")
    elif option != correct_answer:
        st.write("Try again")



# %% --------------------------------------------------------------------------
# Writing Answers
# -----------------------------------------------------------------------------
def writing_answers(subject, qualification, subject_area):

    response = initial_questions_writing_answers(subject, qualification ,subject_area)

    question = response['question'].strip().split(",")
    answer = response['answer'].strip().split(",")

    question = question[0]
    answer = answer[0]

    st.write(f"{question}?")

    st.header("Write your answer")

    # Question 1 
    user_answer_1 = st.text_input("Your answer:")
    llm_answer_1 = answer[0]
    check_q1 = st.button("Check my answer!")

    if check_q1 or user_answer_1:

        score = compare_sentences(user_answer_1, llm_answer_1)
        
        if score > 0.8:
            st.write("This answer is perfect!")

        elif 0.4 < score < 0.8:
            st.write("This answer is good!")
        
        else:
            st.write("Try again!")

        st.write(f"The answer is {answer}")



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

# %% --------------------------------------------------------------------------
# Streamlit App Design
# -----------------------------------------------------------------------------
st.title("Study Helper")

subject = st.sidebar.selectbox(
    "Which subject would you like to revise today?",
    ("Maths","Physics","Chemistry","Biology","History"),
    placeholder="Maths"
)

qualification = st.sidebar.selectbox(
    "Which exam are you revising for?",
    ("GCSE","A-Level"),
    placeholder="GCSE"
)

subject_area = st.sidebar.text_input(
    f"Which area of {subject} would you like to revise?",
    placeholder=""
)

type_of_question = st.sidebar.selectbox(
    "What type of revision do you want to do?",
    ("Multiple Choice", "Writing Answers")
)

# Initialize session state (if not already initialized)
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False  # Default value

# Button
if st.sidebar.button("Generate questions!"):
    # Update session state when button is clicked
    st.session_state.button_clicked = True
else:
    st.session_state.button_clicked = False

st.write(f"You've chosen to study {subject}! Let's help you with {subject_area} so that you can pass your {qualification}!")  

if st.session_state.button_clicked and type_of_question == "Multiple Choice":
 
    multi_choice(subject, qualification, subject_area)

elif st.session_state.button_clicked and type_of_question == "Writing Answers":

    writing_answers(subject, qualification, subject_area)

