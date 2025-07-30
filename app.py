import streamlit as st
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="Cricket Vision | Home",
    page_icon="🏏",
    layout="wide"
)

# --- Data Store (ENHANCED) ---
# I've added more details like 'venue' in matches and 'h2h' stats in players.
def get_datasets():
    datasets = {
        "historicData": {
            "name": "Historic Era (2008-2016)",
            "teams": ["Chennai Super Kings", "Mumbai Indians", "Royal Challengers Bangalore", "Kolkata Knight Riders", "Kings XI Punjab", "Rajasthan Royals", "Deccan Chargers", "Pune Warriors"],
            "players": {
                "SR Tendulkar": { "type": "Batsman", "seasons": { 2010: 618, 2011: 553, 2012: 324, 2013: 287 }, "stats": { "runs": 2334, "avg": 34.83, "sr": 119.81, "dismissals": 67 }, "h2h": { "SL Malinga": {"runs": 45, "balls": 30, "dismissals": 2}, "A Mishra": {"runs": 60, "balls": 45, "dismissals": 1} } },
                "CH Gayle": { "type": "Batsman", "seasons": { 2011: 608, 2012: 733, 2013: 720, 2015: 491 }, "stats": { "runs": 3420, "avg": 43.29, "sr": 152.75, "dismissals": 79 }, "h2h": { "Harbhajan Singh": {"runs": 80, "balls": 40, "dismissals": 1} } },
                "V Sehwag": { "type": "Batsman", "seasons": { 2011: 424, 2012: 495, 2014: 455 }, "stats": { "runs": 2728, "avg": 27.55, "sr": 155.44, "dismissals": 99 }, "h2h": {} },
                "G Gambhir": { "type": "Batsman", "seasons": { 2012: 590, 2016: 501 }, "stats": { "runs": 4217, "avg": 31.01, "sr": 123.88, "dismissals": 136 }, "h2h": {} },
                "SK Raina": { "type": "Batsman", "seasons": { 2010: 520, 2013: 548, 2014: 523 }, "stats": { "runs": 5528, "avg": 32.51, "sr": 136.76, "dismissals": 170 }, "h2h": {} },
                "SL Malinga": { "type": "Bowler", "seasons": { 2011: 28, 2012: 22, 2013: 20, 2015: 24 }, "stats": { "wickets": 170, "econ": 7.14, "avg": 19.8, "overs": 471.1 } },
                "A Mishra": { "type": "Bowler", "seasons": { 2011: 19, 2013: 21, 2016: 13 }, "stats": { "wickets": 166, "econ": 7.35, "avg": 23.95, "overs": 541.1 } },
                "Harbhajan Singh": { "type": "Bowler", "seasons": { 2013: 24, 2015: 18 }, "stats": { "wickets": 150, "econ": 7.07, "avg": 26.44, "overs": 569.2 } },
                "DJ Bravo": { "type": "All-Rounder", "seasons": { 2013: 32, 2015: 26 }, "stats": { "runs": 1538, "avg": 24.81, "sr": 128.93, "dismissals": 62, "wickets": 183, "econ": 8.38, "bowl_avg": 23.82, "overs": 543.2 }, "h2h": {} },
                "SR Watson": { "type": "All-Rounder", "seasons": { 2013: 543, 2016: 179 }, "stats": { "runs": 3874, "avg": 30.99, "sr": 139.53, "dismissals": 125, "wickets": 92, "econ": 7.93, "bowl_avg": 29.15, "overs": 343.4 }, "h2h": {} },
            },
            "matches": [
                { "team1": "Mumbai Indians", "team2": "Chennai Super Kings", "winner": "Mumbai Indians", "venue": "Wankhede Stadium, Mumbai" },
                { "team1": "Mumbai Indians", "team2": "Chennai Super Kings", "winner": "Chennai Super Kings", "venue": "MA Chidambaram Stadium, Chennai" },
                { "team1": "Royal Challengers Bangalore", "team2": "Kolkata Knight Riders", "winner": "Kolkata Knight Riders", "venue": "Eden Gardens, Kolkata" },
                { "team1": "Kings XI Punjab", "team2": "Rajasthan Royals", "winner": "Kings XI Punjab", "venue": "Sawai Mansingh Stadium, Jaipur" },
                { "team1": "Deccan Chargers", "team2": "Pune Warriors", "winner": "Deccan Chargers", "venue": "DY Patil Stadium, Mumbai" },
                { "team1": "Mumbai Indians", "team2": "Kolkata Knight Riders", "winner": "Mumbai Indians", "venue": "Wankhede Stadium, Mumbai" },
            ]
        },
        "modernData": {
            "name": "Modern Era (2017-2022)",
            "teams": ["Chennai Super Kings", "Mumbai Indians", "Royal Challengers Bangalore", "Kolkata Knight Riders", "Delhi Capitals", "Punjab Kings", "Rajasthan Royals", "Sunrisers Hyderabad", "Gujarat Titans"],
            "players": {
                "V Kohli": { "type": "Batsman", "seasons": { 2018: 530, 2019: 464, 2020: 466, 2021: 405, 2022: 341 }, "stats": { "runs": 6624, "avg": 36.2, "sr": 129.15, "dismissals": 183 }, "h2h": {"JJ Bumrah": {"runs": 140, "balls": 105, "dismissals": 4}, "K Rabada": {"runs": 90, "balls": 60, "dismissals": 2}, "R Ashwin": {"runs": 120, "balls": 110, "dismissals": 1}} },
                "RG Sharma": { "type": "Batsman", "seasons": { 2018: 286, 2019: 405, 2020: 332, 2021: 381, 2022: 268 }, "stats": { "runs": 5879, "avg": 29.54, "sr": 129.89, "dismissals": 199 }, "h2h": {"YS Chahal": {"runs": 95, "balls": 70, "dismissals": 3}} },
                "KL Rahul": { "type": "Batsman", "seasons": { 2018: 659, 2020: 670, 2022: 616 }, "stats": { "runs": 3889, "avg": 47.43, "sr": 136.22, "dismissals": 82 }, "h2h": {} },
                "S Dhawan": { "type": "Batsman", "seasons": { 2019: 521, 2020: 618, 2022: 460 }, "stats": { "runs": 6244, "avg": 35.08, "sr": 126.35, "dismissals": 178 }, "h2h": {} },
                "DA Warner": { "type": "Batsman", "seasons": { 2017: 641, 2019: 692, 2020: 548 }, "stats": { "runs": 5881, "avg": 41.13, "sr": 140.69, "dismissals": 143 }, "h2h": {} },
                "JJ Bumrah": { "type": "Bowler", "seasons": { 2018: 17, 2019: 19, 2020: 27, 2021: 21, 2022: 15 }, "stats": { "wickets": 145, "econ": 7.39, "avg": 23.31, "overs": 457.1 } },
                "YS Chahal": { "type": "Bowler", "seasons": { 2018: 12, 2019: 18, 2020: 21, 2021: 18, 2022: 27 }, "stats": { "wickets": 170, "econ": 7.61, "avg": 21.69, "overs": 483.1 } },
                "K Rabada": { "type": "Bowler", "seasons": { 2019: 25, 2020: 30, 2022: 23 }, "stats": { "wickets": 99, "econ": 8.21, "avg": 20.52, "overs": 382.2 } },
                "R Ashwin": { "type": "Bowler", "seasons": { 2018: 14, 2019: 15, 2022: 12 }, "stats": { "wickets": 157, "econ": 6.94, "avg": 28.46, "overs": 649.3 } },
                "AD Russell": { "type": "All-Rounder", "seasons": { 2018: 316, 2019: 510, 2022: 335 }, "stats": { "runs": 2035, "avg": 29.07, "sr": 177.88, "dismissals": 70, "wickets": 89, "econ": 9.19, "bowl_avg": 26.5, "overs": 271.1 }, "h2h": {} },
            },
            "matches": [
                { "team1": "Mumbai Indians", "team2": "Chennai Super Kings", "winner": "Mumbai Indians", "venue": "Wankhede Stadium, Mumbai" },
                { "team1": "Gujarat Titans", "team2": "Rajasthan Royals", "winner": "Gujarat Titans", "venue": "Narendra Modi Stadium, Ahmedabad" },
                { "team1": "Delhi Capitals", "team2": "Sunrisers Hyderabad", "winner": "Delhi Capitals", "venue": "Arun Jaitley Stadium, Delhi" },
                { "team1": "Royal Challengers Bangalore", "team2": "Punjab Kings", "winner": "Royal Challengers Bangalore", "venue": "M. Chinnaswamy Stadium, Bengaluru" },
            ]
        },
        # Future data remains the same for now
        "futureData": {
            "name": "Future Era (Simulated 2023-2025)",
            "teams": ["Gujarat Titans", "Lucknow Super Giants", "Rajasthan Royals", "Royal Challengers Bangalore", "Delhi Capitals", "Punjab Kings", "Kolkata Knight Riders", "Sunrisers Hyderabad", "Chennai Super Kings", "Mumbai Indians"],
            "players": {
                "JC Buttler": { "type": "Batsman", "seasons": { 2023: 392, 2024: 570, 2025: 650 }, "stats": { "runs": 4000, "avg": 38.5, "sr": 150.1, "dismissals": 105 }, "h2h": {} },
                "Shubman Gill": { "type": "Batsman", "seasons": { 2023: 890, 2024: 420, 2025: 750 }, "stats": { "runs": 4000, "avg": 40.0, "sr": 140.0, "dismissals": 100 }, "h2h": {} },
                "H Pandya": { "type": "All-Rounder", "seasons": { 2023: 346, 2024: 250, 2025: 450 }, "stats": { "runs": 3000, "avg": 30.0, "sr": 148.0, "dismissals": 100, "wickets": 80, "econ": 8.9, "bowl_avg": 30.0, "overs": 300 }, "h2h": {} },
                "R Khan": { "type": "Bowler", "seasons": { 2023: 27, 2024: 22, 2025: 30 }, "stats": { "wickets": 180, "econ": 6.5, "avg": 20.0, "overs": 600 } },
            },
            "matches": []
        }
    }
    return datasets

