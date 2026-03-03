import streamlit as st
import altair as alt
from utils.data_loader import load_first_season, load_second_season

from charts.charts import (
    base_theme,
    location_chart,
    cards_chart,
    dot_chart,
    rolling_points_chart
)

first_season = load_first_season()
season_season = load_second_season()


st.set_page_config(page_title="Story", layout="wide")

alt.themes.register("project", base_theme)
alt.themes.enable("project")

st.title("A Data Story: The Premier League")
st.markdown("**Central question:** *Do offensive aggression and discpline seperate elite clubs such as Liverpool and Man City from bottom-tier clubs such as Brentford and the Wolves?*")

st.header("Figure 1: Points Table Over the Past Two Seasons")
st.write("Before identifying what seperates elite clubs from the rest, we must first establish the peformance gap.")
st.altair_chart(dot_chart(first_season, season_season), use_container_width=True)
st.caption("As you can see teams at the top consistently performed well in each of the last two seasons, while there are some teams who performed at the bottom of the table consistently." \
" For this analysis below, I will focus on four teams, including two who were consistently at the top of the table over the past two seasons, and two teams who were consistenly near the bottom over the past "
" two seasons. A quick sidenote is that I will not be analyzing teams who only have one season of data due to the promotion/relegation nature of the Premier League. The two teams consistently at the top are Liverpool " \
" and Man City, while the two teams consistently at the bottom (who were in the Premier League for both seasons) are the Wolves and Brentford." )

st.header("Three potential factors will be analyzed:")
st.markdown("1. Do Elite Clubs Take Advantage of their Home Field?")
st.markdown("2. Does Discipline Explain the Seperation between Elite Clubs and Bottom-Tier Clubs?")
st.markdown("3. Does Offensive Aggression explain the Seperaton between Elite Clubs and Bottom-Tier Clubs?")


st.header("Figure 2: Do Elite Clubs take Advantage of Home Field?")
st.write("One possible explanation that seperates elite from bottom-tier teams is home-field advantage. If elite clubs like Liverpool and Man City dominate on their home-field compared to Brentford and Wolves that could explain the seperation.")
st.altair_chart(location_chart(first_season, season_season), use_container_width=True)
st.caption("While all the teams are available in Figure 2 for educational purposes I will focus on the teams listed above. As you can see when comparing Brentford and Wolves to" \
" Liverpool and Man City, there is not a significant difference in terms of home advantage. Both Man City and Liverpool did not seem to have any significant" \
" advantage at home compared to their lesser counterparts. Moreover, when we also look at away performance the Wolves actually performed better than Liverpool when it comes" \
" to away performance as a percentage of total points. ")

st.caption("Takeaway: From this, we can conclude that Home Field Advantage does not appear to be one of the factors that seperates elite teams such as Man City and Liverpool from "
" their lesser counterparts Brentford and Wolves. Thus, we move onto another metric, and examine if discpline played a significant role in the success of the" \
" elite clubs." )


st.header("Figure 3: Discipline: Do Elite Teams Play Cleaner Soccer")
st.write("Considering that home field advantage did not play a signficant factor into the success of elite teams, let's see if discipline does." \
" The chart below aggregates the total number of cards per team over a season as a proxy for discipline, and the toggle can be used to switch seasons.")
st.altair_chart(cards_chart(first_season, season_season), use_container_width=True)
st.caption("From figure 3, we notice that Man City has 53 total cards in 2023-2024 and 59 total cards in 2024-2025. Liverpool had 70 cards in " \
" 2023-2024 and 67 in 2024-2025. On the other hand, the Wolves had 102 cards in 2023-2024 and 76 total cards in 2024-2025. Brentford had 90 cards in 2023-2024 and 63 in 2024-2025. Thus, " \
" we notice that elite teams such as Man City and Liverpool have significantly less cards than bottom-tier clubs.")
 
