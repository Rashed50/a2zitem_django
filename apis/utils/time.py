import calendar
from datetime import datetime, timedelta, time, date
from django.utils.timezone import make_aware, is_aware



def StartDate(date_input):
    """
    Convert various date inputs to timezone-aware datetime at start of day (00:00:00)
    Accepts: string (YYYY-MM-DD), date object, or datetime object
    """
    if isinstance(date_input, str):
        # Check if string contains time component
        if ' ' in date_input or 'T' in date_input:
            date_obj = datetime.fromisoformat(date_input.replace('Z', '+00:00'))
        else:
            date_obj = datetime.strptime(date_input, "%Y-%m-%d")
        date_obj = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
    elif isinstance(date_input, datetime):
        date_obj = date_input.replace(hour=0, minute=0, second=0, microsecond=0)
    else:  # Assume it's a date object
        date_obj = datetime.combine(date_input, time.min)
    
    # Make aware only if not already aware
    if not is_aware(date_obj):
        return make_aware(date_obj)
    return date_obj

def EndDate(date_input):
    """
    Convert various date inputs to timezone-aware datetime at end of day (23:59:59.999999)
    Accepts: string (YYYY-MM-DD), date object, or datetime object
    """
    if isinstance(date_input, str):
        # Check if string contains time component
        if ' ' in date_input or 'T' in date_input:
            date_obj = datetime.fromisoformat(date_input.replace('Z', '+00:00'))
        else:
            date_obj = datetime.strptime(date_input, "%Y-%m-%d")
        date_obj = date_obj.replace(hour=23, minute=59, second=59, microsecond=999999)
    elif isinstance(date_input, datetime):
        date_obj = date_input.replace(hour=23, minute=59, second=59, microsecond=999999)
    else:  # Assume it's a date object
        date_obj = datetime.combine(date_input, time.max)
    
    # Make aware only if not already aware
    if not is_aware(date_obj):
        return make_aware(date_obj)
    return date_obj





def get_last_day_of_month(date_input):
    """
    Get the last day of month from any date input format
    Accepts: string (any format), date object, or datetime object
    Returns: timezone-aware datetime at end of last day of month
    """
    # First convert any input to datetime object
    if isinstance(date_input, str):
        # Try different date formats
        date_formats = [
            "%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y", 
            "%Y/%m/%d", "%b %d, %Y", "%d %b, %Y", "%B %d, %Y"
        ]
        
        date_obj = None
        for fmt in date_formats:
            try:
                date_obj = datetime.strptime(date_input, fmt)
                break
            except ValueError:
                continue
        
        # If standard formats don't work, try fromisoformat
        if date_obj is None:
            try:
                date_obj = datetime.fromisoformat(date_input.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError(f"Unable to parse date string: {date_input}")
                
    elif isinstance(date_input, datetime):
        date_obj = date_input
    elif isinstance(date_input, date):
        date_obj = datetime.combine(date_input, time.min)
    else:
        raise TypeError("Input must be string, date or datetime")
    
    # Calculate last day of month
    year = date_obj.year
    month = date_obj.month
    
    # Get last day number using calendar
    _, last_day_num = calendar.monthrange(year, month)
    
    # Create datetime for last day of month
    last_day = datetime(year, month, last_day_num)
    
    # Make aware if original was aware, otherwise make naive
    if isinstance(date_input, datetime) and is_aware(date_input):
        return make_aware(last_day)
    elif not is_aware(last_day):
        return make_aware(last_day)
    
    return last_day

def get_last_day_of_month_end(date_input):
    """
    Get the last day of month at end of day (23:59:59.999999)
    Accepts: string (any format), date object, or datetime object
    Returns: timezone-aware datetime at end of last day of month
    """
    last_day = get_last_day_of_month(date_input)
    return last_day.replace(hour=23, minute=59, second=59, microsecond=999999)

def get_first_day_of_month(date_input):
    """
    Get the first day of month from any date input format
    Accepts: string (any format), date object, or datetime object
    Returns: timezone-aware datetime at start of first day of month
    """
    # First convert any input to datetime object
    if isinstance(date_input, str):
        date_formats = [
            "%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y", 
            "%Y/%m/%d", "%b %d, %Y", "%d %b, %Y", "%B %d, %Y"
        ]
        
        date_obj = None
        for fmt in date_formats:
            try:
                date_obj = datetime.strptime(date_input, fmt)
                break
            except ValueError:
                continue
        
        if date_obj is None:
            try:
                date_obj = datetime.fromisoformat(date_input.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError(f"Unable to parse date string: {date_input}")
                
    elif isinstance(date_input, datetime):
        date_obj = date_input
    elif isinstance(date_input, date):
        date_obj = datetime.combine(date_input, time.min)
    else:
        raise TypeError("Input must be string, date or datetime")
    
    # First day is always day 1
    first_day = datetime(date_obj.year, date_obj.month, 1)
    
    # Make aware if original was aware, otherwise make naive
    if isinstance(date_input, datetime) and is_aware(date_input):
        return make_aware(first_day)
    elif not is_aware(first_day):
        return make_aware(first_day)
    
    return first_day


"""
##! Last Day of Month Examples
# String formats
print(get_last_day_of_month("2025-10-15"))           # 2025-10-31 00:00:00+06:00
print(get_last_day_of_month("15-10-2025"))           # 2025-10-31 00:00:00+06:00  
print(get_last_day_of_month("10/15/2025"))           # 2025-10-31 00:00:00+06:00
print(get_last_day_of_month("Oct 15, 2025"))         # 2025-10-31 00:00:00+06:00
print(get_last_day_of_month("2025-10-15 14:30:00"))  # 2025-10-31 00:00:00+06:00

# With end of day
print(get_last_day_of_month_end("2025-10-15"))       # 2025-10-31 23:59:59.999999+06:00

# Date and datetime objects
from datetime import date, datetime
print(get_last_day_of_month(date(2025, 10, 15)))     # 2025-10-31 00:00:00+06:00
print(get_last_day_of_month(datetime(2025, 10, 15, 10, 30)))  # 2025-10-31 00:00:00+06:00

# Edge cases
print("\n=== Edge Cases ===")
print(get_last_day_of_month("2024-02-15"))           # 2024-02-29 (leap year)
print(get_last_day_of_month("2025-02-15"))           # 2025-02-28 (non-leap year)
print(get_last_day_of_month("2025-12-15"))           # 2025-12-31
print(get_last_day_of_month("2025-04-15"))           # 2025-04-30

##! First day of month
print("\n=== First Day of Month Examples ===")
print(get_first_day_of_month("2025-10-15"))          # 2025-10-01 00:00:00+06:00
print(get_first_day_of_month("2025-02-28"))          # 2025-02-01 00:00:00+06:00




##! Menual Calculation
# 31 days months
if today.month in [1, 3, 5, 7, 8, 10, 12]:
    last_day = 31
# 30 days months  
elif today.month in [4, 6, 9, 11]:
    last_day = 30
# February
else:
    if (today.year % 4 == 0 and today.year % 100 != 0) or (today.year % 400 == 0):
        last_day = 29  # leap year
    else:
        last_day = 28  # non-leap year

last_day_of_month = today.replace(day=last_day)
"""

