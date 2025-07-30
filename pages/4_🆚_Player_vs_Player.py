import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- Page Setup ---
st.set_page_config(page_title="Player vs Player", page_icon="🆚", layout="wide")
st.title("🆚 Player vs. Player (H2H)")
st.markdown("Analyze the head-to-head battle between a specific batsman and bowler.")

# --- Load Data from Session State ---
if 'active_data_key' not in st.session_state:
    st.warning("No dataset selected. Please go to the Home page to select a dataset.")
    st.stop()

active_data = st.session_state.datasets[st.session_state.active_data_key]
players = active_data.get('players', {})

if not players:
    st.warning("No player data available for the selected era.")
    st.stop()

# --- Helper Functions to get player lists ---
def get_player_lists(players_dict):
    batsmen = sorted([p for p, d in players_dict.items() if d.get('type') in ['Batsman', 'All-Rounder'] and d.get('h2h')])
    bowlers = sorted([p for p, d in players_dict.items() if d.get('type') in ['Bowler', 'All-Rounder']])
    return batsmen, bowlers

batsmen_with_h2h, all_bowlers = get_player_lists(players)

if not batsmen_with_h2h:
    st.info("No simulated Player vs. Player data is available for this era.")
    st.stop()

# --- Selection Boxes ---
col1, col2 = st.columns(2)
with col1:
    selected_batsman = st.selectbox("Select Batsman", batsmen_with_h2h)
with col2:
    # Filter bowlers to only those the selected batsman has faced
    available_bowlers = sorted(list(players[selected_batsman].get('h2h', {}).keys()))
    if not available_bowlers:
        st.warning(f"No H2H data found for {selected_batsman}.")
        st.stop()
    selected_bowler = st.selectbox("Select Bowler", available_bowlers)


st.markdown("---")

# --- H2H Analysis ---
if selected_batsman and selected_bowler:
    st.header(f"Matchup: {selected_batsman} (Batsman) vs {selected_bowler} (Bowler)")
    
    h2h_data = players[selected_batsman].get('h2h', {}).get(selected_bowler)
    
    if not h2h_data:
        st.warning(f"No specific H2H data found for this matchup.")
    else:
        runs = h2h_data.get('runs', 0)
        balls = h2h_data.get('balls', 0)
        dismissals = h2h_data.get('dismissals', 0)
        
        strike_rate = (runs / balls * 100) if balls > 0 else 0
        average = (runs / dismissals) if dismissals > 0 else "Not Out"
        
        # Display Metrics
        metric_cols = st.columns(4)
        metric_cols[0].metric("Runs Scored", runs)
        metric_cols[1].metric("Balls Faced", balls)
        metric_cols[2].metric("Dismissals", dismissals)
        metric_cols[3].metric("Strike Rate", f"{strike_rate:.2f}")
        
        if isinstance(average, float):
            st.metric("Average", f"{average:.2f}")
        else:
            st.metric("Average", "∞ (Not Out)")

        # Donut chart for simulated run breakdown
        st.subheader("Simulated Run Breakdown")
        
        # Simulate a breakdown for visualization
        fours = runs // 6
        sixes = runs // 10
        singles = runs - (fours * 4) - (sixes * 6)
        dots = max(0, balls - (fours + sixes + singles))
        
        run_labels = ['Dots', '1s, 2s, 3s', 'Fours', 'Sixes']
        run_values = [dots, singles, fours, sixes]
        
        fig = go.Figure(data=[go.Pie(labels=run_labels, values=run_values, hole=.4,
                                     marker_colors=['#a0aec0', '#4299e1', '#38b2ac', '#ed64a6'])])
        fig.update_layout(title_text='Runs Distribution (Simulated)', height=400)
        st.plotly_chart(fig, use_container_width=True)

