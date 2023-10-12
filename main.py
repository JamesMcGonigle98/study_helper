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
import llm_chains


# %% --------------------------------------------------------------------------
# Streamlit App Design
# -----------------------------------------------------------------------------
st.title("Study Helper")

subject = st.sidebar.selectbox(
    "Which subject would you like to revise today?",
    ("Maths","Physics","Chemistry","Biology"),
    placeholder="Maths"
)

qualification = st.sidebar.selectbox(
    "Which exam are you revising for?",
    ("GCSE","A-Level"),
    placeholder="GCSE"
)

subject_area = st.sidebar.text_input(
    f"Which area of {subject} would you like to revise?",
    placeholder="Algebra"
)

search = st.sidebar.button("Help me study!")

if search:

    st.write(f"You've chosen to study {subject}! Let's help you with {subject_area} so that you can pass your {qualification}!")

    response = llm_chains.initial_questions(subject, qualification ,subject_area)

    st.write("Let's start with some questions to gauge your knowledge:")
    
    question = response['question'].strip().split(",")
    answer = response['answer'].strip().split(",")

    question = question[0]
    answer = answer[0]

    st.write(f"{question}?")

    st.header("Write your answer")

    # Question 1 
    user_answer_1 = st.text_input("Answer 1")
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

# %%
