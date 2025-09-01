import streamlit as st
import datetime
import pytz
from math import floor

# --- Day Master traits database ---
DAY_MASTER_TRAITS = {
    "Jia (Yang Wood)": {
        "element": "Wood",
        "name": "Jia (Yang Wood)",
        "description": "Like a great tree, Jia stands tall, steady, and principled. It seeks growth and expansion, often inspiring others with its integrity.",
        "positive_traits": ["Resilient", "Dependable", "Upright character", "Natural leader"],
        "challenges": ["Can be rigid", "Slow to adapt", "Sometimes stubborn"]
    },
    "Yi (Yin Wood)": {
        "element": "Wood",
        "name": "Yi (Yin Wood)",
        "description": "Like vines and flowers, Yi is flexible, gentle, and persuasive. It adapts with grace and thrives through connection.",
        "positive_traits": ["Adaptable", "Tactful", "Creative", "Diplomatic"],
        "challenges": ["Can be indecisive", "Overly reliant on others", "Prone to worry"]
    },
    "Bing (Yang Fire)": {
        "element": "Fire",
        "name": "Bing (Yang Fire)",
        "description": "Like the sun, Bing radiates warmth, visibility, and energy. It shines brightly, bringing clarity and enthusiasm.",
        "positive_traits": ["Charismatic", "Generous", "Enthusiastic", "Inspiring"],
        "challenges": ["Overbearing at times", "Impatient", "Can burn out quickly"]
    },
    "Ding (Yin Fire)": {
        "element": "Fire",
        "name": "Ding (Yin Fire)",
        "description": "Like a candle flame, Ding is gentle yet persistent. It illuminates quietly, bringing comfort and guidance.",
        "positive_traits": ["Insightful", "Supportive", "Gentle strength", "Warm presence"],
        "challenges": ["Easily affected by environment", "Can be doubtful", "Sometimes withdrawn"]
    },
    "Wu (Yang Earth)": {
        "element": "Earth",
        "name": "Wu (Yang Earth)",
        "description": "Like mountains, Wu is solid, protective, and grounding. It provides stability and endurance.",
        "positive_traits": ["Steadfast", "Responsible", "Protective", "Grounded"],
        "challenges": ["Can be immovable", "Resistant to change", "Overly serious"]
    },
    "Ji (Yin Earth)": {
        "element": "Earth",
        "name": "Ji (Yin Earth)",
        "description": "Like fertile soil, Ji nurtures and supports growth. It is humble, considerate, and resourceful.",
        "positive_traits": ["Caring", "Practical", "Thoughtful", "Supportive"],
        "challenges": ["Can overextend for others", "Worries too much", "Sometimes insecure"]
    },
    "Geng (Yang Metal)": {
        "element": "Metal",
        "name": "Geng (Yang Metal)",
        "description": "Like solid steel, Geng is strong, determined, and unyielding. It represents discipline and courage.",
        "positive_traits": ["Courageous", "Disciplined", "Determined", "Loyal"],
        "challenges": ["Can be inflexible", "Harsh at times", "Overly strict"]
    },
    "Xin (Yin Metal)": {
        "element": "Metal",
        "name": "Xin (Yin Metal)",
        "description": "Like fine jewelry, Xin is refined, elegant, and precise. It values beauty, clarity, and sophistication.",
        "positive_traits": ["Charming", "Refined", "Detail-oriented", "Graceful"],
        "challenges": ["Can be vain", "Overly critical", "Easily hurt"]
    },
    "Ren (Yang Water)": {
        "element": "Water",
        "name": "Ren (Yang Water)",
        "description": "Like the ocean, Ren is vast, deep, and resourceful. It symbolizes wisdom, adaptability, and flow.",
        "positive_traits": ["Resourceful", "Wise", "Adventurous", "Adaptable"],
        "challenges": ["Can be overwhelming", "Restless", "Hard to contain"]
    },
    "Gui (Yin Water)": {
        "element": "Water",
        "name": "Gui (Yin Water)",
        "description": "Like morning dew, Gui is subtle, gentle, and nurturing. It symbolizes sensitivity, intuition, and renewal.",
        "positive_traits": ["Intuitive", "Gentle", "Compassionate", "Perceptive"],
        "challenges": ["Can be elusive", "Overly emotional", "Easily influenced"]
    }
}

# --- Core calculation functions ---
def julian_day(dt):
    """Calculate Julian Day from UTC datetime."""
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour + dt.minute/60.0

    if month <= 2:
        year -= 1
        month += 12

    A = floor(year/100)
    B = 2 - A + floor(A/4)
    jd = floor(365.25*(year + 4716)) + floor(30.6001*(month + 1)) + day + B - 1524.5
    jd += hour / 24.0
    return jd

