# bazi_app.py
import streamlit as st
from datetime import datetime, date, time as dtime
import pytz

# Attempt to import sxtwl
try:
    import sxtwl
except ImportError:
    sxtwl = None

# -------------------------
# BaZi Constants
# -------------------------
HEAVENLY_STEMS = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
HEAVENLY_STEMS_EN = ["Jia","Yi","Bing","Ding","Wu","Ji","Geng","Xin","Ren","Gui"]

# -------------------------
# Helper Functions
# -------------------------
def hour_branch_index(hour:int) -> int:
    """Return Earthly Branch index for hour (0-23), Zi starts 23:00-0:59"""
    return ((hour + 1) // 2) % 12

def get_day_master(year:int, month:int, day:int, hour:int, minute:int, tz_offset:float=0.0):
    """
    Calculate Day Master (Heavenly Stem of the Day) with sxtwl (latest API)
    tz_offset: numeric hours offset from UTC (e.g., 8 for Malaysia)
    Returns: tuple (stem_char, stem_en)
    """
    if sxtwl is None:
        raise RuntimeError("sxtwl not installed. Add `sxtwl` to requirements.txt.")

    # Construct naive datetime, then adjust to UTC by subtracting offset
    dt = datetime(year, month, day, hour, minute)
    dt_utc = dt - pytz.timedelta(hours=tz_offset)

    # Get lunar day object using latest API
    lunar_day = sxtwl.fromSolar(dt_utc.year, dt_utc.month, dt_utc.day)

    # Day GanZhi
    d_gz = lunar_day.getDayGZ()
    d_gan_idx = int(d_gz.tg)

    return HEAVENLY_STEMS[d_gan_idx], HEAVENLY_STEMS_EN[d_gan_idx]

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Whispers of YI — BaZi Calculator", layout="centered")
st.title("Whispers of YI — BaZi Calculator")
st.write("A solar-term-aware, accurate Day Master calculator. Enter your full birth details for best results.")

if sxtwl is None:
    st.error(
        "The Chinese calendar library `sxtwl` is not available.\n"
        "If running locally, `pip install sxtwl`.\n"
        "On Streamlit Cloud, ensure it's in requirements.txt."
    )
    st.stop()

# --- Input Form ---
with st.form("bazi_form"):
    col1, col2 = st.columns(2)
    with col1:
        bdate = st.date_input("Date of Birth", value=date(1990,1,1), min_value=date(1900,1,1))
    with col2:
        btime = st.time_input("Time of Birth", value=dtime(hour=12, minute=0))
    tz_options = [str(i) for i in range(-12, 15)]  # simple numeric offsets
    tz_offset = float(st.selectbox("UTC Offset (Birth Timezone)", options=tz_options, index=20))  # default UTC+8
    dst = st.checkbox("Daylight saving in effect?", value=False)
    submitted = st.form_submit_button("Reveal Day Master")

if submitted:
    Y, M, D = bdate.year, bdate.month, bdate.day
    h, mi = btime.hour, btime.minute
    if dst:
        tz_offset += 1.0

    try:
        stem_char, stem_en = get_day_master(Y, M, D, h, mi, tz_offset)
        st.subheader("Your Day Master")
        st.write(f"**{stem_char} — {stem_en}**")
        st.info("This calculation uses solar-term-aware day GanZhi. Year and Hour pillars can be added in future updates.")
    except Exception as e:
        st.error(f"Calculation failed: {e}")
