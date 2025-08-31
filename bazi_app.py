# bazi_app.py

import streamlit as st
from datetime import datetime, timedelta
import pytz

# Attempt to import sxtwl
try:
    import sxtwl
except ImportError:
    sxtwl = None

# -------------------------
# BaZi Day Master Helpers
# -------------------------
HEAVENLY_STEMS = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
HEAVENLY_STEMS_EN = ["Jia","Yi","Bing","Ding","Wu","Ji","Geng","Xin","Ren","Gui"]

def get_day_master(year:int, month:int, day:int, hour:int, minute:int, tz_offset:float=0.0):
    """
    Calculate Day Master (Heavenly Stem of the Day) using sxtwl
    tz_offset: numeric hours offset from UTC (e.g., 8 for Malaysia)
    Returns: tuple (stem_char, stem_en)
    """
    if sxtwl is None:
        raise RuntimeError("sxtwl library not installed. Please add `sxtwl` to requirements.txt and install.")

    # Construct naive datetime, then adjust to UTC by subtracting offset
    dt = datetime(year, month, day, hour, minute)
    dt_utc = dt - timedelta(hours=tz_offset)

    # Get lunar day object
    lunar_day = sxtwl.fromSolar(dt_utc.year, dt_utc.month, dt_utc.day)

    # Day GanZhi
    d_gz = lunar_day.getDayGZ()
    d_gan_idx = int(d_gz.tg)

    return HEAVENLY_STEMS[d_gan_idx], HEAVENLY_STEMS_EN[d_gan_idx]

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Whispers of YI — Day Master Calculator", layout="centered")

st.title("Whispers of YI — Day Master Calculator")
st.write("Calculate your **Day Master** (Heavenly Stem of your birth day) with timezone & full time input.")

if sxtwl is None:
    st.error(
        "The `sxtwl` library is not available. "
        "Install it locally via `pip install sxtwl`, "
        "or ensure it is listed in requirements.txt for Streamlit Cloud."
    )
    st.stop()

# Input: Date
dob = st.date_input("Date of Birth (YYYY-MM-DD)", min_value=datetime(1900,1,1).date())

# Input: Time
birth_hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=12)
birth_minute = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=0)

# Input: Timezone as numeric offset
tz_options = [
    "-12","-11","-10","-9","-8","-7","-6","-5","-4","-3","-2","-1",
    "0","1","2","3","3.5","4","4.5","5","5.5","5.75","6","6.5","7","8","9","9.5","10","11","12","13","14"
]
tz_default = "8"
tz_offset = st.selectbox("Timezone (UTC offset, numeric)", options=tz_options, index=tz_options.index(tz_default))
dst = st.checkbox("Daylight saving in effect at birth (+1 hour)?", value=False)

# Calculate button
if st.button("Reveal Day Master"):
    Y, M, D = dob.year, dob.month, dob.day
    tz_val = float(tz_offset)
    if dst:
        tz_val += 1.0

    try:
        stem_char, stem_en = get_day_master(Y, M, D, birth_hour, birth_minute, tz_val)
        st.subheader("Your Day Master:")
        st.write(f"**{stem_char} — {stem_en}**")
        st.info("This is solar-term-aware and handles leap months. Optional Year/Hour Pillars can be added in future updates.")
    except Exception as e:
        st.error(f"Calculation failed: {e}")

st.caption("Ensure your birth time is as accurate as possible for correct Day Master calculation. Timezone matters for precise results.")
