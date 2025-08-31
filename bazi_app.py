# bazi_app.py

import streamlit as st
from datetime import datetime
import pytz

# -------------------------
# BaZi Calculation Helpers
# -------------------------

HEAVENLY_STEMS = ['Jia', 'Yi', 'Bing', 'Ding', 'Wu', 'Ji', 'Geng', 'Xin', 'Ren', 'Gui']
EARTHLY_BRANCHES = ['Zi', 'Chou', 'Yin', 'Mao', 'Chen', 'Si', 'Wu', 'Wei', 'Shen', 'You', 'Xu', 'Hai']

def get_bazi(year, month, day, hour, minute, tz_str):
    """
    Calculate basic BaZi (Four Pillars) from Gregorian datetime and timezone.
    Note: Lunar conversion and solar terms not fully implemented yet — placeholder.
    """

    # Convert input to aware datetime
    try:
        tz = pytz.timezone(tz_str)
    except Exception:
        tz = pytz.UTC
    dt = datetime(year, month, day, hour, minute, tzinfo=tz)

    # -------------------------
    # Simplified placeholder logic
    # -------------------------

    # Year Pillar
    year_stem = HEAVENLY_STEMS[year % 10]
    year_branch = EARTHLY_BRANCHES[year % 12]

    # Month Pillar (approximation)
    month_stem = HEAVENLY_STEMS[(month + 1) % 10]
    month_branch = EARTHLY_BRANCHES[(month + 1) % 12]

    # Day Pillar (placeholder, simple modulo)
    day_stem = HEAVENLY_STEMS[day % 10]
    day_branch = EARTHLY_BRANCHES[day % 12]

    # Hour Pillar (2-hour blocks, starting from 23:00-01:00 as Zi)
    hour_index = (hour + 1) // 2 % 12
    hour_stem = HEAVENLY_STEMS[hour_index % 10]
    hour_branch = EARTHLY_BRANCHES[hour_index]

    return {
        "Year": f"{year_stem} {year_branch}",
        "Month": f"{month_stem} {month_branch}",
        "Day": f"{day_stem} {day_branch}",
        "Hour": f"{hour_stem} {hour_branch}"
    }

# -------------------------
# Streamlit App UI
# -------------------------

st.set_page_config(page_title="Whispers of YI — BaZi Calculator", layout="centered")

st.title("Whispers of YI — BaZi Calculator")
st.write("Enter your birth details to calculate your Four Pillars (BaZi). Timezone is required for accuracy.")

# Input: Date
dob = st.date_input("Date of Birth")

# Input: Time
birth_hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=12)
birth_minute = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=0)

# Input: Timezone
timezone_input = st.selectbox(
    "Timezone",
    pytz.all_timezones,
    index=pytz.all_timezones.index("Asia/Kuala_Lumpur") if "Asia/Kuala_Lumpur" in pytz.all_timezones else 0
)

# Button to calculate
if st.button("Calculate BaZi"):
    year, month, day = dob.year, dob.month, dob.day
    pillars = get_bazi(year, month, day, birth_hour, birth_minute, timezone_input)

    st.subheader("Your Four Pillars (BaZi):")
    st.write(f"**Year Pillar:** {pillars['Year']}")
    st.write(f"**Month Pillar:** {pillars['Month']}")
    st.write(f"**Day Pillar:** {pillars['Day']}")
    st.write(f"**Hour Pillar:** {pillars['Hour']}")

    st.info("Note: This is a simplified calculation. Lunar conversion and solar terms are placeholders for now. Accuracy will improve in future updates.")
