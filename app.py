# app.py
import streamlit as st
import datetime
import calendar
import math

# ---- Page configuration ----
st.set_page_config(
    page_title="Day Master Calculator - Whispers of YI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- Minimal, safe font + color override (system sans-serif) ----
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif !important;
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    /* Pillar Chinese characters (large, horizontal) */
    .big-chinese {
        font-size: 48px;
        font-weight: 700;
        line-height: 1;
        display: inline-block;
        letter-spacing: 2px;
    }
    .pillar-title {
        text-align: center;
        margin-bottom: 0.25rem;
    }
    .pillar-caption {
        text-align: center;
        color: #555;
    }
    .center-block {
        text-align: center;
    }
    .correction-box {
        text-align: center;
        padding: 0.25rem 0.5rem;
    }
    .correction-label { font-size: 14px; color: #444; }
    .correction-value { font-size: 20px; font-weight: 600; }
    .privacy-note { font-size: 12px; color: #666; margin-top: 1rem; }
    @media (max-width: 700px) {
        .big-chinese { font-size: 36px; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- DAY_MASTER_DATA (concise entries for stability) ----
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

# ---- Solar time helpers ----
def day_of_year(year, month, day):
    return datetime.date(year, month, day).timetuple().tm_yday

def equation_of_time(doy):
    # NOAA-ish formula (minutes)
    B = 2 * math.pi * (doy - 81) / 364.0
    return 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)

def longitude_correction(longitude_deg, timezone_offset_hours):
    # timezone meridian at 15° * offset
    tz_meridian = timezone_offset_hours * 15.0
    return (longitude_deg - tz_meridian) / 15.0 * 60.0  # minutes

def civil_to_apparent_solar(dt_civil, longitude_deg, timezone_offset_hours):
    doy = day_of_year(dt_civil.year, dt_civil.month, dt_civil.day)
    eot = equation_of_time(doy)
    long_corr = longitude_correction(longitude_deg, timezone_offset_hours)
    total = long_corr + eot
    dt_solar = dt_civil + datetime.timedelta(minutes=total)
    return dt_solar, long_corr, eot

# ---- Gregorian -> Julian Date (accurate) ----
def gregorian_to_julian_date(year, month, day, hour=0, minute=0, second=0):
    day_fraction = (hour + minute / 60.0 + second / 3600.0) / 24.0
    Y = year
    M = month
    D = day + day_fraction
    if M <= 2:
        Y -= 1
        M += 12
    A = Y // 100
    B = 2 - A + (A // 4)
    jd = math.floor(365.25 * (Y + 4716)) + math.floor(30.6001 * (M + 1)) + D + B - 1524.5
    return jd

def julian_day_number_at_noon(jd):
    return int(math.floor(jd + 0.5))

# ---- Sexagenary calculations ----
HEAVENLY_STEMS = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
EARTHLY_BRANCHES = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

def calculate_day_master_from_solar(dt_solar):
    jd = gregorian_to_julian_date(dt_solar.year, dt_solar.month, dt_solar.day, dt_solar.hour, dt_solar.minute, dt_solar.second)
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

# ---- Utilities: timezone list (half-hour steps) ----
def generate_timezone_options():
    opts = []
    step = 0.5
    start = -12.0
    end = 14.0
    cur = start
    while cur <= end + 1e-9:
        sign = "+" if cur >= 0 else "-"
        abs_cur = abs(cur)
        hours = int(abs_cur)
        minutes = int(round((abs_cur - hours) * 60))
        if minutes == 0:
            label = f"GMT{sign}{hours}"
        else:
            label = f"GMT{sign}{hours}:{minutes:02d}"
        opts.append(label)
        cur = round(cur + step, 3)
    return opts

def parse_gmt_offset(tz_str):
    # Accepts "GMT+8", "GMT-4:30", "GMT+5:30"
    if not tz_str.startswith("GMT"):
        return 0.0
    off = tz_str[3:]
    if off == "" or off == "+" or off == "+0" or off == "0":
        return 0.0
    sign = 1
    if off.startswith("-"):
        sign = -1
        off = off[1:]
    elif off.startswith("+"):
        off = off[1:]
    if ":" in off:
        h, m = off.split(":")
        return sign * (int(h) + int(m) / 60.0)
    else:
        return sign * float(off)

# ---- Input validation ----
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
        return "Longitude must be between -180 and 180"
    return None

# ---- UI ----
st.title("Day Master Calculator")
st.caption("A quiet voice in the scrollstorm — discover your elemental nature through the ancient wisdom of BaZi")

# Solar time short summary (consolidated)
st.subheader("Solar Time Accuracy")
st.write("This calculator uses **longitude correction** and the **Equation of Time** to convert clock time to apparent solar time — improving Day Master and hour-pillar accuracy.")

timezone_options = generate_timezone_options()
default_tz = "GMT+8" if "GMT+8" in timezone_options else timezone_options[len(timezone_options)//2]

# Sidebar: birth form + immediate longitude controls (longitude outside form so it shows/hides instantly)
with st.sidebar:
    st.header("Birth Information")

    # birth inputs inside a form for stable submit behaviour
    with st.form("birth_form"):
        current_year = datetime.datetime.now().year
        birth_year = st.number_input("Birth Year", min_value=1900, max_value=current_year, value=1990, step=1, key="birth_year")
        birth_month = st.number_input("Birth Month", min_value=1, max_value=12, value=1, step=1, key="birth_month")
        birth_day = st.number_input("Birth Day", min_value=1, max_value=31, value=1, step=1, key="birth_day")
        col1, col2 = st.columns(2)
        with col1:
            birth_hour = st.number_input("Hour (0–23)", min_value=0, max_value=23, value=12, key="birth_hour")
        with col2:
            birth_minute = st.number_input("Minute (0–59)", min_value=0, max_value=59, value=0, key="birth_minute")

        selected_timezone = st.selectbox("Time Zone (GMT offset)", timezone_options, index=timezone_options.index(default_tz), key="selected_timezone")

        submit_button = st.form_submit_button("Calculate Day Master")

    st.markdown("---")
    st.write("For best accuracy you may provide precise longitude (optional). Example inputs: `Hong Kong = 114.1694`, `London = -0.1276`.")
    precise_longitude = st.checkbox("Enable precise longitude (optional — shows immediately)", key="precise_longitude")
    if precise_longitude:
        longitude = st.number_input("Longitude (degrees)", min_value=-180.0, max_value=180.0, value=114.1694, format="%.6f",
                                    help="Positive = East; Negative = West. Example: 114.1694 for Hong Kong.")
    else:
        longitude = None

    st.markdown("---")
    st.markdown("[← Back to Whispers of YI](https://whispersofyi.github.io/)")

# ---- Calculation & Results ----
if submit_button:
    # Determine timezone offset float (hours)
    tz_offset_hours = parse_gmt_offset(selected_timezone)

    # If no precise longitude supplied, approximate by timezone meridian
    if longitude is None:
        longitude_used = tz_offset_hours * 15.0
    else:
        longitude_used = longitude

    # Validate inputs (use longitude_used for validation)
    err = validate_input(birth_year, birth_month, birth_day, birth_hour, birth_minute, longitude_used)
    if err:
        st.error(err)
    else:
        try:
            civil_dt = datetime.datetime(birth_year, birth_month, birth_day, birth_hour, birth_minute, 0)
            solar_dt, long_corr, eot = civil_to_apparent_solar(civil_dt, longitude_used, tz_offset_hours)

            pillars = create_four_pillars_from_solar(solar_dt)
            day_master = pillars["day_master"]
            day_master_info = DAY_MASTER_DATA.get(day_master)

            # Success message (concise)
            st.success("Day Master calculated successfully")

            # Corrections summary (centered)
            st.markdown("<div style='display:flex; justify-content:center; gap:1rem; margin-top:1rem;'>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='correction-box'><div class='correction-label'>Longitude Correction</div>"
                f"<div class='correction-value'>{long_corr:+.1f} min</div></div>",
                unsafe_allow_html=True)
            st.markdown(
                f"<div class='correction-box'><div class='correction-label'>Equation of Time</div>"
                f"<div class='correction-value'>{eot:+.1f} min</div></div>",
                unsafe_allow_html=True)
            st.markdown(
                f"<div class='correction-box'><div class='correction-label'>Total Correction</div>"
                f"<div class='correction-value'>{(long_corr+eot):+.1f} min</div></div>",
                unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Warning / info about magnitude
            total_corr = abs(long_corr + eot)
            if total_corr > 30:
                st.warning("Large time correction applied — this may affect your hour pillar or even the day pillar.")
            elif total_corr > 15:
                st.info("Moderate time correction applied — results are more accurate for BaZi analysis.")

            st.markdown("---")

            # Pillars block
            c1, c2, c3, c4 = st.columns(4)
            pillars_list = [("Year Pillar", pillars["year"], "Ancestry & Foundation"),
                            ("Month Pillar", pillars["month"], "Career & Relationships"),
                            ("Day Pillar", pillars["day"], "Self & Spouse"),
                            ("Hour Pillar", pillars["hour"], "Children & Legacy")]

            for col, (title, chinese, caption) in zip([c1, c2, c3, c4], pillars_list):
                with col:
                    st.markdown(f"<div class='pillar-title'><strong>{title}</strong></div>", unsafe_allow_html=True)
                    # Large Chinese (horizontal)
                    st.markdown(f"<div class='center-block'><span class='big-chinese'>{chinese}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='pillar-caption'>{caption}</div>", unsafe_allow_html=True)

            st.markdown("---")

            # Single Day Master line (prominent, once)
            if day_master_info:
                st.header(f"You are a {day_master_info['name']} — {day_master} ({day_master_info['element']}) Day Master")
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
                st.error("Day Master data unavailable for computed stem.")

            # Technical expander with full details (Apparent Solar time, corrections, JD)
            with st.expander("Birth Details & Technical Information"):
                st.write(f"**Civil Time (Clock Time):** {civil_dt.strftime('%B %d, %Y at %H:%M')} ({selected_timezone})")
                st.write(f"**Longitude used for calculation:** {longitude_used:+.6f}°")
                st.write(f"**Apparent Solar Time (used for pillars):** {solar_dt.strftime('%B %d, %Y at %H:%M:%S')}")
                st.markdown("")
                st.write("**Solar Time Corrections Applied:**")
                st.write(f"- Longitude correction: {long_corr:+.2f} minutes")
                st.write(f"- Equation of Time: {eot:+.2f} minutes")
                st.write(f"- Total correction: {long_corr + eot:+.2f} minutes")
                st.markdown("")
                st.write("**Four Pillars (based on apparent solar time):**")
                st.write(f"- Year: {pillars['year']}")
                st.write(f"- Month: {pillars['month']}")
                st.write(f"- Day: {pillars['day']}")
                st.write(f"- Hour: {pillars['hour']}")
                st.markdown("")
                st.write("**Julian Date info (used for day-stem):**")
                jd = gregorian_to_julian_date(solar_dt.year, solar_dt.month, solar_dt.day, solar_dt.hour, solar_dt.minute, solar_dt.second)
                jd_noon = julian_day_number_at_noon(jd)
                st.write(f"- JD (fractional): {jd:.6f}")
                st.write(f"- JD noon integer: {jd_noon}")
                st.markdown("---")
                st.info("For ultimate precision you may also consider solar-term boundaries (e.g., 立春) and local apparent time conventions; this calculator addresses the largest sources of clock-to-solar discrepancy.")
                st.markdown("")
                st.info("This calculator does not store or log any personal information.")

            # bottom small privacy & copyright
            st.markdown("---")
            st.markdown("<div class='privacy-note'>This calculator does not store or log personal birth data. Use it locally or on trusted devices.</div>", unsafe_allow_html=True)
            st.caption("© 2025 Whispers of YI — Code under MIT, Guides under CC BY-NC-ND 4.0")

        except Exception as e:
            st.error(f"An error occurred during calculation: {e}")
            st.write("Please check your inputs and try again.")

else:
    # Home / instructions view
    st.markdown("## How to use")
    st.write("Enter your birth date and exact time (including minutes). Select the GMT offset for your birth location. For best accuracy you may enable precise longitude and input the longitude in degrees (optional). Then click **Calculate Day Master**.")
    st.markdown("")
    st.markdown("**What you'll get:**")
    st.markdown("- Four Pillars (based on apparent solar time)\n- Day Master (Heavenly Stem of the day)\n- Solar-time corrections used and Julian-date diagnostics")
    st.markdown("")
    st.info("A concise summary of the solar-time corrections is shown with results; full technical details are kept in the 'Birth Details & Technical Information' expander.")
    st.caption("© 2025 Whispers of YI — Code under MIT, Guides under CC BY-NC-ND 4.0")
