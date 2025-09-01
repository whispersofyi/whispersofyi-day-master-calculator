# app.py
import streamlit as st
import datetime
import pytz
from bazi_calculator import calculate_bazi

st.set_page_config(page_title="Accurate Bazi Calculator", page_icon="☯️")
st.title("☯️ Accurate Bazi Day Master Calculator")
st.markdown("""
This calculator uses astronomical calculations to determine the **Start of Spring (立春)** 
and Solar Terms for accurate year and month pillars.
""")

with st.sidebar:
    st.header("Settings")
    timezone_str = st.selectbox("Birth Timezone", pytz.all_timezones, index=pytz.all_timezones.index('Asia/Singapore'))
    selected_tz = pytz.timezone(timezone_str)

with st.form("birth_form"):
    col1, col2 = st.columns(2)
    with col1:
        birth_date = st.date_input("Birth Date", datetime.date(1974, 12, 26))
    with col2:
        birth_time = st.time_input("Birth Time", datetime.time(1, 20))
    
    submitted = st.form_submit_button("Calculate My Bazi")

if submitted:
    try:
        # Create timezone-aware datetime
        local_dt = selected_tz.localize(datetime.datetime.combine(birth_date, birth_time))
        utc_dt = local_dt.astimezone(pytz.UTC)
        
        pillars = calculate_bazi(utc_dt)
        
        st.success("Calculation Complete! ✅")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Year Pillar", f"{pillars['year'][0]}{pillars['year'][1]}")
        with col2:
            st.metric("Month Pillar", f"{pillars['month'][0]}{pillars['month'][1]}")
        with col3:
            st.metric("**Day Master**", f"**{pillars['day'][0]}{pillars['day'][1]}**")
        with col4:
            st.metric("Hour Pillar", f"{pillars['hour'][0]}{pillars['hour'][1]}")
        
        # Day Master interpretation
        day_master_map = {
            "甲": "Yang Wood (甲) - The大树 Big Tree",
            "乙": "Yin Wood (乙) - The 花草 Flowers & Grass",
            "丙": "Yang Fire (丙) - The 太阳 Sun",
            "丁": "Yin Fire (丁) - The 灯烛 Lamp Flame",
            "戊": "Yang Earth (戊) - The 城墙 Mountain",
            "己": "Yin Earth (己) - The 田园 Garden Soil",
            "庚": "Yang Metal (庚) - The 钢铁 Metal",
            "辛": "Yin Metal (辛) - The 珠宝 Jewelry",
            "壬": "Yang Water (壬) - The 大海 Ocean",
            "癸": "Yin Water (癸) - The 雨露 Rain",
        }
        
        day_master = pillars['day'][0]
        st.info(f"**Your Day Master is {day_master_map.get(day_master, 'Unknown')}.**")
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.info("Please check your input and try again.")
