import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

# This assumes you have a 'diary_core.py' file with these functions defined.
# If not, you will need to create them for the app to run without errors.
from diary_core import save_entry, reflect_on_entry, load_entries, analyze_mood_trends

st.set_page_config(
    page_title="MemoraAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Final "Modular Dark" CSS with a more refined Button ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

:root {
    --primary-bg-color: #111; /* Darker charcoal */
    --card-bg-color: #1e1e28;
    --text-color: #f1c40f; /* Soft gold */
    --subtle-text-color: #a0aec0;
    --border-color: #333;

    /* Accent Theme: Neon Blue */
    --accent-main: #00ffff;     /* Cyan Blue */
    --accent-sidebar: #20c997;  /* Teal Green */
    --accent-history: #ffd700;  /* Golden Yellow */
    --accent-danger: #ff4d4d;   /* Vibrant Red */

    --font-sans-serif: 'Poppins', sans-serif;
    --border-radius: 10px;
}

/* Base */
html, body, [class*="st-"] {
    font-family: var(--font-sans-serif);
    background-color: var(--primary-bg-color);
    color: var(--text-color);
}

/* Icon / Logo Effects */
.colorful-icon {
    display: inline-block;
    margin-right: 0.5em;
    text-shadow: 0 0 3px #00ffff, 0 0 5px #f1c40f, 0 0 8px #ff4d4d;
}

/* Header & Subtitles */
.main-header {
    font-size: 3.5rem;
    font-weight: 700;
    text-align: center;
    color: #00ffff; /* Neon Blue */
    padding-top: 2rem;
    margin-bottom: 0.5rem;
}
.subtitle {
    text-align: center;
    color: var(--subtle-text-color);
    font-size: 1.25rem;
    font-weight: 400;
    margin-bottom: 4rem;
}

/* Text Area */
.stTextArea textarea {
    background-color: var(--card-bg-color);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius);
    color: var(--text-color);
    transition: all 0.2s ease;
}
.stTextArea textarea:focus {
    border-color: var(--accent-main);
    box-shadow: 0 0 0 3px rgba(0, 255, 255, 0.3);
}

/* Button Styling */
div.stButton > button[kind="primary"] {
    background: transparent;
    border: 2px solid var(--accent-main);
    color: var(--accent-main);
    font-weight: 600;
    border-radius: var(--border-radius);
    padding: 12px 24px;
    transition: all 0.3s ease-in-out;
}
div.stButton > button[kind="primary"]:hover {
    color: #a2fafa;
    border-color: #a2fafa;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.6);
    transform: translateY(-2px);
}
div.stButton > button[kind="primary"]:active {
    transform: translateY(0px) scale(0.97);
}

/* Reflection Box */
.reflection-box {
    background: rgba(0, 255, 255, 0.1);
    border-left: 3px solid var(--accent-main);
    padding: 1.5rem;
    border-radius: var(--border-radius);
    margin: 1.5rem 0;
}

/* Sidebar & Stats */
.st-emotion-cache-16txtl3 {
    background-color: var(--card-bg-color);
    border-right: 1px solid var(--border-color);
    padding: 1rem;
}
.st-emotion-cache-16txtl3 .stMetric {
    border-left: 3px solid var(--accent-sidebar);
    padding-left: 10px;
    border-radius: var(--border-radius);
}
.st-emotion-cache-16txtl3 h3 {
    color: var(--accent-sidebar);
}

/* Entry History */
.stExpander {
    background: var(--card-bg-color);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius);
    margin-bottom: 1rem;
    overflow: hidden;
    transition: all 0.2s ease;
}
.stExpander:hover {
    border-color: var(--accent-history);
}
.stExpander header {
    font-size: 1.1rem;
    font-weight: 600;
}
.entry-card {
    background: var(--primary-bg-color);
    border: 1px solid var(--border-color);
    padding: 1.5rem;
    border-radius: var(--border-radius);
    margin-bottom: 1rem;
}

