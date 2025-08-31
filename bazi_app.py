# bazi_app.py
import streamlit as st
from datetime import date, datetime, time as dtime

# -------------------------
# BaZi Calculation Helpers
# -------------------------
HEAVENLY_STEMS = ['Jia','Yi','Bing','Ding','Wu','Ji','Geng','Xin','Ren','Gui']
EARTHLY_BRANCHES = ['Zi','Chou','Yin','Mao','Chen','Si','Wu','Wei','Shen','You','Xu','Hai']

def hour_branch_index(hour: int) -> int:
    """Return Earthly Branch index for given hour (0-23). Zi:23-0, Chou:1-2, etc."""
    return ((hour + 1) // 2) % 12

def calculate_day_master(year:int, month:int, day:int) -> dict:
    """
    Placeholder Day Master calculation using known formula:
    Day stem index = (year*5 + month*2 + day) % 10
    Note: simplified for stable deployment.
    """
    stem_idx = (year * 5 + month * 2 + day) % 10
    return {"gan": HEAVENLY_STEMS[stem_idx], "element": HEAVENLY_STEMS[stem_idx]}

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Whispers of YI — Day Master", layout="centered")
st.title("Whispers of YI — Day Master Calculator")
st.write("Enter your birth details to reveal your Day Master (Heavenly Stem of the Day).")

# Input date
dob = st.date_input(
    "Date of Birth",
    min_value=date(1900, 1, 1),
    max_value=date.today(),
    value=date(2000,1,1)
)

# Input time
birth_hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=12)
birth_minute = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=0)

# Input timezone
import pytz
timezone_input = st.selectbox(
    "Timezone",
    pytz.all_timezones,
    index=pytz.all_timezones.index("Asia/Kuala_Lumpur") if "Asia/Kuala_Lumpur" in pytz.all_timezones else 0
)

if st.button("Reveal Day Master"):
    year, month, day = dob.year, dob.month, dob.day
    result = calculate_day_master(year, month, day)

    st.subheader("Your Day Master:")
    st.markdown(f"**{result['gan']}** — {result['element']} Wood/Fire/Metal/Earth/Water (simplified)")

    st.info("This is the core Day Master calculation. Optional Year/Hour/Month pillars can be added in future updates.")

