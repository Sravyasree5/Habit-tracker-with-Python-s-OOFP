from habit import Habit
import streamlit as st
import pandas as pd
import database as db
import analytics as an
import quotes as q

# --- Page Configuration ---
st.set_page_config(
    page_title="Habit Tracker",
    page_icon="🔥",
    layout="wide"
)

# Initialize Database Schema
db.init_db()

st.title(" Habit Tracker Dashboard")
st.caption("Track habits, log completions, and analyze streaks.")

daily_quote = q.get_motivation()
st.info(f"💡 Daily Motivation: \"{daily_quote}\"")

# --- Sidebar: Direct Actions ---
st.sidebar.header("Actions & Controls")

# Quick Action: Add New Habit
with st.sidebar.expander("➕ Add New Habit"):
    with st.form("add_habit_form", clear_on_submit=True):
        habit_id = st.text_input("Habit ID (e.g., h_07)")
        name = st.text_input("Habit Name (e.g., Morning Meditate)")
        periodicity = st.selectbox("Periodicity", ["daily", "weekly"])
        category = st.text_input("Category (e.g., Wellness)")
        habit_type = st.selectbox("Type", ["build", "break"])
        
        submitted = st.form_submit_button("Create Habit")
        if submitted:
            if habit_id and name:
                try:
                    new_habit = Habit(habit_id, name, periodicity, category, habit_type)
                    db.add_habit(new_habit)
                    st.success(f"Habit '{name}' created!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please fill in all required fields.")

# Quick Action: Load Sample Fixtures
if st.sidebar.button("🔄 Reset & Load Sample Data"):
    db.load_predefined_data()
    st.sidebar.success("Sample 4-week test data loaded!")
    st.rerun()

# --- Main Dashboard Data Fetching ---
raw_habits = db.get_all_habits()

if not raw_habits:
    st.info("No habits found in the database. Use the sidebar to add a new habit or load sample data.")
else:
    # Build enriched dataset with calculated streaks
    enriched_data = []
    for h in raw_habits:
        logs = db.get_logs_for_habit(h['habit_id'])
        current_streak = an.calculate_streak(logs, h['periodicity'])
        enriched_data.append({
            "ID": h['habit_id'],
            "Name": h['name'],
            "Periodicity": h['periodicity'],
            "Category": h['category'],
            "Type": h['habit_type'],
            "Total Check-ins": len(logs),
            "Current Streak 🔥": f"{current_streak} days"
        })

    df = pd.DataFrame(enriched_data)

    # --- Top Analytics Metrics Cards ---
    st.subheader(" Key Performance Metrics")
    col1, col2, col3 = st.columns(3)
    
    top_habit_name, top_streak_val = an.get_longest_streak_all_habits(raw_habits, db.get_logs_for_habit)
    
    with col1:
        st.metric(label="Total Active Habits", value=len(raw_habits))
    with col2:
        st.metric(label="Top Performing Habit 🏆", value=top_habit_name)
    with col3:
        st.metric(label="Longest System Streak", value=f"{top_streak_val} Days")

    st.markdown("---")

    # --- Interactive Habits Table ---
    st.subheader("📋 Your Habits & Active Streaks")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # --- Check-off & Delete Actions Section ---
    st.subheader("⚡ Quick Logging & Management")
    log_col, delete_col = st.columns(2)

    habit_options = {f"{h['name']} ({h['habit_id']})": h['habit_id'] for h in raw_habits}

    # Column 1: Log Completion
    with log_col:
        st.markdown("##### Check-Off Habit")
        selected_log = st.selectbox("Select habit to check off:", list(habit_options.keys()), key="log_select")
        if st.button("✅ Log Completion"):
            target_id = habit_options[selected_log]
            db.log_completion(target_id)
            
            # Show random motivational quote upon completion
            quote = q.get_motivation()
            st.success(f"Habit logged! 💡 \"{quote}\"")
            st.rerun()

    # Column 2: Delete Habit
    with delete_col:
        st.markdown("##### Delete Habit")
        selected_del = st.selectbox("Select habit to delete:", list(habit_options.keys()), key="del_select")
        if st.button("🗑️ Delete Habit", type="secondary"):
            target_id = habit_options[selected_del]
            db.delete_habit(target_id)
            st.warning("Habit deleted successfully.")
            st.rerun()