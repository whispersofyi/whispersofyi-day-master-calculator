import streamlit as st
from datetime import datetime
import pytz
from zhdate import ZhDate

# --- Page Config ---
st.set_page_config(
    page_title="Whispers of Yi - Day Master Calculator",
    page_icon="☯️",
    layout="centered"
)

# --- Theme Styling (fonts, colors, buttons) ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather&display=swap');

    html, body, [class*="css"] {
        font-family: 'Merriweather', serif !important;
        background-color: #FFFFFF;
        color: #000000;
    }

    .stButton button {
        border-radius: 12px;
        padding: 0.5rem 1.2rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        transition: 0.2s ease-in-out;
        border: 1px solid #000000;
    }
    .stButton button:hover {
        background-color: #000000;
        color: #FFFFFF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Day Master Calculation ---
heavenly_stems = ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]
stem_traits = {
    "Jia": "Jia (Yang Wood): Tall trees, resilient, upright, principled, but sometimes rigid.",
    "Yi": "Yi (Yin Wood): Flexible plants, adaptable, diplomatic, nurturing, but can be indecisive.",
    "Bing": "Bing (Yang Fire): Sunlight, warm, passionate, inspiring, but sometimes overwhelming.",
    "Ding": "Ding (Yin Fire): Candlelight, gentle, wise, refined, but can be unpredictable.",
    "Wu": "Wu (Yang Earth): Mountain, stable, dependable, protective, but stubborn.",
    "Ji": "Ji (Yin Earth): Farmland, nurturing, supportive, practical, but sometimes worrisome.",
    "Geng": "Geng (Yang Metal): Axe, strong, disciplined, decisive, but harsh.",
    "Xin": "Xin (Yin Metal): Jewelry, elegant, meticulous, refined, but perfectionistic.",
    "Ren": "Ren (Yang Water): Ocean, deep, wise, resourceful, but overwhelming.",
    "Gui": "Gui (Yin Water): Rain, gentle, insightful, adaptable, but elusive."
}

def get_day_master(year, month, day, hour, minute, tz_str):
    try:
        tz = pytz.timezone(tz_str)
        dt = datetime(year, month, day, hour, minute, tzinfo=tz)
        lunar_date = ZhDate.from_datetime(dt)
        day_gan_index = (lunar_date.lunar_day - 1) % 10
        return heavenly_stems[day_gan_index]
    except Exception as e:
        return None

# --- UI Layout ---
st.title("☯️ Whispers of Yi - Day Master Calculator")
st.write("Enter your birth details to discover your **Day Master** and its elemental traits.")

with st.form("bazi_form"):
    col1, col2 = st.columns(2)

    with col1:
        year = st.number_input("Year", min_value=1900, max_value=2100, value=1990)
        month = st.number_input("Month", min_value=1, max_value=12, value=1)
        day = st.number_input("Day", min_value=1, max_value=31, value=1)

    with col2:
        hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=0)
        minute = st.selectbox("Minute", options=list(range(0, 60, 5)), index=0)
        timezone = st.selectbox("Timezone", pytz.all_timezones, index=pytz.all_timezones.index("Asia/Shanghai"))

    submitted = st.form_submit_button("Calculate Day Master")

if submitted:
    day_master = get_day_master(year, month, day, hour, minute, timezone)
    if day_master:
        st.subheader(f"Your Day Master: {day_master}")
        st.info(stem_traits[day_master])
    else:
        st.error("Could not calculate Day Master. Please check your inputs.")
