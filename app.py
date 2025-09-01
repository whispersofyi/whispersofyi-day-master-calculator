# app.py - Improved Day Master Calculator with Stability
import streamlit as st
import datetime
import calendar

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

.error-box {
    background-color: #ffeef0;
    border: 1px solid #f85149;
    border-radius: 6px;
    padding: 16px;
    margin: 20px 0;
    color: #cf222e;
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

# Complete Day Master information database
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
    },
    "己": {
        "name": "Yin Earth",
        "symbol": "🌱 Garden Soil",
        "description": "The Yin Earth Day Master represents nurturing, cultivation, and growth. Like fertile soil, you provide the foundation for others to flourish.",
        "positive_traits": [
            "Nurturing and supportive",
            "Excellent at developing others",
            "Patient and understanding",
            "Good at bringing out potential",
            "Stable and grounding presence"
        ],
        "challenges": [
            "Can be overly self-sacrificing",
            "May neglect own needs",
            "Sometimes too passive",
            "Can be taken advantage of",
            "May lack personal boundaries"
        ],
        "compatibility": "Works well with Yang Fire (丙) for warmth and Yang Water (壬) for moisture",
        "career_paths": "Teaching, counseling, healthcare, social work, agriculture, nutrition"
    },
    "庚": {
        "name": "Yang Metal",
        "symbol": "⚔️ Sword and Steel",
        "description": "The Yang Metal Day Master represents strength, determination, and precision. Like a sharp sword, you cut through obstacles with decisive action.",
        "positive_traits": [
            "Strong-willed and determined",
            "Excellent problem-solver",
            "Direct and straightforward",
            "Good at making tough decisions",
            "Natural sense of justice"
        ],
        "challenges": [
            "Can be too harsh or critical",
            "May lack sensitivity",
            "Sometimes inflexible",
            "Can be overly competitive",
            "May struggle with emotions"
        ],
        "compatibility": "Works well with Yin Wood (乙) for refinement and Yin Fire (丁) for tempering",
        "career_paths": "Law enforcement, military, surgery, engineering, sports, entrepreneurship"
    },
    "辛": {
        "name": "Yin Metal",
        "symbol": "💎 Precious Jewelry",
        "description": "The Yin Metal Day Master represents refinement, beauty, and precision. Like precious jewelry, you value quality and attention to detail.",
        "positive_traits": [
            "Refined and elegant",
            "Excellent attention to detail",
            "Good aesthetic sense",
            "Diplomatic and tactful",
            "Values quality over quantity"
        ],
        "challenges": [
            "Can be too perfectionist",
            "May be overly critical of self",
            "Sometimes indecisive",
            "Can be materialistic",
            "May lack boldness"
        ],
        "compatibility": "Works well with Yang Wood (甲) for structure and Yang Fire (丙) for brilliance",
        "career_paths": "Design, jewelry, fashion, consulting, quality control, luxury goods"
    },
    "壬": {
        "name": "Yang Water",
        "symbol": "🌊 Ocean and Rivers",
        "description": "The Yang Water Day Master represents flow, adaptability, and wisdom. Like a mighty river, you navigate around obstacles while maintaining your course.",
        "positive_traits": [
            "Highly adaptable and flexible",
            "Wise and intuitive",
            "Excellent communicator",
            "Good at connecting people",
            "Natural problem-solver"
        ],
        "challenges": [
            "Can be inconsistent",
            "May lack focus",
            "Sometimes overly emotional",
            "Can be manipulative",
            "May avoid responsibility"
        ],
        "compatibility": "Works well with Yang Earth (戊) for containment and Yang Wood (甲) for direction",
        "career_paths": "Communication, media, transportation, logistics, counseling, diplomacy"
    },
    "癸": {
        "name": "Yin Water",
        "symbol": "🌧️ Rain and Dew",
        "description": "The Yin Water Day Master represents gentleness, nourishment, and intuition. Like gentle rain, you provide subtle but essential support.",
        "positive_traits": [
            "Gentle and compassionate",
            "Highly intuitive",
            "Good at providing emotional support",
            "Adaptable and understanding",
            "Natural healer"
        ],
        "challenges": [
            "Can be too sensitive",
            "May lack assertiveness",
            "Sometimes overly emotional",
            "Can be easily hurt",
            "May avoid confrontation"
        ],
        "compatibility": "Works well with Yang Fire (丙) for balance and Yin Earth (己) for absorption",
        "career_paths": "Healthcare, counseling, arts, spirituality, social work, research"
    }
}

# Earthly Branches (for more realistic display)
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
BRANCH_ANIMALS = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]

# Heavenly Stems
HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

