# app.py - Ultra Simple Bazi Calculator
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

MONTH_BRANCH_MAP = {
    1: '丑', 2: '寅', 3: '寅', 4: '卯', 5: '辰', 6: '巳',
    7: '午', 8: '未', 9: '申', 10: '酉', 11: '戌', 12: '亥'
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
    '癸': {'寅': '甲', '卯': '乙', '辰': '丙', '巳': '丁', '午': '戊', '未': '己', '申': '庚', '酉': '辛', '戌': '壬', '亥': '癸', '子': '甲', '丑': 'B'}
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

def get_month_pillar(year_stem, month):
    """Get month pillar."""
    month_branch = MONTH_BRANCH_MAP.get(month, '寅')
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
    month_stem, month_branch = get_month_pillar(year_stem, dt.month)
    day_stem, day_branch = get_day_stem_branch(dt)
    hour_stem, hour_branch = get_hour_pillar(day_stem, dt.hour)
    
    return {
        'year': (year_stem, year_branch),
        'month': (month_stem, month_branch),
        'day': (day_stem, day_branch),
        'hour': (hour_stem, hour_branch)
    }

# --- Streamlit UI ---
st.set_page_config(page_title="Simple Bazi Calculator", page_icon="☯️")
st.title("☯️ Simple Bazi Calculator")
st.markdown("Calculate your Four Pillars of Destiny")

# Input form
with st.form("birth_form"):
    birth_date = st.date_input("Birth Date", datetime.date(1990, 1, 1))
    birth_time = st.time_input("Birth Time", datetime.time(12, 0))
    submitted = st.form_submit_button("Calculate")

# Calculation and results
if submitted:
    try:
        # Create datetime object
        birth_dt = datetime.datetime.combine(birth_date, birth_time)
        
        # Calculate Bazi
        pillars = calculate_bazi(birth_dt)
        
        # Display results
        st.success("Calculation Complete!")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Year", f"{pillars['year'][0]}{pillars['year'][1]}")
        with col2:
            st.metric("Month", f"{pillars['month'][0]}{pillars['month'][1]}")
        with col3:
            st.metric("Day Master", f"**{pillars['day'][0]}{pillars['day'][1]}**")
        with col4:
            st.metric("Hour", f"{pillars['hour'][0]}{pillars['hour'][1]}")
        
        # Day Master interpretation
        day_master_info = {
            "甲": "Yang Wood (甲) - The Big Tree",
            "乙": "Yin Wood (乙) - Flowers & Grass",
            "丙": "Yang Fire (丙) - The Sun",
            "丁": "Yin Fire (丁) - Lamp Flame",
            "戊": "Yang Earth (戊) - Mountain",
            "己": "Yin Earth (己) - Garden Soil",
            "庚": "Yang Metal (庚) - Metal",
            "辛": "Yin Metal (辛) - Jewelry",
            "壬": "Yang Water (壬) - Ocean",
            "癸": "Yin Water (癸) - Rain"
        }
        
        day_master = pillars['day'][0]
        st.info(f"**Your Day Master is {day_master_info.get(day_master, 'Unknown')}.**")
        
    except Exception as e:
        st.error(f"Error in calculation: {str(e)}")
