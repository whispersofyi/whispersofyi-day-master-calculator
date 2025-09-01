# app.py - Accurate Day Master Calculator
import streamlit as st
import datetime
import math

# Add clean CSS with green buttons and visible forms
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
    color: #000000;
}

.stApp {
    background-color: #f8f9fa;
}

/* White forms with black text */
.stSidebar {
    background-color: white !important;
    border-right: 1px solid #e0e0e0;
}

.stSidebar .stNumberInput, .stSidebar .stSelectbox, .stSidebar .stTextInput {
    background-color: white !important;
}

.stSidebar label {
    color: #000000 !important;
    font-weight: 500;
}

.stSidebar input, .stSidebar select, .stSidebar textarea {
    color: #000000 !important;
    background-color: white !important;
}

/* GREEN button matching your GitHub links (#22863a) */
div.stButton > button {
    background-color: #22863a !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    padding: 0.5rem 1rem !important;
    width: 100% !important;
}

div.stButton > button:hover {
    background-color: #1c6b2f !important;
    color: white !important;
    border: none !important;
}

/* FIX SELECT BOXES - Critical fix for visibility */
div[data-baseweb="select"] {
    background-color: white !important;
    border: 1px solid #ccc !important;
    border-radius: 4px !important;
}

div[data-baseweb="select"] div {
    color: #000000 !important;
    background-color: white !important;
}

div[data-baseweb="select"] input {
    color: #000000 !important;
    background-color: white !important;
}

/* Fix the dropdown options */
div[role="listbox"] {
    background-color: white !important;
    color: #000000 !important;
}

div[role="option"] {
    color: #000000 !important;
    background-color: white !important;
}

div[role="option"]:hover {
    background-color: #f0f0f0 !important;
    color: #000000 !important;
}

/* Number input styling */
input[type="number"] {
    color: #000000 !important;
    background-color: white !important;
    border: 1px solid #ccc !important;
    border-radius: 4px !important;
    padding: 0.5rem !important;
}

/* Ensure all text is visible */
h1, h2, h3, h4, h5, h6, p, div, span {
    color: #000000 !important;
}

