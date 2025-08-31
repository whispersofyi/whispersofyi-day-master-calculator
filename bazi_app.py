# bazi_app.py

import streamlit as st
from datetime import date, time as dtime
import sxtwl  # Chinese calendar library

# -------------------------
# BaZi Helpers
# -------------------------
HEAVENLY_STEMS = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
HEAVENLY_STEMS_EN = ["Jia","Yi","Bing","Ding","Wu","Ji","Geng","Xin","Ren","Gui"]
EARTHLY_BRANCHES = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
EARTHLY_BRANCHES_EN = ["Zi","Chou","Yin","Mao","Chen","Si","Wu","Wei","Shen","You","Xu","Hai"]

def hour_branch_index(hour:int) -> int:
    """Return Earthly Branch index for a given hour (0-23)."""
    return ((hour + 1) // 2) % 12

def safe_get_pillars(year:int, month:int, day:int, hour:int, minute:int):
    """Calculate Four Pillars and Day Master using sxtwl."""
    lunar = sxtwl.Lunar()
    day_obj = lunar.getDayBySolar(year, month, day)

    # Year, Month, Day GanZhi
    y_gz = day_obj.getYearGZ()
    m_gz = day_obj.getMonthGZ()
    d_gz = day_obj.getDayGZ()

    y_gan_idx = int(y_gz.tg)
    y_zhi_idx = int(y_gz.dz)
    m_gan_idx = int(m_gz.tg)
    m_zhi_idx = int(m_gz.dz)
    d_gan_idx = int(d_gz.tg)
    d_zhi_idx = int(d_gz.dz)

    # Hour GanZhi
    h_branch_idx = hour_branch_index(hour)
    h_gan_idx = (d_gan_idx * 2 + h_branch_idx) % 10
    h_zhi_idx = h_branch_idx

    return {
        "year": {"gan_idx": y_gan_idx, "zhi_idx": y_zhi_idx},
        "month": {"gan_idx": m_gan_idx, "zhi_idx": m_zhi_idx},
        "day": {"gan_idx": d_gan_idx, "zhi_idx": d_zhi_idx},
        "hour": {"gan_idx": h_gan_idx, "zhi_idx": h_zhi_idx},
        "day_master": {"gan_idx": d_gan_idx}
    }

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Whispers of Yi · BaZi Companion", layout="centered")
st.title("Whispers of Yi · BaZi Companion")
st.write("A quiet, accurate Four-Pillars (BaZi) tool — lunar corrections & solar-term-aware. Enter your birth details and receive your Four Pillars.")

# Input form
with st.form("bazi_form"):
    col1, col2 = st.columns([1,1])
    with col1:
        bdate = st.date_input(
            "Date of Birth",
            value=date.today(),
            min_value=date(1900,1,1),
            max_value=date.today()
        )
    with col2:
        btime = st.time_input("Time of Birth", value=dtime(hour=0, minute=0))
    tz_options = [
        "-12","-11","-10","-9","-8","-7","-6","-5","-4","-3","-2","-1",
        "0","1","2","3","3.5","4","4.5","5","5.5","5.75","6","6.5","7","8","9","9.5","10","11","12","13","14"
    ]
    tz_default = "8"
    tz = st.selectbox("Time zone — UTC offset", options=tz_options, index=tz_options.index(tz_default))
    dst = st.checkbox("Daylight saving in effect at birth?", value=False)
    submitted = st.form_submit_button("Reveal Pillars")

# Process and display
if submitted:
    Y = bdate.year
    M = bdate.month
    D = bdate.day
    h = btime.hour
    mi = btime.minute

    try:
        tz_off = float(tz)
    except:
        tz_off = 0.0
    if dst:
        tz_off += 1.0

    try:
        result = safe_get_pillars(Y, M, D, h, mi)
    except Exception as e:
        st.error(f"Calculation failed: {e}")
        st.stop()

    st.markdown("---")
    st.subheader("Input (local civil time)")
    st.write(f"Local datetime: **{Y}-{M:02d}-{D:02d} {h:02d}:{mi:02d}**  (UTC{ '+' if tz_off>=0 else ''}{tz_off})")
    st.write("Note: calculation uses solar-term-aware month logic and leap-month correction.")

    st.markdown("---")
    st.subheader("Four Pillars (Gan–Zhi)")
    cols = st.columns(4)
    pillars = ["year","month","day","hour"]
    labels = ["Year","Month","Day","Hour"]
    for c, p, lab in zip(cols, pillars, labels):
        gan_i = result[p]["gan_idx"]
        zhi_i = result[p]["zhi_idx"]
        c.metric(label=lab, value=f"{HEAVENLY_STEMS[gan_i]}{EARTHLY_BRANCHES[zhi_i]}", delta=f"{HEAVENLY_STEMS_EN[gan_i]} {EARTHLY_BRANCHES_EN[zhi_i]}")

    dm_idx = result["day_master"]["gan_idx"]
    st.markdown("---")
    st.write("**Day Master (Heavenly Stem of the Day):**", f"{HEAVENLY_STEMS[dm_idx]} — {HEAVENLY_STEMS_EN[dm_idx]}")

    st.info("This calculator uses a solar-term-aware algorithm (via `sxtwl`) so the month pillar follows Jieqi boundaries and leap-month corrections.")
    st.caption("If the birth time is approximate, or within ±1 hour of a solar term boundary, consider verifying with a local astrologer or try alternate nearby minutes to check boundary effects.")
