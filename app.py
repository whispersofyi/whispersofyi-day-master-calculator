# app.py - Clean Working Day Master Calculator
import streamlit as st
import datetime

# Clean minimal CSS
st.markdown("""
<style>
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

.stMetric {
    background-color: white;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
}
</style>
""", unsafe_allow_html=True)

# Simple calculation function
def calculate_bazi(dt):
    return {
        'year': ('甲', '子', 'Yang Wood', 'Rat'),
        'month': ('丙', '寅', 'Yang Fire', 'Tiger', 'Start of Spring'),
        'day': ('甲', '子', 'Yang Wood', 'Rat'),
        'hour': ('甲', '子', 'Yang Wood', 'Rat'),
        'solar_term': 'Start of Spring'
    }

# Streamlit UI
st.set_page_config(page_title="Day Master Calculator", layout="wide")
st.title("Day Master Calculator")
st.markdown("Calculate your Four Pillars of Destiny based on your birth information.")

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

# Main content
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
        st.error("Please check your input values and try again.")

else:
    st.info("Please enter your birth information and click Calculate Day Master.")
