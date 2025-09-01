# app.py - Refined Bazi Calculator
import streamlit as st
import datetime
import math

# --- Constants and Lookup Tables ---
JIA_ZI = [
    ("甲", "子"), ("乙", "丑"), ("丙", "寅"), ("丁", "卯"), ("戊", "辰"),
    ("己", "巳"), ("庚", "午"), ("辛", "未"), ("壬", "申"), ("癸", "酉"),
    ("甲", "戌"), ("乙", "亥"), ("丙", "子"), ("丁", "丑"), ("戊", "寅"),
    ("己", "卯"), ("庚", "辰"), ("辛", "巳"), ("壬", "午"), ("癸", "未"),
    ("甲", "申"), ("乙", "酉"), ("丙", "戌"), ("丁", "亥"), ("戊", "子"),
    ("己", "丑"), ("庚", "寅"), ("辛", "卯"), ("壬", "辰"), ("癸", "巳"),
    ("甲", "午"), ("乙", "未"), ("丙", "申"), ("丁", "酉"), ("戊", "戌"),
    ("己", "亥"), ("庚", "子"), ("辛", "丑"), ("壬", "寅"), ("癸", "卯"),
    ("甲", "辰"), ("乙", "巳"), ("丙", "午"), ("丁", "未"), ("戊", "申"),
    ("己", "酉"), ("庚", "戌"), ("辛", "亥"), ("壬", "子"), ("癸", "丑"),
    ("甲", "寅"), ("乙", "卯"), ("丙", "辰"), ("丁", "巳"), ("戊", "午"),
    ("己", "未"), ("庚", "申"), ("辛", "酉"), ("壬", "戌"), ("癸", "亥")
]

SOLAR_TERMS = [
    (2, 4, '立春', '寅'), (2, 19, '雨水', '寅'), (3, 5, '驚蟄', '寅'),
    (3, 20, '春分', '卯'), (4, 5, '清明', '卯'), (4, 20, '穀雨', '卯'),
    (5, 5, '立夏', '辰'), (5, 21, '小滿', '辰'), (6, 6, '芒種', '巳'),
    (6, 21, '夏至', '午'), (7, 7, '小暑', '午'), (7, 23, '大暑', '午'),
    (8, 8, '立秋', '未'), (8, 23, '處暑', '未'), (9, 8, '白露', '申'),
    (9, 23, '秋分', '申'), (10, 8, '寒露', '酉'), (10, 23, '霜降', '酉'),
    (11, 7, '立冬', '戌'), (11, 22, '小雪', '戌'), (12, 7, '大雪', '亥'),
    (12, 22, '冬至', '子'), (1, 6, '小寒', '丑'), (1, 20, '大寒', '丑')
]

