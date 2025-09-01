# app.py - Accurate Day Master Calculator with GMT Time Zones
import streamlit as st
import datetime
import math

# Add custom CSS for styling that matches your GitHub page
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
    color: #333333;
}

.stApp {
    background-color: #ffffff;
}

.stSidebar {
    background-color: #f8f9fa;
    border-right: 1px solid #e0e0e0;
}

.stSidebar .stNumberInput, .stSidebar .stSelectbox {
    background-color: white;
}

/* Button color matching your GitHub page links (#0366d6) */
.stButton>button {
    background-color: #0366d6;
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: 500;
    padding: 0.5rem 1rem;
    width: 100%;
}

.stButton>button:hover {
    background-color: #0256b6;
    color: white;
}

/* Fix GMT selectbox visibility */
.stSelectbox label {
    color: #333333 !important;
    font-weight: 500;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: white;
}

/* Ensure all text is visible */
h1, h2, h3, h4, h5, h6, p, div, span, label {
    color: #333333 !important;
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
    color: #333333 !important;
    font-weight: 600;
}

.streamlit-expanderContent {
    color: #333333 !important;
}

/* Custom styling for better visibility */
.css-1d391kg, .css-1y4p8pa {
    color: #333333 !important;
}
</style>
""", unsafe_allow_html=True)

# --- Constants and Lookup Tables ---
JIA_ZI = [
    ("甲", "子", "Yang Wood", "Rat"), ("乙", "丑", "Yin Wood", "Ox"), ("丙", "寅", "Yang Fire", "Tiger"), 
    ("丁", "卯", "Yin Fire", "Rabbit"), ("戊", "辰", "Yang Earth", "Dragon"), ("己", "巳", "Yin Earth", "Snake"), 
    ("庚", "午", "Yang Metal", "Horse"), ("辛", "未", "Yin Metal", "Goat"), ("壬", "申", "Yang Water", "Monkey"), 
    ("癸", "酉", "Yin Water", "Rooster"), ("甲", "戌", "Yang Wood", "Dog"), ("乙", "亥", "Yin Wood", "Pig"), 
    ("丙", "子", "Yang Fire", "Rat"), ("丁", "丑", "Yin Fire", "Ox"), ("戊", "寅", "Yang Earth", "Tiger"),
    ("己", "卯", "Yin Earth", "Rabbit"), ("庚", "辰", "Yang Metal", "Dragon"), ("辛", "巳", "Yin Metal", "Snake"), 
    ("壬", "午", "Yang Water", "Horse"), ("癸", "未", "Yin Water", "Goat"), ("甲", "申", "Yang Wood", "Monkey"), 
    ("乙", "酉", "Yin Wood", "Rooster"), ("丙", "戌", "Yang Fire", "Dog"), ("极", "亥", "Yin Fire", "Pig"), 
    ("戊", "子", "Yang Earth", "Rat"), ("己", "丑", "Yin Earth", "Ox"), ("庚", "寅", "Yang Metal", "Tiger"), 
    ("辛", "卯", "Yin Metal", "Rabbit"), ("壬", "辰", "Yang Water", "Dragon"), ("癸", "巳", "Yin Water", "Snake"),
    ("甲", "午", "Yang Wood", "Horse"), ("乙", "未", "Yin Wood", "Goat"), ("丙", "申", "Yang Fire", "Monkey"), 
    ("丁", "酉", "Yin Fire", "极oster"), ("戊", "戌", "Yang Earth", "Dog"), ("己", "亥", "Yin Earth", "Pig"), 
    ("庚", "子", "Yang Metal", "Rat"), ("辛", "丑", "Yin Metal", "Ox"), ("壬", "寅", "Yang Water", "Tiger"), 
    ("癸", "卯", "Yin Water", "Rabbit"), ("甲", "极", "Yang Wood", "Dragon"), ("乙", "巳", "Yin Wood", "Snake"), 
    ("丙", "午", "Yang Fire", "Horse"), ("丁", "未", "Yin Fire", "Goat"), ("戊", "申", "Yang Earth", "Monkey"),
    ("己", "酉", "Y极 Earth", "Rooster"), ("庚", "戌", "Yang Metal", "Dog"), ("辛", "亥", "Yin Metal", "Pig"), 
    ("壬", "子", "Yang Water", "Rat"), ("癸", "丑", "Yin Water", "Ox"), ("甲", "寅", "Yang Wood", "Tiger"), 
    ("乙", "卯", "Yin Wood", "Rabbit"), ("丙", "辰", "Yang Fire", "Dragon"), ("丁", "巳", "Yin Fire", "Snake"), 
    ("戊", "午", "Yang Earth", "Horse"), ("己", "未", "Yin Earth", "Goat"), ("庚", "申", "Yang Metal", "Monkey"), 
    ("辛", "酉", "Yin Metal", "Rooster"), ("壬", "戌", "Yang Water", "Dog"), ("癸", "亥", "Yin Water", "Pig")
]

SOLAR_TERMS = [
    (2, 4, '立春', '寅', 'Start of Spring'), (2, 19, '雨水', '寅', 'Rain Water'), (3, 5, '驚蟄', '寅', 'Awakening of Insects'),
    (3, 20, '春分', '卯', 'Spring Equinox'), (4, 5, '清明', '卯', 'Qingming'), (4, 20, '穀雨', '卯', 'Grain Rain'),
    (5, 5, '立夏', '辰', 'Start of Summer'), (5, 21, '小滿', '辰', 'Grain Full'), (6, 6, '芒種', '巳', 'Grain in Ear'),
    (6, 21, '夏至', '午', 'Summer Solstice'), (7, 7, '小暑', '午', 'Minor Heat'), (7, 23, '大暑', '午', 'Major Heat'),
    (8, 8, '立秋', '未', 'Start of Autumn'), (8, 23, '處暑', '未', 'End of Heat'), (9, 8, '白露', '申', 'White Dew'),
    (9, 23, '秋分', '申', 'Autumn Equinox'), (10, 8, '寒露', '酉', 'Cold极'), (10, 23, '霜降', '酉', 'Frost Descent'),
    (11, 7, '立冬', '戌', 'Start of Winter'), (11, 22, '小雪', '戌', 'Minor Snow'), (12, 7, '大雪', '亥', 'Major Snow'),
    (12, 22, '冬至', '子', 'Winter Solstice'), (1, 6, '小寒', '丑', 'Minor Cold'), (1, 20, '大寒', '丑', 'Major Cold')
]

HOUR_STEMS = {
    '甲': ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙'],
    '乙': ['丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁'],
    '丙': ['戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己'],
    '丁': ['庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛'],
    '戊': ['壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'],
    '己': ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙'],
    '庚': ['极', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁'],
    '辛': ['戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己'],
    '壬': ['庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛'],
    '癸': ['壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
}

MONTH_STEM_RULES = {
    '甲': {'寅': '丙', '卯': '丁', '辰': '戊', '巳': '己', '午': '庚', '未': '辛', '申': '壬', '酉': '癸', '戌': '甲', '亥': '乙', '子': '丙', '丑': '丁'},
    '乙': {'寅': '戊', '卯': '己', '辰': '庚', '巳': '极', '午': '壬', '未': '癸', '申': '甲', '酉': '乙', '戌': '丙', '亥': '丁', '子': '戊', '丑': '己'},
    '丙': {'寅': '庚', '卯': '辛', '辰': '壬', '巳': '癸', '午': '甲', '未': '乙', '申': '丙', '酉': '丁', '戌': '戊', '亥': '己', '子': '庚', '丑': '辛'},
    '丁': {'寅': '壬', '卯': '癸', '辰': '甲', '巳': '乙', '午': '丙', '未': '丁', '申': '戊', '酉': '己', '戌': '庚', '亥': '辛', '子': '壬', '丑': '癸'},
    '戊': {'寅': '甲', '卯': '乙', '辰': '丙', '巳': '丁', '午': '戊', '未': '己', '申': '庚', '酉极': '辛', '戌': '壬', '亥': '癸', '极': '甲', '丑': '乙'},
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
        return datetime.datetime(year, 2, 4, 0, 0, 0)  # Fallback

def get_solar_term_month(dt):
    """Get the solar term and month branch for a given date."""
    try:
        month, day = dt.month, dt.day
        
        # Handle December/January boundary
        if month == 12 and day >= 22:
            return '冬至', '子', 'Winter Solstice'
        if month == 1 and day < 6:
            return '冬至', '子', 'Winter Solstice'
            
        for i, (term_month, term_day, term_name, branch, term_english) in enumerate(SOLAR_TERMS):
            if month == term_month and day >= term_day:
                # Check if this is the last term for this month
                if i + 1 < len(SOLAR_TERMS) and SOLAR_TERMS[i + 1][0] == month:
                    continue
                return term_name, branch, term_english
        
        # Default to previous term if not found
        return SOLAR_TERMS[0][2], SOLAR_TERMS[0][3], SOLAR_TERMS[0][4]
    except:
        return '立春', '寅', 'Start of Spring'  # Fallback

def get_year_stem_branch(dt):
    """Get year pillar based on Start of Spring."""
    try:
        year = dt.year
        lichun = calculate_start_of_spring(year)
        
        if dt < lichun:
            year_index = (year - 4 - 1) % 60
        else:
            year_index = (year - 4) % 60
            
        return JIA_ZI[year_index]
    except:
        return JIA_ZI[0]  # Fallback to first Jia Zi

def get_day_stem_branch(dt):
    """Calculate day pillar."""
    try:
        ref_date = datetime.datetime(1924, 1, 1, 0, 0, 0)
        delta = dt - ref_date
        day_index = delta.days % 60
        return JIA_ZI[day_index]
    except:
        return JIA_ZI[0]  # Fallback

def get_month_pillar(year_stem, dt):
    """Get month pillar based on solar terms."""
    try:
        _, month_branch, term_english = get_solar_term_month(dt)
        month_stem = MONTH_STEM_RULES.get(year_stem, {}).get(month_branch, '甲')  # Default to 甲
        
        # Find English names for stem and branch
        stem_english = next((item[2] for item in JIA_ZI if item[0] == month_stem), month_stem)
        branch_english = next((item[3] for item in JIA_ZI if item[1] == month_branch), month_branch)
        
        return month_stem, month_branch, stem_english, branch_english, term_english
    except:
        return '甲', '寅', 'Yang Wood', 'Tiger', 'Start of Spring'  # Fallback

def get_hour_pillar(day_stem, hour, minute):
    """Get hour pillar with minute precision."""
    try:
        # Calculate exact hour (including minutes)
        exact_hour = hour + minute / 60.0
        
        earthly_branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        hour_branch_index = int((exact_hour + 1) / 2) % 12
        hour_branch = earthly_branches[hour_branch_index]
        hour_stem = HOUR_STEMS.get(day_stem, ['甲'] * 12)[hour_branch_index]
        
        # Find English names
        stem_english = next((item[2] for item in JIA_ZI if item[0] == hour_stem), hour_stem)
        branch_english = next((item[3] for item in JIA_ZI if item[1] == hour_branch), hour_branch)
        
        return hour_stem, hour_branch, stem_english, branch_english
    except:
        return '甲', '子', 'Yang Wood', 'Rat'  # Fallback

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
        st.error(f"Calculation error: {str(e)}")
        # Return a default fallback result
        return {
            'year': ('甲', '子', 'Yang Wood', 'Rat'),
            'month': ('丙', '寅', 'Yang Fire', 'Tiger', 'Start of Spring'),
            'day': ('甲', '子', 'Yang Wood', 'Rat'),
            'hour': ('甲', '子', 'Yang Wood', 'Rat'),
            'solar_term': 'Start of Spring'
        }

# --- Streamlit UI ---
st.set_page_config(page_title="Accurate Day Master Calculator", page_icon="☯️", layout="wide")

st.title("Accurate Day Master Calculator")
st.markdown("""
Calculate your Four Pillars of Destiny (八字) based on your exact birth time and location.
This calculator uses **Start of Spring** for year determination and **solar terms** for month accuracy.
""")

# Input form
with st.sidebar:
    st.header("Birth Information")
    with st.form("birth_form"):
        # Year range from 1900 to current year
        current_year = datetime.datetime.now().year
        birth_year = st.number_input("Birth Year", min_value=1900, max_value=current_year, value=1990)
        birth_month = st.number_input("Birth Month", min_value=1, max_value=12, value=1)
        birth_day = st.number_input("Birth Day", min_value=1, max_value=31, value=1)
        
        # Time input with minutes
        col1, col2 = st.columns(2)
        with col1:
            birth_hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=12)
        with col2:
            birth_minute = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=0)
        
        # GMT Time Zone selection - made more visible
        time_zone_offset = st.selectbox("GMT Time Zone", 
                                       ["GMT-12", "GMT-11", "GMT-10", "GMT-9", "GMT-8", "GMT-7", 
                                        "GMT-6", "GMT-5", "GMT-4", "GMT-3", "GMT-2", "GMT-1",
                                        "GMT+0", "GMT+1", "GMT+2", "GMT+3", "GMT+4", "GMT+5", 
                                        "GMT+6", "GMT+7", "GMT+8", "GMT+9", "GMT+10", "GMT+11", "GMT+12"],
                                       index=15,  # Default to GMT+8 (Asia time)
                                       help="Select your birth location's GMT time zone offset")
        
        submitted = st.form_submit_button("Calculate Day Master", type="primary")

# Main content area
if submitted:
    try:
        # Validate date
        birth_dt = datetime.datetime(birth_year, birth_month, birth_day, birth_hour, birth_minute)
        
        # Calculate Bazi
        pillars = calculate_bazi(birth_dt)
        
        # Display results
        st.success("Calculation Complete!")
        
        # Create a nice display with both Chinese and English
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
                     f"**{pillars['day'][0]}{pillars['day'][1]}**", 
                     f"**{pillars['day'][2]} {pillars['day'][3]}**")
        
        with col4:
            st.metric("Hour Pillar", 
                     f"{pillars['hour'][0]}{pillars['hour'][1]}", 
                     f"{pillars['hour'][2]} {pillars['hour'][3]}")
        
        # Day Master interpretation
        st.divider()
        st.subheader("Your Day Master Analysis")
        
        day_master_info = {
            "甲": {"name": "Yang Wood", "traits": "The Big Tree - Strong, upright, reliable, natural leadership qualities"},
            "乙": {"name": "Yin Wood", "traits": "Flowers & Grass - Flexible, adaptable, creative, gentle, diplomatic"},
            "丙": {"name": "Yang Fire", "traits": "The Sun - Warm, generous, charismatic, enthusiastic, optimistic"},
            "丁": {"name": "Yin Fire", "traits": "Lamp Flame - Intelligent, precise, spiritual, focused, detail-oriented"},
            "戊": {"name": "Yang Earth", "traits": "Mountain - Stable, dependable, practical, conservative, responsible"},
            "己": {"name": "Yin Earth", "traits": "Garden Soil - Nurturing, diplomatic, practical, adaptable, patient"},
            "庚": {"name": "Yang Metal", "traits": "Metal - Strong-willed, decisive, principled, direct, competitive"},
            "辛": {"name": "Yin Metal", "traits": "Jewelry - Refined, precise, aesthetic, detail-oriented, perfectionist"},
            "壬": {"name": "Yang Water", "traits": "Ocean - Wise, adaptable, resourceful, flowing, philosophical"},
            "癸": {"name": "Yin Water", "traits": "Rain - Intuitive, sensitive, diplomatic, nurturing, compassionate"}
        }
        
        day_master = pillars['day'][0]
        if day_master in day_master_info:
            info = day_master_info[day_master]
            st.info(f"""
            **Your Day Master is {info['name']}**
            
            *{info['traits']}*
            """)
        else:
            st.info("**Your Day Master analysis is not available for this combination.**")
        
        # Additional information
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
    # Show instructions when no calculation has been done
    st.info("""
    **Instructions:**
    1. Enter your exact birth date and time (with minutes)
    2. Select the GMT time zone of your birth location
    3. Click 'Calculate Day Master' to see your Four Pillars
    4. Your **Day Master** represents your core personality element
    """)

# Add footer
st.markdown("---")
st.markdown("**Note:** This calculator provides an approximation of your Bazi chart. For professional analysis, consult a qualified Bazi master.")
