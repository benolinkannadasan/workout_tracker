import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

# Load sheet
@st.cache_resource
def get_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Workout Tracker").worksheet("workout_log")
    data = sheet.get_all_records()
    return pd.DataFrame(data)

df = get_data()

st.title("📊 Workout Dashboard")

if df.empty:
    st.warning("No data found yet. Log your first workout in the main app!")
    st.stop()

# Clean data
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.sort_values(by='Date', ascending=False)
users = df['Name'].unique()

selected_user = st.selectbox("Select user", users)
user_df = df[df['Name'] == selected_user]

# XP over time
st.subheader(f"📈 XP Progress: {selected_user}")
xp_chart = user_df[['Date', 'XP']].sort_values('Date')
st.line_chart(xp_chart.set_index('Date'))

# Streak timeline
st.subheader("🔥 Active Days Timeline")
user_df['Workout Done'] = user_df[['Burpees Done', 'Skipping Done', 'Pushups Done', 'High Knees Done']].apply(
    lambda row: '✅' in row.values, axis=1
)
calendar_df = user_df[['Date', 'Workout Done']].sort_values('Date')
calendar_df['Active'] = calendar_df['Workout Done'].apply(lambda x: 1 if x else 0)
st.bar_chart(calendar_df.set_index('Date')['Active'])

# Recent logs
st.subheader("📅 Recent Workouts")
st.dataframe(user_df[['Date', 'XP', 'Burpees Done', 'Pushups Done', 'High Knees Done', 'Protein Taken']].head(10))

# Leaderboard
st.subheader("🏆 Leaderboard (Total XP)")
leaderboard = df.groupby('Name')['XP'].sum().sort_values(ascending=False).reset_index()
st.table(leaderboard)
