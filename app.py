import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from diary_core import save_entry, reflect_on_entry, load_entries, analyze_mood_trends


st.set_page_config(
    page_title="MemoraAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .reflection-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .mood-indicator {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.2rem;
    }
    
    .mood-positive { background: #d4edda; color: #155724; }
    .mood-neutral { background: #fff3cd; color: #856404; }
    .mood-negative { background: #f8d7da; color: #721c24; }
    .mood-concerning { background: #f5c6cb; color: #721c24; border: 2px solid #dc3545; }
    
    .entry-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
    
    .stat-box {
        text-align: center;
        padding: 1rem;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🧠 MemoraAI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your intelligent diary companion for self-reflection and growth</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📊 Your Journey")
    entries = load_entries()
    
    if entries:
        st.metric("Total Entries", len(entries))
        
        # Recent streak
        dates = sorted(entries.keys(), reverse=True)
        streak = 0
        current_date = datetime.now().date()
        
        for date_str in dates:
            entry_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if entry_date == current_date - timedelta(days=streak):
                streak += 1
            else:
                break
        
        st.metric("Current Streak", f"{streak} days")
        
        # Mood trends
        if len(entries) >= 3:
            mood_data = analyze_mood_trends(entries)
            if mood_data:
                fig = px.line(
                    x=list(mood_data.keys()), 
                    y=list(mood_data.values()),
                    title="Mood Trend (Last 7 days)",
                    labels={'x': 'Date', 'y': 'Mood Score'}
                )
                fig.update_layout(height=300, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.info("Write about your feelings, experiences, and thoughts. Be honest and authentic for better insights.")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("✍️ Today's Entry")
    
    # Writing area
    user_input = st.text_area(
        "How was your day? What's on your mind?",
        height=250,
        placeholder="Share your thoughts, feelings, experiences... I'm here to listen and reflect with you."
    )
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("💾 Save Entry", type="primary", use_container_width=True):
            if user_input.strip():
                save_entry(user_input)
                st.success("✅ Entry saved successfully!")
                st.rerun()
            else:
                st.warning("⚠️ Please write something first.")
    
    with col_btn2:
        if st.button("🪞 Get Reflection", use_container_width=True):
            if user_input.strip():
                with st.spinner("🤔 Analyzing your thoughts..."):
                    reflection = reflect_on_entry(user_input)
                
                if "SAFETY_CONCERN" in reflection:
                    st.error("🚨 I noticed some concerning thoughts in your entry. Please consider reaching out to a mental health professional or crisis helpline.")
                    st.info("📞 Crisis Resources:\n- National Suicide Prevention Lifeline: 988\n- Crisis Text Line: Text HOME to 741741")
                else:
                    st.markdown('<div class="reflection-box">', unsafe_allow_html=True)
                    st.markdown("### 🪞 AI Reflection")
                    st.markdown(reflection)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("⚠️ Please write something first.")

with col2:
    st.subheader("📈 Quick Stats")
    
    if entries:
        # Today's entry status
        today = datetime.now().strftime("%Y-%m-%d")
        if today in entries:
            st.success("✅ You've written today!")
        else:
            st.info("📝 Haven't written today yet")
        
        # Word count for today
        if today in entries:
            word_count = len(entries[today].split())
            st.metric("Today's Words", word_count)


st.markdown("---")
st.subheader("📅 Your Journal History")

if entries:
  
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        entries_to_show = st.selectbox("Show entries", [5, 10, 20, "All"], index=0)
    with col_filter2:
        search_term = st.text_input("🔍 Search entries", placeholder="Search your thoughts...")
    
    
    filtered_entries = entries.copy()
    if search_term:
        filtered_entries = {
            date: text for date, text in entries.items() 
            if search_term.lower() in text.lower()
        }
    
    sorted_entries = sorted(filtered_entries.items(), reverse=True)
    if entries_to_show != "All":
        sorted_entries = sorted_entries[:entries_to_show]
    
    for date, text in sorted_entries:
        with st.expander(f"📘 {date} - {len(text.split())} words"):
            st.markdown(f'<div class="entry-card">{text}</div>', unsafe_allow_html=True)
            
            # Quick actions
            col_act1, col_act2 = st.columns(2)
            with col_act1:
                if st.button(f"🪞 Reflect on {date}", key=f"reflect_{date}"):
                    with st.spinner("Reflecting..."):
                        reflection = reflect_on_entry(text)
                    st.markdown(reflection)
            with col_act2:
                if st.button(f"📊 Analyze {date}", key=f"analyze_{date}"):
                    word_count = len(text.split())
                    char_count = len(text)
                    st.info(f"📝 {word_count} words, {char_count} characters")
else:
    st.info("🌟 Start your journaling journey by writing your first entry above!")