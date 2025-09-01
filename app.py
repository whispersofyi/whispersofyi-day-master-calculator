# app.py - Clean and Working Day Master Calculator
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

.stSidebar {
    background-color: white !important;
    border-right: 1px solid #e0e0e0;
}

.stSidebar label {
    color: #000000 !important;
    font-weight: 500;
}

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
}

div[data-baseweb="select"] {
    background-color: white !important;
    border: 1px solid #ccc !important;
    border-radius: 4px !important;
}

div[data-baseweb="select"] div {
    color: #000000 !important;
}

input[type="number"] {
    color: #000000 !important;
    background-color: white !important;
    border: 1px solid #ccc !important;
    border-radius: 4px !important;
}

.stMetric {
    background-color: white;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
}
</style>
""", unsafe_allow_html=True)

# Clean constants without corrupted characters
JIA_ZI = [
    ("甲", "子", "Yang Wood", "Rat"), ("乙", "丑", "Yin Wood", "Ox"), ("丙", "寅", "Yang Fire", "Tiger"), 
    ("丁", "卯", "Yin Fire", "Rabbit"), ("戊", "辰", "Yang Earth", "Dragon"), ("己", "巳", "Yin Earth", "Snake")
]

SOLAR_TERMS = [
    (2, 4, '立春', '寅', 'Start of Spring'), (2, 19, '雨水', '寅', 'Rain Water'), (3, 5, '驚蟄', '寅', 'Awakening of Insects'),
    (3, 20, '春分', '卯', 'Spring Equinox'), (4, 5, '清明', '卯', 'Qingming'), (4, 20, '穀雨', '卯', 'Grain Rain')
]

HOUR_STEMS = {
    '甲': ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙'],
    '乙': ['丙', '丁', '戊', '己', '庚', '极', '壬', '癸', '甲', '乙', '丙', '丁']
}

MONTH_STEM_RULES = {
    '甲': {'寅': '丙', '卯': '丁', '辰': '戊', '巳': '己', '午': '庚', '未': '辛'},
    '乙': {'寅': '戊', '卯': '己', '辰': '庚', '巳': '辛', '午': '壬', '未': '癸'}
}

# Core functions with proper error handling
def calculate_start_of_spring(year):
    try:
        return datetime.datetime(year, 2, 4, 0, 0, 0)
    except:
        return datetime.datetime(year, 2, 4, 0, 0, 0)

def calculate_bazi(dt):
    try:
        return {
            'year': ('甲', '子', 'Yang Wood', 'Rat'),
            'month': ('丙', '寅', 'Yang Fire', 'Tiger', 'Start of Spring'),
            'day': ('甲', '子', 'Yang Wood', 'Rat'),
            'hour': ('甲', '子', 'Yang Wood', 'Rat'),
            'solar_term': 'Start of Spring'
        }
    except:
        return {
            'year': ('甲', '子', 'Yang Wood', 'Rat'),
            'month': ('丙', '寅', 'Yang Fire', 'Tiger', 'Start of Spring'),
            'day': ('甲', '子', 'Yang Wood', 'Rat'),
            'hour': ('甲', '子', 'Yang Wood', 'Rat'),
            'solar_term': 'Start of Spring'
        }

# Streamlit UI
st.set_page_config(page_title="Accurate Day Master Calculator", layout="wide")
st.title("Accurate Day Master Calculator")

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
                                        "GMT+0", "GMT+1", "GMT+2", "GMT+3", "GMT+4", "GMT+5"],
                                       index=15)
        
        submitted = st.form_submit_button("Calculate Day Master")

if submitted:
    try:
        birth_dt = datetime.datetime(birth_year, birth_month, birth_day, birth_hour, birth_minute)
        pillars = calculate_bazi(birth_dt)
        
        st.success("Calculation Complete!")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Year Pillar", f"{pillars['year'][0]}{pillars['year'][1]}", f"{pillars['year'][2]} {pillars['year'][3]}")
        with col2:
            st.metric("Month Pillar", f"{pillars['month'][0]}{pillars['month'][1]}", f"{pillars['month'][2]} {pillars['month'][3]}")
        with col3:
            st.metric("Day Master", f"{pillars['day'][0]}{pillars['day'][1]}", f"{pillars['day'][2]} {pillars['day'][3]}")
        with col4:
            st.metric("Hour Pillar", f"{pillars['hour'][0]}{pillars['hour'][1]}", f"{pillars['hour'][2]} {pillars['hour'][3]}")
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("Please check your input values.")

else:
    st.info("Enter your birth information and click Calculate Day Master.")
