import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Setup ---
st.set_page_config(page_title="Team Strategy", page_icon="⚔️", layout="wide")
st.title("⚔️ Team Strategy & Head-to-Head")
st.markdown("Analyze team rivalries and their performance across different phases of an innings.")

# --- Load Data from Session State ---
if 'active_data_key' not in st.session_state:
    st.warning("No dataset selected. Please go to the Home page to select a dataset.")
    st.stop()

active_data = st.session_state.datasets[st.session_state.active_data_key]
teams = active_data.get('teams', [])
matches = active_data.get('matches', [])

if not teams:
    st.warning("No team data available for the selected era.")
    st.stop()

# --- Head-to-Head Analysis ---
with st.container(border=True):
    st.subheader("Head-to-Head (H2H) Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        team1 = st.selectbox("Select Team 1", teams, index=0)
    with col2:
        team2 = st.selectbox("Select Team 2", teams, index=1)

    if st.button("Analyze H2H", use_container_width=True):
        if team1 == team2:
            st.error("Please select two different teams.")
        else:
            relevant_matches = [
                m for m in matches 
                if (m['team1'] == team1 and m['team2'] == team2) or \
                   (m['team1'] == team2 and m['team2'] == team1)
            ]
            
            if not relevant_matches:
                st.warning(f"No H2H data available between {team1} and {team2} for this era.")
            else:
                total_matches = len(relevant_matches)
                team1_wins = sum(1 for m in relevant_matches if m['winner'] == team1)
                team2_wins = sum(1 for m in relevant_matches if m['winner'] == team2)

                res_col1, res_col2 = st.columns([1, 1.5])
                
                with res_col1:
                    st.metric("Total Matches Played", total_matches)
                    st.metric(f"{team1} Wins", team1_wins)
                    st.metric(f"{team2} Wins", team2_wins)

                with res_col2:
                    win_data = pd.DataFrame({
                        'Team': [team1, team2],
                        'Wins': [team1_wins, team2_wins]
                    })
                    fig = px.pie(
                        win_data, 
                        names='Team', 
                        values='Wins', 
                        title=f'H2H Win Distribution: {team1} vs {team2}',
                        color='Team',
                        color_discrete_map={team1: '#2563EB', team2: '#F59E0B'}
                    )
                    fig.update_layout(height=350)
                    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# --- Phase Analysis ---
# NOTE: This uses mock data, as the original dataset doesn't contain ball-by-ball info.
# In a real project, this would be computed from a detailed dataset.
phase_data_mock = {
    "Mumbai Indians": {
        "batting": {"Powerplay (1-6)": {"runs": 45, "wickets": 1, "rr": 7.5}, "Middle (7-15)": {"runs": 80, "wickets": 2, "rr": 8.88}, "Death (16-20)": {"runs": 60, "wickets": 2, "rr": 12.0}},
        "bowling": {"Powerplay (1-6)": {"conceded": 50, "wickets": 2, "econ": 8.33}, "Middle (7-15)": {"conceded": 75, "wickets": 3, "econ": 8.33}, "Death (16-20)": {"conceded": 55, "wickets": 3, "econ": 11.0}}
    },
    "Chennai Super Kings": {
        "batting": {"Powerplay (1-6)": {"runs": 52, "wickets": 0, "rr": 8.67}, "Middle (7-15)": {"runs": 75, "wickets": 3, "rr": 8.33}, "Death (16-20)": {"runs": 65, "wickets": 1, "rr": 13.0}},
        "bowling": {"Powerplay (1-6)": {"conceded": 48, "wickets": 1, "econ": 8.0}, "Middle (7-15)": {"conceded": 80, "wickets": 2, "econ": 8.88}, "Death (16-20)": {"conceded": 50, "wickets": 4, "econ": 10.0}}
    }
}

with st.container(border=True):
    st.subheader("Performance by Innings Phase")
    selected_team_phase = st.selectbox("Select Team for Phase Analysis", teams)

    if selected_team_phase in phase_data_mock:
        data = phase_data_mock[selected_team_phase]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"#### Batting by Phase: {selected_team_phase}")
            batting_df = pd.DataFrame(data['batting']).T.reset_index()
            batting_df.columns = ["Phase", "Runs", "Wickets", "Run Rate"]
            st.dataframe(batting_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown(f"#### Bowling by Phase: {selected_team_phase}")
            bowling_df = pd.DataFrame(data['bowling']).T.reset_index()
            bowling_df.columns = ["Phase", "Runs Conceded", "Wickets", "Economy"]
            st.dataframe(bowling_df, use_container_width=True, hide_index=True)
    else:
        st.info(f"No mock phase data available for {selected_team_phase}. This is a demonstrative feature.")
