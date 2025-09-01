import streamlit as st
import datetime
import calendar

# Page configuration
st.set_page_config(
    page_title="Day Master Calculator - Whispers of YI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling including fixing h1 color to black
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');

/* Global styles */
.stApp {
    background-color: #fafafa;
    font-family: 'Inter', sans-serif;
}

/* Typography */
h1, h2, h3 {
    font-family: 'Crimson Text', serif;
    color: #2c3e50;
}

h1 {
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    text-align: center;
    border-bottom: 1px solid #e8e8e8;
    padding-bottom: 1rem;
    color: black;
}

.subtitle {
    font-style: italic;
    color: #6c757d;
    text-align: center;
    margin-bottom: 2rem;
    font-size: 1.1rem;
    line-height: 1.6;
}

/* Sidebar styling */
.stSidebar {
    background-color: #ffffff;
    border-right: 1px solid #e8e8e8;
    box-shadow: 0 0 10px rgba(0,0,0,0.05);
}

.stSidebar .stSelectbox label,
.stSidebar .stNumberInput label {
    font-weight: 500;
    color: #495057;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}

/* Form elements */
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background-color: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 4px;
    color: #495057;
}

.stSelectbox > div > div:focus-within,
.stNumberInput > div > div > input:focus {
    border-color: #6c757d;
    box-shadow: 0 0 0 0.1rem rgba(108, 117, 125, 0.25);
}

/* Button styling */
.stButton > button {
    background-color: #495057;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 0.75rem 2rem;
    font-weight: 500;
    width: 100%;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background-color: #343a40;
    transform: translateY(-1px);
}

/* Content containers */
.result-container {
    background-color: #ffffff;
    border-radius: 8px;
    padding: 2rem;
    margin: 1rem 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    border-left: 4px solid #6c757d;
}

.day-master-header {
    text-align: center;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #e8e8e8;
}

.day-master-title {
    font-size: 2rem;
    color: #2c3e50;
    margin-bottom: 0.5rem;
    font-family: 'Crimson Text', serif;
}

.day-master-element {
    font-size: 1.2rem;
    color: #6c757d;
    font-weight: 300;
}

.description-text {
    line-height: 1.8;
    color: #495057;
    margin-bottom: 2rem;
    font-size: 1.1rem;
    text-align: justify;
}

/* Trait sections */
.trait-section {
    margin: 1.5rem 0;
    background-color: #f8f9fa;
    border-radius: 6px;
    padding: 1.5rem;
}

.trait-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 1rem;
    font-family: 'Crimson Text', serif;
}

.trait-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.trait-item {
    padding: 0.5rem 0;
    border-bottom: 1px solid #e9ecef;
    color: #495057;
    line-height: 1.6;
}

.trait-item:last-child {
    border-bottom: none;
}

/* Four Pillars display */
.pillars-container {
    display: flex;
    justify-content: space-between;
    margin: 2rem 0;
    gap: 1rem;
}

