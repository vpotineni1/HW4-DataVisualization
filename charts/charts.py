import altair as alt
import pandas as pd
import numpy as np


def base_theme():
    return {
        "config": {
            "view": {"stroke": None},
            "axis": {"labelFontSize": 12, "titleFontSize": 14},
            "legend": {"labelFontSize": 12, "titleFontSize": 14},
        }
    }

def points_table(df: pd.DataFrame, season_label: str) -> pd.DataFrame:
    df = df.copy()
    df['home_win'] = (df['FTR'] == 'H').astype(int)
    df['away_win'] = (df['FTR'] == 'A').astype(int)
    df['away_draw'] = (df['FTR'] == 'D').astype(int)
    df['home_draw'] = (df['FTR'] == 'D').astype(int)

    home_performance = (df.groupby('HomeTeam')).agg(home_wins = ('home_win', 'sum'), home_draws = ('home_draw', 'sum')).reset_index()
    away_performance = (df.groupby('AwayTeam')).agg(away_wins = ('away_win', 'sum'), away_draws = ('away_draw', 'sum')).reset_index()
    home_performance.rename(columns={"HomeTeam": "Team"}, inplace=True)
    away_performance.rename(columns={"AwayTeam": "Team"}, inplace=True) 

    full_table = pd.merge(home_performance,away_performance, on = 'Team', how = 'outer')

    full_table['total_points'] = (full_table['home_wins'] + full_table['away_wins']) * 3 + (full_table['home_draws'] + full_table['away_draws']) * 1
    full_table['Home_Points'] = (full_table['home_wins']) * 3 + (full_table['home_draws']) * 1
    full_table['Away_Points'] = (full_table['away_wins']) * 3 + (full_table['away_draws']) * 1

    full_table['Season'] = season_label

    return full_table 


def dot_chart(first_season: pd.DataFrame, second_season:pd.DataFrame) -> alt.Chart:


    table1 = points_table(first_season, '2023-2024')
    table2 = points_table(second_season, '2024-2025') 

    both_seasons = pd.concat([table1,table2],ignore_index= True)
    
    chart = alt.Chart(both_seasons, title = 'Team Performance Across Seasons').mark_circle(size = 80).encode(
        x= alt.X('total_points:Q', title = 'Points'),
        y=alt.Y("Team:N", sort = '-x'),
        color = alt.Color('Season:N', title = 'Season'),
        tooltip = [alt.Tooltip('Team:N', title = 'Team'), alt.Tooltip('total_points:Q', title = 'Points'),  alt.Tooltip('Season:N', title = 'Season')]
        ).properties(width = 400, height = 600)
    
    return chart


def offensive_metrics(df: pd.DataFrame, season_label: str) -> pd.DataFrame:
    df = df.copy()
    df['Date_American'] = pd.to_datetime(df['Date'], dayfirst= True) 
    home_shots = df[['Date_American','HomeTeam','HS', 'HC', 'HST']]
    home_shots = home_shots.rename(columns={'HomeTeam': 'Team', 'Date_American': 'Date', 'HS': 'Shots', 'HC':'Corners','HST':'Shots_on_Target'})
    away_shots = df[['Date_American','AwayTeam','AS','AC','AST']]
    away_shots = away_shots.rename(columns={'AwayTeam': 'Team', 'Date_American': 'Date', 'AS' :'Shots','AC':'Corners','AST':'Shots_on_Target'}) 

    shots = pd.concat([home_shots, away_shots])
    shots = shots.sort_values(['Team','Date'])
    shots['MatchWeek'] = shots.groupby('Team').cumcount() 

    shots = shots.reset_index().melt(id_vars= ['MatchWeek', 'Team'],value_vars=['Shots','Corners','Shots_on_Target'], var_name = 'Metric', value_name = 'Value')
    shots['rolling_average'] = (shots.groupby(['Team','Metric'])['Value'].rolling(window = 5, min_periods = 1).mean().reset_index(level = [0,1], drop = True))

    shots['Season'] = season_label

    return shots

