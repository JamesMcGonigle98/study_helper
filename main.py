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
if st.sidebar.button("Go!!!"):
    # Update session state when button is clicked
    st.session_state.button_clicked = True
else:
    st.session_state.button_clicked = False

st.write(f"You've chosen to study {subject}! Let's help you with {subject_area} so that you can pass your {qualification}!")  

if st.session_state.button_clicked and type_of_question == "Multiple Choice":
 
    types_of_questions.multi_choice(subject, qualification, subject_area)

elif st.session_state.button_clicked and type_of_question == "Writing Answers":

    types_of_questions.writing_answers(subject, qualification, subject_area)

