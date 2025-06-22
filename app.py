import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date, timedelta
import pandas as pd

# Google Sheets setup
@st.cache_resource
def get_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Workout Tracker").worksheet("workout_log")
    return sheet

sheet = get_sheet()

# UI Header
st.title("🔥 Workout Tracker")

name = st.selectbox("Your Name", ["Beno", "Yal", "Sati", "Pal","Krishna"])
today = date.today().isoformat()
st.markdown(f"📅 **Date:** {today}")

# ⏱️ Streak Calculation
def calculate_streak_and_break(name):
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    df = df[df['Name'] == name]
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.sort_values('Date', ascending=False)

    streak = 0
    today = pd.to_datetime(date.today())

    # Set of dates with at least one core workout ✅
    workout_dates = {
        row['Date'].date()
        for _, row in df.iterrows()
        if '✅' in [row['Burpees Done'], row['Skipping Done'], row['Pushups Done'], row['High Knees Done']]
    }

    # Check consecutive calendar days backward
    check_day = today
    while check_day in workout_dates:
        streak += 1
        check_day -= timedelta(days=1)

    # Did the streak break today?
    streak_broken_today = today not in workout_dates and streak != 0
    return streak, streak_broken_today

# Show streak after name is selected
if name:
    streak, broke_today = calculate_streak_and_break(name)
    if streak >= 3:
        st.markdown(f"🔥 **Streak: {streak} days!** You're on fire!")
    elif streak == 2:
        st.markdown(f"⚡ **Streak: 2 days** — nice rhythm!")
    elif streak == 1:
        st.markdown("🚶 **Streak: 1 day** — let’s build it!")
    else:
        st.markdown("🟡 **No current streak. Start fresh today!**")

# Exercise Input
st.header("🏋️ Daily Exercises")

def log_exercise(label, is_time_based=False):
    col1, col2, col3 = st.columns([1, 1, 2])
    done = col1.checkbox(label)
    sets = col2.number_input(f"{label} Sets", min_value=0, max_value=10, value=0) if done else 0
    reps_label = "Duration (secs)" if is_time_based else "Reps"
    reps = col3.number_input(f"{label} {reps_label}", min_value=0, max_value=1000, value=0) if done else 0
    return done, sets, reps

# Inputs for each exercise
burpees_done, burpees_sets, burpees_reps = log_exercise("Burpees")
skipping_done, skipping_sets, skipping_reps = log_exercise("Skipping", is_time_based=True)
pushups_done, pushups_sets, pushups_reps = log_exercise("Push-ups")
highknees_done, highknees_sets, highknees_reps = log_exercise("High Knees")

# Bonus
st.subheader("🚴 Bonus Activity (Optional)")
bonus = st.multiselect("Any extras today?", ["Swimming", "Cycling", "Walking"])

# Protein
st.subheader("💊 Supplements")
protein = st.radio("Protein taken?", ["✅ Yes", "❌ No"])

# XP Calculation (core + protein, max 10)
num_ex_done = sum([burpees_done, skipping_done, pushups_done, highknees_done])

if num_ex_done == 4:
    xp = 9
elif num_ex_done == 3:
    xp = 7
elif num_ex_done == 2:
    xp = 5
elif num_ex_done == 1:
    xp = 3
else:
    xp = 0

# Add +1 XP for protein
if protein == "✅ Yes":
    xp += 1

# Streak penalty
_, streak_broken_today, _ = calculate_streak_and_break(name)
if streak_broken_today and xp > 0:
    xp = max(0, xp - 2)
    st.warning("⚠️ You broke your streak today — 2 XP deducted.")

# Final cap
xp = min(10, xp)


# Feedback message
if xp == 10:
    st.success("🌟 Perfect score! 10/10 XP today!")
elif xp >= 6:
    st.info("💪 Good effort! Keep building the habit.")
elif xp >= 1:
    st.info("👣 Small steps matter — you showed up.")
else:
    st.markdown("😴 No XP today — rest or missed day.")

# Submit button
if st.button("🚀 Submit Workout"):
    sheet.append_row([
        today, name,
        "✅" if burpees_done else "❌", burpees_sets, burpees_reps,
        "✅" if skipping_done else "❌", skipping_sets, skipping_reps,
        "✅" if pushups_done else "❌", pushups_sets, pushups_reps,
        "✅" if highknees_done else "❌", highknees_sets, highknees_reps,
        ', '.join(bonus) if bonus else "",
        protein,
        int(xp)
    ])
    
    st.success(f"🎉 Workout logged for {name} on {today}!")
    st.markdown(f"🏆 **XP earned today: {int(xp)}**")
    st.balloons()

    if num_ex_done == 4:
        st.markdown("🥇 **Perfect Day! Gold Badge!**")
    elif num_ex_done == 3:
        st.markdown("🥈 **Solid effort! Silver Badge.**")
    elif num_ex_done >= 1:
        st.markdown("🥉 **You showed up. Bronze Badge.**")
    else:
        st.markdown("🛌 Rest day? Try not to miss tomorrow!")
