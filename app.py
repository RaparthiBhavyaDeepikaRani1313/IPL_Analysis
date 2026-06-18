import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="IPL Analysis Dashboard",
    page_icon="🏏",
    layout="wide"
)
st.markdown("""
<style>


[data-testid="stDataFrame"] {
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)
# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

h1, h2, h3 {
    color: #0b3d91;
}

[data-testid="stSidebar"] {
    background-color: #0b3d91;
}

[data-testid="stSidebar"] * {
    color: white;
}

.metric-box {
    background-color: white;
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    deliveries = pd.read_csv("deliveries.csv")

    try:
        player_stats = pd.read_csv("most_runs_average_strikerate.csv")
    except:
        player_stats = None

    return matches, deliveries, player_stats


matches, deliveries, player_stats = load_data()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title("🏏 IPL Dashboard")

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📊 Overview",
        "🏏 Team Analysis",
        "👤 Player Analysis",
        "🏟 Venue Analysis",
        "🔥 Team Comparison",
        "🏆 Awards Analysis",
        "ℹ️ About"
    ]
)

st.sidebar.markdown("---")
st.sidebar.write("Developed By")
st.sidebar.write("RAPARTHI BHAVYA DEEPIKA RANI")

# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------
if menu == "🏠 Home":

    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    st.title("🏏 Indian Premier League (IPL)")

    st.markdown("""
The **Indian Premier League (IPL)** is the premier professional Twenty20 (T20) cricket league in India and one of the most popular and financially successful sporting competitions in the world. Since its inception in 2008 by the **Board of Control for Cricket in India (BCCI)**, the IPL has revolutionized the game of cricket by combining high-quality competition, entertainment, and advanced sports management.

The tournament features franchise-based teams representing major Indian cities and attracts some of the finest cricket players from across the globe. Every season, millions of fans follow the league passionately, making it one of the most-watched sporting events internationally. The IPL has provided a platform for young and emerging cricketers to showcase their talent alongside established international stars, significantly contributing to the growth and development of cricket.

Over the years, the league has witnessed numerous memorable matches, record-breaking performances, thrilling finishes, and legendary rivalries. Its innovative format, strategic team compositions, player auctions, and dynamic gameplay have made it a benchmark for T20 cricket leagues worldwide. The IPL has also played a crucial role in introducing data-driven decision-making and advanced performance analysis in modern cricket.

This **IPL Analysis Dashboard** is designed to provide a comprehensive exploration of historical IPL data through interactive visualizations and statistical insights. The dashboard enables users to analyze various aspects of the tournament, including team performances, player achievements, venue statistics, season-wise trends, match outcomes, and championship records.

Key features of this dashboard include:

* Analysis of team-wise performance across different seasons.
* Detailed player statistics such as runs scored, wickets taken, strike rates, and batting averages.
* Venue-based insights highlighting scoring patterns and match outcomes.
* Season-wise comparison of teams and players.
* Toss decision analysis and its impact on match results.
* Winning trends, championship records, and head-to-head team comparisons.
* Identification of top performers and emerging patterns through data visualization.
* Interactive charts and graphs for easier interpretation of complex cricket statistics.

By leveraging data analytics, visualization techniques, and cricket performance metrics, this project transforms raw IPL match data into meaningful insights. Whether you are a cricket enthusiast, researcher, student, analyst, or sports fan, this dashboard provides an engaging and informative platform to understand the evolution of the IPL and the factors that influence success in one of the world's most competitive cricket tournaments.

""")

   
    st.subheader("📊 IPL Dataset Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🏏 Total Matches", matches.shape[0])
    col2.metric("📅 Seasons", matches["Season"].nunique())
    col3.metric("👥 Teams", len(set(matches["team1"]).union(set(matches["team2"]))))
    col4.metric("🏟 Venues", matches["venue"].nunique())
# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------
elif menu == "📊 Overview":

    st.header("📊 IPL Overview Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Matches",
        matches.shape[0]
    )

    col2.metric(
        "Total Seasons",
        matches["Season"].nunique()
    )

    col3.metric(
        "Total Teams",
        len(set(matches["team1"]).union(set(matches["team2"])))
    )

    col4.metric(
        "Total Venues",
        matches["venue"].nunique()
    )

    st.markdown("---")

    # Most Successful Team
    most_successful_team = (
        matches["winner"]
        .value_counts()
        .idxmax()
    )

    # Most Awards
    most_awards = (
        matches["player_of_match"]
        .value_counts()
        .idxmax()
    )

    # Most Used Venue
    top_venue = (
        matches["venue"]
        .value_counts()
        .idxmax()
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(
            f"""
🏆 Most Successful Team

**{most_successful_team}**
"""
        )

    with col2:
        st.info(
            f"""
⭐ Most Player of Match Awards

**{most_awards}**
"""
        )

    with col3:
        st.warning(
            f"""
🏟 Most Used Venue

**{top_venue}**
"""
        )

    st.markdown("---")

    st.subheader("📅 Matches Played Per Season")

    matches_per_season = (
        matches["Season"]
        .value_counts()
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(8,4))

    sns.lineplot(
        x=matches_per_season.index,
        y=matches_per_season.values,
        marker="o",
        ax=ax
    )

    ax.set_ylabel("Matches")

    st.pyplot(fig)

    st.markdown("---")

    st.subheader("🏏 Top 5 Most Successful Teams")

    top_teams = (
        matches["winner"]
        .value_counts()
        .head(5)
    )

    fig, ax = plt.subplots(figsize=(8,4))

    sns.barplot(
        x=top_teams.values,
        y=top_teams.index,
        ax=ax
    )

    ax.set_xlabel("Wins")

    st.pyplot(fig)

    st.markdown("---")

    st.subheader("🏟 Top 5 IPL Venues")

    top_venues = (
        matches["venue"]
        .value_counts()
        .head(5)
    )

    fig, ax = plt.subplots(figsize=(8,4))

    sns.barplot(
        x=top_venues.values,
        y=top_venues.index,
        ax=ax
    )

    ax.set_xlabel("Matches")

    st.pyplot(fig)

    st.markdown("---")

    st.subheader("📋 Dataset Snapshot")

    st.dataframe(
        matches.head(10),
        use_container_width=True,
        height=350
    )
# --------------------------------------------------
# TEAM ANALYSIS
# --------------------------------------------------
elif menu == "🏏 Team Analysis":

    st.header("Team Performance")

    teams = sorted(matches['winner'].dropna().unique())

    selected_team = st.selectbox(
        "Select Team",
        teams
    )

    team_wins = matches[
        matches['winner'] == selected_team
    ]

    total_wins = len(team_wins)

    team_matches = (
        ((matches['team1'] == selected_team) |
         (matches['team2'] == selected_team))
    ).sum()

    st.metric("Total Matches Played", int(team_matches))
    st.metric("Total Wins", int(total_wins))

    st.subheader("Winning Matches")

    st.dataframe(
        team_wins[
            ['Season','team1','team2','winner','venue']
        ].head(20),
        use_container_width=True,
        height=400
    )

# --------------------------------------------------
# PLAYER ANALYSIS
# --------------------------------------------------
elif menu == "👤 Player Analysis":

    st.header("👤 Player Performance Analysis")

    player_list = sorted(deliveries["batsman"].unique())

    selected_player = st.selectbox(
        "Select a Player",
        player_list
    )

    # Player balls faced
    player_data = deliveries[
        deliveries["batsman"] == selected_player
    ]

    total_runs = player_data["batsman_runs"].sum()

    balls_faced = len(
        player_data[
            ~player_data["wide_runs"].astype(bool)
        ]
    )

    strike_rate = round(
        (total_runs / balls_faced) * 100,
        2
    ) if balls_faced > 0 else 0

    matches_played = player_data["match_id"].nunique()

    dismissals = player_data[
        player_data["player_dismissed"] == selected_player
    ].shape[0]

    average = round(
        total_runs / dismissals,
        2
    ) if dismissals > 0 else total_runs

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🏏 Runs", total_runs)
    col2.metric("🎯 Strike Rate", strike_rate)
    col3.metric("📅 Matches", matches_played)
    col4.metric("⭐ Average", average)

    st.markdown("---")

    # Runs Distribution
    st.subheader(f"Runs Scored Distribution - {selected_player}")

    run_dist = (
        player_data["batsman_runs"]
        .value_counts()
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(7,4))

    sns.barplot(
        x=run_dist.index,
        y=run_dist.values,
        ax=ax
    )

    ax.set_xlabel("Runs per Ball")
    ax.set_ylabel("Frequency")

    st.pyplot(fig)

    st.markdown("---")

    # Match-wise Runs
    st.subheader("Match-wise Performance")

    match_runs = (
        player_data
        .groupby("match_id")["batsman_runs"]
        .sum()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(9,4))

    ax.plot(
        match_runs["match_id"],
        match_runs["batsman_runs"],
        marker="o"
    )

    ax.set_xlabel("Match ID")
    ax.set_ylabel("Runs")

    st.pyplot(fig)

    st.markdown("---")

    # Performance Summary
    st.subheader("📋 Performance Summary")

    st.write(
        f"""
        **{selected_player}** has scored **{total_runs} runs**
        across **{matches_played} matches** with a strike rate of
        **{strike_rate}** and an average of **{average}**.
        """
    )

# --------------------------------------------------
# VENUE ANALYSIS
# --------------------------------------------------
elif menu == "🏟 Venue Analysis":

    st.header("🏟 Venue Analysis")

    venue = st.selectbox(
        "Select Venue",
        sorted(matches["venue"].dropna().unique())
    )

    venue_matches = matches[
        matches["venue"] == venue
    ]

    venue_match_ids = venue_matches["id"]

    venue_deliveries = deliveries[
        deliveries["match_id"].isin(venue_match_ids)
    ]

    total_matches = len(venue_matches)

    st.subheader(f"Venue: {venue}")

    st.metric(
        "Matches Played",
        total_matches
    )

    # -----------------------------
    # Highest Team Score
    # -----------------------------
    innings_score = (
        venue_deliveries
        .groupby(
            ["match_id", "inning", "batting_team"]
        )["total_runs"]
        .sum()
        .reset_index()
    )

    highest_score = innings_score["total_runs"].max()

    highest_score_team = innings_score.loc[
        innings_score["total_runs"].idxmax(),
        "batting_team"
    ]

    # -----------------------------
    # Lowest Team Score
    # -----------------------------
    lowest_score = innings_score["total_runs"].min()

    lowest_score_team = innings_score.loc[
        innings_score["total_runs"].idxmin(),
        "batting_team"
    ]

    # -----------------------------
    # Top Run Scorer
    # -----------------------------
    batsman_runs = (
        venue_deliveries
        .groupby("batsman")["batsman_runs"]
        .sum()
        .sort_values(ascending=False)
    )

    top_batsman = batsman_runs.index[0]
    top_batsman_runs = batsman_runs.iloc[0]

    # -----------------------------
    # Top Wicket Taker
    # -----------------------------
    wickets = venue_deliveries[
        venue_deliveries["dismissal_kind"].notnull()
    ]

    bowler_wickets = wickets["bowler"].value_counts()

    top_bowler = bowler_wickets.index[0]
    top_bowler_wickets = bowler_wickets.iloc[0]

    # -----------------------------
    # Most Successful Team
    # -----------------------------
    team_wins = (
        venue_matches["winner"]
        .value_counts()
    )

    top_team = team_wins.index[0]
    top_team_wins = team_wins.iloc[0]

    # -----------------------------
    # Metrics
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Highest Score",
        f"{highest_score}"
    )

    col2.metric(
        "Lowest Score",
        f"{lowest_score}"
    )

    col3.metric(
        "Most Successful Team",
        top_team
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            f"""
🏏 Highest Score Team: **{highest_score_team}**

🔥 Highest Score: **{highest_score}**
"""
        )

        st.success(
            f"""
👑 Top Run Scorer

**{top_batsman}**

Runs: **{top_batsman_runs}**
"""
        )

    with col2:
        st.warning(
            f"""
📉 Lowest Score Team: **{lowest_score_team}**

Runs: **{lowest_score}**
"""
        )

        st.info(
            f"""
🎯 Top Wicket Taker

**{top_bowler}**

Wickets: **{top_bowler_wickets}**
"""
        )

    st.markdown("---")

    st.subheader("Most Successful Teams at Venue")

    fig, ax = plt.subplots(figsize=(8,4))

    team_wins.head(10).plot(
        kind="bar",
        ax=ax
    )

    ax.set_ylabel("Wins")

    st.pyplot(fig)

# --------------------------------------------------
# TEAM COMPARISON
# --------------------------------------------------
elif menu == "🔥 Team Comparison":

    st.header("🔥 Head-to-Head Team Analysis")

    teams = sorted(
        list(
            set(matches["team1"]).union(
                set(matches["team2"])
            )
        )
    )

    col1, col2 = st.columns(2)

    with col1:
        team1 = st.selectbox(
            "Select Team 1",
            teams
        )

    with col2:
        team2 = st.selectbox(
            "Select Team 2",
            teams,
            index=1
        )

    if team1 != team2:

        h2h = matches[
            (
                (matches["team1"] == team1) &
                (matches["team2"] == team2)
            )
            |
            (
                (matches["team1"] == team2) &
                (matches["team2"] == team1)
            )
        ]

        total_matches = len(h2h)

        team1_wins = (
            h2h["winner"] == team1
        ).sum()

        team2_wins = (
            h2h["winner"] == team2
        ).sum()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Matches Played",
            total_matches
        )

        col2.metric(
            f"{team1} Wins",
            team1_wins
        )

        col3.metric(
            f"{team2} Wins",
            team2_wins
        )

        st.markdown("---")

        match_ids = h2h["id"]

        h2h_deliveries = deliveries[
            deliveries["match_id"].isin(match_ids)
        ]

        # --------------------------
        # TOP BATSMAN TEAM 1
        # --------------------------

        team1_batting = h2h_deliveries[
            h2h_deliveries["batting_team"] == team1
        ]

        top_batsman_team1 = (
            team1_batting
            .groupby("batsman")["batsman_runs"]
            .sum()
            .sort_values(ascending=False)
        )

        batsman1 = top_batsman_team1.index[0]
        batsman1_runs = top_batsman_team1.iloc[0]

        # --------------------------
        # TOP BATSMAN TEAM 2
        # --------------------------

        team2_batting = h2h_deliveries[
            h2h_deliveries["batting_team"] == team2
        ]

        top_batsman_team2 = (
            team2_batting
            .groupby("batsman")["batsman_runs"]
            .sum()
            .sort_values(ascending=False)
        )

        batsman2 = top_batsman_team2.index[0]
        batsman2_runs = top_batsman_team2.iloc[0]

        # --------------------------
        # TOP BOWLERS
        # --------------------------

        wickets = h2h_deliveries[
            h2h_deliveries["dismissal_kind"].notnull()
        ]

        bowler1_data = wickets[
            wickets["bowling_team"] == team1
        ]

        bowler2_data = wickets[
            wickets["bowling_team"] == team2
        ]

        top_bowler1 = (
            bowler1_data["bowler"]
            .value_counts()
        )

        top_bowler2 = (
            bowler2_data["bowler"]
            .value_counts()
        )

        bowler1 = top_bowler1.index[0]
        wickets1 = top_bowler1.iloc[0]

        bowler2 = top_bowler2.index[0]
        wickets2 = top_bowler2.iloc[0]

        st.subheader("⭐ Team Performance Leaders")

        col1, col2 = st.columns(2)

        with col1:

            st.success(f"""
### {team1}

🏏 Top Batsman: {batsman1}

Runs: {batsman1_runs}

🎯 Top Bowler: {bowler1}

Wickets: {wickets1}
""")

        with col2:

            st.success(f"""
### {team2}

🏏 Top Batsman: {batsman2}

Runs: {batsman2_runs}

🎯 Top Bowler: {bowler2}

Wickets: {wickets2}
""")

        st.markdown("---")

        st.subheader("Head-to-Head Wins")

        wins_df = pd.DataFrame({
            "Team":[team1, team2],
            "Wins":[team1_wins, team2_wins]
        })

        fig, ax = plt.subplots(figsize=(6,4))

        sns.barplot(
            data=wins_df,
            x="Team",
            y="Wins",
            ax=ax
        )

        st.pyplot(fig)

    else:
        st.warning(
            "Please select two different teams."
        )
# --------------------------------------------------
# AWARDS
# --------------------------------------------------
elif menu == "🏆 Awards Analysis":

    st.header("🏆 ")

    col1, col2 = st.columns(2)

    # Most Player of Match
    pom = matches["player_of_match"].value_counts().head(10)

    with col1:
        st.subheader("Most Player of Match Awards")

        fig, ax = plt.subplots(figsize=(7,4))
        pom.plot(kind="bar", ax=ax)
        st.pyplot(fig)

    # Top Run Scorers
    top_runs = (
        deliveries.groupby("batsman")["batsman_runs"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    with col2:
        st.subheader("Highest Run Scorers")

        fig, ax = plt.subplots(figsize=(7,4))
        top_runs.plot(kind="bar", ax=ax)
        st.pyplot(fig)

    st.markdown("---")

    col1, col2 = st.columns(2)

    # Top Wicket Takers
    wickets = deliveries[
        deliveries["dismissal_kind"].notnull()
    ]

    top_bowlers = wickets["bowler"].value_counts().head(10)

    with col1:
        st.subheader("Highest Wicket Takers")

        fig, ax = plt.subplots(figsize=(7,4))
        top_bowlers.plot(kind="bar", ax=ax)
        st.pyplot(fig)

    # Successful Teams
    team_wins = matches["winner"].value_counts().head(10)

    with col2:
        st.subheader("Most Successful Teams")

        fig, ax = plt.subplots(figsize=(7,4))
        team_wins.plot(kind="bar", ax=ax)
        st.pyplot(fig)

# --------------------------------------------------
# ABOUT
# --------------------------------------------------
elif menu == "ℹ️ About":

    st.header("ℹ️ About the Project")

    st.markdown("""
# 🏏 IPL Analysis Dashboard

The Indian Premier League (IPL) is one of the most successful and popular Twenty20 cricket leagues in the world. Since its inception in 2008, the tournament has revolutionized the game of cricket by introducing a fast-paced format, attracting international players, and creating a massive global fan base.

This IPL Analysis Dashboard is designed to provide comprehensive insights into IPL matches, teams, players, venues, and overall tournament performance through data-driven analysis and interactive visualizations.

The project utilizes historical IPL datasets containing ball-by-ball and match-level information to identify trends, patterns, and key performance indicators that influence match outcomes and team success.

---

## 🎯 Project Objectives

- Analyze IPL match statistics across multiple seasons.
- Compare team performances and winning patterns.
- Evaluate player batting and bowling performances.
- Study venue-specific trends and records.
- Explore head-to-head team comparisons.
- Visualize cricket data using interactive charts and dashboards.

---

## 📊 Key Features

### 🏏 Team Analysis
- Team-wise performance statistics.
- Matches played and wins.
- Team comparison dashboard.
- Head-to-head records between teams.

### 👤 Player Analysis
- Individual player performance.
- Batting statistics.
- Strike rate and average analysis.
- Match-wise performance trends.

### 🏟 Venue Analysis
- Venue-wise match statistics.
- Highest and lowest scores.
- Most successful teams.
- Top performers at each venue.

### 🏆 IPL Hall of Fame
- Most successful players.
- Highest run scorers.
- Leading wicket takers.
- Most Player of the Match awards.

### 📈 Interactive Visualizations
- Bar Charts
- Performance Comparisons
- Statistical Summaries
- Trend Analysis

---

## 🛠 Technologies Used

### Programming Language
- Python

### Libraries
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit

### Dataset Files
- matches.csv
- deliveries.csv
- teams.csv
- Players.xlsx
- most_runs_average_strikerate.csv

---

## 📚 Dataset Description

The project uses IPL historical datasets containing detailed information about matches and ball-by-ball deliveries.

The datasets include:

- Match details
- Team information
- Venue information
- Toss results
- Match winners
- Batting statistics
- Bowling statistics
- Player awards

These datasets help generate meaningful insights into player performances, team strengths, and tournament trends.

---

## 🚀 Future Enhancements

The dashboard can be further enhanced by incorporating:

- Live IPL Data Integration
- Match Outcome Prediction using Machine Learning
- Player Performance Forecasting
- Interactive Filters and Search Features
- Advanced Analytics and AI-based Insights

---

## 👨‍💻 Developer Information

**Project Title:** IPL Analysis Dashboard

**Project Type:** College Mini Project

**Developed By:** R. Bhavya Deepika Rani

This project demonstrates the practical application of Data Science, Data Visualization, and Dashboard Development techniques using real-world IPL cricket data.
""")