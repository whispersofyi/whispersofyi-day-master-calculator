# bazi_app.py

import streamlit as st
from datetime import date, time as dtime
import pytz

# --- Attempt to import sxtwl ---
try:
    import sxtwl
except Exception:
    st.error("Library `sxtwl` not found. Install via `pip install sxtwl`.")
    st.stop()

# --- Heavenly Stems & Earthly Branches ---
HEAVENLY_STEMS = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
HEAVENLY_STEMS_EN = ["Jia","Yi","Bing","Ding","Wu","Ji","Geng","Xin","Ren","Gui"]
EARTHLY_BRANCHES = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
EARTHLY_BRANCHES_EN = ["Zi","Chou","Yin","Mao","Chen","Si","Wu","Wei","Shen","You","Xu","Hai"]

# --- Helper Functions ---
def hour_branch_index(hour:int) -> int:
    """Return Earthly Branch index for a given hour (0-23)."""
    return ((hour + 1) // 2) % 12

def safe_get_pillars(Y:int, M:int, D:int, h:int, mi:int):
    """Return Day Master and optional Year/Month/Hour pillars using sxtwl."""
    lunar = sxtwl.Lunar()
    day_obj = lunar.getDayBySolar(Y, M, D)

    # Day Master (Heavenly Stem of Day)
    d_gan_idx = int(day_obj.getDayGZ().tg)
    d_zhi_idx = int(day_obj.getDayGZ().dz)

    # Month Pillar (solar-term aware, leap month handled)
    m_gz = day_obj.getMonthGZ()
    m_gan_idx = int(m_gz.tg)
    m_zhi_idx = int(m_gz.dz)

    # Year Pillar (optional)
    y_gz = day_obj.getYearGZ()
    y_gan_idx = int(y_gz.tg)
    y_zhi_idx = int(y_gz.dz)

    # Hour Pillar (optional)
    h_branch_idx = hour_branch_index(h)
    h_gan_idx = (d_gan_idx * 2 + h_branch_idx) % 10
    h_zhi_idx = h_branch_idx

    return {
        "day_master": {"gan_idx": d_gan_idx, "zhi_idx": d_zhi_idx},
        "month": {"gan_idx": m_gan_idx, "zhi_idx": m_zhi_idx},
        "year": {"gan_idx": y_gan_idx, "zhi_idx": y_zhi_idx},
        "hour": {"gan_idx": h_gan_idx, "zhi_idx": h_zhi_idx}
    }

# --- Streamlit UI ---
st.set_page_config(page_title="Whispers of Yi · Day Master", layout="centered")
st.title("Whispers of Yi · Day Master Calculator")
st.write("Enter your birth details to calculate your **Day Master**. Month Pillar is solar-term aware and handles leap months. Optional Year & Hour pillars can be displayed.")

# Input Form
with st.form("bazi_form"):
    col1, col2 = st.columns(2)
    with col1:
        bdate = st.date_input("Date of Birth", min_value=date(1900,1,1), max_value=date.today(), value=date.today())
    with col2:
        btime = st.time_input("Time of Birth (24h)", value=dtime(hour=12, minute=0))

    tz_options = [
        "-12","-11","-10","-9","-8","-7","-6","-5","-4","-3","-2","-1",
        "0","1","2","3","3.5","4","4.5","5","5.5","5.75","6","6.5","7","8","9","9.5","10","11","12","13","14"
    ]
    tz_default = "8"
    tz = st.selectbox("Time zone (UTC offset)", options=tz_options, index=tz_options.index(tz_default))
    dst = st.checkbox("Daylight saving in effect at birth?", value=False)
    show_optional = st.checkbox("Show Year & Hour Pillars?", value=False)

    submitted = st.form_submit_button("Reveal Day Master")

if submitted:
    Y, M, D = bdate.year, bdate.month, bdate.day
    h, mi = btime.hour, btime.minute

    tz_off = float(tz)
    if dst:
        tz_off += 1.0

    try:
        result = safe_get_pillars(Y, M, D, h, mi)
    except Exception as e:
        st.error(f"Calculation failed: {e}")
        st.stop()

    st.markdown("---")
    st.subheader("Input (local civil time)")
    st.write(f"Local datetime: **{Y}-{M:02d}-{D:02d} {h:02d}:{mi:02d}** (UTC{ '+' if tz_off>=0 else ''}{tz_off})")

    st.markdown("---")
    st.subheader("Day Master")
    dm_idx = result["day_master"]["gan_idx"]
    st.metric("Day Master", f"{HEAVENLY_STEMS[dm_idx]}{EARTHLY_BRANCHES[result['day_master']['zhi_idx']]}", delta=f"{HEAVENLY_STEMS_EN[dm_idx]}")

    st.subheader("Month Pillar")
    st.write(f"{HEAVENLY_STEMS[result['month']['gan_idx']]}{EARTHLY_BRANCHES[result['month']['zhi_idx']]} — {HEAVENLY_STEMS_EN[result['month']['gan_idx']]} {EARTHLY_BRANCHES_EN[result['month']['zhi_idx']]}")

    if show_optional:
        st.subheader("Year Pillar (optional)")
        st.write(f"{HEAVENLY_STEMS[result['year']['gan_idx']]}{EARTHLY_BRANCHES[result['year']['zhi_idx']]} — {HEAVENLY_STEMS_EN[result['year']['gan_idx']]} {EARTHLY_BRANCHES_EN[result['year']['zhi_idx']]}")

        st.subheader("Hour Pillar (optional)")
        st.write(f"{HEAVENLY_STEMS[result['hour']['gan_idx']]}{EARTHLY_BRANCHES[result['hour']['zhi_idx']]} — {HEAVENLY_STEMS_EN[result['hour']['gan_idx']]} {EARTHLY_BRANCHES_EN[result['hour']['zhi_idx']]}")

    st.info("✅ Day Master is the primary stem of the day. Month pillar accounts for solar terms and leap months. Optional pillars are for reference and can be expanded later.")
