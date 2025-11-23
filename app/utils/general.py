from datetime import datetime

def parse_date(date_str):
    """
    Parse ISO date string to Python date object.
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        
    Returns:
        date or None: Date object if parsing succeeds, None otherwise
    """
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None