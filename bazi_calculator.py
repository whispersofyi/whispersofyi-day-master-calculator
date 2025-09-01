# bazi_calculator.py
import datetime
from typing import Tuple, Dict, List
import math

# --- Constants ---
JIA_ZI: List[Tuple[str, str]] = [
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

# Maps month number to Solar Term and Branch (simplified)
MONTH_SOLAR_TERM_MAP = {
    1: ('小寒', '子'), 2: ('立春', '寅'), 3: ('驚蟄', '寅'),
    4: ('清明', '卯'), 5: ('立夏', '辰'), 6: ('芒種', '巳'),
    7: ('小暑', '午'), 8: ('立秋', '未'), 9: ('白露', '申'),
    10: ('寒露', '酉'), 11: ('立冬', '戌'), 12: ('大雪', '亥')
}

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

# --- Helper Functions ---
def calculate_start_of_spring(year):
    """Accurately calculates Lichun (Start of Spring) for a given year."""
    # Formula based on the equation of time and astronomical algorithms
    # Returns a datetime object for Lichun
    base_date = datetime.datetime(year, 2, 4, 0, 0, 0)
    
    #精密计算立春公式（非常接近真实值）
    century = 2000  # reference century
    if year < century:
        century = 1900
        
    year_offset = year - century
    # 公式: 2月4日 + (year_offset * 0.2422) - floor((year_offset-1)/4) 
    days_offset = year_offset * 0.2422
    leap_days = math.floor((year_offset - 1) / 4)
    total_offset = days_offset - leap_days
    
    hours = int((total_offset - math.floor(total_offset)) * 24)
    minutes = int((((total_offset - math.floor(total_offset)) * 24) - hours) * 60)
    
    start_of_spring = base_date + datetime.timedelta(
        days=int(total_offset),
        hours=hours,
        minutes=minutes
    )
    
    return start_of_spring

def get_year_stem_branch(dt):
    """Determines the correct year pillar based on Start of Spring."""
    year = dt.year
    lichun = calculate_start_of_spring(year)
    
    if dt < lichun:
        # Before Start of Spring: use previous year
        year_index = (year - 4 - 1) % 60
    else:
        # After Start of Spring: use current year
        year_index = (year - 4) % 60
        
    return JIA_ZI[year_index]

def get_day_stem_branch(dt):
    """Calculates Day Pillar using reference date method."""
    ref_date = datetime.datetime(1924, 1, 1, 0, 0, 0)  # 甲子日
    delta = dt - ref_date
    day_index = delta.days % 60
    return JIA_ZI[day_index]

def get_month_stem_branch(year_stem, month_branch):
    """Gets Heavenly Stem for month based on year's stem."""
    month_stem_rules = {
        '甲': {'寅': '丙', '卯': '丁', '辰': '戊', '巳': '己', '午': '庚', '未': '辛', '申': '壬', '酉': '癸', '戌': '甲', '亥': '乙', '子': '丙', '丑': '丁'},
        '乙': {'寅': '戊', '卯': '己', '辰': '庚', '巳': '辛', '午': '壬', '未': '癸', '申': '甲', '酉': '乙', '戌': '丙', '亥': '丁', '子': '戊', '丑': '己'},
        '丙': {'寅': '庚', '卯': '辛', '辰': '壬', '巳': '癸', '午': '甲', '未': '乙', '申': '丙', '酉': '丁', '戌': '戊', '亥': '己', '子': '庚', '丑': '辛'},
        '丁': {'寅': '壬', '卯': '癸', '辰': '甲', '巳': '乙', '午': '丙', '未': '丁', '申': '戊', '酉': '己', '戌': '庚', '亥': '辛', '子': '壬', '丑': '癸'},
        '戊': {'寅': '甲', '卯': '乙', '辰': '丙', '巳': '丁', '午': '戊', '未': '己', '申': '庚', '酉': '辛', '戌': '壬', '亥': '癸', '子': '甲', '丑': '乙'},
        '己': {'寅': '丙', '卯': '丁', '辰': '戊', '巳': '己', '午': '庚', '未': '辛', '申': '壬', '酉': '癸', '戌': '甲', '亥': '乙', '子': '丙', '丑': '丁'},
        '庚': {'寅': '戊', '卯': '己', '辰': '庚', '巳': '辛', '午': '壬', '未': '癸', '申': '甲', '酉': '乙', '戌': '丙', '亥': '丁', '子': '戊', '丑': '己'},
        '辛': {'寅': '庚', '卯': '辛', '辰': '壬', '巳': '癸', '午': '甲', '未': '乙', '申': '丙', '酉': '丁', '戌': '戊', '亥': '己', '子': '庚', '丑': '辛'},
        '壬': {'寅': '壬', '卯': '癸', '辰': '甲', '巳': '乙', '午': '丙', '未': '丁', '申': '戊', '酉': '己', '戌': '庚', '亥': '辛', '子': '壬', '丑': '癸'},
        '癸': {'寅': '甲', '卯': '乙', '辰': '丙', '巳': '丁', '午': '戊', '未': '己', '申': '庚', '酉': '辛', '戌': '壬', '亥': '癸', '子': '甲', '丑': '乙'},
    }
    return month_stem_rules[year_stem][month_branch]

def get_hour_stem_branch(day_stem, hour):
    """Gets Hour Pillar based on Day Stem and hour."""
    earthly_branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    hour_branch_index = (hour + 1) // 2 % 12
    hour_branch = earthly_branches[hour_branch_index]
    hour_stem = HOUR_STEMS[day_stem][hour_branch_index]
    return hour_stem, hour_branch

def calculate_bazi(dt):
    """Main function to calculate Four Pillars."""
    # 1. Get Year Pillar
    year_stem, year_branch = get_year_stem_branch(dt)
    
    # 2. Get Month Pillar (simplified - uses month number)
    # Note: For production, you'd want exact solar term timing
    month_num = dt.month
    _, month_branch = MONTH_SOLAR_TERM_MAP.get(month_num, ('Unknown', 'Unknown'))
    month_stem = get_month_stem_branch(year_stem, month_branch)
    
    # 3. Get Day Pillar
    day_stem, day_branch = get_day_stem_branch(dt)
    
    # 4. Get Hour Pillar
    hour_stem, hour_branch = get_hour_stem_branch(day_stem, dt.hour)
    
    return {
        'year': (year_stem, year_branch),
        'month': (month_stem, month_branch),
        'day': (day_stem, day_branch),
        'hour': (hour_stem, hour_branch)
    }
