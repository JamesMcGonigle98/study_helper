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

# Initialize session state (if not already initialized)
if 'type_of_question' not in st.session_state:
    st.session_state.type_of_question = "Multiple Choice"  # Default value

type_of_question = st.sidebar.selectbox(
    "What type of revision do you want to do?",
    ("Multiple Choice", "Writing Answers"))

# Update session state when selectbox changes
if st.session_state.type_of_question != type_of_question:
    st.session_state.type_of_question = type_of_question

# Initialize session state (if not already initialized)
if 'go' not in st.session_state:
    st.session_state.go = ""  # Default value


go = st.sidebar.button(
    "Go!!!"
)

if go:
    st.write(f"You've chosen to study {subject}! Let's help you with {subject_area} so that you can pass your {qualification}!")

    types_of_questions.multi_choice(subject, qualification, subject_area)








        # st.write("Let's start with some questions to gauge your knowledge:")
        # new_q = st.button("Generate Question", key ='new_q_key')

        # if new_q:
        #     response = llm_chains.initial_questions_multi_choice(subject, qualification, subject_area)

        #     question = response['question']
        #     answer = response['answer'].strip().split(",")

        #     correct_answer = answer[0]
        #     incorrect_answers = answer[1:]

        #     shuffled_answers = random.sample(answer, len(answer))

        #     st.write(f"{question}?")

        #     option = st.selectbox('Answer',
        #                  (shuffled_answers[0],
        #                   shuffled_answers[1],
        #                   shuffled_answers[2],
        #                   shuffled_answers[3],
        #                   shuffled_answers[4]))
            
        #     if option == correct_answer:
        #         st.write("Correct!")

        #     elif option == None:
        #         st.write("Choose an answer")

        #     elif option != correct_answer:
        #         st.write("Try again")



    # if type_of_question == "Writing Answers":

    #     response = llm_chains.initial_questions_multi_choice(subject, qualification ,subject_area)

    #     st.write("Let's start with some questions to gauge your knowledge:")
        
    #     question = response['question'].strip().split(",")
    #     answer = response['answer'].strip().split(",")

    #     question = question[0]
    #     answer = answer[0]

    #     st.write(f"{question}?")

    #     st.header("Write your answer")

    #     # Question 1 
    #     user_answer_1 = st.text_input("Your answer:")
    #     llm_answer_1 = answer[0]
    #     check_q1 = st.button("Check my answer!")

    #     if check_q1 or user_answer_1:

    #         score = llm_chains.compare_sentences(user_answer_1, llm_answer_1)
            
    #         if score > 0.8:
    #             st.write("This answer is perfect!")

    #         elif 0.4 < score < 0.8:
    #             st.write("This answer is good!")
            
    #         else:
    #             st.write("Try again!")

    #         st.write(f"The answer is {answer}")

    # %%
