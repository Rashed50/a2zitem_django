def truncate_string(value, max_length=100):
    """Helper function to truncate string to max_length"""
    if value is None:
        return ""
    
    # Convert to string first in case it's not a string
    str_value = str(value) if value is not None else ""
    
    if len(str_value) > max_length:
        return str_value[:max_length]
    return str_value