# --- Helper Functions for Leaderboards ---
def get_top_run_scorers(players_data, top_n=5):
    batsmen = [
        {'Player': name, 'Runs': data['stats']['runs']}
        for name, data in players_data.items()
        if 'runs' in data.get('stats', {})
    ]
    if not batsmen:
        return pd.DataFrame()
    df = pd.DataFrame(batsmen)
    return df.sort_values('Runs', ascending=False).head(top_n)

def get_top_wicket_takers(players_data, top_n=5):
    bowlers = [
        {'Player': name, 'Wickets': data['stats']['wickets']}
        for name, data in players_data.items()
        if 'wickets' in data.get('stats', {})
    ]
    if not bowlers:
        return pd.DataFrame()
    df = pd.DataFrame(bowlers)
    return df.sort_values('Wickets', ascending=False).head(top_n)


# --- Session State Initialization ---
if 'datasets' not in st.session_state:
    st.session_state.datasets = get_datasets()

if 'active_data_key' not in st.session_state:
    st.session_state.active_data_key = "modernData"

# --- Sidebar ---
st.sidebar.title("🔄 Switch Dataset")
dataset_options = {key: data['name'] for key, data in st.session_state.datasets.items()}

def on_dataset_change():
    st.session_state.active_data_key = st.session_state.dataset_selector

