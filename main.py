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
    ("GCSE","A-Level")
)

subject_area = st.sidebar.text_input(
    f"Which area of {subject} would you like to revise?"
)

search = st.sidebar.button("Help me study!")

if search or subject_area:

    st.write(f"You've chosen to study {subject}! Let's help you with {subject_area} so that you can pass your {qualification}!")

