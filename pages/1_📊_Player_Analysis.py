import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Setup ---
st.set_page_config(page_title="Player Analysis", page_icon="📊", layout="wide")
st.title("📊 Player Performance Analysis")
st.markdown("Dive deep into individual player statistics and compare performance archetypes.")

# --- Load Data from Session State ---
if 'active_data_key' not in st.session_state:
    st.warning("No dataset selected. Please go to the Home page to select a dataset.")
    st.stop()

active_data = st.session_state.datasets[st.session_state.active_data_key]
players = active_data.get('players', {})

if not players:
    st.warning("No player data available for the selected era.")
    st.stop()

# --- Helper Functions ---
def get_player_lists(players_dict):
    batsmen = sorted([p for p, d in players_dict.items() if d.get('type') in ['Batsman', 'All-Rounder']])
    bowlers = sorted([p for p, d in players_dict.items() if d.get('type') in ['Bowler', 'All-Rounder']])
    return batsmen, bowlers

batsmen, bowlers = get_player_lists(players)

# --- Player Selection ---
col1, col2 = st.columns(2)
with col1:
    selected_batsman = st.selectbox("Select a Batsman", batsmen, index=0 if batsmen else -1)
with col2:
    selected_bowler = st.selectbox("Select a Bowler", bowlers, index=0 if bowlers else -1)

st.markdown("---")

# --- Player Stats Display ---
col_batsman, col_bowler = st.columns(2)

# Batsman Analysis
with col_batsman:
    st.subheader(f"🏏 Batting Analysis: {selected_batsman}")
    if selected_batsman and selected_batsman in players:
        player_data = players[selected_batsman]
        stats = player_data.get('stats', {})
        
        # Display metrics
        metric_cols = st.columns(2)
        metric_cols[0].metric("Total Runs", f"{stats.get('runs', 'N/A')}")
        metric_cols[1].metric("Strike Rate", f"{stats.get('sr', 'N/A'):.2f}")
        metric_cols[0].metric("Batting Avg", f"{stats.get('avg', 'N/A'):.2f}")
        metric_cols[1].metric("Dismissals", f"{stats.get('dismissals', 'N/A')}")
        
        # Chart
        seasons = player_data.get('seasons', {})
        if seasons:
            season_df = pd.DataFrame(list(seasons.items()), columns=['Season', 'Runs'])
            fig = px.line(season_df, x='Season', y='Runs', title=f"Runs per Season for {selected_batsman}", markers=True)
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No seasonal run data available for this player.")
    else:
        st.info("Select a batsman to see their analysis.")

# Bowler Analysis
with col_bowler:
    st.subheader(f"🔥 Bowling Analysis: {selected_bowler}")
    if selected_bowler and selected_bowler in players:
        player_data = players[selected_bowler]
        stats = player_data.get('stats', {})
        
        # Display metrics
        metric_cols = st.columns(2)
        metric_cols[0].metric("Total Wickets", f"{stats.get('wickets', 'N/A')}")
        metric_cols[1].metric("Economy", f"{stats.get('econ', 'N/A'):.2f}")
        # Use 'bowl_avg' for all-rounders if 'avg' is batting avg
        bowl_avg = stats.get('bowl_avg', stats.get('avg', 'N/A'))
        metric_cols[0].metric("Bowling Avg", f"{bowl_avg:.2f}" if isinstance(bowl_avg, (int, float)) else "N/A")
        metric_cols[1].metric("Overs Bowled", f"{stats.get('overs', 'N/A')}")

        # Chart
        seasons = player_data.get('seasons', {})
        if seasons:
            season_df = pd.DataFrame(list(seasons.items()), columns=['Season', 'Wickets'])
            fig = px.bar(season_df, x='Season', y='Wickets', title=f"Wickets per Season for {selected_bowler}")
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No seasonal wicket data available for this player.")
    else:
        st.info("Select a bowler to see their analysis.")

st.markdown("---")

# --- Player Archetype Analysis ---
st.subheader("🎯 Player Archetypes (Batsmen)")
st.markdown("This scatter plot classifies batsmen based on their career strike rate and batting average. The size of the bubble represents the total runs scored.")

archetype_data = []
for name, data in players.items():
    if data.get('type') in ['Batsman', 'All-Rounder'] and data.get('stats', {}).get('runs', 0) > 100:
        stats = data['stats']
        archetype_data.append({
            'Player': name,
            'Average': stats.get('avg', 0),
            'Strike Rate': stats.get('sr', 0),
            'Runs': stats.get('runs', 1) # Use 1 to avoid size 0
        })

if archetype_data:
    archetype_df = pd.DataFrame(archetype_data)
    fig = px.scatter(
        archetype_df,
        x="Average",
        y="Strike Rate",
        size="Runs",
        color="Player",
        hover_name="Player",
        size_max=60,
        title="Batsman Archetypes: Average vs. Strike Rate"
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Not enough batsman data to generate the archetype plot for this era.")