st.caption("Takeaway: Discipline appears to be correlated with sustained success as elite clubs seem to avoid picking up cards as frequently as bottom-tier clubs. " \
"While, I am not implying causation, this relationship does make sense. Teams with lots of discpline can avoid picking up suspensions, which would hurt the tean. Thus, more successful clubs have fewer cards, and more available players." \
"Further, Brentford also improved substantially in terms of points from 2023-2024 to 2024-2025, which is also associated with a strong decrease in total cards, suggesting that discpline could play an important role in winning games. ")


st.header("Figure 4: Offensive Aggression: Do Elite Teams have more Aggressive Offenses?")
st.write("If discipline plays an important role in success, offensive aggression or intensity might also be a crucial role as it dictates how a team controls the game." \
" Next, we summarize the offensive attack for each Premier League team by examining the rolling averages of key offensive metrics such as shots, shots on target," \
" and corners for Man City, Liverpool, Brentford, and Wolves.")
st.altair_chart(rolling_points_chart(first_season, season_season), use_container_width=True)
st.caption("Note: These Figure 4 is interactive, so by clicking on the teams in the points table, their rolling average offensive metric will appear on the line chart on the right. Hold Shift when clicking to select multiple teams.")

st.caption("Across both seasons, a consistent pattern emerges. Liverpool and Man City both have significantly higher shot volumes than the Wolves and Brentford. There is a large gap "
" throughout much of the season, and corners show a somewhat similar pattern, though the seperation is a bit weaker. When we look at Shots on Target, in 2023-2024 there is a clear divergence where Liverpool and Man City" \
" took way more shots on target than the other two teams, however, this pattern becomes narrow in 2024-2025. This could suggest than volume is more important than precision alone.")

st.caption("Takeaway: A clear differentiator between elite clubs like Liverpool and Man City and struggling clubs such as the Wolves and Brentford is offensive pressure. Top teams generate" \
" more opportunities to score goals, which allows for more opportunities to finish. If I had to hypothesize, these teams do a great job with controlling the game by holding the ball" \
" and sustaining pressure on the oppposing defence. This allows them to generate more opportunties to shoot the ball, and thus score more goals." \
" This analysis does not establish causation, however, the data suggests that aggressive offensive play that results in more shots is a potential factor that seperates elite clubs from bottom-tier clubs.")



st.header("Conclusion:")

st.caption("This analysis was examining which factors seperate elite clubs such as Liverpool and Man City from bottom-tier clubs such as the Wolves and Brentford. Through exploratory analysis," \
" we were able to establish a couple of hypotheses. ")

st.caption("First, we looked at home-field advantage to see if elite clubs took advantage of their home turf more than bottom-tier clubs. However, after examining the difference in advantage " \
" between elite clubs and bottom tier clubs, there was no meaningful difference found. Thus, we moved on to see if discpline played" \
" a role. When looking at discipline, we notice that the elite clubs pick up fewer cards on average. This could explain the seperation between elite clubs and bottom-tier clubs. Two hypotheses for this" \
" is that with more discpline, players are able to maintain greater compusre, which could help when making strategic decisions. Another hypothesis is that greater discpline leads to picking up less cards, so that the best" \
" players stay on the field for the team.")


st.caption("What was most interesting, however, was the offensive gap. The strongest teams generated higher volumes of shots, and were able to apply more attacking pressure throughout the season." \
" We saw this trend when examining the elite clubs and the bottom-tier clubs. This suggests that volume rather than shots on target seperates elite clubs from bottom-tier clubs.")

st.caption("Taking these results together, evidence suggests that sustained offensive aggression along with discpline is strongly associated with long-term success. This analysis" \
" was not done to prove causation, rather it was an exploratory data analysis where we zoomed in on specific teams such as Liverpool, Man City, Brentford, and Wolves across two seasons. We were able to find" \
" meaningful differences in metrics among these four teams, and establish a couple of factors that could explain the seperation between elite clubs and bottom-tier clubs. ")