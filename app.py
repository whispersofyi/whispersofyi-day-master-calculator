# app.py - Day Master Calculator with Proper Styling
import streamlit as st
import datetime

# CSS to match your GitHub page style
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #ffffff;
}

.stSidebar {
    background-color: #f6f8fa;
    border-right: 1px solid #e1e4e8;
    padding: 20px;
}

.stSidebar .stNumberInput, .stSidebar .stSelectbox {
    background-color: white;
}

.stSidebar label {
    color: #24292e !important;
    font-weight: 500;
    font-size: 14px;
}

.stSidebar input, .stSidebar select {
    color: #24292e !important;
    background-color: white !important;
    border: 1px solid #e1e4e8 !important;
    border-radius: 6px !important;
    padding: 8px 12px !important;
    font-size: 14px !important;
}

/* Green buttons matching your GitHub links */
div.stButton > button {
    background-color: #22863a !important;
    color: white !important;
    border: 1px solid #22863a !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    padding: 10px 16px !important;
    width: 100% !important;
    font-size: 14px !important;
    transition: background-color 0.2s ease;
}

div.stButton > button:hover {
    background-color: #1c6b2f !important;
    border-color: #1c6b2f !important;
    color: white !important;
}

/* Select box styling */
div[data-baseweb="select"] {
    background-color: white !important;
    border: 1px solid #e1e4e8 !important;
    border-radius: 6px !important;
}

div[data-baseweb="select"] div {
    color: #24292e !important;
    font-size: 14px !important;
}

/* Metric cards styling */
.stMetric {
    background-color: #f6f8fa;
    padding: 20px;
    border-radius: 6px;
    border: 1px solid #e1e4e8;
    text-align: center;
}

