import streamlit as st
import math

# --- Page Setup ---
st.set_page_config(page_title="Match Predictor", page_icon="🔮", layout="wide")
st.title("🔮 Match Predictor")
st.markdown("Use simple models to predict match outcomes and final scores based on live-match scenarios.")

# --- Load Data from Session State ---
if 'active_data_key' not in st.session_state:
    st.warning("No dataset selected. Please go to the Home page to select a dataset.")
    st.stop()
    
active_data = st.session_state.datasets[st.session_state.active_data_key]
teams = active_data.get('teams', [])

if not teams:
    st.warning("No team data available for the selected era.")
    st.stop()

# --- Win Probability Predictor ---
with st.container(border=True):
    st.subheader("Win Probability Predictor (Chasing Team)")
    
    cols = st.columns([2, 2, 1])
    with cols[0]:
        batting_team = st.selectbox("Batting Team", teams, index=0, key="wp_bat")
    with cols[1]:
        bowling_team = st.selectbox("Bowling Team", teams, index=1, key="wp_bowl")
    with cols[2]:
        target = st.number_input("Target", min_value=1, value=180)

    cols = st.columns(3)
    with cols[0]:
        score = st.number_input("Current Score", min_value=0, value=90)
    with cols[1]:
        overs = st.number_input("Overs Completed", min_value=0.0, max_value=19.5, value=10.0, step=0.1)
    with cols[2]:
        wickets = st.number_input("Wickets Down", min_value=0, max_value=10, value=3)

    if st.button("Predict Win Probability", use_container_width=True):
        if batting_team == bowling_team:
            st.error("Batting and Bowling teams must be different.")
        else:
            runs_left = target - score
            balls_left = 120 - (math.floor(overs) * 6 + (overs * 10 % 10))
            wickets_left = 10 - wickets
            
            if runs_left <= 0:
                win_prob = 100.0
            elif wickets_left == 0 or balls_left <= 0:
                win_prob = 0.0
            else:
                # Replicating the simple logic from your JS code
                win_prob = 50 + (wickets_left * 4) - (runs_left / balls_left * 20)
                win_prob = max(5.0, min(95.0, win_prob))

            loss_prob = 100 - win_prob
            
            res_cols = st.columns(2)
            res_cols[0].metric(f"{batting_team} Win Probability", f"{win_prob:.2f}%")
            res_cols[1].metric(f"{bowling_team} Win Probability", f"{loss_prob:.2f}%")

st.markdown("---")

# --- First Innings Score Predictor ---
with st.container(border=True):
    st.subheader("First Innings Score Predictor")
    
    cols = st.columns(2)
    with cols[0]:
        fip_batting_team = st.selectbox("Batting Team", teams, index=0, key="fip_bat")
    with cols[1]:
        fip_bowling_team = st.selectbox("Bowling Team", teams, index=1, key="fip_bowl")

    cols = st.columns(3)
    with cols[0]:
        fip_overs = st.number_input("Current Overs", min_value=0.0, max_value=19.5, value=8.0, step=0.1)
    with cols[1]:
        fip_runs = st.number_input("Current Runs", min_value=0, value=64)
    with cols[2]:
        fip_wickets = st.number_input("Wickets Down", min_value=0, max_value=10, value=1, key="fip_wickets")

    if st.button("Predict Final Score", use_container_width=True):
        if fip_overs == 0:
            predicted_score = 175 # Default from your JS
        else:
            current_rr = fip_runs / fip_overs
            remaining_overs = 20 - fip_overs
            # Replicating the simple logic from your JS code
            projected_runs = fip_runs + (remaining_overs * (current_rr + 1.5 - (fip_wickets * 0.1)))
            predicted_score = round(projected_runs)
        
        st.metric("Predicted Final Score", f"~{predicted_score} Runs")
