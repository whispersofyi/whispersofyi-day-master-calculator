import streamlit as st
from datetime import datetime
import pytz
import math

st.set_page_config(page_title="Day Master Calculator", page_icon="✨", layout="centered")

# --- Simple White/Black Theme ---
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }

    .title {
        font-size: 2rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 1.5rem;
        color: #000000;
    }
    .subtitle {
        font-size: 1.25rem;
        font-weight: 500;
        text-align: center;
        margin-bottom: 1rem;
        color: #000000;
    }

    .result-box {
        border: 1px solid #00000020;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        background-color: #ffffff;
    }
    .day-master {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        color: #000000;
    }
    .pillar {
        font-size: 1.25rem;
        margin: 0.25rem 0;
        text-align: center;
        color: #000000;
    }

    /* Keep Streamlit widgets clean */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #000000 !important;
        border-radius: 6px !important;
        font-weight: 500;
    }
    div.stButton > button:hover {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Core Calculation ---
heavenly_stems = ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]
stem_traits = {
    "Jia": "Tall tree, upright, principled, resilient",
    "Yi": "Gentle wood, flexible, diplomatic, persuasive",
    "Bing": "Sun fire, warm, generous, charismatic",
    "Ding": "Candle flame, subtle, insightful, supportive",
    "Wu": "Big mountain, stable, reliable, protective",
    "Ji": "Nurturing soil, practical, empathetic, grounded",
    "Geng": "Solid metal, strong, disciplined, determined",
    "Xin": "Ornamental metal, refined, meticulous, elegant",
    "Ren": "Vast ocean, wise, resourceful, adaptive",
    "Gui": "Rain water, intuitive, gentle, mysterious",
}

def calculate_day_master(year, month, day, hour, minute, tz_str):
    tz = pytz.timezone(tz_str)
    dt = datetime(year, month, day, hour, minute, tzinfo=tz)

    # Simplified day stem calculation
    ref_date = datetime(1900, 1, 31, tzinfo=pytz.UTC)
    days_diff = (dt.astimezone(pytz.UTC) - ref_date).days
    stem_index = days_diff % 10
    return heavenly_stems[stem_index]

# --- UI ---
st.markdown('<div class="title">✨ Day Master Calculator ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Discover your Heavenly Stem and its traits</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    year = st.number_input("Year", min_value=1900, max_value=2100, value=1990)
    month = st.number_input("Month", min_value=1, max_value=12, value=1)
    day = st.number_input("Day", min_value=1, max_value=31, value=1)
with col2:
    hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=12)
    minute = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=0)
    tz_str = st.selectbox("Time Zone", pytz.all_timezones, index=pytz.all_timezones.index("Asia/Kuala_Lumpur"))

if st.button("Calculate"):
    dm = calculate_day_master(year, month, day, hour, minute, tz_str)
    traits = stem_traits.get(dm, "Traits not found.")

    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown(f'<div class="day-master">{dm}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pillar">{traits}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