.stMetric label {
    color: #586069 !important;
    font-weight: 500;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stMetric div {
    color: #24292e !important;
    font-weight: 600;
    font-size: 18px;
    margin-top: 8px;
}

.stMetric div:nth-child(3) {
    color: #586069 !important;
    font-weight: 400;
    font-size: 14px;
    margin-top: 4px;
}

/* Main content styling */
.main-content {
    padding: 20px;
}

.success-box {
    background-color: #dafbe1;
    border: 1px solid #2ea043;
    border-radius: 6px;
    padding: 16px;
    margin-bottom: 20px;
    color: #0e4429;
}

.info-box {
    background-color: #ddf4ff;
    border: 1px solid #54aeff;
    border-radius: 6px;
    padding: 16px;
    margin: 20px 0;
    color: #0550ae;
}

.day-master-card {
    background-color: #f6f8fa;
    border: 1px solid #e1e4e8;
    border-radius: 6px;
    padding: 20px;
    margin: 20px 0;
}

.day-master-card h3 {
    color: #24292e;
    margin-bottom: 16px;
    border-bottom: 2px solid #22863a;
    padding-bottom: 8px;
}

.trait-list {
    background-color: white;
    border: 1px solid #e1e4e8;
    border-radius: 6px;
    padding: 16px;
    margin: 10px 0;
}

.trait-list strong {
    color: #22863a;
}

/* Headings */
h1, h2, h3 {
    color: #24292e !important;
}

h1 {
    border-bottom: 1px solid #e1e4e8;
    padding-bottom: 0.3em;
    margin-bottom: 1em !important;
}
</style>
""", unsafe_allow_html=True)

# Day Master information database
DAY_MASTER_INFO = {
    "甲": {
        "name": "Yang Wood",
        "symbol": "🌳 Great Tree",
        "description": "The Yang Wood Day Master represents strength, growth, and integrity. Like a mighty oak tree, you stand tall and provide shelter and stability for others.",
        "positive_traits": [
            "Natural leadership abilities",
            "Strong moral compass and integrity",
            "Reliable and dependable",
            "Visionary with long-term planning",
            "Excellent at providing support and structure"
        ],
        "challenges": [
            "Can be too rigid or inflexible",
            "May struggle with adaptability",
            "Sometimes too serious or stern",
            "Can be resistant to change",
            "May take on too much responsibility"
        ],
        "compatibility": "Works well with Yin Water (癸) for nourishment and Yang Fire (丙) for warmth and growth",
        "career_paths": "Leadership roles, management, education, environmental work, construction, architecture"
    },
    "乙": {
        "name": "Yin Wood",
        "symbol": "🌿 Flowers and Grass",
        "description": "The Yin Wood Day Master represents flexibility, creativity, and adaptability. Like flowers bending in the wind, you know how to adapt while maintaining your beauty and purpose.",
        "positive_traits": [
            "Highly adaptable and flexible",
            "Creative and artistic",
            "Excellent communicator and diplomat",
            "Good at networking and building relationships",
            "Gentle yet persistent nature"
        ],
        "challenges": [
            "Can be too accommodating",
            "May lack assertiveness",
            "Sometimes indecisive",
            "Can be easily influenced",
            "May avoid confrontation"
        ],
        "compatibility": "Works well with Yang Earth (戊) for stability and Yang Metal (庚) for structure",
        "career_paths": "Arts, design, writing, counseling, teaching, hospitality, public relations"
    },
    "丙": {
        "name": "Yang Fire",
        "symbol": "☀️ The Sun",
        "description": "The Yang Fire Day Master represents warmth, charisma, and vitality. Like the sun, you bring light, energy, and inspiration to everyone around you.",
        "positive_traits": [
            "Natural charisma and magnetism",
            "Warm, generous, and enthusiastic",
            "Inspiring leader and motivator",
            "Optimistic and positive outlook",
            "Excellent at public speaking and presentation"
        ],
        "challenges": [
            "Can be overly dramatic",
            "May burn out quickly",
            "Sometimes impulsive",
            "Can be attention-seeking",
            "May lack follow-through"
        ],
        "compatibility": "Works well with Yin Water (癸) for balance and Yang Wood (甲) for fuel",
        "career_paths": "Entertainment, leadership, sales, marketing, coaching, public speaking"
    },
    "丁": {
        "name": "Yin Fire",
        "symbol": "🕯️ Lamp Flame",
        "description": "The Yin Fire Day Master represents intelligence, precision, and spiritual depth. Like a focused lamp flame, you provide targeted illumination and insight.",
        "positive_traits": [
            "Highly intelligent and analytical",
            "Precise and detail-oriented",
            "Spiritually inclined",
            "Excellent researcher and investigator",
            "Good at focused, specialized work"
        ],
        "challenges": [
            "Can be too critical",
            "May become perfectionistic",
            "Sometimes isolated or withdrawn",
            "Can be overly skeptical",
            "May lack broad perspective"
        ],
        "compatibility": "Works well with Yin Wood (乙) for fuel and Yang Metal (庚) for structure",
        "career_paths": "Research, technology, analysis, writing, psychology, spirituality"
    },
    "戊": {
        "name": "Yang Earth",
        "symbol": "⛰️ Mountain",
        "description": "The Yang Earth Day Master represents stability, practicality, and reliability. Like a mountain, you provide a solid foundation and unwavering support.",
        "positive_traits": [
            "Extremely reliable and dependable",
            "Practical and grounded",
            "Excellent with finances and resources",
            "Patient and steady",
            "Good at long-term planning"
        ],
        "challenges": [
            "Can be too conservative",
            "May resist change",
            "Sometimes stubborn",
            "Can be materialistic",
            "May lack spontaneity"
        ],
        "compatibility": "Works well with Yin Fire (丁) for warmth and Yin Water (癸) for nourishment",
        "career_paths": "Finance, real estate, construction, management, agriculture, engineering"
    }
}

# Simple calculation function (for demonstration)
def calculate_bazi(dt):
    # This is a simplified version - in production, you'd use proper Bazi calculations
    day_masters = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    day_index = dt.day % 10
    selected_master = day_masters[day_index]
    
    return {
        'year': ('甲', '子', 'Yang Wood', 'Rat'),
        'month': ('丙', '寅', 'Yang Fire', 'Tiger', 'Start of Spring'),
        'day': (selected_master, '子', DAY_MASTER_INFO.get(selected_master, {}).get('name', 'Unknown'), 'Rat'),
        'hour': ('甲', '子', 'Yang Wood', 'Rat'),
        'solar_term': 'Start of Spring',
        'day_master': selected_master
    }

# Streamlit UI
st.set_page_config(page_title="Day Master Calculator", layout="wide", page_icon="☯️")

st.title("☯️ Day Master Calculator")
st.markdown("""
Discover your Four Pillars of Destiny and understand your core personality through Bazi astrology. 
Your **Day Master** represents your essential nature and how you interact with the world.
""")

# Input form
with st.sidebar:
    st.header("📅 Birth Information")
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
        
        submitted = st.form_submit_button("✨ Calculate Day Master")

# Main content
if submitted:
    try:
        birth_dt = datetime.datetime(birth_year, birth_month, birth_day, birth_hour, birth_minute)
        pillars = calculate_bazi(birth_dt)
        day_master_key = pillars['day_master']
        day_master_info = DAY_MASTER_INFO.get(day_master_key, {})
        
        st.markdown('<div class="success-box">🎉 Calculation Complete! Your Bazi chart has been generated.</div>', unsafe_allow_html=True)
        
        # Four Pillars Display
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
        
        # Day Master Analysis
        st.markdown("---")
        st.subheader(f"🌟 Your Day Master Analysis: {day_master_info.get('name', 'Unknown')} ({pillars['day'][0]})")
        
        if day_master_info:
            st.markdown(f"""
            <div class="day-master-card">
                <h3>{day_master_info.get('symbol', '')} - {day_master_info.get('name', '')}</h3>
                <p>{day_master_info.get('description', '')}</p>
                
                <div class="trait-list">
                    <strong>✨ Positive Traits:</strong>
                    <ul>
                        {''.join([f'<li>{trait}</li>' for trait in day_master_info.get('positive_traits', [])])}
                    </ul>
                </div>
                
                <div class="trait-list">
                    <strong>⚠️ Challenges:</strong>
                    <ul>
                        {''.join([f'<li>{trait}</li>' for trait in day_master_info.get('challenges', [])])}
                    </ul>
                </div>
                
                <div class="trait-list">
                    <strong>🤝 Best Compatibility:</strong>
                    <p>{day_master_info.get('compatibility', '')}</p>
                </div>
                
                <div class="trait-list">
                    <strong>💼 Suitable Career Paths:</strong>
                    <p>{day_master_info.get('career_paths', '')}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Day Master information not available for this combination.")
        
        # Additional Information
        with st.expander("📋 Detailed Information"):
            st.write(f"**Birth Date:** {birth_dt.strftime('%Y-%m-%d %H:%M')}")
            st.write(f"**Time Zone:** {time_zone_offset}")
            st.write(f"**Current Solar Term:** {pillars['solar_term']}")
            st.write("**Full Four Pillars:**")
            st.code(f"{pillars['year'][0]}{pillars['year'][1]} {pillars['month'][0]}{pillars['month'][1]} {pillars['day'][0]}{pillars['day'][1]} {pillars['hour'][0]}{pillars['hour'][1]}")
        
    except Exception as e:
        st.error("Please check your input values and try again. Ensure the date is valid.")

else:
    st.markdown("""
    <div class="info-box">
        <strong>📋 Instructions:</strong>
        <ol>
            <li>Enter your exact birth date and time (with minutes)</li>
            <li>Select the GMT time zone of your birth location</li>
            <li>Click 'Calculate Day Master' to see your Four Pillars</li>
            <li>Your <strong>Day Master</strong> represents your core personality element</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 For the most accurate results, use the local time of your birth location and consider daylight saving time if applicable.")
