# bazi_app.py

import streamlit as st
from datetime import datetime, date, time as dtime
import pytz

# Attempt to import sxtwl
try:
    import sxtwl
except ImportError:
    sxtwl = None

# Heavenly Stems & Earthly Branches
HEAVENLY_STEMS = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
HEAVENLY_STEMS_EN = ["Jia","Yi","Bing","Ding","Wu","Ji","Geng","Xin","Ren","Gui"]

def hour_branch_index(hour: int) -> int:
    """Return Earthly Branch index for Chinese hour (2-hour blocks)."""
    return ((hour + 1) // 2) % 12

def get_day_master(year: int, month: int, day: int) -> dict:
    """
    Returns Day Master stem (Heavenly Stem) for a given Gregorian date.
    Uses sxtwl (latest API) and lunar calendar corrections.
    """
    if sxtwl is None:
        raise RuntimeError("sxtwl library not installed. Please add it to requirements.txt and install.")

    lunar = sxtwl.Lunar()  # latest sxtwl uses Lunar() to access methods
    day_obj = lunar.getDayBySolar(year, month, day)

    # Day Master (Heavenly Stem of the day)
    dm_idx = day_obj.Tg  # Updated property name in latest sxtwl
    return {
        "index": dm_idx,
        "stem_ch": HEAVENLY_STEMS[dm_idx],
        "stem_en": HEAVENLY_STEMS_EN[dm_idx]
    }

# --- Streamlit UI ---
st.set_page_config(page_title="Whispers of YI · Day Master", layout="centered")

st.title("Whispers of YI · Day Master")
st.write("Enter your birth date, time, and timezone to find your Day Master (Heavenly Stem).")

if sxtwl is None:
    st.error(
        "The `sxtwl` library is not installed. "
        "Install locally with `pip install sxtwl` or add it to requirements.txt for Streamlit Cloud."
    )
    st.stop()

# Input: Date of Birth
dob = st.date_input("Date of Birth", min_value=date(1900,1,1))

# Input: Time of Birth
btime = st.time_input("Time of Birth", value=dtime(hour=12, minute=0))

# Input: Timezone
tz_input = st.selectbox(
    "Timezone (UTC offset)",
    pytz.all_timezones,
    index=pytz.all_timezones.index("Asia/Kuala_Lumpur") if "Asia/Kuala_Lumpur" in pytz.all_timezones else 0
)

# Button
if st.button("Reveal Day Master"):
    year, month, day = dob.year, dob.month, dob.day
    hour, minute = btime.hour, btime.minute

    # Apply timezone
    try:
        tz = pytz.timezone(tz_input)
    except Exception:
        tz = pytz.UTC
    dt = datetime(year, month, day, hour, minute, tzinfo=tz)

    try:
        dm = get_day_master(year, month, day)
    except Exception as e:
        st.error(f"Calculation failed: {e}")
    else:
        st.subheader("Your Day Master (Heavenly Stem)")
        st.markdown(f"**{dm['stem_ch']} — {dm['stem_en']}**")
        st.info("This is the Heavenly Stem of your birth day, also called your Day Master in BaZi.")