def rolling_points_chart(first_season: pd.DataFrame, second_season:pd.DataFrame) -> alt.Chart:

    selection = alt.selection_point(fields=['Team'], empty = False, value = [{'Team': 'Man City'}, {'Team' : 'Liverpool'}, {'Team': 'Brentford'}, {'Team' : 'Wolves'}])
    input_dropdown = alt.binding_select(options=['2023-2024', '2024-2025'], name='Season: ') 
    season_selection = alt.selection_point(fields=['Season'], bind=input_dropdown, value = '2023-2024')
    options = ['Shots', 'Corners', 'Shots_on_Target']
    labels = ['Shots', 'Corners', 'Shots on Target'] 
    input_dropdown2 = alt.binding_radio(options=options, labels=labels , name='Offensive Metric: ')
    metric_selection = alt.selection_point(fields=['Metric'], bind=input_dropdown2, value = 'Shots')

    table1 = points_table(first_season, '2023-2024')
    table2 = points_table(second_season, '2024-2025')
    both_seasons = pd.concat([table1,table2],ignore_index= True)

    shots1 = offensive_metrics(first_season, '2023-2024')
    shots2 = offensive_metrics(second_season, '2024-2025')
    shots_seasons = pd.concat([shots1,shots2],ignore_index= True)

    points_chart = alt.Chart(both_seasons, title = "Premier League Points Table").transform_filter(season_selection).mark_bar().encode(
        x= alt.X('total_points:Q', title = 'Points'),
        y=alt.Y("Team:O", sort = '-x'),
        color = alt.Color('total_points:Q', scale = alt.Scale(scheme = 'viridis'), title = 'Points'),
        opacity = alt.condition(selection, alt.value(1.0), alt.value(0.3)),
        tooltip = [alt.Tooltip('Team:N', title = 'Team'), alt.Tooltip('total_points:Q', title = 'Points')]
        ).properties(width = 400,height=600).add_params(selection, season_selection)
    
    rolling_chart = alt.Chart(shots_seasons, title = "Rolling Average Offensive Performance by Team").transform_filter(season_selection).transform_filter(selection).transform_filter(metric_selection).mark_line().encode(
        x= alt.X('MatchWeek:Q', title = 'MatchWeek'),
        y=alt.Y("rolling_average:Q", title = 'Rolling Average'),
        color = alt.Color('Team:N', title = 'Selected Team'),
        tooltip = [alt.Tooltip('Team:N', title = 'Team'), alt.Tooltip('Metric:N', title = 'Metric'), alt.Tooltip('rolling_average:Q', title = 'Average Over Past 5 Games')]
        ).properties(width = 700,height=400).add_params(metric_selection, selection)
    
    combined = points_chart | rolling_chart

    return combined



def location_chart(first_season: pd.DataFrame, second_season:pd.DataFrame) -> alt.Chart:
    selection = alt.selection_point(fields=['Team'], empty = False, value = [{'Team': 'Man City'}, {'Team' : 'Liverpool'}, {'Team': 'Brentford'}, {'Team' : 'Wolves'}])
    table1 = points_table(first_season, '2023-2024')
    table2 = points_table(second_season, '2024-2025')
    both_seasons = pd.concat([table1,table2],ignore_index= True)  

    both_seasons['percent_home'] = (both_seasons['Home_Points']/ both_seasons['total_points']) 
    both_seasons['percent_away'] = (both_seasons['Away_Points']/ both_seasons['total_points']) 

    homevaway = both_seasons.melt(id_vars=['Team','Season'], value_vars =['percent_home', 'percent_away'], var_name = 'Location', value_name = 'Percent_Points')
    homevaway['Location'] = homevaway['Location'].replace({'percent_home':'Home', 'percent_away':'Away'}) 

    
    input_dropdown = alt.binding_select(options=['2023-2024', '2024-2025'], name='Season: ') 

    season_selection = alt.selection_point(fields=['Season'], bind=input_dropdown, value = '2023-2024')

    chart = alt.Chart(homevaway, title = 'Perecentage of Points won at Home vs. Away').transform_filter(season_selection).mark_bar().encode(
        x= alt.X('Percent_Points:Q', title = 'Percentage of Points', axis = alt.Axis(format = '%') ),
        y= alt.Y("Team:N", sort = '-x'),
        color = alt.Color('Location:N', legend = alt.Legend(title = "Location"), scale = alt.Scale(scheme = 'redblue')),
        opacity = alt.condition(selection, alt.value(1.0), alt.value(0.3)),
        tooltip = [alt.Tooltip('Percent_Points:Q', title = 'Percentage'), alt.Tooltip('Location:N'), alt.Tooltip('Team:N')]
        ).properties(width = 400,height=600).add_params(season_selection,selection)
    
    return chart


