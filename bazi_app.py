# bazi_app.py

import streamlit as st
from datetime import datetime, timedelta
import pytz

# -------------------------
# BaZi Helpers
# -------------------------
try:
    import sxtwl
except ImportError:
    sxtwl = None

HEAVENLY_STEMS = ["Jia","Yi","Bing","Ding","Wu","Ji","Geng","Xin","Ren","Gui"]
HEAVENLY_STEMS_EN = ["Jia","Yi","Bing","Ding","Wu","Ji","Geng","Xin","Ren","Gui"]
EARTHLY_BRANCHES = ["Zi","Chou","Yin","Mao","Chen","Si","Wu","Wei","Shen","You","Xu","Hai"]

# Map stem to element
STEM_ELEMENTS = {
    "Jia": "Wood",
    "Yi": "Wood",
    "Bing": "Fire",
    "Ding": "Fire",
    "Wu": "Earth",
    "Ji": "Earth",
    "Geng": "Metal",
    "Xin": "Metal",
    "Ren": "Water",
    "Gui": "Water"
}

def get_day_master(year:int, month:int, day:int):
    if sxtwl is None:
        raise RuntimeError("sxtwl library not installed. Install via `pip install sxtwl`.")

    day_obj = sxtwl.fromSolar(year, month, day)
    d_gan_idx = day_obj.getDayTianGan()  # 0-9
    gan = HEAVENLY_STEMS[d_gan_idx]
    element = STEM_ELEMENTS[gan]
    return f"{gan} — {gan} ({element})"

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Whispers of YI — Day Master", layout="centered")

st.title("Whispers of YI — Day Master")
st.write("Enter your birth details to calculate your Day Master (Gan of the Day).")

if sxtwl is None:
    st.error("The `sxtwl` library is not installed. Please install via `pip install sxtwl` and rerun.")
    st.stop()

# Input: Date
dob = st.date_input("Date of Birth (YYYY-MM-DD)", min_value=datetime(1900,1,1), max_value=datetime.now())

# Input: Time
birth_hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=12)
birth_minute = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=0)

# Input: Timezone (string for pytz)
timezone_input = st.selectbox(
    "Timezone",
    pytz.all_timezones,
    index=pytz.all_timezones.index("Asia/Kuala_Lumpur") if "Asia/Kuala_Lumpur" in pytz.all_timezones else 0
)

if st.button("Reveal Day Master"):
    try:
        tz = pytz.timezone(timezone_input)
    except:
        tz = pytz.UTC

    local_dt = datetime(dob.year, dob.month, dob.day, birth_hour, birth_minute)
    local_dt = tz.localize(local_dt)

    try:
        day_master_str = get_day_master(local_dt.year, local_dt.month, local_dt.day)
        st.subheader("Your Day Master")
        st.success(day_master_str)
    except Exception as e:
        st.error(f"Calculation failed: {e}")

st.caption("Whispers of YI — a quiet companion for your journey.")