def validate_date(year, month, day, hour, minute):
    """Validate input date and time"""
    try:
        # Check if the date is valid
        if not (1900 <= year <= 2100):
            return False, "Year must be between 1900 and 2100"
        
        if not (1 <= month <= 12):
            return False, "Month must be between 1 and 12"
        
        # Check if day is valid for the given month and year
        max_day = calendar.monthrange(year, month)[1]
        if not (1 <= day <= max_day):
            return False, f"Day must be between 1 and {max_day} for {calendar.month_name[month]} {year}"
        
        if not (0 <= hour <= 23):
            return False, "Hour must be between 0 and 23"
        
        if not (0 <= minute <= 59):
            return False, "Minute must be between 0 and 59"
        
        # Try to create the datetime object
        datetime.datetime(year, month, day, hour, minute)
        return True, "Valid date"
    
    except ValueError as e:
        return False, f"Invalid date: {str(e)}"

def calculate_bazi(dt):
    """
    Simplified Bazi calculation for demonstration purposes.
    Note: This is not the actual complex Bazi calculation used in professional systems.
    """
    try:
        # Simple approximation - for demo purposes only
        # In real Bazi, this involves complex calendar calculations
        
        # Day stem calculation (simplified)
        day_stems = HEAVENLY_STEMS
        year_offset = (dt.year - 1900) * 365
        month_offset = sum([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][:dt.month-1])
        if dt.month > 2 and calendar.isleap(dt.year):
            month_offset += 1
        
        total_days = year_offset + month_offset + dt.day
        day_stem_index = (total_days + 5) % 10  # Offset for alignment
        day_branch_index = (total_days + 5) % 12
        
        day_master = day_stems[day_stem_index]
        
        # Generate other pillars (simplified for demo)
        year_stem_index = (dt.year - 1900 + 6) % 10
        year_branch_index = (dt.year - 1900 + 6) % 12
        
        month_stem_index = (dt.month + day_stem_index + 2) % 10
        month_branch_index = (dt.month - 1) % 12
        
        hour_stem_index = (dt.hour // 2 + day_stem_index) % 10
        hour_branch_index = (dt.hour // 2) % 12
        
        return {
            'year': (day_stems[year_stem_index], EARTHLY_BRANCHES[year_branch_index], 
                    DAY_MASTER_INFO[day_stems[year_stem_index]]['name'], BRANCH_ANIMALS[year_branch_index]),
            'month': (day_stems[month_stem_index], EARTHLY_BRANCHES[month_branch_index], 
                     DAY_MASTER_INFO[day_stems[month_stem_index]]['name'], BRANCH_ANIMALS[month_branch_index]),
            'day': (day_master, EARTHLY_BRANCHES[day_branch_index], 
                   DAY_MASTER_INFO[day_master]['name'], BRANCH_ANIMALS[day_branch_index]),
            'hour': (day_stems[hour_stem_index], EARTHLY_BRANCHES[hour_branch_index], 
                    DAY_MASTER_INFO[day_stems[hour_stem_index]]['name'], BRANCH_ANIMALS[hour_branch_index]),
            'solar_term': 'Calculated Solar Term',
            'day_master': day_master
        }
    except Exception as e:
        st.error(f"Calculation error: {str(e)}")
        return None

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
        
        time_zones = [f"GMT{'+' if i >= 0 else ''}{i}" for i in range(-12, 13)]
        time_zone_offset = st.selectbox("GMT Time Zone", time_zones, index=20)  # GMT+8 default
        
        submitted = st.form_submit_button("✨ Calculate Day Master")

# Main content
if submitted:
    # Validate inputs
    is_valid, validation_message = validate_date(birth_year, birth_month, birth_day, birth_hour, birth_minute)
    
    if not is_valid:
        st.markdown(f'<div class="error-box">❌ {validation_message}</div>', unsafe_allow_html=True)
    else:
        try:
            birth_dt = datetime.datetime(birth_year, birth_month, birth_day, birth_hour, birth_minute)
            pillars = calculate_bazi(birth_dt)
            
            if pillars is None:
                st.error("Unable to calculate Bazi chart. Please try again.")
            else:
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
                    st.write(f"**Solar Term:** {pillars['solar_term']}")
                    st.write("**Full Four Pillars:**")
                    st.code(f"{pillars['year'][0]}{pillars['year'][1]} {pillars['month'][0]}{pillars['month'][1]} {pillars['day'][0]}{pillars['day'][1]} {pillars['hour'][0]}{pillars['hour'][1]}")
                    st.markdown("**Note:** This is a simplified calculation for demonstration purposes. Professional Bazi readings involve more complex astronomical calculations.")
        
        except Exception as e:
            st.markdown(f'<div class="error-box">❌ An unexpected error occurred: {str(e)}</div>', unsafe_allow_html=True)

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
    
    st.markdown("""
    <div class="info-box">
        <strong>⚠️ Important Note:</strong><br>
        This calculator uses a simplified algorithm for demonstration purposes. 
        Professional Bazi calculations involve complex astronomical data and should be done by qualified practitioners for serious decisions.
    </div>
    """, unsafe_allow_html=True)
