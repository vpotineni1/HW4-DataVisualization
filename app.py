import streamlit as st
from utils.data_loader import load_first_season, load_second_season


st.set_page_config(page_title="HW4: Data Visualization - Vishal Potineni", layout="wide")

st.title("What Specific Factors Seperates Elite Clubs such as Liverpool and Manchester City from Bottom-Tier Clubs such as Brenton and the Wolves?")

st.write(
    "To explore this visual data story, please navigate it through the pages in the sidebar:\n"
    "- **Central Narrative**: We begin by examining the factors that might seperate elite and bottom-tier clubs in the Premier League.\n"
    "- **Exploration**: For a closer reader-driven exploration of the data, we provide a few interactive designs.\n"
    "- **Methodology**: We lay down some key details about our data to our analysis.\n"
)