.pillar-card {
    flex: 1;
    background-color: #ffffff;
    border: 1px solid #e8e8e8;
    border-radius: 6px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.pillar-title {
    font-size: 0.9rem;
    color: #6c757d;
    font-weight: 500;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.pillar-content {
    font-size: 1.5rem;
    color: #2c3e50;
    font-weight: 600;
    margin-bottom: 0.25rem;
}

.pillar-description {
    font-size: 0.85rem;
    color: #6c757d;
}

/* Instructions */
.instructions {
    background-color: #e7f3ff;
    border: 1px solid #b8daff;
    border-radius: 6px;
    padding: 1.5rem;
    margin: 2rem 0;
    color: #004085;
}

/* Error and success messages */
.error-message {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
    border-radius: 4px;
    padding: 1rem;
    margin: 1rem 0;
}

.success-message {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
    border-radius: 4px;
    padding: 1rem;
    margin: 1rem 0;
}

/* Responsive design */
@media (max-width: 768px) {
    .pillars-container {
        flex-direction: column;
    }
    
    h1 {
        font-size: 2rem;
    }
}
</style>
""", unsafe_allow_html=True)

# Day Master data (complete as before)
DAY_MASTER_DATA = {
    "甲": {
        "name": "Yang Wood",
        "element": "Great Tree",
        "description": "The Yang Wood day master embodies the essence of a towering tree - strong, upright, and deeply rooted. Like an ancient oak that has weathered countless storms, you possess an unwavering integrity and natural authority that others instinctively respect. Your presence brings stability to chaotic situations, and your moral compass guides not only your own path but often illuminates the way for others. You are the pillar that supports communities, the mentor who shapes futures, and the guardian of traditions and values. Your strength is not merely physical but deeply spiritual - rooted in purpose and reaching toward higher ideals.",
        "positive_traits": [
            "Natural leadership with authentic authority that inspires rather than intimidates",
            "Unwavering moral compass and ethical standards that guide all decisions",
            "Exceptional ability to provide structure, stability, and security to others",
            "Long-term strategic thinking with vision that extends beyond immediate concerns",
            "Reliable and dependable nature that makes you a cornerstone in relationships and organizations",
            "Strong sense of justice and fairness in all dealings",
            "Ability to remain calm and grounded during turbulent times",
            "Natural mentor and teacher who helps others grow and develop",
            "Deep respect for tradition while maintaining progressive ideals",
            "Capacity to build lasting foundations for future generations"
        ],
        "challenges": [
            "Tendency toward inflexibility when your principles are challenged",
            "Difficulty adapting quickly to unexpected changes or new circumstances",
            "May appear stern or unapproachable due to your serious demeanor",
            "Resistance to compromise, even when flexibility would be beneficial",
            "Taking on excessive responsibility, leading to overwhelm and burnout",
            "Impatience with those who don't share your strong work ethic or values",
            "Difficulty expressing emotions or appearing vulnerable to others",
            "May become rigid in thinking patterns or stuck in established routines",
            "Tendency to be overly critical of yourself and others",
            "Struggle with delegation due to high personal standards"
        ],
        "compatibility": "Harmonizes beautifully with Yin Water (癸), which nourishes your growth like gentle rain on fertile soil. Yang Fire (丙) brings warmth and energy that helps you flourish and reach your full potential. These elements create natural cycles of support and mutual benefit.",
        "career_paths": "Executive leadership roles, educational administration, environmental conservation, sustainable architecture, construction management, forestry, government service, judicial positions, consulting, organizational development, mentoring and coaching, traditional medicine, and any field requiring ethical leadership and long-term vision.",
        "life_philosophy": "Growth through integrity, strength through service, and wisdom through experience. You believe that true success comes from building something meaningful that will endure long after you're gone."
    },
    # Include all other DAY_MASTER_DATA entries here similarly...
    # ...
}

def validate_input(year, month, day, hour, minute):
    current_year = datetime.datetime.now().year
    if not (1900 <= year <= current_year):
        return f"Year must be between 1900 and {current_year}"
    if not (1 <= month <= 12):
        return "Month must be between 1 and 12"
    try:
        max_day = calendar.monthrange(year, month)[1]
        if not (1 <= day <= max_day):
            return f"Day must be between 1 and {max_day} for {calendar.month_name[month]}"
    except:
        return "Invalid month/year combination"
    if not (0 <= hour <= 23):
        return "Hour must be between 0 and 23"
    if not (0 <= minute <= 59):
        return "Minute must be between 0 and 59"
    return None

def calculate_day_master(birth_date):
    base_date = datetime.datetime(1900, 1, 1)
    days_diff = (birth_date - base_date).days
    stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    day_master_index = (days_diff + 6) % 10
    return stems[day_master_index]

def create_four_pillars(birth_date):
    day_master = calculate_day_master(birth_date)
    stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    year_stem = stems[(birth_date.year - 1900 + 6) % 10]
    year_branch = branches[(birth_date.year - 1900 + 6) % 12]
    month_stem = stems[(birth_date.month + stems.index(day_master) + 2) % 10]
    month_branch = branches[(birth_date.month - 1) % 12]
    hour_stem = stems[(birth_date.hour // 2 + stems.index(day_master)) % 10]
    hour_branch = branches[(birth_date.hour // 2) % 12]
    return {
        'year': f"{year_stem}{year_branch}",
        'month': f"{month_stem}{month_branch}",
        'day': f"{day_master}{branches[(stems.index(day_master) + 2) % 12]}",
        'hour': f"{hour_stem}{hour_branch}",
        'day_master': day_master
    }

# Main application title and subtitle
st.markdown('<h1>Day Master Calculator</h1>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">A quiet voice in the scrollstorm — discover your elemental nature through the ancient wisdom of BaZi</div>', unsafe_allow_html=True)

# Sidebar for birth info input
with st.sidebar:
    st.header("Birth Information")
    with st.form("birth_form"):
        current_year = datetime.datetime.now().year
        birth_year = st.number_input("Birth Year", min_value=1900, max_value=current_year, value=1990)
        birth_month = st.number_input("Birth Month", min_value=1, max_value=12, value=1)
        birth_day = st.number_input("Birth Day", min_value=1, max_value=31, value=1)
        col1, col2 = st.columns(2)
        with col1:
            birth_hour = st.number_input("Hour", min_value=0, max_value=23, value=12)
        with col2:
            birth_minute = st.number_input("Minute", min_value=0, max_value=59, value=0)
        timezone_options = [f"GMT{'+' if i >= 0 else ''}{i}" for i in range(-12, 13)]
        selected_timezone = st.selectbox("Time Zone", timezone_options, index=20)  # Default GMT+8
        submit_button = st.form_submit_button("Calculate Day Master")

if submit_button:
    error_message = validate_input(birth_year, birth_month, birth_day, birth_hour, birth_minute)
    if error_message:
        st.markdown(f'<div class="error-message">{error_message}</div>', unsafe_allow_html=True)
    else:
        try:
            birth_datetime = datetime.datetime(birth_year, birth_month, birth_day, birth_hour, birth_minute)
            pillars = create_four_pillars(birth_datetime)
            day_master_key = pillars['day_master']
            day_master_info = DAY_MASTER_DATA[day_master_key]
            
            st.markdown('<div class="success-message">Your Day Master has been calculated successfully</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="pillars-container">
                <div class="pillar-card">
                    <div class="pillar-title">Year Pillar</div>
                    <div class="pillar-content">{pillars['year']}</div>
                    <div class="pillar-description">Ancestry & Foundation</div>
                </div>
                <div class="pillar-card">
                    <div class="pillar-title">Month Pillar</div>
                    <div class="pillar-content">{pillars['month']}</div>
                    <div class="pillar-description">Career & Relationships</div>
                </div>
                <div class="pillar-card">
                    <div class="pillar-title">Day Pillar</div>
                    <div class="pillar-content">{pillars['day']}</div>
                    <div class="pillar-description">Self & Spouse</div>
                </div>
                <div class="pillar-card">
                    <div class="pillar-title">Hour Pillar</div>
                    <div class="pillar-content">{pillars['hour']}</div>
                    <div class="pillar-description">Children & Legacy</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="result-container">
                <div class="day-master-header">
                    <div class="day-master-title">{day_master_info['name']}</div>
                    <div class="day-master-element">{day_master_info['element']} ({day_master_key})</div>
                </div>
                <div class="description-text">{day_master_info['description']}</div>
                <div class="trait-section">
                    <div class="trait-title">Natural Strengths & Positive Traits</div>
                    <div class="trait-list">
                        {"".join([f'<div class="trait-item">{trait}</div>' for trait in day_master_info['positive_traits']])}
                    </div>
                </div>
                <div class="trait-section">
                    <div class="trait-title">Growth Areas & Potential Challenges</div>
                    <div class="trait-list">
                        {"".join([f'<div class="trait-item">{trait}</div>' for trait in day_master_info['challenges']])}
                    </div>
                </div>
                <div class="trait-section">
                    <div class="trait-title">Elemental Harmony & Compatibility</div>
                    <div class="description-text">{day_master_info['compatibility']}</div>
                </div>
                <div class="trait-section">
                    <div class="trait-title">Career Paths & Life Direction</div>
                    <div class="description-text">{day_master_info['career_paths']}</div>
                </div>
                <div class="trait-section">
                    <div class="trait-title">Life Philosophy & Core Values</div>
                    <div class="description-text">{day_master_info['life_philosophy']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("Birth Details & Technical Information"):
                st.write(f"**Complete Birth Information:**")
                st.write(f"Date: {birth_datetime.strftime('%B %d, %Y')}")
                st.write(f"Time: {birth_datetime.strftime('%H:%M')} ({selected_timezone})")
                st.write(f"**Four Pillars:** {pillars['year']} {pillars['month']} {pillars['day']} {pillars['hour']}")
                st.write(f"**Day Master Element:** {day_master_key} ({day_master_info['name']})")
                st.markdown("---")
                st.write("**Important Note:** This calculator uses a simplified algorithm for demonstration purposes. Professional BaZi readings require precise astronomical calculations, solar calendar conversions, and consideration of birth location. For serious life decisions, consult with a qualified BaZi practitioner.")
        except Exception as e:
            st.markdown('<div class="error-message">An error occurred during calculation. Please check your input and try again.</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="instructions">
        <h3>How to Use This Calculator</h3>
        <p>Enter your complete birth information in the sidebar to discover your Day Master - the core element that represents your essential nature according to BaZi astrology.</p>
        <p><strong>What You'll Discover:</strong></p>
        <ul>
            <li>Your Four Pillars of Destiny with detailed explanations</li>
            <li>Comprehensive Day Master analysis with personality insights</li>
            <li>Natural strengths and growth opportunities</li>
            <li>Compatible elements and relationship dynamics</li>
            <li>Career paths aligned with your elemental nature</li>
            <li>Core life philosophy and values</li>
        </ul>
        <p><strong>For Best Results:</strong></p>
        <ul>
            <li>Use your exact birth time including minutes if known</li>
            <li>Select the correct time zone for your birth location</li>
            <li>Remember that BaZi uses solar time, not standard time</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0; font-style: italic; color: #6c757d; font-size: 1.1rem; line-height: 1.6;">
        "The flame flickers in wind, but never forgets it burns."<br>
        <small>— Understanding your Day Master is understanding the element that never changes within you</small>
    </div>
    """, unsafe_allow_html=True)
