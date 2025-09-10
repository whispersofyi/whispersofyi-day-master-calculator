# app.py
import streamlit as st
import datetime
import calendar
import math

# Page configuration
st.set_page_config(
    page_title="Day Master Calculator - Whispers of YI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Minimal, safe font + color override ---
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif !important;
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    .pillar-char {
        font-size: 42px !important;
        font-weight: bold !important;
        display: block;
        text-align: center;
    }
    .pillar-caption {
        text-align: center;
        font-size: 14px;
        color: #555555;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------
# Day Master database (full, unchanged)
# ----------------------
DAY_MASTER_DATA = {
    "甲": {"name": "Yang Wood", "element": "Great Tree",
           "description": "Strong, upright, and expansive like a great tree reaching skyward.",
           "positive_traits": ["Resilient", "Principled", "Visionary"],
           "challenges": ["Rigid", "Stubborn", "Slow to adapt"],
           "compatibility": "Harmonises with Yin Water (癸) and benefits from Yang Fire (丙).",
           "career_paths": "Leadership, education, environmental stewardship.",
           "life_philosophy": "Growth through steady, principled action."},
    "乙": {"name": "Yin Wood", "element": "Flowing Grass",
           "description": "Flexible and graceful; finds light in narrow spaces and connects others.",
           "positive_traits": ["Diplomatic", "Creative", "Supportive"],
           "challenges": ["Overly accommodating", "Indecisive"],
           "compatibility": "Benefits from Yang Earth (戊) and Yang Metal (庚).",
           "career_paths": "Arts, counseling, diplomacy.",
           "life_philosophy": "Quiet adaptability cultivates lasting beauty."},
    "丙": {"name": "Yang Fire", "element": "Radiant Sun",
           "description": "Brilliant, warm, and energising — a presence that inspires others.",
           "positive_traits": ["Charismatic", "Generous", "Energetic"],
           "challenges": ["Impulsive", "Prone to burnout"],
           "compatibility": "Balanced by Yin Water (癸) and supported by Yang Wood (甲).",
           "career_paths": "Public speaking, creative leadership, media.",
           "life_philosophy": "Illuminate with warmth, not scorch with heat."},
    "丁": {"name": "Yin Fire", "element": "Focused Flame",
           "description": "Subtle, refined warmth — precise and quietly illuminating.",
           "positive_traits": ["Perceptive", "Disciplined", "Cultivated"],
           "challenges": ["Fragile if exposed", "Overly private"],
           "compatibility": "Fuelled by Yin Wood (乙), tempered by Yang Metal (庚).",
           "career_paths": "Research, craftsmanship, counseling.",
           "life_philosophy": "Small light, deep insight."},
    "戊": {"name": "Yang Earth", "element": "Solid Mountain",
           "description": "Steady, dependable, and enduring — a foundation for others.",
           "positive_traits": ["Reliable", "Practical", "Judicious"],
           "challenges": ["Conservative", "Resistant to change"],
           "compatibility": "Nourished by Yin Fire (丁) and tempered by Yin Water (癸).",
           "career_paths": "Finance, management, stewardship.",
           "life_philosophy": "Create stability where others can grow."},
    "己": {"name": "Yin Earth", "element": "Nurturing Soil",
           "description": "Generous, patient, and quietly strong — nourishes growth.",
           "positive_traits": ["Supportive", "Kind", "Patient"],
           "challenges": ["Overgiving", "Difficulty saying no"],
           "compatibility": "Flourishes with Yang Fire (丙) and Yang Water (壬).",
           "career_paths": "Teaching, healing, community work.",
           "life_philosophy": "Care that sustains."},
    "庚": {"name": "Yang Metal", "element": "Refined Steel",
           "description": "Sharp, just, and decisive — a force of clarity and action.",
           "positive_traits": ["Disciplined", "Principled", "Courageous"],
           "challenges": ["Harshness", "Rigidity"],
           "compatibility": "Refined by Yin Wood (乙) and tempered by Yin Fire (丁).",
           "career_paths": "Law, engineering, surgical or crisis roles.",
           "life_philosophy": "Strength used wisely becomes honour."},
    "辛": {"name": "Yin Metal", "element": "Precious Jewel",
           "description": "Elegant, precise, and discerning — value revealed through refinement.",
           "positive_traits": ["Meticulous", "Tasteful", "Measured"],
           "challenges": ["Perfectionism", "Indecision"],
           "compatibility": "Showcased by Yang Wood (甲) and warmed by Yang Fire (丙).",
           "career_paths": "Design, luxury crafts, consultancy.",
           "life_philosophy": "Refinement reveals worth."},
    "壬": {"name": "Yang Water", "element": "Flowing River",
           "description": "Adaptable, wide-ranging, and resourceful — a connector in motion.",
           "positive_traits": ["Resourceful", "Communicative", "Curious"],
           "challenges": ["Inconsistency", "Elusiveness"],
           "compatibility": "Guided by Yang Earth (戊) and focused by Yang Metal (庚).",
           "career_paths": "Transport, communications, exploration.",
           "life_philosophy": "Flow opens possibilities."},
    "癸": {"name": "Yin Water", "element": "Gentle Rain",
           "description": "Quietly receptive, intuitive and healing in small, steady ways.",
           "positive_traits": ["Empathic", "Intuitive", "Adaptable"],
           "challenges": ["Overly sensitive", "Withdrawn"],
           "compatibility": "Supports and is supported by Yang Fire (丙) and Yin Earth (己).",
           "career_paths": "Therapy, spiritual guidance, research.",
           "life_philosophy": "Soft persistence brings depth."}
}

# ----------------------
# Solar Time Calculation Functions
# ----------------------
def day_of_year(year, month, day):
    date = datetime.date(year, month, day)
    return date.timetuple().tm_yday

def equation_of_time(day_of_year):
    B = 2 * math.pi * (day_of_year - 81) / 364
    eot = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)
    return eot

def longitude_correction(longitude, timezone_offset):
    tz_meridian = timezone_offset * 15
    correction_minutes = (longitude - tz_meridian) / 15 * 60
    return correction_minutes

def civil_to_apparent_solar(dt_civil, longitude, timezone_offset):
    doy = day_of_year(dt_civil.year, dt_civil.month, dt_civil.day)
    eot = equation_of_time(doy)
    long_corr = longitude_correction(longitude, timezone_offset)
    total_correction = long_corr + eot
    dt_solar = dt_civil + datetime.timedelta(minutes=total_correction)
    return dt_solar, long_corr, eot

def validate_input(year, month, day, hour, minute, longitude):
    current_year = datetime.datetime.now().year
    if not (1900 <= year <= current_year):
        return f"Year must be between 1900 and {current_year}"
    if not (1 <= month <= 12):
        return "Month must be between 1 and 12"
    try:
        max_day = calendar.monthrange(year, month)[1]
        if not (1 <= day <= max_day):
            return f"Day must be between 1 and {max_day}"
    except:
        return "Invalid month/year combination"
    if not (0 <= hour <= 23):
        return "Hour must be between 0 and 23"
    if not (0 <= minute <= 59):
        return "Minute must be between 0 and 59"
    if not (-180 <= longitude <= 180):
        return "Longitude must be between -180 and 180 degrees"
    return None

# Astronomical helpers
def gregorian_to_julian_date(year, month, day, hour=0, minute=0, second=0):
    day_fraction = (hour + minute/60.0 + second/3600.0) / 24.0
    Y, M, D = year, month, day + day_fraction
    if M <= 2:
        Y -= 1
        M += 12
    A = Y // 100
    B = 2 - A + (A // 4)
    jd = math.floor(365.25 * (Y + 4716)) + math.floor(30.6001 * (M + 1)) + D + B - 1524.5
    return jd

def julian_day_number_at_noon(jd):
    return int(math.floor(jd + 0.5))

# Sexagenary cycle
HEAVENLY_STEMS = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
EARTHLY_BRANCHES = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

def calculate_day_master_from_solar(dt_solar):
    jd = gregorian_to_julian_date(dt_solar.year, dt_solar.month, dt_solar.day,
                                  dt_solar.hour, dt_solar.minute, dt_solar.second)
    jd_noon = julian_day_number_at_noon(jd)
    stem_idx = ((jd_noon - 1) % 10)
    branch_idx = ((jd_noon + 1) % 12)
    return HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx], jd, jd_noon

def create_four_pillars_from_solar(dt_solar):
    year_num = dt_solar.year
    sexagenary_year_index = (year_num - 3) % 60
    year_stem = HEAVENLY_STEMS[sexagenary_year_index % 10]
    year_branch = EARTHLY_BRANCHES[sexagenary_year_index % 12]
    month_branch = EARTHLY_BRANCHES[(dt_solar.month - 1) % 12]
    month_stem_index = (HEAVENLY_STEMS.index(year_stem) + 2 + (dt_solar.month - 1)) % 10
    month_stem = HEAVENLY_STEMS[month_stem_index]
    day_stem, day_branch, jd, jd_noon = calculate_day_master_from_solar(dt_solar)
    hour_slot = (dt_solar.hour + 1) // 2
    hour_branch = EARTHLY_BRANCHES[hour_slot % 12]
    hour_stem = HEAVENLY_STEMS[(HEAVENLY_STEMS.index(day_stem) + hour_slot) % 10]
    return {
        "year": f"{year_stem}{year_branch}",
        "month": f"{month_stem}{month_branch}",
        "day": f"{day_stem}{day_branch}",
        "hour": f"{hour_stem}{hour_branch}",
        "day_master": day_stem,
        "jd": jd,
        "jd_noon": jd_noon
    }

def parse_gmt_offset(tz_str):
    try:
        if tz_str.startswith("GMT"):
            offset_str = tz_str[3:]
            if offset_str:
                return float(offset_str)
            else:
                return 0
    except:
        pass
    return 0

# ----------------------
# UI
# ----------------------
st.title("Day Master Calculator")
st.caption("A quiet voice in the scrollstorm — discover your elemental nature through the ancient wisdom of BaZi")

# Sidebar form
with st.sidebar:
    st.header("Birth Information")
    with st.form("birth_form"):
        current_year = datetime.datetime.now().year
        birth_year = st.number_input("Birth Year", min_value=1900, max_value=current_year, value=1990)
        birth_month = st.number_input("Birth Month", min_value=1, max_value=12, value=1)
        birth_day = st.number_input("Birth Day", min_value=1, max_value=31, value=1)
        col1, col2 = st.columns(2)
        with col1:
            birth_hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=12)
        with col2:
            birth_minute = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=0)

        timezone_options = [f"GMT{'+' if i >= 0 else ''}{i}" for i in range(-12, 13)]
        default_tz_index = timezone_options.index("GMT+8")
        selected_timezone = st.selectbox("Time Zone", timezone_options, index=default_tz_index)

        # Longitude option directly below timezone
        enable_longitude = st.checkbox("Enable precise longitude (for best accuracy)")
        longitude = 0.0
        if enable_longitude:
            longitude = st.number_input(
                "Longitude (degrees)", min_value=-180.0, max_value=180.0, value=0.0,
                help="Enter decimal degrees. East = positive, West = negative. (e.g., Hong Kong = 114.1694, London = -0.1276)"
            )

        submit_button = st.form_submit_button("Calculate Day Master")

    st.markdown("---")
    st.markdown("[← Back to Whispers of YI](https://whispersofyi.github.io/)")

