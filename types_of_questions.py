"""
Multiple Choice

This is the multiple choice part of the study helper
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
import llm_chains

import random


# %% --------------------------------------------------------------------------
# Multiple Choice
# -----------------------------------------------------------------------------
def multi_choice(subject, qualification ,subject_area): 

    response = llm_chains.initial_questions_multi_choice(subject, qualification ,subject_area)   

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

    response = llm_chains.initial_questions_writing_answers(subject, qualification ,subject_area)

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

        score = llm_chains.compare_sentences(user_answer_1, llm_answer_1)
        
        if score > 0.8:
            st.write("This answer is perfect!")

        elif 0.4 < score < 0.8:
            st.write("This answer is good!")
        
        else:
            st.write("Try again!")

        st.write(f"The answer is {answer}")

