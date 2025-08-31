# bazi_app.py
import streamlit as st
from datetime import datetime, time as dtime
import pytz

# Ensure sxtwl is installed and import
try:
    import sxtwl
except ImportError:
    st.error("The `sxtwl` library is not installed. Please run `pip install sxtwl`.")
    st.stop()

# --- Heavenly Stems ---
HEAVENLY_STEMS = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
HEAVENLY_STEMS_EN = ["Jia","Yi","Bing","Ding","Wu","Ji","Geng","Xin","Ren","Gui"]

# --- Element mapping ---
ELEMENTS = {
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

# --- Streamlit UI ---
st.set_page_config(page_title="Whispers of YI — Day Master", layout="centered")
st.title("Whispers of YI — Day Master")
st.write("Discover your accurate Day Master. Enter your birth date, time, and timezone.")

# --- Inputs ---
dob = st.date_input(
    "Date of Birth",
    min_value=datetime(1900,1,1),
    max_value=datetime.today(),
    value=datetime(2000,1,1)
)

birth_hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=12)
birth_minute = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=0)

timezone_input = st.selectbox(
    "Timezone",
    pytz.all_timezones,
    index=pytz.all_timezones.index("Asia/Kuala_Lumpur") if "Asia/Kuala_Lumpur" in pytz.all_timezones else 0
)

if st.button("Reveal Day Master"):
    # --- Build aware datetime ---
    try:
        tz = pytz.timezone(timezone_input)
    except:
        tz = pytz.UTC
    dt = datetime(dob.year, dob.month, dob.day, birth_hour, birth_minute)
    dt = tz.localize(dt)

    # --- Accurate Day Master using sxtwl ---
    try:
        # sxtwl uses integers for year, month, day
        day_obj = sxtwl.getDayBySolar(dob.year, dob.month, dob.day)
        day_master_idx = day_obj.getDayTianGan()
        day_master_zh = HEAVENLY_STEMS[day_master_idx]
        day_master_en = HEAVENLY_STEMS_EN[day_master_idx]
        element = ELEMENTS[day_master_en]

        st.subheader("Your Day Master")
        st.write(f"**{day_master_zh} — {day_master_en} ({element})**")

    except Exception as e:
        st.error(f"Calculation failed: {e}")
