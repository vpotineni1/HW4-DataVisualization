import streamlit as st

st.set_page_config(page_title="Methods", layout="wide")

st.title("Methods & Limitations")
st.write("- Data source: 2023-2024 and 2024-2025 Premier League Season Datasets")
st.write("- Variables used: `date`, `HomeTeam`, `AwayTeam`, `FTHG`,`FTAG`, `HS`, `AS`, `HST`, `AST`,`FTAG`, `HC`, `AC`, `HY`, `AY`, `HR`, `AR` ")
st.write("- Limitations: This exploratory analysis was conducted using four main teams including Liverpool, Man City, Brentford, and Wolves. Thus the results are not necessarily generalizable to the whole league")