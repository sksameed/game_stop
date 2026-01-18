def format_score(score):
    """
    Format a score number into a string.
    
    Args:
        score (int/float): The score to format.
        
    Returns:
        str: Formatted score string.
    """
    try:
        return f"{int(score):,}"
    except (ValueError, TypeError):
        return str(score)

def format_time(seconds):
    """
    Format seconds into MM:SS string.
    
    Args:
        seconds (int): Time in seconds.
        
    Returns:
        str: Formatted time string.
    """
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"
