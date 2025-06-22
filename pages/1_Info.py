import streamlit as st

st.title("ℹ️ How This Tracker Works")

st.markdown("## 🏋️ Your Daily Routine")
st.markdown("""
You commit to doing **any or all of these core exercises daily**:
- ✅ **Jumping Jacks**
- ✅ **Skipping**
- ✅ **Push-ups**
- ✅ **High Knees**

You can also optionally log:
- 🚴 **Bonus activities** like swimming, walking, cycling
- 💊 **Protein intake** (yes/no)
""")

st.markdown("---")

st.markdown("## 🧠 XP System (Max 10/day)")
st.markdown("""
You earn points based on consistency:

| Core Exercises Done | XP  |
|---------------------|-----|
| 4/4 (perfect day)   | 9   |
| 3 exercises         | 7   |
| 2 exercises         | 5   |
| 1 exercise          | 3   |
| 0 exercises         | 0   |

- ✅ **+1 XP** for taking protein
- ❗ **−2 XP** if you break your workout streak
- ⛔ **XP is capped at 10**
""")

st.caption("💡 XP is your consistency score. Think of it as workout fuel for your journey!")

st.markdown("---")

st.markdown("## 🔥 Streaks")
st.markdown("""
A **streak** means you're showing up **daily without skipping a calendar day**.

- Even weekends count!
- At least one core exercise (✅) must be done to count.
- If you miss a day, your streak resets to 0.

Examples:
- Jacks + Push-ups on Monday → ✅ streak continues  
- Only bonus activities → ❌ no streak  
- No log on Tuesday → ❌ streak breaks
""")

st.markdown("---")

st.markdown("## 🏅 Badges (Motivation Only)")
st.markdown("""
You unlock fun badges daily based on how much effort you put in:

- 🥇 **Gold**: All 4 core exercises  
- 🥈 **Silver**: 2–3 exercises  
- 🥉 **Bronze**: 1 exercise  
- 🛌 **None**: Missed day
""")

st.caption("Note: These are not linked to XP — just encouragement 💪")

st.markdown("---")

st.success("🎉 Stay consistent. Your future self will thank you!")
