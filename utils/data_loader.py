import streamlit as st
import pandas as pd

@st.cache_data
def load_first_season() -> pd.DataFrame:
    first_season = pd.read_csv("data/PL-season-2324 (1).csv")
    return first_season

@st.cache_data
def load_second_season() -> pd.DataFrame:
    second_season = pd.read_csv("data/PL-season-2425 (1).csv")
    return second_season