/* Mood Tags */
.mood-indicator {
    padding: 0.3rem 0.8rem;
    border-radius: 15px;
    font-weight: 600;
    font-size: 0.8rem;
    margin: 0.2rem;
    border: 1px solid;
}
.mood-positive {
    border-color: #00e676;
    color: #00e676;
}
.mood-neutral {
    border-color: #ffd700;
    color: #ffd700;
}
.mood-negative {
    border-color: #ff4d4d;
    color: #ff4d4d;
}
.mood-concerning {
    background: #c0392b;
    color: white;
    border-color: #c0392b;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(f'<h1 class="main-header"><span class="colorful-icon">🧠</span>MemoraAI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your intelligent diary companion for self-reflection and growth.</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📊 Your Journey")
    entries = load_entries()

    if entries:
        st.metric("Total Entries", len(entries))

        dates = sorted(list(entries.keys()), reverse=True)
        streak = 0
        if dates:
            today_date = datetime.now().date()
            last_entry_date = datetime.strptime(dates[0], "%Y-%m-%d").date()

            if (today_date - last_entry_date).days <= 1:
                streak = 1
                for i in range(len(dates) - 1):
                    current_entry_date = datetime.strptime(dates[i], "%Y-%m-%d").date()
                    next_entry_date = datetime.strptime(dates[i+1], "%Y-%m-%d").date()
                    if (current_entry_date - next_entry_date).days == 1:
                        streak += 1
                    else:
                        break
        st.metric("Current Streak", f"{streak} days")

        if len(entries) >= 3:
            mood_data = analyze_mood_trends(entries)
            if mood_data:
                df = pd.DataFrame(list(mood_data.items()), columns=['Date', 'Mood Score'])
                fig = px.line(df, x='Date', y='Mood Score', title="Mood Trend", markers=True)
                fig.update_layout(
                    showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#e1e1e6',
                    xaxis=dict(gridcolor='#40404a'), yaxis=dict(gridcolor='#40404a')
                )
                fig.update_traces(line_color='#00b894', marker=dict(color='#ffb86c', size=8))
                st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown(f'💡Tips')
    st.info("Write about your feelings, experiences, and thoughts. Be honest and authentic for better insights.")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Today's Entry")
    user_input = st.text_area("How was your day? What's on your mind?", height=250, placeholder="Share your thoughts, feelings, experiences...")

    if st.button("Reflect & Save", type="primary", use_container_width=True):
        if user_input.strip():
            with st.spinner("Analyzing your thoughts..."):
                save_entry(user_input)
                reflection = reflect_on_entry(user_input)

            if "SAFETY_CONCERN" in reflection:
                st.error("I noticed some concerning thoughts. Please consider reaching out to a mental health professional.", icon="🚨")
                st.info(f'📞 Crisis Resources:\n- National Suicide Prevention Lifeline: 988\n- Crisis Text Line: Text HOME to 741741')
            else:
                st.success("Entry saved and reflection ready!", icon="✅")
                # FIXED BLOCK: This now correctly renders the colorful icon inside the reflection box
                st.markdown('<div class="reflection-box">', unsafe_allow_html=True)
                st.markdown(f'#### <span class="colorful-icon">🪞</span>AI Reflection', unsafe_allow_html=True)
                st.markdown(reflection)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Please write something first.", icon="⚠️")

with col2:
    st.subheader("Quick Stats")
    if entries:
        today = datetime.now().strftime("%Y-%m-%d")
        if today in entries:
            st.success("✅ You've written today!")
        else:
            st.info("📝 Haven't written today yet")

        if today in entries:
            word_count = len(entries[today].split())
            st.metric("Today's Words", word_count)

st.markdown("---")
st.subheader("Journal History")

if entries:
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        entries_to_show = st.selectbox("Show entries", [5, 10, 20, "All"], index=0)
    with col_filter2:
        search_term = st.text_input("Search entries", placeholder="Search your thoughts...")

    filtered_entries = entries.copy()
    if search_term:
        filtered_entries = {date: text for date, text in entries.items() if search_term.lower() in text.lower()}

    sorted_entries = sorted(filtered_entries.items(), reverse=True)
    if entries_to_show != "All":
        sorted_entries = sorted_entries[:entries_to_show]

    for date, text in sorted_entries:
        with st.expander(f'{date} - {len(text.split())} words'):
            st.markdown(f'<div class="entry-card">{text}</div>', unsafe_allow_html=True)
            col_act1, col_act2 = st.columns(2)
            with col_act1:
                if st.button(f"Reflect on {date}", key=f"reflect_{date}"):
                    with st.spinner("Reflecting..."):
                        reflection = reflect_on_entry(text)
                    st.markdown(reflection)
            with col_act2:
                if st.button(f"Analyze {date}", key=f"analyze_{date}"):
                    word_count = len(text.split())
                    char_count = len(text)
                    st.info(f'📝 {word_count} words, {char_count} characters')
else:
    st.info(f'<span class="colorful-icon">🌟</span> Start your journaling journey by writing your first entry above!', unsafe_allow_html=True)