import streamlit as st
from PIL import Image
from utils.data_loader import load_first_season, load_second_season


st.set_page_config(page_title="HW4: Data Visualization - Vishal Potineni", layout="wide")
st.title("What seperates Elite Clubs from Bottom-Tier Clubs in the Premier League besides the most salient attribute: Talent?")
st.write(Image.open('images/Premier_League_Logo.jpg'))



st.write(
    "To explore this visual data story, please navigate it through the pages in the sidebar:\n"
    "- **Central Narrative**: We begin by examining the factors that might seperate elite and bottom-tier clubs in the Premier League.\n"
    "- **Exploration**: For a closer reader-driven exploration of the data, we provide a few interactive designs.\n"
    "- **Methodology**: We lay down some key details about our data to our analysis.\n"
)