# Main content
if submit_button:
    error_message = validate_input(birth_year, birth_month, birth_day, birth_hour, birth_minute, longitude)
    if error_message:
        st.error(error_message)
    else:
        try:
            civil_dt = datetime.datetime(birth_year, birth_month, birth_day, birth_hour, birth_minute, 0)
            tz_offset = parse_gmt_offset(selected_timezone)
            solar_dt, long_corr, eot = civil_to_apparent_solar(civil_dt, longitude, tz_offset)
            pillars = create_four_pillars_from_solar(solar_dt)
            day_master_key = pillars["day_master"]
            day_master_info = DAY_MASTER_DATA.get(day_master_key)

            st.success("Day Master calculated successfully")

            # Pillars
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown('<div class="pillar-char">' + pillars['year'] + '</div>', unsafe_allow_html=True)
            c1.markdown('<div class="pillar-caption">Year Pillar<br/>Ancestry & Foundation</div>', unsafe_allow_html=True)
            c2.markdown('<div class="pillar-char">' + pillars['month'] + '</div>', unsafe_allow_html=True)
            c2.markdown('<div class="pillar-caption">Month Pillar<br/>Career & Relationships</div>', unsafe_allow_html=True)
            c3.markdown('<div class="pillar-char">' + pillars['day'] + '</div>', unsafe_allow_html=True)
            c3.markdown('<div class="pillar-caption">Day Pillar<br/>Self & Spouse</div>', unsafe_allow_html=True)
            c4.markdown('<div class="pillar-char">' + pillars['hour'] + '</div>', unsafe_allow_html=True)
            c4.markdown('<div class="pillar-caption">Hour Pillar<br/>Children & Legacy</div>', unsafe_allow_html=True)

            st.markdown("---")

            if day_master_info:
                st.header(f"You are a {day_master_info['name']} — {day_master_key} ({day_master_info['element']})")
                st.write(day_master_info["description"])

                st.subheader("Natural Strengths & Positive Traits")
                for t in day_master_info["positive_traits"]:
                    st.markdown(f"- {t}")

                st.subheader("Growth Areas & Potential Challenges")
                for t in day_master_info["challenges"]:
                    st.markdown(f"- {t}")

                st.subheader("Elemental Harmony & Compatibility")
                st.write(day_master_info["compatibility"])

                st.subheader("Career Paths & Life Direction")
                st.write(day_master_info["career_paths"])

                st.subheader("Life Philosophy & Core Values")
                st.write(day_master_info["life_philosophy"])
            else:
                st.error("Day Master data unavailable.")

            # Technical section
            with st.expander("Birth Details & Technical Information"):
                st.write(f"**Civil Time (Clock Time):** {civil_dt.strftime('%B %d, %Y at %H:%M')} ({selected_timezone})")
                st.write(f"**Apparent Solar Time:** {solar_dt.strftime('%B %d, %Y at %H:%M:%S')}")
                st.write("")
                st.write("**Solar Time Corrections Applied:**")
                st.write(f"- Longitude correction: {long_corr:+.2f} minutes")
                st.write(f"- Equation of Time: {eot:+.2f} minutes")
                st.write(f"- Total correction: {long_corr + eot:+.2f} minutes")
                st.write("")
                st.write("**Four Pillars (based on solar time):**")
                st.write(f"- Year: {pillars['year']}")
                st.write(f"- Month: {pillars['month']}")
                st.write(f"- Day: {pillars['day']}")
                st.write(f"- Hour: {pillars['hour']}")
                st.markdown("---")
                st.info("This calculator uses longitude correction and the Equation of Time to ensure precise Day Master calculations.")
                st.caption("This tool does not log or store any personal information.")

        except Exception as e:
            st.error(f"An error occurred during calculation: {e}")
else:
    st.markdown("## How to use")
    st.write("Enter your exact birth date, time, and timezone in the sidebar. For best accuracy, enable longitude and enter it manually.")
    st.write("Then click 'Calculate Day Master'.")

    st.markdown("## Solar Time Accuracy")
    st.write("This calculator uses longitude correction and the Equation of Time to ensure precise Day Master calculations. "
             "Unlike basic calculators that use clock time only, this method provides significantly more accurate results.")
    st.caption("&copy; 2025 Whispers of YI — Code under MIT, Guides under CC BY-NC-ND 4.0")
