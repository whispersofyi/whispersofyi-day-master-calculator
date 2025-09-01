import streamlit as st
from datetime import datetime
import pytz
import sxtwl

# --- Heavenly Stems mapping ---
HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
HEAVENLY_STEMS_EN = ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]
ELEMENTS = ["Wood", "Wood", "Fire", "Fire", "Earth", "Earth", "Metal", "Metal", "Water", "Water"]

# --- Traits dictionary ---
DAY_MASTER_TRAITS = {
    "Jia": "Like a great tree, Jia Wood stands tall and upright. Strong principles, dependable, but sometimes inflexible.",
    "Yi": "Graceful like vines and flowers, Yi Wood is adaptive, persuasive, and diplomatic, though sometimes indecisive.",
    "Bing": "Like the blazing sun, Bing Fire is warm, generous, and charismatic, though may burn too intensely.",
    "Ding": "Like candlelight, Ding Fire is gentle, insightful, and illuminating, though fragile at times.",
    "Wu": "Like mountains, Wu Earth is steady, reliable, and protective, but may be stubborn and rigid.",
    "Ji": "Like fertile soil, Ji Earth is nurturing, practical, and empathetic, but may overthink or worry.",
    "Geng": "Like raw ore, Geng Metal is strong-willed, disciplined, and courageous, but can be harsh or unyielding.",
    "Xin": "Like polished jewels, Xin Metal is refined, elegant, and detail-oriented, but may appear vain or critical.",
    "Ren": "Like the vast ocean, Ren Water is wise, resourceful, and visionary, but sometimes overwhelming or restless.",
    "Gui": "Like morning dew, Gui Water is subtle, intuitive, and sensitive, but may be elusive or moody.",
}

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="Whispers of YI — Day Master",
    layout="centered"
)

# --- Custom Style to match whispersofyi.github.io ---
st.markdown(
    """
    <style>
    body {
        background-color: white;
        font-family: "Times New Roman", Georgia, serif;
        color: #222222;
    }
    .block-container {
        max-width: 650px;
        padding-top: 2rem;
    }
    h1, h2, h3 {
        text-align: center;
        font-weight: 500;
    }
    .stButton button {
        background-color: black;
        color: white;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        font-size: 1em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Title ---
st.title("Whispers of YI — Day Master")
st.markdown("Enter your birth details to discover your Day Master.")

# --- Input: Date + Time ---
year = st.number_input("Year", min_value=1900, max_value=2100, value=2000)
month = st.number_input("Month", min_value=1, max_value=12, value=1)
day = st.number_input("Day", min_value=1, max_value=31, value=1)
hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=12)
minute = st.number_input("Minute (0-59)", min_value=0, max_value=59, step=5, value=0)

# --- Input: Timezone (GMT offsets only) ---
gmt_offsets = [f"GMT{offset:+d}" for offset in range(-12, 13)]
timezone_choice = st.selectbox("Timezone", gmt_offsets, index=gmt_offsets.index("GMT+8"))

# --- Button ---
if st.button("Reveal Day Master"):
    try:
        # Map GMT offset to tzinfo
        offset_hours = int(timezone_choice.replace("GMT", ""))
        tz = pytz.FixedOffset(offset_hours * 60)

        dt = datetime(year, month, day, hour, minute, tzinfo=tz)

        # --- Get Lunar object from sxtwl ---
        day_obj = sxtwl.fromSolar(dt.year, dt.month, dt.day)

        # --- Extract Day Stem ---
        tg_index = day_obj.getDayGZ().tg  # Heavenly Stem index (0–9)
        day_master_zh = HEAVENLY_STEMS[tg_index]
        day_master_en = HEAVENLY_STEMS_EN[tg_index]
        element = ELEMENTS[tg_index]

        # --- Traits ---
        traits = DAY_MASTER_TRAITS.get(day_master_en, "No traits available.")

        # --- Output ---
        st.subheader("Your Day Master")
        st.markdown(
            f"""
            <div style='text-align:center; font-size:1.2em;'>
            <b>{day_master_zh} — {day_master_en} ({element})</b><br><br>
            <i>{traits}</i>
            </div>
            """,
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"Calculation failed: {e}")