def cards_table(df:pd.DataFrame, season_label:str) -> pd.DataFrame:
    df = df.copy()

    home_yellow = df.groupby("HomeTeam")['HY'].sum()
    away_yellow = df.groupby("AwayTeam")["AY"].sum() 

    total_yellow = home_yellow + away_yellow
    yellow_df = total_yellow.reset_index()
    yellow_df.columns = ["Team", "Total_Yellow_Cards"] 

    home_red = df.groupby("HomeTeam")['HR'].sum()
    away_red = df.groupby("AwayTeam")['AR'].sum() 

    total_red = home_red + away_red
    red_df = total_red.reset_index()
    red_df.columns = ["Team", "Total_Red_Cards"] 

    cards_df = pd.merge(yellow_df, red_df, on = 'Team')

    cards_df['Season'] = season_label 

    return cards_df


def cards_chart(first_season: pd.DataFrame, second_season:pd.DataFrame) -> alt.Chart:

    selection = alt.selection_point(fields=['Team'], empty = False, value = [{'Team': 'Man City'}, {'Team' : 'Liverpool'}, {'Team': 'Brentford'}, {'Team' : 'Wolves'}])

    cards1 = cards_table(first_season, '2023-2024')
    cards2 = cards_table(second_season, '2024-2025') 
 
    cards_full = pd.concat([cards1,cards2], ignore_index= True) 

    cards_full['Total_Cards'] = cards_full['Total_Yellow_Cards'] + cards_full['Total_Red_Cards'] 

    input_dropdown = alt.binding_select(options=['2023-2024', '2024-2025'], name='Season: ') 

    season_selection = alt.selection_point(fields=['Season'], bind=input_dropdown, value = '2023-2024')

    chart = alt.Chart(cards_full, title = "Total Cards by Team").transform_filter(season_selection).mark_bar().encode(
        y=alt.Y("Team:N", sort="-x"),
        x="Total_Cards:Q",
        color = alt.Color('Total_Cards:Q', scale = alt.Scale(scheme = 'viridis'), title = 'Total Cards'),
        opacity = alt.condition(selection, alt.value(1.0), alt.value(0.3)),
        tooltip = [alt.Tooltip('Team:N', title = 'Team'), alt.Tooltip('Total_Cards:Q', title = 'Total Cards')]
        ).properties(width = 400,height=600).add_params(season_selection, selection)
    
    return chart


