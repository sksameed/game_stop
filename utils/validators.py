# utils/validators.py
import re
from typing import Tuple


def validate_username(username: str) -> Tuple[bool, str]:
    if not username:
        return False, "Username cannot be empty"
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    
    if len(username) > 50:
        return False, "Username must be less than 50 characters"
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    
    return True, ""


def validate_password(password: str, min_length: int = 6) -> Tuple[bool, str]:
    if not password:
        return False, "Password cannot be empty"
    
    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters"
    
    if len(password) > 100:
        return False, "Password is too long"
    
    return True, ""


def validate_email(email: str) -> Tuple[bool, str]:
    if not email:
        return True, ""  # Email is optional
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        return False, "Invalid email format"
    
    if len(email) > 100:
        return False, "Email is too long"
    
    return True, ""