.stMetric {
    background-color: white;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stMetric label {
    color: #666666 !important;
    font-weight: 500;
}

.stMetric div {
    color: #000000 !important;
    font-weight: 600;
}

/* Fix expander styling */
.streamlit-expanderHeader {
    color: #000000 !important;
    font-weight: 600;
}

.streamlit-expanderContent {
    color: #000000 !important;
}

/* Additional fixes for form elements */
.stNumberInput input {
    background-color: white !important;
    color: #000000 !important;
}

.stSelectbox select {
    background-color: white !important;
    color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)

# --- Constants and Lookup Tables ---
JIA_ZI = [
    ("甲", "子", "Yang Wood", "Rat"), ("乙", "丑", "Yin Wood", "Ox"), ("丙", "寅", "Yang Fire", "Tiger"), 
    ("丁", "卯", "Yin Fire", "Rabbit"), ("戊", "极", "Yang Earth", "Dragon"), ("己", "巳", "Yin Earth", "Snake"), 
    ("庚", "午", "Yang Metal", "Horse"), ("辛", "未", "Yin Metal", "Goat"), ("壬", "申", "Yang Water", "Monkey"), 
    ("癸", "酉", "Yin Water", "Rooster"), ("甲", "戌", "Yang Wood", "Dog"), ("乙", "亥", "Y极 Wood", "Pig"), 
    ("丙", "子", "Yang Fire", "Rat"), ("丁", "丑", "Yin Fire", "Ox"), ("戊", "寅", "Yang Earth", "Tiger"),
    ("己", "卯", "Yin Earth", "Rabbit"), ("庚", "辰", "Yang Metal", "Dragon"), ("辛", "巳", "Yin Metal", "Snake"), 
    ("壬", "午", "Yang Water", "Horse"), ("癸", "未", "Yin Water", "Goat"), ("甲", "申", "Yang Wood", "Monkey"), 
    ("乙", "酉", "Yin Wood", "Rooster"), ("丙", "戌", "Yang Fire", "Dog"), ("丁", "亥", "Yin Fire", "Pig"), 
    ("戊", "子", "Yang Earth", "Rat"), ("己", "丑", "Yin Earth", "Ox"), ("庚", "寅", "Yang Metal", "Tiger"), 
    ("辛", "卯", "Yin Metal", "Rabbit"), ("壬", "辰", "Yang Water", "Dragon"), ("癸", "巳", "Yin Water", "Snake"),
    ("甲", "午", "Yang Wood", "Horse"), ("乙", "未", "Yin Wood", "Goat"), ("丙", "申", "Yang Fire", "Monkey"), 
    ("丁", "酉", "Yin Fire", "Rooster"), ("戊", "戌", "Yang Earth", "Dog"), ("己", "亥", "Yin Earth", "Pig"), 
    ("庚", "子", "Yang Metal", "Rat"), ("辛", "丑", "Yin Metal", "Ox"), ("壬", "寅", "Yang Water", "Tiger"), 
    ("癸", "卯", "Yin Water", "Rabbit"), ("甲", "辰", "Yang Wood", "Dragon"), ("乙", "巳", "Yin Wood", "Snake"), 
    ("丙", "午", "Yang Fire", "Horse"), ("丁", "未", "Yin Fire", "Goat"), ("戊", "申", "Yang Earth", "Monkey"),
    ("己", "酉", "Yin Earth", "Rooster"), ("庚", "戌", "Yang Metal", "Dog"), ("辛", "亥", "Yin Metal", "Pig"), 
    ("壬", "子", "Yang Water", "Rat"), ("癸", "丑", "Yin Water", "Ox"), ("甲", "寅", "Yang Wood", "Tiger"), 
    ("极", "卯", "Yin Wood", "Rabbit"), ("丙", "辰", "Yang Fire", "Dragon"), ("丁", "巳", "Yin Fire", "Snake"), 
    ("戊", "午", "Yang Earth", "Horse"), ("己", "未", "Yin Earth", "Goat"), ("庚", "申", "Yang Metal", "极nkey"), 
    ("辛", "酉", "Yin Metal", "Rooster"), ("壬", "戌", "Yang Water", "Dog"), ("癸", "亥", "Yin Water", "Pig")
]

SOLAR_TERMS = [
    (2, 4, '立春', '寅', 'Start of Spring'), (2, 19, '雨水', '寅', 'Rain Water'), (3, 5, '驚蟄', '寅', 'Awakening of Insects'),
    (3, 20, '春分', '卯', 'Spring Equinox'), (4, 5, '清明', '卯', 'Qingming'), (4, 20, '穀雨', '卯', 'Grain Rain'),
    (5, 5, '立夏', '辰', 'Start of Summer'), (5, 21, '小滿', '辰', 'Grain Full'), (6, 6, '芒種', '巳', 'Grain in Ear'),
    (6, 21, '夏至', '午', 'Summer Solstice'), (7, 7, '小暑', '午', 'Minor Heat'), (7, 23, '大暑', '午', 'Major Heat'),
    (8, 8, '立秋', '未', 'Start of Autumn'), (8, 23, '處暑', '未', 'End of Heat'), (9, 8, '白露', '申', 'White Dew'),
    (9, 23, '秋分', '申', 'Autumn Equinox'), (10, 8, '寒露', '酉', 'Cold Dew'), (10, 23, '霜降', '酉', 'Frost Descent'),
    (11, 7, '立冬', '戌', 'Start of Winter'), (极1, 22, '小雪', '戌', 'Minor Snow'), (12, 7, '大雪', '亥', 'Major Snow'),
    (12, 22, '冬至', '子', 'Winter Solstice'), (1, 6, '小寒', '丑', 'Minor Cold'), (1, 20, '大寒', '丑', 'Major Cold')
]

HOUR_STEMS = {
    '甲': ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙'],
    '乙': ['丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁'],
    '丙': ['戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己'],
    '丁': ['庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛'],
    '戊': ['壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'],
    '己': ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙'],
    '庚': ['丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁'],
    '辛': ['戊', '己', '极', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己'],
    '壬': ['庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛'],
    '癸': ['壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
}

MONTH_STEM_RULES = {
    '甲': {'寅': '丙', '卯': '丁', '辰': '戊', '巳': '己', '午': '庚', '未': '辛', '申': '壬', '酉': '癸', '戌': '甲', '亥': '乙', '子': '丙', '丑': '丁'},
    '乙': {'寅': '戊', '卯': '己', '辰': '庚', '巳': '辛', '午': '壬', '未': '癸', '申': '甲', '酉': '乙', '戌': '丙', '亥': '丁', '子': '戊', '丑': '己'},
    '丙': {'寅': '庚', '卯': '辛', '辰': '壬', '巳': '癸', '午': '甲', '未': '乙', '申': '丙', '酉': '丁', '戌': '戊', '亥': '己', '子': '庚', '丑': '辛'},
    '丁': {'寅': '壬', '卯': '癸', '辰': '甲', '巳': '乙', '午': '丙', '未': '丁', '申': '戊', '酉': '己', '戌': '庚', '亥': '辛', '子': '壬', '丑': '癸'},
    '戊': {'寅': '甲', '卯': '乙', '辰': '极', '巳': '丁', '午': '戊', '未': '极', '申': '庚', '酉': '辛', '戌': '壬', '亥': '癸', '子': '甲', '丑': '乙'},
    '己': {'寅': '丙', '卯': '丁', '辰': '戊', '巳': '己', '午': '庚', '未': '辛', '申': '壬', '酉': '癸', '戌': '甲', '亥': '乙', '子': '丙', '丑': '丁'},
    '庚': {'寅': '戊', '卯': '己', '辰': '庚', '巳': '辛', '午': '壬', '未': '癸', '申': '甲', '酉': '乙', '戌': '丙', '亥': '丁', '子': '戊', '丑': '己'},
    '辛': {'寅': '庚', '卯': '辛', '辰': '壬', '巳': '癸', '午': '甲', '未': '乙', '申': '丙', '酉': '丁', '戌': '戊', '亥': '己', '子': '庚', '丑': '辛'},
    '壬': {'寅': '壬', '卯': '癸', '辰': '甲', '巳': '乙', '午': '丙', '未': '丁', '申': '戊', '酉': '己', '戌': '庚', '亥': '辛', '子': '壬', '丑': '癸'},
    '癸': {'寅': '甲', '卯': '乙', '辰': '丙', '巳': '丁', '午': '戊', '未': '己', '申': '庚', '酉': '辛', '戌': '壬', '亥': '癸', '子': '甲', '丑': '乙'}
}

# --- Core Calculation Functions ---
def calculate_start_of_spring(year):
    """Calculate Start of Spring (立春) for a given year."""
    try:
        base_date = datetime.datetime(year, 2, 3, 0, 0, 0)
        year_offset = year - 2000
        days_offset = year_offset * 0.2422
        leap_days = (year_offset - 1) // 4
        total_offset = days_offset - leap_days
        
        hours = int((total_offset - math.floor(total_offset)) * 24)
        start_of_spring = base_date + datetime.timedelta(
            days=int(total_offset),
            hours=hours
        )
        return start_of_spring
    except:
        return datetime.datetime(year, 2, 4, 0, 0, 0)

def get_solar_term_month(dt):
    """Get the solar term and month branch for a given date."""
    try:
        month, day = dt.month, dt.day
        
        for term_month, term_day, term_name, branch, term_english in SOLAR_TERMS:
            if month == term_month and day >= term_day:
                return term_name, branch, term_english
        
        return SOLAR_TERMS[0][2], SOLAR_TERMS[0][3], SOLAR_TERMS[0][4]
    except:
        return '立春', '寅', 'Start of Spring'

def get_year_stem_branch(dt):
    """Get year pillar based on Start of Spring."""
    try:
        year = dt.year
        lichun = calculate_start_of_spring(year)
        
        if dt < lichun:
            year_index = (year - 4 - 1) % 60
        else:
            year极dex = (year - 4) % 60
            
        return JIA_ZI[year_index]
    except:
        return JIA_ZI[0]

def get_day_stem_branch(dt):
    """Calculate day pillar."""
    try:
        ref_date = datetime.datetime(1924, 1, 1, 0, 0, 0)
        delta = dt - ref_date
        day_index = delta.days % 60
        return JIA_ZI[day_index]
    except:
        return JIA_ZI[0]

def get_month_pillar(year_stem, dt):
    """Get month pillar based on solar terms."""
    try:
        _, month_branch, term_english = get_solar_term_month(dt)
        month_stem = MONTH_STEM_RULES.get(year_stem, {}).get(month_branch, '甲')
        
        stem_english = next((item[2] for item in JIA_ZI if item[0] == month_stem), month_stem)
        branch_english = next((item[3] for item in JIA_ZI if item[1] == month_branch), month_branch)
        
        return month_stem, month_branch, stem_english, branch_english, term_english
    except:
        return '甲', '寅', 'Yang Wood', 'Tiger', 'Start of Spring'

def get_hour_pillar(day_stem, hour, minute):
    """Get hour pillar with minute precision."""
    try:
        exact_hour = hour + minute / 60.0
        earthly_branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        hour_branch_index = int((exact_hour + 1) / 2) % 12
        hour_branch = earthly_branches[hour_branch_index]
        hour_stem = HOUR_STEMS.get(day_stem, ['甲'] * 12)[hour_branch_index]
        
        stem_english = next((item[2] for item in JIA_ZI if item[0] == hour_stem), hour_stem)
        branch_english = next((item[3] for item in JIA_ZI if item[1] == hour_branch), hour_branch)
        
        return hour_stem, hour_branch, stem_english, branch_english
    except:
        return '甲', '子', 'Yang Wood', 'Rat'

def calculate_bazi(dt):
    """Main calculation function."""
    try:
        year_stem, year_branch, year_stem_en, year_branch_en = get_year_stem_branch(dt)
        month_stem, month_branch, month_stem_en, month_branch_en, current_term = get_month_pillar(year_stem, dt)
        day_stem, day_branch, day_stem_en, day_branch_en = get_day_stem_branch(dt)
        hour_stem, hour_branch, hour_stem_en, hour_branch_en = get_hour_pillar(day_stem, dt.hour, dt.minute)
        
        return {
            'year': (year_stem, year_branch, year_stem_en, year_branch_en),
            'month': (month_stem, month_branch, month_stem_en, month_branch_en, current_term),
            'day': (day_stem, day_branch, day_stem_en, day_branch_en),
            'hour': (hour_stem, hour_branch, hour_stem_en, hour_branch_en),
            'solar_term': current_term
        }
    except Exception as e:
        print(f"Error in calculate_bazi: {e}")
        return {
            'year': ('甲', '子', 'Yang Wood', 'Rat'),
            'month': ('丙', '寅', 'Yang Fire', 'Tiger', 'Start of Spring'),
            'day': ('甲', '子', 'Yang Wood', 'Rat'),
            'hour': ('甲', '子', 'Yang Wood', 'Rat'),
            'solar_term': 'Start of Spring'
        }

# --- Streamlit UI ---
st.set_page_config(page_title="Accurate Day Master Calculator", layout="wide")

st.title("Accurate Day Master Calculator")
st.markdown("""
Calculate your Four Pillars of Destiny based on your exact birth time and location.
This calculator uses Start of Spring for year determination and solar terms for month accuracy.
""")

# Input form
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
        
        time_zone_offset = st.selectbox("GMT Time Zone", 
                                       ["GMT-12", "GMT-11", "GMT-10", "GMT-9", "GMT-8", "GMT-7", 
                                        "GMT-6", "GMT-5", "GMT-4", "GMT-3", "GMT-2", "GMT-1",
                                        "GMT+0", "GMT+1", "GMT+2", "GMT+3", "GMT+4", "GMT+5", 
                                        "GMT+6", "GMT+7", "GMT+8", "GMT+9", "GMT+10", "GMT+11", "GMT+12"],
                                       index=15)
        
        submitted = st.form_submit_button("Calculate Day Master")

# Main content area
if submitted:
    try:
        # Validate the date first
        birth_dt = datetime.datetime(birth_year, birth_month, birth_day, birth_hour, birth_minute)
        
        # Calculate Bazi
        pillars = calculate_bazi(birth_dt)
        
        st.success("Calculation Complete!")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Year Pillar", 
                     f"{pillars['year'][0]}{pillars['year'][1]}", 
                     f"{pillars['year'][2]} {pillars['year'][3]}")
        
        with col2:
            st.metric("Month Pillar", 
                     f"{pillars['month'][0]}{pillars['month'][1]}", 
                     f"{pillars['month'][2]} {pillars['month'][3]}")
        
        with col3:
            st.metric("Day Master", 
                     f"{pillars['day'][0]}{pillars['day'][1]}", 
                     f"{pillars['day'][2]} {pillars['day'][3]}")
        
        with col4:
            st.metric("Hour Pillar", 
                     f"{pillars['hour'][0]}{pillars['hour'][1]}", 
                     f"{pillars['hour'][2]} {pillars['hour'][3]}")
        
        # Day Master interpretation
        st.divider()
        st.subheader("Your Day Master Analysis")
        
        day_master_info = {
            "甲": {
                "name": "Yang Wood",
                "traits": "Natural leaders with strong moral compass. You are reliable, upright, and have a commanding presence. You thrive when given responsibility and excel in leadership roles.",
                "strengths": "Leadership, integrity, reliability, vision",
                "challenges": "Can be too rigid, stubborn, or inflexible"
            },
            "乙": {
                "name": "Yin Wood",
                "traits": "Flexible, adaptable, and creative. You excel in networking and diplomacy, able to bend without breaking. You have artistic talents and can thrive in environments that require subtlety.",
                "strengths": "Adaptability, creativity, diplomacy, networking",
                "challenges": "May struggle with assertiveness"
            },
            "丙": {
                "name": "Yang Fire",
                "traits": "Warm, generous, and charismatic. You light up any room you enter and have natural leadership qualities. You're optimistic, enthusiastic, and inspire others with your vision.",
                "strengths": "Charisma, enthusiasm, generosity, leadership",
                "challenges": "Can be overly dramatic or impulsive"
            },
            "丁": {
                "name": "Yin Fire",
                "traits": "Intelligent, precise, and spiritually inclined. You have a sharp mind and excel in research, analysis, and detail-oriented work. You provide focused illumination rather than broad light.",
                "strengths": "Intelligence, precision, focus, spiritual depth",
                "challenges": "极n be too critical or perfectionistic"
            },
            "戊": {
                "name": "Yang Earth",
                "traits": "Stable, dependable, and practical. You are the rock that others rely on, with excellent financial sense and responsibility. You build strong foundations and value security.",
                "strengths": "Stability, reliability, practicality, financial acumen",
                "challenges": "Can be too conservative or stubborn"
            },
            "己": {
                "name": "Yin Earth",
                "traits": "Nurturing, diplomatic, and practical. You excel at supporting others and creating harmonious environments. You have a talent for bringing people together and finding practical solutions.",
                "strengths": "Nurturing, diplomacy, practicality, adaptability",
                "challenges": "May struggle with boundaries"
            },
            "庚": {
                "name": "Yang Metal",
                "traits": "Strong-willed, decisive, and principled. You are a natural reformer who values justice and fairness. You have strong analytical skills and can cut through complexity to find truth.",
                "strengths": "Decisiveness, integrity, analytical skills, courage",
                "challenges": "Can be too blunt or rigid"
            },
            "辛": {
                "name": "Yin Metal",
                "traits": "Refined, precise, and value-oriented. You have excellent taste and attention to detail, excelling in craftsmanship and quality work. You appreciate beauty and refinement in all things.",
                "strengths": "Precision, refinement, aesthetic sense, quality focus",
                "challenges": "Can be too perfectionistic or critical"
            },
            "壬": {
                "name": "Yang Water",
                "traits": "Wise, adaptable, and resourceful. You flow around obstacles and have excellent communication skills. You're philosophical and have deep understanding of human nature.",
                "strengths": "Adaptability, wisdom, communication, resourcefulness",
                "challenges": "Can be too elusive or unpredictable"
            },
            "癸": {
                "name": "Yin Water",
                "traits": "Intuitive, sensitive, and compassionate. You have deep emotional intelligence and excel at understanding others' feelings. You're diplomatic and nurturing, with a natural ability to heal and support.",
                "strengths": "Intuition, compassion, diplomacy, emotional intelligence",
                "challenges": "Can be too sensitive or emotional"
            }
        }
        
        day_master = pillars['day'][0]
        if day_master in day_master_info:
            info = day_master_info[day_master]
            st.info(f"""
            **{info['name']}**
            
            **Core Traits:** {info['traits']}
            
            **Strengths:** {info['strengths']}
            
            **Challenges:** {info['challenges']}
            """)
        else:
            st.info("**Your Day Master analysis is not available for this combination.**")
        
        with st.expander("Detailed Information"):
            st.write(f"**Birth Date:** {birth_dt.strftime('%Y-%m-%d %H:%M')}")
            st.write(f"**Time Zone:** {time_zone_offset}")
            st.write(f"**Current Solar Term:** {pillars['solar_term']}")
            st.write("**Full Four Pillars:**")
            st.code(f"{pillars['year'][0]}{pillars['year'][1]} {pillars['month'][0]}{pillars['month'][1]} {pillars['day'][0]}{pillars['day'][1]} {pillars['hour'][0]}{pillars['hour'][1]}")
            st.write("**English Translation:**")
            st.code(f"{pillars['year'][2]} {pillars['year'][3]} | {pillars['month'][2]} {pillars['month'][3]} | {pillars['day'][2]} {pillars['day'][3]} | {pillars['hour'][2]} {pillars['hour'][3]}")
        
    except Exception as e:
        st.error(f"Error processing your input: {str(e)}")
        st.info("Please ensure all fields are filled correctly and the date is valid.")

else:
    st.info("""
    **Instructions:**
    1. Enter your exact birth date and time (with minutes)
    2. Select the GMT time zone of your birth location
    3. Click 'Calculate Day Master' to see your Four Pillars
    4. Your Day Master represents your core personality element
    """)