def chart_dashboard(first_season: pd.DataFrame, second_season:pd.DataFrame) -> alt.Chart:


    selection = alt.selection_point(fields=['Team'], empty = False)
    input_dropdown = alt.binding_select(options=['2023-2024', '2024-2025'], name='Season: ') 
    season_selection = alt.selection_point(fields=['Season'], bind=input_dropdown, value = '2023-2024')
    options = ['Shots', 'Corners', 'Shots_on_Target']
    labels = ['Shots', 'Corners', 'Shots on Target'] 
    input_dropdown2 = alt.binding_radio(options=options, labels=labels , name='Offensive Metric: ')
    metric_selection = alt.selection_point(fields=['Metric'], bind=input_dropdown2, value = 'Shots')

    cards1 = cards_table(first_season, '2023-2024')
    cards2 = cards_table(second_season, '2024-2025') 
 
    cards_full = pd.concat([cards1,cards2], ignore_index= True) 

    cards_full['Total_Cards'] = cards_full['Total_Yellow_Cards'] + cards_full['Total_Red_Cards'] 


    table1 = points_table(first_season, '2023-2024')
    table2 = points_table(second_season, '2024-2025')
    both_seasons = pd.concat([table1,table2],ignore_index= True)  

    homevaway = both_seasons.melt(id_vars=['Team','Season'], value_vars =['Home_Points', 'Away_Points'], var_name = 'Location', value_name = 'Points')
    homevaway['Location'] = homevaway['Location'].replace({'Home_Points':'Home', 'Away_Points':'Away'}) 


    shots1 = offensive_metrics(first_season, '2023-2024')
    shots2 = offensive_metrics(second_season, '2024-2025')
    shots_seasons = pd.concat([shots1,shots2],ignore_index= True)


    points_chart = alt.Chart(both_seasons, title = "Premier League Points Table").transform_filter(season_selection).mark_bar().encode(
        x= alt.X('total_points:Q', title = 'Points'),
        y=alt.Y("Team:O", sort = '-x'),
        color = alt.Color('total_points:Q', scale = alt.Scale(scheme = 'viridis'), title = 'Points'),
        opacity = alt.condition(selection, alt.value(1.0), alt.value(0.3)),
        tooltip = [alt.Tooltip('Team:N', title = 'Team'), alt.Tooltip('total_points:Q', title = 'Points')]
        ).properties(width = 400,height=600).add_params(selection, season_selection)
    
    rolling_chart = alt.Chart(shots_seasons, title = "Rolling Average Offensive Performance by Team").transform_filter(season_selection).transform_filter(selection).transform_filter(metric_selection).mark_line().encode(
        x= alt.X('MatchWeek:Q', title = 'MatchWeek'),
        y=alt.Y("rolling_average:Q", title = 'Rolling Average'),
        color = alt.Color('Team:N', title = 'Selected Team'),
        tooltip = [alt.Tooltip('Team:N', title = 'Team'), alt.Tooltip('Metric:N', title = 'Metric'), alt.Tooltip('rolling_average:Q', title = 'Average Over Past 5 Games')]
        ).properties(width = 700,height=400).add_params(metric_selection, selection, season_selection)

    cards_chart = alt.Chart(cards_full, title = "Total Cards by Team").transform_filter(season_selection).transform_filter(selection).mark_bar().encode(
        y=alt.Y("Team:N", sort="-x"),
        x="Total_Cards:Q",
        color = alt.Color('Total_Cards:Q', scale = alt.Scale(scheme = 'viridis'), title = 'Total Cards'),
        tooltip = [alt.Tooltip('Team:N', title = 'Team'), alt.Tooltip('Total_Cards:Q', title = 'Total Cards')]
        ).properties(width = 400,height= alt.Step(25)).add_params(season_selection, selection)
    
    location_chart = alt.Chart(homevaway, title = 'Total Home vs. Away Points').transform_filter(season_selection).transform_filter(selection).mark_bar().encode(
        x= alt.X('Points:Q'),
        y= alt.Y("Team:N", sort = '-x'),
        color = alt.Color('Location:N', legend = alt.Legend(title = "Location")),
        tooltip = [alt.Tooltip('Points:Q', title = 'Points'), alt.Tooltip('Location:N'), alt.Tooltip('Team:N')]
        ).properties(width = 400, height = alt.Step(25)).add_params(season_selection,selection)
    
    dot_chart = alt.Chart(both_seasons, title = 'Team Performance Across Seasons').mark_circle(size = 80).encode(
        x= alt.X('total_points:Q', title = 'Points'),
        y=alt.Y("Team:N", sort = '-x'),
        color = alt.Color('Season:N', title = 'Season'),
        tooltip = [alt.Tooltip('Team:N', title = 'Team'), alt.Tooltip('total_points:Q', title = 'Points'),  alt.Tooltip('Season:N', title = 'Season')]
        ).properties(width = 600, height = 600)
    
    left_column = alt.vconcat(points_chart, location_chart, cards_chart).resolve_scale(color = 'independent')
    right_column = alt.vconcat(dot_chart, rolling_chart).resolve_scale(color = 'independent')

    dashboard = alt.hconcat(left_column, right_column).properties(padding = {'top' : 80, 'left' :80, 'bottom':80, 'right':80})
    dashboard = dashboard.properties(title = alt.TitleParams('Interactive Dashboard of Premier League Statistics', fontSize = 30, anchor = 'middle', offset = 50))
    
    return dashboard