def get_day_master(year, month, day, hour, minute, tz_str):
    tz = pytz.timezone(tz_str)
    local_dt = datetime.datetime(year, month, day, hour, minute)
    local_dt = tz.localize(local_dt)
    dt_utc = local_dt.astimezone(pytz.utc)

    jd = julian_day(dt_utc)
    jd_noon = floor(jd + 0.5)

    # Day Stem calculation
    day_stem_index = (jd_noon + 9) % 10
    stems = ["Jia (Yang Wood)", "Yi (Yin Wood)", "Bing (Yang Fire)", "Ding (Yin Fire)",
             "Wu (Yang Earth)", "Ji (Yin Earth)", "Geng (Yang Metal)", "Xin (Yin Metal)",
             "Ren (Yang Water)", "Gui (Yin Water)"]

    return stems[day_stem_index], dt_utc, jd, jd_noon

# --- Streamlit UI ---
st.set_page_config(page_title="Day Master Calculator", page_icon="✨", layout="wide")

st.markdown(
    """
    <style>
    body { background-color: #ffffff; color: #000000; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align:center;'>✨ Day Master Calculator ✨</h1>", unsafe_allow_html=True)

# --- Input form ---
with st.form("birth_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.number_input("Year", min_value=1900, max_value=2100, value=1990)
    with col2:
        month = st.number_input("Month", min_value=1, max_value=12, value=1)
    with col3:
        day = st.number_input("Day", min_value=1, max_value=31, value=1)

    col4, col5, col6 = st.columns(3)
    with col4:
        hour = st.number_input("Hour", min_value=0, max_value=23, value=12)
    with col5:
        minute = st.selectbox("Minute", options=[0, 15, 30, 45], index=0)
    with col6:
        tz = st.selectbox("Timezone", pytz.all_timezones, index=pytz.all_timezones.index("Asia/Shanghai"))

    submitted = st.form_submit_button("Calculate Day Master")

# --- Process form ---
if submitted:
    try:
        day_master_key, dt_utc, jd, jd_noon = get_day_master(year, month, day, hour, minute, tz)
        day_master_info = DAY_MASTER_TRAITS.get(day_master_key, {})

        # --- Results layout ---
        col_left, col_right = st.columns([2, 1.2])

        # LEFT
        with col_left:
            st.subheader("Four Pillars")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Year Pillar**")
                st.write("N/A")
                st.markdown("**Month Pillar**")
                st.write("N/A")
            with c2:
                st.markdown("**Day Pillar**")
                st.write(day_master_key)
                st.markdown("**Hour Pillar**")
                st.write("N/A")

            st.markdown("---")
            with st.expander("Birth Details & Technical Information"):
                local_dt = datetime.datetime(year, month, day, hour, minute)
                st.write("**Entered (local) birth:**")
                st.write(f"- Date: {local_dt.strftime('%Y-%m-%d')}")
                st.write(f"- Time (local): {local_dt.strftime('%H:%M')} ({tz})")
                st.write("")
                st.write("**Converted to UTC for calculation:**")
                st.write(f"- UTC: {dt_utc.strftime('%Y-%m-%d %H:%M')} (UTC)")
                st.write("")
                st.write("**Julian info used for Day Stem calculation:**")
                st.write(f"- JD (fractional): {jd:.6f}")
                st.write(f"- JD noon integer: {jd_noon}")

        # RIGHT (styled card)
        with col_right:
            strengths_html = "".join(
                [f'<div style="padding:6px 0;border-bottom:1px solid #f0f0f0;">{t}</div>'
                 for t in day_master_info.get("positive_traits", [])]
            ) or '<div style="color:#666">No strengths available.</div>'

            challenges_html = "".join(
                [f'<div style="padding:6px 0;border-bottom:1px solid #f0f0f0;">{t}</div>'
                 for t in day_master_info.get("challenges", [])]
            ) or '<div style="color:#666">No challenges available.</div>'

            right_card = f"""
            <div style="
                background: #ffffff;
                color: #000000;
                border: 1px solid rgba(0,0,0,0.15);
                border-radius: 14px;
                padding: 18px;
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            ">
              <div style="text-align:center; margin-bottom:10px;">
                <div style="font-size:19px; font-weight:700;">{day_master_info.get('name', day_master_key)}</div>
                <div style="color: #222; margin-top:4px;">{day_master_key} — {day_master_info.get('element','')}</div>
              </div>

              <div style="margin-top:10px; font-size:13px; line-height:1.4; color:#111;">
                {day_master_info.get('description','')}
              </div>

              <div style="margin-top:14px;">
                <div style="font-weight:700; margin-bottom:6px;">Strengths</div>
                {strengths_html}
              </div>

              <div style="margin-top:14px;">
                <div style="font-weight:700; margin-bottom:6px;">Growth Areas / Challenges</div>
                {challenges_html}
              </div>

              <div style="margin-top:16px; text-align:center; font-size:11px; color:#555; border-top:1px solid #eee; padding-top:6px;">
                Whispers of Yi · Elemental Reflections
              </div>
            </div>
            """
            st.markdown(right_card, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {e}")