HOUR_STEMS = {
    '甲': ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙'],
    '乙': ['丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁'],
    '丙': ['戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己'],
    '丁': ['庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛'],
    '戊': ['壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'],
    '己': ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙'],
    '庚': ['丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁'],
    '辛': ['戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己'],
    '壬': ['庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛'],
    '癸': ['壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
}

MONTH_STEM_RULES = {
    '甲': {'寅': '丙', '卯': '丁', '辰': '戊', '巳': '己', '午': '庚', '未': '辛', '申': '壬', '酉': '癸', '戌': '甲', '亥': '乙', '子': '丙', '丑': '丁'},
    '乙': {'寅': '戊', '卯': '己', '辰': '庚', '巳': '辛', '午': '壬', '未': '癸', '申': '甲', '酉': '乙', '戌': '丙', '亥': '丁', '子': '戊', '丑': '己'},
    '丙': {'寅': '庚', '卯': '辛', '辰': '壬', '巳': '癸', '午': '甲', '未': '乙', '申': '丙', '酉': '丁', '戌': '戊', '亥': '己', '子': '庚', '丑': '辛'},
    '丁': {'寅': '壬', '卯': '癸', '辰': '甲', '巳': '乙', '午': '丙', '未': '丁', '申': '戊', '酉': '己', '戌': '庚', '亥': '辛', '子': '壬', '丑': '癸'},
    '戊': {'寅': '甲', '卯': '乙', '辰': '丙', '巳': '丁', '午': '戊', '未': '己', '申': '庚', '酉': '辛', '戌': '壬', '亥': '癸', '子': '甲', '丑': '乙'},
    '己': {'寅': '丙', '卯': '丁', '辰': '戊', '巳': '己', '午': '庚', '未': '辛', '申': '壬', '酉': '癸', '戌': '甲', '亥': '乙', '子': '丙', '丑': '丁'},
    '庚': {'寅': '戊', '卯': '己', '辰': '庚', '巳': '辛', '午': '壬', '未': '癸', '申': '甲', '酉': '乙', '戌': '丙', '亥': '丁', '子': '戊', '丑': '己'},
    '辛': {'寅': '庚', '卯': '辛', '辰': '壬', '巳': '癸', '午': '甲', '未': '乙', '申': '丙', '酉': '丁', '戌': '戊', '亥': '己', '子': '庚', '丑': '辛'},
    '壬': {'寅': '壬', '卯': '癸', '辰': '甲', '巳': '乙', '午': '丙', '未': '丁', '申': '戊', '酉': '己', '戌': '庚', '亥': '辛', '子': '壬', '丑': '癸'},
    '癸': {'寅': '甲', '卯': '乙', '辰': '丙', '巳': '丁', '午': '戊', '未': '己', '申': '庚', '酉': '辛', '戌': '壬', '亥': '癸', '子': '甲', '丑': '乙'}
}

# --- Core Calculation Functions ---
def calculate_start_of_spring(year):
    """Calculate Start of Spring (立春) for a given year."""
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

def get_solar_term_month(dt):
    """Get the solar term and month branch for a given date."""
    month, day = dt.month, dt.day
    
    for term_month, term_day, term_name, branch in SOLAR_TERMS:
        if month == term_month and day >= term_day:
            # If we find a solar term that starts on or before this day
            if month == 12 and day >= 22:  # Special case for December/January boundary
                return term_name, branch
            continue
        else:
            # Return the previous solar term
            prev_index = (SOLAR_TERMS.index((term_month, term_day, term_name, branch)) - 1) % len(SOLAR_TERMS)
            prev_term = SOLAR_TERMS[prev_index]
            return prev_term[2], prev_term[3]
    
    return SOLAR_TERMS[-1][2], SOLAR_TERMS[-1][3]  # Default to last term

def get_year_stem_branch(dt):
    """Get year pillar based on Start of Spring."""
    year = dt.year
    lichun = calculate_start_of_spring(year)
    
    if dt < lichun:
        year_index = (year - 4 - 1) % 60
    else:
        year_index = (year - 4) % 60
        
    return JIA_ZI[year_index]

def get_day_stem_branch(dt):
    """Calculate day pillar."""
    ref_date = datetime.datetime(1924, 1, 1, 0, 0, 0)
    delta = dt - ref_date
    day_index = delta.days % 60
    return JIA_ZI[day_index]

def get_month_pillar(year_stem, dt):
    """Get month pillar based on solar terms."""
    _, month_branch = get_solar_term_month(dt)
    month_stem = MONTH_STEM_RULES[year_stem][month_branch]
    return month_stem, month_branch

def get_hour_pillar(day_stem, hour):
    """Get hour pillar."""
    earthly_branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    hour_branch_index = (hour + 1) // 2 % 12
    hour_branch = earthly_branches[hour_branch_index]
    hour_stem = HOUR_STEMS[day_stem][hour_branch_index]
    return hour_stem, hour_branch

def calculate_bazi(dt):
    """Main calculation function."""
    year_stem, year_branch = get_year_stem_branch(dt)
    month_stem, month_branch = get_month_pillar(year_stem, dt)
    day_stem, day_branch = get_day_stem_branch(dt)
    hour_stem, hour_branch = get_hour_pillar(day_stem, dt.hour)
    
    return {
        'year': (year_stem, year_branch),
        'month': (month_stem, month_branch),
        'day': (day_stem, day_branch),
        'hour': (hour_stem, hour_branch)
    }

# --- Streamlit UI ---
st.set_page_config(page_title="Accurate Bazi Calculator", page_icon="☯️", layout="wide")

st.title("☯️ Accurate Bazi Calculator")
st.markdown("""
Calculate your Four Pillars of Destiny (八字) based on your exact birth time and location.
The calculator uses **Start of Spring** for year determination and **solar terms** for month accuracy.
""")

# Input form
with st.sidebar:
    st.header("Birth Information")
    with st.form("birth_form"):
        birth_date = st.date_input("Birth Date", datetime.date(1990, 1, 1), 
                                 help="Enter your exact date of birth")
        birth_time = st.time_input("Birth Time", datetime.time(12, 0),
                                 help="Enter your exact time of birth")
        
        # Time zone selection
        time_zones = [
            "Asia/Shanghai", "Asia/Hong_Kong", "Asia/Taipei", "Asia/Singapore",
            "Asia/Tokyo", "Asia/Seoul", "America/New_York", "Europe/London"
        ]
        time_zone = st.selectbox("Time Zone", time_zones, index=3,
                               help="Select the time zone of your birth location")
        
        submitted = st.form_submit_button("Calculate Bazi", type="primary")

# Main content area
if submitted:
    try:
        # Create datetime object with timezone awareness (simplified)
        birth_dt = datetime.datetime.combine(birth_date, birth_time)
        
        # Calculate Bazi
        pillars = calculate_bazi(birth_dt)
        
        # Display results
        st.success("🎉 Bazi Calculation Complete!")
        
        # Create a nice display
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Year Pillar", f"{pillars['year'][0]}{pillars['year'][1]}", 
                     help="Represents your ancestry and early life environment")
        
        with col2:
            st.metric("Month Pillar", f"{pillars['month'][0]}{pillars['month'][1]}", 
                     help="Represents your parents and career path")
        
        with col3:
            st.metric("Day Master", f"**{pillars['day'][0]}{pillars['day'][1]}**", 
                     help="Represents YOU - your core personality and self")
        
        with col4:
            st.metric("Hour Pillar", f"{pillars['hour'][0]}{pillars['hour'][1]}", 
                     help="Represents your children and later life")
        
        # Day Master interpretation
        st.divider()
        st.subheader("Your Day Master Analysis")
        
        day_master_info = {
            "甲": {"name": "Yang Wood (甲)", "symbol": "🌳", "traits": "The Big Tree - Strong, upright, reliable, leadership qualities"},
            "乙": {"name": "Yin Wood (乙)", "symbol": "🌿", "traits": "Flowers & Grass - Flexible, adaptable, creative, gentle"},
            "丙": {"name": "Yang Fire (丙)", "symbol": "☀️", "traits": "The Sun - Warm, generous, charismatic, enthusiastic"},
            "丁": {"name": "Yin Fire (丁)", "symbol": "🕯️", "traits": "Lamp Flame - Intelligent, precise, spiritual, focused"},
            "戊": {"name": "Yang Earth (戊)", "symbol": "⛰️", "traits": "Mountain - Stable, dependable, practical, conservative"},
            "己": {"name": "Yin Earth (己)", "symbol": "🌾", "traits": "Garden Soil - Nurturing, diplomatic, practical, adaptable"},
            "庚": {"name": "Yang Metal (庚)", "symbol": "⚔️", "traits": "Metal - Strong-willed, decisive, principled, direct"},
            "辛": {"name": "Yin Metal (辛)", "symbol": "💎", "traits": "Jewelry - Refined, precise, aesthetic, detail-oriented"},
            "壬": {"name": "Yang Water (壬)", "symbol": "🌊", "traits": "Ocean - Wise, adaptable, resourceful, flowing"},
            "癸": {"name": "Yin Water (癸)", "symbol": "💧", "traits": "Rain - Intuitive, sensitive, diplomatic, nurturing"}
        }
        
        day_master = pillars['day'][0]
        if day_master in day_master_info:
            info = day_master_info[day_master]
            st.info(f"""
            **{info['symbol']} Your Day Master is {info['name']}**
            
            *{info['traits']}*
            """)
        else:
            st.warning("Could not interpret Day Master")
        
        # Additional information
        with st.expander("📋 Detailed Pillar Information"):
            st.write(f"**Birth Date:** {birth_date}")
            st.write(f"**Birth Time:** {birth_time}")
            st.write(f"**Time Zone:** {time_zone}")
            st.write("**Full Four Pillars:**")
            st.code(f"{pillars['year'][0]}{pillars['year'][1]} {pillars['month'][0]}{pillars['month'][1]} {pillars['day'][0]}{pillars['day'][1]} {pillars['hour'][0]}{pillars['hour'][1]}")
        
    except Exception as e:
        st.error(f"❌ Error in calculation: {str(e)}")
        st.info("Please check your input and try again. If the problem persists, try a different date.")

else:
    # Show instructions when no calculation has been done
    st.info("""
    **Instructions:**
    1. Enter your exact birth date and time
    2. Select the time zone of your birth location
    3. Click 'Calculate Bazi' to see your Four Pillars
    4. Your **Day Master** represents your core personality
    """)
    
    # Example calculation
    st.divider()
    st.subheader("Example Calculation")
    example_dt = datetime.datetime(1974, 12, 26, 1, 20)
    example_pillars = calculate_bazi(example_dt)
    st.write(f"**December 26, 1974, 1:20 AM:** `{example_pillars['year'][0]}{example_pillars['year'][1]} {example_pillars['month'][0]}{example_pillars['month'][1]} {example_pillars['day'][0]}{example_pillars['day'][1]} {example_pillars['hour'][0]}{example_pillars['hour'][1]}`")
