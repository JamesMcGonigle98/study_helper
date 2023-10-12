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
# 
# -----------------------------------------------------------------------------
def multi_choice(subject, qualification, subject_area):    

    response = initial_questions_multi_choice(subject, qualification ,subject_area)
    
    question = response['question']
    # question = question[2:-2]
    
    answer = response['answer'].strip().split(",")
    # answer = [item[2:-1] for item in answer]

    correct_answer = answer[0]
    # correct_answer = correct_answer[:1]

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


##################################################################

    # option = st.selectbox('Answer',
    #                 ("Choose an answer",
    #                 shuffled_answers[0],
    #                 shuffled_answers[1],
    #                 shuffled_answers[2],
    #                 shuffled_answers[3],
    #                 shuffled_answers[4]))
    
    # if option == correct_answer:
    #     st.write("Correct!")

    # elif option == "Choose an answer":
    #     st.write("")

    # elif option != correct_answer:
    #     st.write("Try again")
