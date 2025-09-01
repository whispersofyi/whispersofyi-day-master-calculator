import streamlit as st
from datetime import datetime, timedelta

# ---------------------------
# CSS Styling for Whispers of Yi identity
# ---------------------------
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }

    /* Titles */
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

    /* Cards */
    .card {
        border: 1px solid #00000020;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem auto;
        background-color: #ffffff;
        box-shadow: none;
        max-width: 700px;
    }

    /* Results */
    .day-master {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        color: #000000;
    }
    .pillar {
        font-size: 1.25rem;
        margin: 0.25rem 0;
        text-align: center;
        color: #000000;
    }

    /* Form inputs */
    .stSelectbox, .stNumberInput, .stDateInput, .stTimeInput, .stTextInput {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #00000040 !important;
        border-radius: 6px !important;
    }
    .stSelectbox div, .stSelectbox option {
        color: #000000 !important;
        background-color: #ffffff !important;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #000000 !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    div.stButton > button:hover {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 1px solid #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Data for Heavenly Stems (Day Masters)
# ---------------------------
DAY_MASTER_DATA = {
    "甲": "Yang Wood – Upright tree, principled, dependable, resilient.",
    "乙": "Yin Wood – Flexible vine, adaptive, graceful, persuasive.",
    "丙": "Yang Fire – Sun, radiant, inspiring, generous.",
    "丁": "Yin Fire – Candle flame, subtle, warm, insightful.",
    "戊": "Yang Earth – Mountain, steady, protective, reliable.",
    "己": "Yin Earth – Garden soil, nurturing, supportive, practical.",
    "庚": "Yang Metal – Axe, bold, decisive, disciplined.",
    "辛": "Yin Metal – Jewelry, refined, meticulous, elegant.",
    "壬": "Yang Water – Ocean, vast, resourceful, wise.",
    "癸": "Yin Water – Morning dew, gentle, thoughtful, intuitive."
}

HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# ---------------------------
# Calculation Helpers (simplified version)
# ---------------------------
def get_day_master(birth_datetime: datetime) -> str:
    """Simplified calculation of Heavenly Stem of the day."""
    base_date = datetime(1900, 1, 31)  # Reference: Jia Zi day
    days_diff = (birth_datetime - base_date).days
    stem_index = days_diff % 10
    return HEAVENLY_STEMS[stem_index]

def get_four_pillars(birth_datetime: datetime):
    """Very simplified placeholder for Four Pillars calculation."""
    # Year Pillar (simplified)
    year_stem = HEAVENLY_STEMS[(birth_datetime.year - 4) % 10]
    year_branch = EARTHLY_BRANCHES[(birth_datetime.year - 4) % 12]
    # Month Pillar (placeholder logic)
    month_stem = HEAVENLY_STEMS[(birth_datetime.month + birth_datetime.year) % 10]
    month_branch = EARTHLY_BRANCHES[birth_datetime.month % 12]
    # Day Pillar
    day_stem = get_day_master(birth_datetime)
    day_branch = EARTHLY_BRANCHES[birth_datetime.day % 12]
    # Hour Pillar
    hour_branch_index = (birth_datetime.hour + 1) // 2 % 12
    hour_branch = EARTHLY_BRANCHES[hour_branch_index]
    hour_stem = HEAVENLY_STEMS[(hour_branch_index + HEAVENLY_STEMS.index(day_stem)) % 10]

    return {
        "Year": year_stem + year_branch,
        "Month": month_stem + month_branch,
        "Day": day_stem + day_branch,
        "Hour": hour_stem + hour_branch
    }

# ---------------------------
# Streamlit App
# ---------------------------
st.markdown('<div class="title">Day Master Calculator</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Enter Your Birth Details</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        year = st.number_input("Year", min_value=1900, max_value=2100, value=1990)
        month = st.number_input("Month", min_value=1, max_value=12, value=1)
        day = st.number_input("Day", min_value=1, max_value=31, value=1)
    with col2:
        hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=12)
        minute = st.number_input("Minute (0-59)", min_value=0, max_value=0, value=0)
        gmt_offset = st.selectbox("GMT Offset", [f"GMT{offset:+d}" for offset in range(-12, 13)], index=8)

    st.markdown('</div>', unsafe_allow_html=True)

if st.button("Calculate Day Master"):
    try:
        birth_datetime = datetime(year, month, day, hour, minute)
        offset_hours = int(gmt_offset.replace("GMT", ""))
        birth_datetime = birth_datetime - timedelta(hours=offset_hours)

        day_master = get_day_master(birth_datetime)
        pillars = get_four_pillars(birth_datetime)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="day-master">{day_master}</div>', unsafe_allow_html=True)
        st.write(DAY_MASTER_DATA.get(day_master, "No data available."))
        st.markdown("---")
        st.markdown('<div class="subtitle">Your Four Pillars</div>', unsafe_allow_html=True)
        for pillar, value in pillars.items():
            st.markdown(f'<div class="pillar">{pillar}: {value}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {e}")
