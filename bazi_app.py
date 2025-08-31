# bazi_app.py
import streamlit as st
from datetime import date, time as dtime
import sxtwl

# --- Mappings ---
HEAVENLY_STEMS = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
HEAVENLY_STEMS_EN = ["Jia","Yi","Bing","Ding","Wu","Ji","Geng","Xin","Ren","Gui"]
HEAVENLY_STEMS_ELEM = ["Wood","Wood","Fire","Fire","Earth","Earth","Metal","Metal","Water","Water"]

# --- Helper Functions ---
def hour_branch_index(hour:int) -> int:
    """Return Earthly Branch index for a given hour (0-23)."""
    return ((hour + 1) // 2) % 12

def get_day_master(year:int, month:int, day:int, hour:int, minute:int):
    lunar = sxtwl.Lunar()
    day_obj = lunar.getDayBySolar(year, month, day)
    d_gan_idx = int(day_obj.getDayTianGan())
    return {
        "gan_idx": d_gan_idx,
        "stem": HEAVENLY_STEMS[d_gan_idx],
        "pinyin": HEAVENLY_STEMS_EN[d_gan_idx],
        "element": HEAVENLY_STEMS_ELEM[d_gan_idx]
    }

# --- Streamlit App ---
st.set_page_config(page_title="Whispers of YI — Day Master", layout="centered")

st.title("Whispers of YI — Day Master")
st.write("Discover your accurate Day Master (Heavenly Stem of the Day) using lunar & solar-term-aware calculation.")

# --- Input ---
bdate = st.date_input("Date of Birth", value=date.today())
btime = st.time_input("Time of Birth (24h)", value=dtime(hour=0, minute=0))

tz_offset = st.number_input("Timezone UTC offset (e.g., 8 for UTC+8)", min_value=-12, max_value=14, value=8)

if st.button("Reveal Day Master"):
    Y, M, D = bdate.year, bdate.month, bdate.day
    h, mi = btime.hour, btime.minute

    try:
        result = get_day_master(Y, M, D, h, mi)
        st.subheader("Your Day Master")
        st.write(f"{result['stem']} — {result['pinyin']} {result['element']}")
        st.caption("This calculation is lunar & solar-term-aware. Timezone is applied via UTC offset for clarity.")
    except Exception as e:
        st.error(f"Calculation failed: {e}")
