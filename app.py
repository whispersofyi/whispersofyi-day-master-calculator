# app.py
import streamlit as st
import datetime
import calendar
import math

# Page configuration (no emoji/icon)
st.set_page_config(
    page_title="Day Master Calculator - Whispers of YI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal, safe font + color override (system sans-serif) + pillar styling
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif !important;
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    /* Pillar visual */
    .woy-pillar { text-align: center; margin: 1.25rem 0; }
    .woy-pillar .hanzi { display:block; font-size:48px; font-weight:700; line-height:1; }
    .woy-pillar .caption { font-size:0.95rem; color:#444; margin-top:0.25rem; }
    /* Center metrics row */
    .woy-metrics { display:flex; justify-content:center; gap:2rem; align-items:stretch; margin:1rem 0; }
    .woy-metric { text-align:center; min-width:160px; padding:0.5rem 0; border-radius:6px; }
    .woy-metric .title { font-size:0.95rem; color:#333; margin-bottom:0.35rem; }
    .woy-metric .value { font-size:1.35rem; font-weight:600; }
    /* Small responsive tweaks */
    @media (max-width:640px) {
        .woy-metric { min-width:120px; }
        .woy-pillar .hanzi { font-size:36px; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------
# Day Master database (all 10 stems) - kept full content you previously supplied
# ----------------------
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
        "compatibility": "Harmonizes beautifully with Yin Water (癸), which nourishes your growth like gentle rain on fertile soil. Yang Fire (丙) brings warmth and energy that helps you flourish and reach your full potential.",
        "career_paths": "Executive leadership roles, educational administration, environmental conservation, sustainable architecture, construction management, forestry, government service, judicial positions, consulting, organizational development, mentoring and coaching, traditional medicine, and any field requiring ethical leadership and long-term vision.",
        "life_philosophy": "Growth through integrity, strength through service, and wisdom through experience. You believe that true success comes from building something meaningful that will endure long after you're gone."
    },
    "乙": {
        "name": "Yin Wood",
        "element": "Flowing Grass",
        "description": "The Yin Wood day master represents the graceful flexibility of bamboo and the persistent beauty of flowering vines. You possess an remarkable ability to adapt while maintaining your essential nature, bending with life's winds without breaking. Your strength lies not in rigid resistance but in fluid responsiveness - you find ways around obstacles rather than confronting them head-on. Like flowers that bloom in the harshest conditions, you bring beauty and growth to even the most challenging environments. Your diplomacy and natural charm allow you to weave connections between people and ideas, creating harmony where others see only discord.",
        "positive_traits": [
            "Exceptional adaptability that allows you to thrive in diverse environments",
            "Natural diplomatic skills that help resolve conflicts and build bridges",
            "Creative and artistic sensibilities that bring beauty to the world",
            "Excellent networking abilities and talent for building meaningful relationships",
            "Gentle persistence that achieves goals through patience rather than force",
            "Strong intuitive understanding of people and social dynamics",
            "Ability to find creative solutions to complex problems",
            "Natural talent for communication and artistic expression",
            "Capacity to bring out the best in others through encouragement and support",
            "Flexible thinking that embraces multiple perspectives and possibilities"
        ],
        "challenges": [
            "Tendency to be overly accommodating at the expense of your own needs",
            "Difficulty asserting yourself when direct action is necessary",
            "May become indecisive when faced with too many options",
            "Vulnerability to being influenced by stronger personalities",
            "Avoidance of necessary confrontations that could resolve important issues",
            "May scatter energy across too many interests without deep focus",
            "Difficulty setting and maintaining firm boundaries",
            "Tendency to seek approval and validation from others",
            "May compromise your values to maintain harmony",
            "Struggle with self-advocacy in competitive environments"
        ],
        "compatibility": "Thrives with Yang Earth (戊), which provides the stable foundation you need to grow and flourish. Yang Metal (庚) offers structure and definition that helps channel your creative energies into concrete achievements.",
        "career_paths": "Creative arts and design, writing and journalism, counseling and therapy, teaching and education, hospitality and customer service, public relations and marketing, diplomacy and international relations, fashion and beauty, landscape design, social work, and any field requiring creativity, communication, and interpersonal skills.",
        "life_philosophy": "Growth through adaptation, strength through flexibility, and beauty through harmony. You believe that life's greatest achievements come from working with natural flows rather than against them."
    },
    "丙": {
        "name": "Yang Fire",
        "element": "Radiant Sun",
        "description": "The Yang Fire day master embodies the magnificent energy of the sun at its zenith - brilliant, warm, and life-giving. Your presence illuminates every room you enter, and your enthusiasm ignites passion in others. Like the sun that gives life to all things, you possess a generous spirit that nurtures growth and brings out the potential in everyone around you. Your charisma is magnetic, drawing people to your warmth and optimism. You have the rare gift of making others believe in themselves and their dreams. Your energy is infectious, your vision inspiring, and your heart genuinely desires to make the world a brighter place.",
        "positive_traits": [
            "Magnetic charisma that naturally attracts and inspires others",
            "Generous heart with genuine desire to help others succeed",
            "Boundless enthusiasm that energizes teams and organizations",
            "Natural optimism that sees possibilities where others see obstacles",
            "Exceptional public speaking and presentation abilities",
            "Intuitive understanding of what motivates and moves people",
            "Ability to bring energy and excitement to any project or situation",
            "Strong leadership presence that people naturally want to follow",
            "Creative vision that sees the big picture and inspiring possibilities",
            "Genuine warmth that makes others feel valued and appreciated"
        ],
        "challenges": [
            "Tendency toward dramatic expressions that may overwhelm others",
            "Risk of burning out from giving too much energy to too many things",
            "May act impulsively without considering long-term consequences",
            "Possible need for constant attention and recognition",
            "Difficulty with follow-through on projects once initial excitement wanes",
            "May overpromise due to enthusiastic optimism",
            "Struggle with details and mundane but necessary tasks",
            "Tendency to take on too much without realistic planning",
            "May become impatient when progress is slower than expected",
            "Difficulty operating effectively in overly structured or restrictive environments"
        ],
        "compatibility": "Finds perfect balance with Yin Water (癸), which cools and sustains your fire without extinguishing it. Yang Wood (甲) provides steady fuel that allows your energy to burn brightly and consistently over time.",
        "career_paths": "Entertainment and performing arts, motivational speaking and coaching, sales and marketing, leadership and executive roles, broadcasting and media, entrepreneurship, teaching and training, public relations, event planning, sports and athletics, and any field requiring charisma, energy, and the ability to inspire others.",
        "life_philosophy": "Shine brightly and help others discover their own inner light. You believe that life is meant to be lived with passion and that everyone has the potential for greatness waiting to be ignited."
    },
    "丁": {
        "name": "Yin Fire",
        "element": "Focused Flame",
        "description": "The Yin Fire day master represents the concentrated power of a laser beam or the steady glow of a candle that burns through the darkest night. Your intelligence is sharp and penetrating, capable of illuminating truths that others cannot see. Unlike the broad warmth of Yang Fire, your energy is precise and targeted, burning away illusions to reveal essential realities. You possess a rare combination of analytical brilliance and spiritual depth, able to understand both the mechanics of how things work and the deeper meaning of why they exist. Your insights are profound, your research thorough, and your understanding of complex subjects often exceeds that of recognized experts.",
        "positive_traits": [
            "Exceptionally sharp analytical mind that cuts through complexity to find core truths",
            "Precise attention to detail that ensures accuracy and quality in all work",
            "Deep spiritual insight and understanding of life's mysteries",
            "Excellent research abilities with patience for thorough investigation",
            "Capacity for focused concentration that produces breakthrough insights",
            "Natural ability to see patterns and connections others miss",
            "Strong intuitive understanding combined with logical analysis",
            "Talent for specialized work that requires expertise and precision",
            "Ability to work independently with minimal supervision or guidance",
            "Deep wisdom that comes from contemplation and careful study"
        ],
        "challenges": [
            "Tendency to be overly critical of yourself and others' work",
            "May become perfectionistic to the point of paralysis",
            "Possible withdrawal from social situations due to intense focus",
            "Skepticism that may dismiss valuable ideas too quickly",
            "Difficulty seeing the broader context when deeply focused on details",
            "May become impatient with those who don't share your high standards",
            "Tendency to overthink decisions leading to analysis paralysis",
            "Possible isolation due to specialized interests or expertise",
            "May be perceived as aloof or unapproachable by others",
            "Difficulty with tasks that require broad rather than deep focus"
        ],
        "compatibility": "Flourishes with Yin Wood (乙), which provides gentle fuel for your focused energy. Yang Metal (庚) offers structure and discipline that helps channel your analytical abilities into practical achievements.",
        "career_paths": "Scientific research and development, technology and software development, data analysis and statistics, psychology and counseling, writing and editing, investigative journalism, forensic sciences, philosophy and theology, specialized consulting, academic research, and any field requiring deep expertise, analytical thinking, and precision.",
        "life_philosophy": "Seek truth through careful observation and analysis. You believe that understanding leads to wisdom, and that the pursuit of knowledge is one of life's highest callings."
    },
    "戊": {
        "name": "Yang Earth",
        "element": "Solid Mountain",
        "description": "The Yang Earth day master embodies the steadfast permanence of mountains and the fertile abundance of rich soil. You are the foundation upon which others build their dreams, the bedrock of stability in an ever-changing world. Your practical wisdom comes from deep understanding of what truly matters - not fleeting trends or temporary excitement, but enduring values and sustainable growth. Like a mountain that weathers millennia while providing shelter and resources to countless generations, you possess the patience to think in decades rather than days. Your reliability is legendary, your judgment sound, and your ability to accumulate and manage resources makes you a natural steward of wealth and security.",
        "positive_traits": [
            "Unshakeable reliability that others can depend on absolutely",
            "Exceptional practical wisdom applied to real-world challenges",
            "Outstanding financial acumen and resource management abilities",
            "Patient long-term planning perspective that builds lasting success",
            "Natural ability to create stability and security for yourself and others",
            "Strong work ethic with consistent, steady progress toward goals",
            "Excellent judgment in evaluating risks, opportunities, and people",
            "Capacity to remain calm and grounded during crises or uncertainty",
            "Natural understanding of systems, processes, and practical efficiency",
            "Ability to build and maintain valuable assets over time"
        ],
        "challenges": [
            "May be overly conservative and resistant to beneficial changes",
            "Tendency to prioritize security over growth or new opportunities",
            "Possible stubbornness when others challenge your methods or decisions",
            "Risk of becoming too materialistic or focused solely on tangible outcomes",
            "May lack spontaneity or flexibility in responding to unexpected situations",
            "Difficulty with tasks requiring quick decisions or rapid change",
            "Tendency to be skeptical of new ideas or innovative approaches",
            "May appear boring or unimaginative to more dynamic personalities",
            "Possible hoarding tendencies or excessive attachment to possessions",
            "Resistance to taking calculated risks that could accelerate progress"
        ],
        "compatibility": "Benefits from the warmth of Yin Fire (丁), which brings energy and vitality to your stable foundation. Yin Water (癸) provides nourishment and helps your practical nature flourish with renewed growth.",
        "career_paths": "Financial planning and investment management, real estate development and management, construction and engineering, agriculture and resource management, banking and insurance, project management, operations management, accounting and auditing, supply chain management, and any field requiring practical skills, financial acumen, and long-term planning.",
        "life_philosophy": "Build solid foundations that will endure. You believe that true wealth comes from patient accumulation, wise stewardship, and creating security that benefits multiple generations."
    },
    "己": {
        "name": "Yin Earth",
        "element": "Nurturing Soil",
        "description": "The Yin Earth day master represents the fertile, nurturing soil from which all life springs. You possess an remarkable ability to recognize potential in others and create the perfect conditions for their growth and development. Like rich garden soil that transforms seeds into flourishing plants, you have the patience and wisdom to nurture talents and abilities until they reach full bloom. Your strength lies in your understanding that the greatest achievements come not from force but from creating supportive environments where natural growth can occur. You are the teacher who sees brilliance in struggling students, the manager who develops overlooked talent, and the friend who believes in others even when they don't believe in themselves.",
        "positive_traits": [
            "Exceptional ability to nurture and develop the potential in others",
            "Patient, understanding nature that creates safe spaces for growth",
            "Natural teaching and mentoring abilities that transform lives",
            "Intuitive understanding of what others need to succeed",
            "Stable, grounding presence that helps others find their center",
            "Generous spirit that gives freely without expecting returns",
            "Ability to see the good in people even when they can't see it themselves",
            "Excellent listening skills and empathetic understanding",
            "Natural talent for creating harmonious, supportive environments",
            "Deep wisdom about human nature and personal development"
        ],
        "challenges": [
            "Tendency to sacrifice your own needs for others' growth and happiness",
            "May neglect self-care while focusing entirely on supporting others",
            "Possible passivity when decisive action is needed",
            "Vulnerability to being taken advantage of due to generous nature",
            "Difficulty setting healthy boundaries with demanding people",
            "May become depleted from constant giving without receiving",
            "Tendency to enable others rather than encouraging independence",
            "Possible resentment when your support isn't appreciated or reciprocated",
            "Difficulty advocating for yourself or pursuing personal ambitions",
            "May struggle with confrontation even when it's necessary for growth"
        ],
        "compatibility": "Thrives with Yang Fire (丙), which brings energy and vitality that helps you flourish while you nurture others. Yang Water (壬) provides the flow and movement that prevents stagnation in your supportive nature.",
        "career_paths": "Teaching and education, counseling and therapy, social work and community development, healthcare and nursing, human resources and talent development, childcare and family services, nutrition and wellness, agriculture and gardening, organizational development, and any field focused on helping others grow and develop their potential.",
        "life_philosophy": "Growth happens through nurturing care and patient support. You believe that the highest purpose in life is to help others discover and develop their unique gifts and talents."
    },
    "庚": {
        "name": "Yang Metal",
        "element": "Refined Steel",
        "description": "The Yang Metal day master embodies the strength of tempered steel and the precision of a masterfully crafted blade. You possess an unwavering determination that cuts through obstacles and challenges with decisive action. Like a sword forged in fire and shaped by countless hammer blows, you have been strengthened by adversity and refined by experience. Your mind is sharp, your judgment clear, and your ability to make difficult decisions sets you apart as a natural leader in times of crisis. You have the rare courage to do what's right rather than what's easy, and your integrity is as unbreakable as the finest steel.",
        "positive_traits": [
            "Exceptional strength of will and determination to overcome any obstacle",
            "Sharp analytical mind that quickly identifies problems and solutions",
            "Direct, honest communication that people respect even when it's difficult to hear",
            "Outstanding decision-making abilities, especially under pressure",
            "Natural sense of justice and fairness that guides all actions",
            "Courage to take unpopular stands when principles are at stake",
            "Ability to cut through complexity and focus on essential issues",
            "Strong leadership presence that inspires confidence in uncertain times",
            "Excellent crisis management skills with calm, decisive action",
            "Unwavering integrity that makes you completely trustworthy"
        ],
        "challenges": [
            "May be too harsh or critical when dealing with others' mistakes",
            "Difficulty understanding or expressing emotional nuances",
            "Tendency to be inflexible once a decision has been made",
            "Possible insensitivity to others' feelings when focused on results",
            "May create unnecessary conflict through overly direct communication",
            "Difficulty with tasks requiring diplomacy or subtle negotiation",
            "Tendency to judge others by your own high standards",
            "May struggle with patience when others work at different speeds",
            "Possible difficulty delegating due to concerns about quality",
            "May appear intimidating or unapproachable to sensitive individuals"
        ],
        "compatibility": "Finds perfect refinement with Yin Wood (乙), which helps shape and direct your strength toward beautiful and useful purposes. Yin Fire (丁) provides the precise heat needed to temper your abilities into their finest form.",
        "career_paths": "Law enforcement and military leadership, surgical medicine, legal advocacy, engineering and manufacturing, sports and athletics, executive leadership, crisis management, quality control, competitive industries, entrepreneurship, and any field requiring decisive action, strong judgment, and unwavering principles.",
        "life_philosophy": "Strength must be tempered with purpose, and power must serve justice. You believe that true leadership means making the hard choices that others cannot or will not make."
    },
    "辛": {
        "name": "Yin Metal",
        "element": "Precious Jewelry",
        "description": "The Yin Metal day master represents the exquisite beauty of fine jewelry and the precious value of refined craftsmanship. You possess an innate appreciation for quality, elegance, and the finer things in life. Like a rare gem that reveals new facets of beauty under different lights, you have multiple talents and interests that continue to develop throughout your life. Your refined sensibilities and attention to detail create work of exceptional quality and lasting value. You understand that true beauty comes not from flashy display but from subtle perfection and masterful execution. Your diplomatic nature and aesthetic sense make you a natural mediator who can find elegant solutions to complex problems.",
        "positive_traits": [
            "Exceptional attention to detail that ensures quality and precision in all work",
            "Refined aesthetic sense that creates beauty and elegance",
            "Natural diplomatic abilities that resolve conflicts gracefully",
            "High standards that result in work of superior quality",
            "Sophisticated understanding of value, both material and intangible",
            "Excellent taste in design, fashion, and artistic expression",
            "Ability to find elegant solutions to complex problems",
            "Natural talent for creating harmony and beauty in environments",
            "Understanding of quality over quantity principles",
            "Capacity for patience and meticulous craftsmanship"
        ],
        "challenges": [
            "Tendency toward perfectionism that can delay completion of projects",
            "May be overly self-critical and never satisfied with your own achievements",
            "Difficulty making quick decisions due to desire to consider all options",
            "Possible excessive concern with material possessions or status symbols",
            "May lack the boldness needed for breakthrough innovations",
            "Tendency to avoid risks that could lead to valuable opportunities",
            "Possible indecisiveness when faced with imperfect choices",
            "May be overly influenced by others' opinions and external validation",
            "Difficulty with tasks that require quick, rough approximations",
            "Tendency to procrastinate when perfectionist standards seem unattainable"
        ],
        "compatibility": "Sparkles brilliantly with Yang Wood (甲), which provides the strong foundation needed to showcase your refined abilities. Yang Fire (丙) brings the energy and warmth that helps your talents shine brightest.",
        "career_paths": "Jewelry design and luxury goods, fashion and beauty industry, interior design and decoration, fine arts and craftsmanship, quality assurance and consulting, diplomatic services, hospitality and luxury services, marketing and brand management, and any field requiring aesthetic judgment, attention to detail, and refined taste.",
        "life_philosophy": "Excellence is found in the details, and true beauty comes from patient refinement. You believe that life should be lived with grace, quality, and appreciation for the finer things."
    },
    "壬": {
        "name": "Yang Water",
        "element": "Flowing River",
        "description": "The Yang Water day master embodies the dynamic power of rivers and oceans - constantly moving, adapting, and finding new paths toward your destination. You possess remarkable fluidity of thought and action, able to navigate around obstacles with the same natural ease that water flows around rocks. Your wisdom comes from understanding that the softest force can overcome the hardest resistance through persistence and patience. Like water that connects all lands and nourishes all life, you have a natural ability to bring people together and facilitate communication between different groups. Your adaptability is your greatest strength, allowing you to thrive in almost any environment or situation.",
        "positive_traits": [
            "Exceptional adaptability that allows you to thrive in any environment",
            "Natural wisdom that comes from broad experience and observation",
            "Outstanding communication skills that connect diverse people and ideas",
            "Intuitive understanding of human nature and social dynamics",
            "Ability to find creative solutions by thinking around problems",
            "Natural networking abilities that create valuable connections",
            "Fluid intelligence that grasps concepts quickly and completely",
            "Excellent mediating skills that help resolve conflicts peacefully",
            "Capacity to bring out the best in others through understanding and encouragement",
            "Resilient nature that bounces back from setbacks with renewed energy"
        ],
        "challenges": [
            "Tendency to be inconsistent or change direction too frequently",
            "May lack the focus needed for deep specialization",
            "Possible emotional volatility that affects decision-making",
            "Difficulty with long-term commitments that require sustained focus",
            "May avoid taking responsibility for difficult or unpopular decisions",
            "Tendency to go with the flow even when decisive action is needed",
            "Possible manipulation of others through emotional influence",
            "May scatter energy across too many interests without mastering any",
            "Difficulty sticking with projects when initial enthusiasm wanes",
            "Tendency to avoid confrontation even when it's necessary"
        ],
        "compatibility": "Flows beautifully with Yang Earth (戊), which provides the banks and direction that channel your energy toward productive outcomes. Yang Wood (甲) offers stability and purpose that helps focus your adaptable nature.",
        "career_paths": "Communications and media, transportation and logistics, international relations and diplomacy, counseling and social work, sales and marketing, teaching and education, travel and hospitality, consulting and advisory services, and any field requiring adaptability, communication skills, and the ability to work with diverse groups of people.",
        "life_philosophy": "Flow with life's currents while maintaining your essential direction. You believe that wisdom comes from experience and that the greatest strength lies in the ability to adapt while staying true to your core values."
    },
    "癸": {
        "name": "Yin Water",
        "element": "Gentle Rain",
        "description": "The Yin Water day master represents the quiet power of morning dew, gentle rain, and underground springs - subtle yet essential forces that sustain all life. You possess a profound intuitive understanding that penetrates beneath surface appearances to touch the deeper truths of existence. Like rain that falls softly but penetrates to the roots of all growing things, your influence is gentle yet transformative. Your compassionate nature and healing presence bring comfort to those in pain and hope to those in despair. You understand that the greatest changes often come through small, consistent acts of kindness rather than dramatic gestures. Your sensitivity is both your gift and your challenge, allowing you to understand others deeply while sometimes absorbing their pain as your own.",
        "positive_traits": [
            "Profound intuitive understanding that sees beyond surface appearances",
            "Gentle, compassionate nature that heals and comforts others",
            "Exceptional emotional intelligence and empathy",
            "Natural ability to provide emotional support and guidance",
            "Highly adaptable nature that flows with life's changes",
            "Deep spiritual connection and understanding of life's mysteries",
            "Talent for research and investigation that uncovers hidden truths",
            "Ability to work quietly behind the scenes to create positive change",
            "Natural healing presence that brings peace to troubled situations",
            "Subtle influence that transforms people and situations over time"
        ],
        "challenges": [
            "Extreme sensitivity that can be overwhelming in harsh environments",
            "Tendency to absorb others' emotions and problems as your own",
            "May lack assertiveness when direct action is required",
            "Possible avoidance of confrontation even when necessary",
            "Vulnerability to being taken advantage of due to gentle nature",
            "May become overwhelmed by too much emotional stimulation",
            "Difficulty setting boundaries with needy or demanding people",
            "Tendency to withdraw when stressed rather than addressing problems",
            "May underestimate your own strength and capabilities",
            "Possible pessimism or depression when exposed to too much negativity"
        ],
        "compatibility": "Flourishes with Yang Fire (丙), which provides warmth and energy that helps you feel secure and confident. Yin Earth (己) offers the gentle support and understanding that allows your sensitive nature to thrive.",
        "career_paths": "Healthcare and healing professions, counseling and therapy, spiritual guidance and ministry, research and investigation, writing and poetry, social work and humanitarian causes, psychology and mental health, environmental conservation, alternative healing modalities, and any field requiring compassion, intuition, and the ability to help others heal and grow.",
        "life_philosophy": "Healing happens through gentle persistence and compassionate understanding. You believe that everyone has the potential for growth and that small acts of kindness can create profound transformations."
    }
}

# ----------------------
# Solar time helpers (Julian date, EoT, longitude correction)
# ----------------------
def day_of_year(year, month, day):
    date = datetime.date(year, month, day)
    return date.timetuple().tm_yday

def equation_of_time(doy):
    # NOAA-like approximation (minutes)
    B = 2 * math.pi * (doy - 81) / 364.0
    eot = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)
    return eot

def longitude_correction(longitude_deg, timezone_offset_hours):
    # timezone meridian (degrees east)
    tz_meridian = timezone_offset_hours * 15.0
    correction_minutes = (longitude_deg - tz_meridian) / 15.0 * 60.0
    return correction_minutes

def civil_to_apparent_solar(dt_civil, longitude_deg, timezone_offset_hours):
    doy = day_of_year(dt_civil.year, dt_civil.month, dt_civil.day)
    eot = equation_of_time(doy)
    long_corr = longitude_correction(longitude_deg, timezone_offset_hours)
    total_correction = long_corr + eot
    dt_solar = dt_civil + datetime.timedelta(minutes=total_correction)
    return dt_solar, long_corr, eot

def gregorian_to_julian_date(year, month, day, hour=0, minute=0, second=0):
    D = day + (hour + minute/60.0 + second/3600.0)/24.0
    Y = year
    M = month
    if M <= 2:
        Y -= 1
        M += 12
    A = Y // 100
    B = 2 - A + (A // 4)
    jd = math.floor(365.25 * (Y + 4716)) + math.floor(30.6001 * (M + 1)) + D + B - 1524.5
    return jd

def julian_day_number_at_noon(jd):
    return int(math.floor(jd + 0.5))

# ----------------------
# Validation (longitude optional)
# ----------------------
def validate_input(year, month, day, hour, minute, longitude, longitude_enabled):
    current_year = datetime.datetime.now().year
    if not (1900 <= year <= current_year):
        return f"Year must be between 1900 and {current_year}"
    if not (1 <= month <= 12):
        return "Month must be between 1 and 12"
    try:
        max_day = calendar.monthrange(year, month)[1]
        if not (1 <= day <= max_day):
            return f"Day must be between 1 and {max_day}"
    except:
        return "Invalid month/year combination"
    if not (0 <= hour <= 23):
        return "Hour must be between 0 and 23"
    if not (0 <= minute <= 59):
        return "Minute must be between 0 and 59"
    if longitude_enabled:
        if longitude is None:
            return "Longitude required when precise correction is enabled"
        if not (-180.0 <= longitude <= 180.0):
            return "Longitude must be between -180 and 180 degrees"
    return None

# ----------------------
# Sexagenary calculations
# ----------------------
HEAVENLY_STEMS = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
EARTHLY_BRANCHES = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

def calculate_day_master_from_solar(dt_solar):
    jd = gregorian_to_julian_date(dt_solar.year, dt_solar.month, dt_solar.day, dt_solar.hour, dt_solar.minute, dt_solar.second)
    jd_noon = julian_day_number_at_noon(jd)
    stem_idx = ((jd_noon - 1) % 10)
    branch_idx = ((jd_noon + 1) % 12)
    return HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx], jd, jd_noon

def create_four_pillars_from_solar(dt_solar):
    # Year pillar (approx - professional reading would use Li Chun boundaries)
    year_num = dt_solar.year
    sexagenary_year_index = (year_num - 3) % 60
    year_stem = HEAVENLY_STEMS[sexagenary_year_index % 10]
    year_branch = EARTHLY_BRANCHES[sexagenary_year_index % 12]
    # Month pillar (simplified)
    month_branch = EARTHLY_BRANCHES[(dt_solar.month - 1) % 12]
    month_stem_index = (HEAVENLY_STEMS.index(year_stem) + 2 + (dt_solar.month - 1)) % 10
    month_stem = HEAVENLY_STEMS[month_stem_index]
    # Day pillar
    day_stem, day_branch, jd, jd_noon = calculate_day_master_from_solar(dt_solar)
    # Hour pillar
    hour_slot = (dt_solar.hour + 1) // 2
    hour_branch = EARTHLY_BRANCHES[hour_slot % 12]
    hour_stem = HEAVENLY_STEMS[(HEAVENLY_STEMS.index(day_stem) + hour_slot) % 10]
    return {
        "year": f"{year_stem}{year_branch}",
        "month": f"{month_stem}{month_branch}",
        "day": f"{day_stem}{day_branch}",
        "hour": f"{hour_stem}{hour_branch}",
        "day_master": day_stem,
        "jd": jd,
        "jd_noon": jd_noon
    }

# ----------------------
# Timezone utilities (supports .5 offsets)
# ----------------------
def generate_timezone_options():
    opts = []
    # -12.0 to +14.0 inclusive in 0.5 steps
    start = -24  # -12 * 2
    end = 28     # 14 * 2
    for i in range(start, end + 1):
        offset = i * 0.5
        if offset == 0:
            label = "GMT+0"
        else:
            sign = "+" if offset > 0 else ""
            # Format: show .5 for half-hour zones, otherwise integer
            if offset.is_integer():
                label = f"GMT{sign}{int(offset)}"
            else:
                label = f"GMT{sign}{offset:.1f}"
        opts.append(label)
    return opts

def parse_gmt_offset(tz_str):
    # tz_str like "GMT+8", "GMT-3.5", "GMT+0"
    try:
        if tz_str.startswith("GMT"):
            s = tz_str[3:]
            if s == "" or s == "+" or s == "0":
                return 0.0
            return float(s)
    except:
        pass
    return 0.0

# ----------------------
# UI - stable, minimal
# ----------------------
st.title("Day Master Calculator")
st.caption("A quiet voice in the scrollstorm — discover your elemental nature through the ancient wisdom of BaZi")
st.info("This calculator uses longitude correction and the Equation of Time to ensure precise Day Master calculations.")

# Sidebar - inputs and detailed explanation
with st.sidebar:
    st.header("Birth information")
    with st.form("birth_form"):
        current_year = datetime.datetime.now().year
        birth_year = st.number_input("Birth Year", min_value=1900, max_value=current_year, value=1990)
        birth_month = st.number_input("Birth Month", min_value=1, max_value=12, value=1)
        birth_day = st.number_input("Birth Day", min_value=1, max_value=31, value=1)
        col1, col2 = st.columns(2)
        with col1:
            birth_hour = st.number_input("Hour (0–23)", min_value=0, max_value=23, value=12)
        with col2:
            birth_minute = st.number_input("Minute (0–59)", min_value=0, max_value=59, value=0)

        timezone_options = generate_timezone_options()
        default_idx = timezone_options.index("GMT+8") if "GMT+8" in timezone_options else 0
        selected_timezone = st.selectbox("Time zone (GMT offset)", timezone_options, index=default_idx)

        longitude_enabled = st.checkbox("Enable precise longitude (optional)", value=False)
        longitude = None
        if longitude_enabled:
            longitude = st.number_input("Longitude (degrees, E + / W -)", min_value=-180.0, max_value=180.0, value=0.0, step=0.1)

        submit_button = st.form_submit_button("Calculate Day Master")

    # Detailed explanation - single canonical place for education
    with st.expander("About solar-time correction (details)"):
        st.write(
            "Traditional BaZi uses apparent solar time rather than civil clock time. "
            "This tool applies two corrections so the calculated Day Master and hour pillar align with solar time:\n\n"
            "- Longitude correction: adjusts clock time to the timezone meridian (in minutes).\n"
            "- Equation of Time: corrects for Earth's orbital eccentricity and axial tilt (± ~16 minutes through the year).\n\n"
            "If precise longitude is not provided this tool uses the timezone meridian as a practical approximation. "
            "For professional accuracy additional rules (solar-term boundaries such as 立春) may be applied; those are outside this simplified tool."
        )

    st.markdown("---")
    st.markdown("[← Back to Whispers of YI](https://whispersofyi.github.io/)")

# ----------------------
# Main behaviour
# ----------------------
if 'submit_button' not in st.session_state:
    # ensure key exists for some Streamlit versions
    st.session_state['submit_button'] = False

if submit_button:
    # validate inputs
    error_message = validate_input(birth_year, birth_month, birth_day, birth_hour, birth_minute, longitude, longitude_enabled)
    if error_message:
        st.error(error_message)
    else:
        try:
            # civil/local datetime from user input
            civil_dt = datetime.datetime(birth_year, birth_month, birth_day, birth_hour, birth_minute, 0)

            tz_offset = parse_gmt_offset(selected_timezone)  # float hours (e.g., 8.0 or 5.5)

            # choose longitude: if precise enabled use it, otherwise approximate by timezone meridian
            if longitude_enabled and longitude is not None:
                used_longitude = float(longitude)
                longitude_note = "Precise longitude provided"
            else:
                # approximate by timezone meridian (timezone_offset * 15 degrees)
                used_longitude = tz_offset * 15.0
                longitude_note = "Approximate longitude from timezone meridian"

            # compute solar time and corrections
            solar_dt, long_corr, eot = civil_to_apparent_solar(civil_dt, used_longitude, tz_offset)
            total_corr = long_corr + eot

            # compute four pillars using solar time
            pillars = create_four_pillars_from_solar(solar_dt)
            day_master_key = pillars.get("day_master")
            day_master_info = DAY_MASTER_DATA.get(day_master_key)

            st.success("Day Master calculated successfully (solar-time corrected)")
            st.caption("Calculated using longitude correction + Equation of Time (see technical details below).")

            # centered metrics with simple HTML
            st.markdown(f"""
                <div class="woy-metrics">
                  <div class="woy-metric">
                    <div class="title">Longitude Correction</div>
                    <div class="value">{long_corr:+.1f} min</div>
                  </div>
                  <div class="woy-metric">
                    <div class="title">Equation of Time</div>
                    <div class="value">{eot:+.1f} min</div>
                  </div>
                  <div class="woy-metric">
                    <div class="title">Total Correction</div>
                    <div class="value">{total_corr:+.1f} min</div>
                  </div>
                </div>
            """, unsafe_allow_html=True)

            # flags for user guidance
            if abs(total_corr) > 30:
                st.warning("Large time correction applied — this may affect your hour pillar or even the day pillar.")
            elif abs(total_corr) > 15:
                st.info("Moderate time correction applied — results are adjusted for higher accuracy.")

            st.markdown("---")

            # Pillars: centered, hanzi large, english caption
            pillar_rows = [
                ("Year Pillar", pillars["year"], "Ancestry & Foundation"),
                ("Month Pillar", pillars["month"], "Career & Relationships"),
                ("Day Pillar", pillars["day"], "Self & Spouse"),
                ("Hour Pillar", pillars["hour"], "Children & Legacy"),
            ]
            for title, hanzi_val, caption in pillar_rows:
                st.markdown(f"""
                    <div class="woy-pillar">
                      <div style="font-weight:600;">{title}</div>
                      <span class="hanzi">{hanzi_val}</span>
                      <div class="caption">{caption}</div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

            # Day Master analysis (textual)
            if day_master_info:
                st.header(f"{day_master_info['name']} — {day_master_key} ({day_master_info['element']})")
                st.write(day_master_info["description"])

                st.subheader("Natural Strengths & Positive Traits")
                for t in day_master_info["positive_traits"]:
                    st.markdown(f"- {t}")

                st.subheader("Growth Areas & Potential Challenges")
                for t in day_master_info["challenges"]:
                    st.markdown(f"- {t}")

                st.subheader("Elemental Harmony & Compatibility")
                st.write(day_master_info["compatibility"])

                st.subheader("Career Paths & Life Direction")
                st.write(day_master_info["career_paths"])

                st.subheader("Life Philosophy & Core Values")
                st.write(day_master_info["life_philosophy"])
            else:
                st.error("Day Master data unavailable for computed stem.")

            # Technical information (single expander with full diagnostics)
            with st.expander("Birth details & technical information"):
                st.write(f"**Complete birth (civil) time:** {civil_dt.strftime('%B %d, %Y at %H:%M')}")
                st.write(f"**Time zone (GMT offset):** {selected_timezone}")
                st.write(f"**Longitude used:** {used_longitude:.3f}°  — {longitude_note}")
                st.write("")
                st.write(f"**Apparent solar time (applied to calculation):** {solar_dt.strftime('%B %d, %Y at %H:%M:%S')}")
                st.write("")
                st.write("**Solar-time corrections applied (minutes):**")
                st.write(f"- Longitude correction: {long_corr:+.2f} min")
                st.write(f"- Equation of Time: {eot:+.2f} min")
                st.write(f"- Total correction: {total_corr:+.2f} min")
                st.write("")
                st.write("**Four Pillars (based on solar time):**")
                st.write(f"- Year: {pillars['year']}")
                st.write(f"- Month: {pillars['month']}")
                st.write(f"- Day: {pillars['day']}")
                st.write(f"- Hour: {pillars['hour']}")
                st.write("")
                st.write("**Julian date diagnostics used for day-stem:**")
                # calculate JD fractional and JD noon
                jd = pillars.get("jd")
                jd_noon = pillars.get("jd_noon")
                if jd is not None:
                    st.write(f"- JD (fractional): {jd:.6f}")
                    st.write(f"- JD noon integer: {jd_noon}")
                st.markdown("---")
                st.write(
                    "Note: This tool improves day-stem accuracy by converting civil time to apparent solar time. "
                    "For full professional BaZi accuracy you'd also incorporate solar-term boundaries (立春 etc.)."
                )

            # Bottom: privacy and navigation
            st.markdown("---")
            st.markdown("<strong>This calculator does not log or store any personal information.</strong>", unsafe_allow_html=True)
            st.caption("© 2025 Whispers of YI — Code under MIT, Guides under CC BY-NC-ND 4.0")

        except Exception as e:
            st.error(f"An error occurred during calculation: {e}")
            st.write("Please check your input and try again.")
else:
    # Home / instructional view
    st.markdown("## How to use")
    st.write("Enter your birth date and exact time in the sidebar, choose the GMT offset for the birth location (include half-hour offsets where relevant), optionally enable precise longitude, then click 'Calculate Day Master'.")
    st.write("")
    st.markdown("**What you'll get:**")
    st.markdown(
        "- Solar-time conversion (longitude + Equation of Time)\n"
        "- Four Pillars overview based on apparent solar time\n"
        "- Day Master personality analysis and technical diagnostics"
    )

    st.markdown("## Solar-time accuracy — brief")
    st.write("This calculator converts civil time into apparent solar time using longitude correction and the Equation of Time so the day-stem and hour pillar are aligned with the sun. If you require ultimate professional precision, add solar-term boundaries (e.g. 立春) — those are outside the scope of this simple tool.")
    st.markdown("---")
    st.caption("© 2025 Whispers of YI — Code under MIT, Guides under CC BY-NC-ND 4.0")
