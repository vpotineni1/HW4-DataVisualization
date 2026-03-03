import streamlit as st
from utils.data_loader import load_first_season, load_second_season
from charts.charts import chart_dashboard

st.set_page_config(page_title="Explore", layout="wide")

first_season = load_first_season()
season_season = load_second_season()


st.title("Interactive Exploratory View")
st.write("Use the dashboard below to conduct your own analysis.")

st.altair_chart(chart_dashboard(first_season, season_season), use_container_width=True)

st.write("- Click on your favorite teams in the points table bar chart, and see the amount of cards they obtained, points breakdown, and offensive metrics")
