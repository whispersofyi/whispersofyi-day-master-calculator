# bazi_app.py
import streamlit as st
from datetime import date
import sxtwl

# -------------------------
# BaZi Calculation Helpers
# -------------------------

HEAVENLY_STEMS = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
HEAVENLY_STEMS_EN = ["Jia","Yi","Bing","Ding","Wu","Ji","Geng","Xin","Ren","Gui"]
ELEMENTS = ["Wood", "Wood", "Fire", "Fire", "Earth", "Earth", "Metal", "Metal", "Water", "Water"]
YINYANG = ["Yang","Yin","Yang","Yin","Yang","Yin","Yang","Yin","Yang","Yin"]

EARTHLY_BRANCHES = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
EARTHLY_BRANCHES_EN = ["Zi","Chou","Yin","Mao","Chen","Si","Wu","Wei","Shen","You","Xu","Hai"]

def get_day_master(year:int, month:int, day:int, hour:int, minute:int):
    """Return Day Master stem index and details."""
    lunar = sxtwl.Lunar()
    day_obj = lunar.getDayBySolar(year, month, day)
    d_gz = day_obj.getDayGZ()
    d_gan_idx = int(d_gz.tg)
    stem_char = HEAVENLY_STEMS[d_gan_idx]
    stem_en = HEAVENLY_STEMS_EN[d_gan_idx]
    element = ELEMENTS[d_gan_idx]
    yin_yang = YINYANG[d_gan_idx]
    return stem_char, stem_en, element, yin_yang

# -------------------------
# Streamlit App UI
# -------------------------

st.set_page_config(page_title="Whispers of YI — Day Master", layout="centered")

st.title("Whispers of YI — Day Master")
st.write("Enter your birth details to reveal your Day Master (Heavenly Stem of the Day).")

# Input: Date
dob = st.date_input("Date of Birth", min_value=date(1900,1,1), max_value=date.today())

# Input: Time
birth_hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=12)
birth_minute = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=0)

# Timezone
tz_options = [str(x) for x in range(-12,15)] + ["3.5","4.5","5.5","5.75","6.5","9.5"]
tz_default = "8"
tz = st.selectbox("Time zone — UTC offset", options=tz_options, index=tz_options.index(tz_default))

# Button
if st.button("Reveal Day Master"):
    Y = dob.year
    M = dob.month
    D = dob.day
    h = birth_hour
    mi = birth_minute

    try:
        stem_char, stem_en, element, yin_yang = get_day_master(Y,M,D,h,mi)
        st.subheader("Your Day Master:")
        st.success(f"{stem_char} — {stem_en} — {element} ({yin_yang})")

        # Legend
        st.markdown("---")
        st.subheader("Day Master Reference")
        legend_md = "| Stem | English | Element | Yin/Yang |\n|---|---|---|---|\n"
        for i in range(10):
            legend_md += f"| {HEAVENLY_STEMS[i]} | {HEAVENLY_STEMS_EN[i]} | {ELEMENTS[i]} | {YINYANG[i]} |\n"
        st.markdown(legend_md)
    except Exception as e:
        st.error(f"Calculation failed: {e}")