selected_key = st.sidebar.selectbox(
    "Select Dataset Era",
    options=list(dataset_options.keys()),
    format_func=lambda key: dataset_options[key],
    key="dataset_selector",
    on_change=on_dataset_change
)

# --- Main Page Content ---
active_data = st.session_state.datasets[st.session_state.active_data_key]

st.title("🏏 Cricket Vision: Professional Analytics")
st.markdown("---")

with st.container(border=True):
    st.markdown(f"<h2 style='text-align: center; color: #2563EB;'>Unlock the Story in the Stats</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>From legendary players of the past to the superstars of today, explore comprehensive data across different eras of T20 cricket.</p>", unsafe_allow_html=True)

st.markdown("### 📈 Current Dataset Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Current Era", active_data['name'])
col2.metric("Players Analyzed", len(active_data['players']))
col3.metric("Teams Covered", len(active_data['teams']))

st.markdown("---")

# --- NEW: Tournament Leaders Section ---
st.header("🏆 Tournament Leaders")
leader_col1, leader_col2 = st.columns(2)

with leader_col1:
    st.subheader("Top Run Scorers")
    top_scorers_df = get_top_run_scorers(active_data['players'])
    if not top_scorers_df.empty:
        st.dataframe(top_scorers_df, use_container_width=True, hide_index=True)
    else:
        st.info("No batting data available for this era.")

with leader_col2:
    st.subheader("Top Wicket Takers")
    top_takers_df = get_top_wicket_takers(active_data['players'])
    if not top_takers_df.empty:
        st.dataframe(top_takers_df, use_container_width=True, hide_index=True)
    else:
        st.info("No bowling data available for this era.")

st.markdown("---")

st.subheader("🚀 Getting Started")
# ... (rest of the home page is the same)
col_a, col_b = st.columns(2)

with col_a:
    with st.container(border=True):
        st.markdown("#### 📊 Analyze a Player")
        st.write("Dive deep into individual player statistics, trends, and performance archetypes.")
        if st.button("Explore Players"):
            st.switch_page("pages/1_📊_Player_Analysis.py")

with col_b:
    with st.container(border=True):
        st.markdown("#### ⚔️ Analyze Team Strategy")
        st.write("Compare teams head-to-head and analyze their performance by phase of the game.")
        if st.button("Explore Teams"):
            st.switch_page("pages/3_⚔️_Team_Strategy.py")



