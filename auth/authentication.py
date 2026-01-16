# auth/authentication.py
from typing import Optional, Tuple, Dict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import get_db_manager
from auth.password_handler import hash_password, verify_password
from config.settings import PASSWORD_MIN_LENGTH


class AuthenticationManager:
    
    def __init__(self):
        self.db = get_db_manager()
    
    
    def register_user(self, username: str, password: str, email: str = None) -> Tuple[bool, str]:
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
        if len(username) > 50:
            return False, "Username must be less than 50 characters"
        
        if not password or len(password) < PASSWORD_MIN_LENGTH:
            return False, f"Password must be at least {PASSWORD_MIN_LENGTH} characters long"
        
        if email and '@' not in email:
            return False, "Invalid email address"
        
        # Check if username already exists
        if self.db.get_user_by_username(username):
            return False, "Username already exists"
        
        # Hash password and create user
        password_hash = hash_password(password)
        user_id = self.db.create_user(username, password_hash, email)
        
        if user_id:
            return True, "Registration successful!"
        else:
            return False, "Registration failed. Please try again."
    
    def login_user(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        if not username or not password:
            return False, "Please enter both username and password", None
        
        user = self.db.get_user_by_username(username)
        
        if not user:
            return False, "Invalid username or password", None
        
        if not verify_password(password, user['password_hash']):
            return False, "Invalid username or password", None
        
        self.db.update_last_login(user['id'])
        
        # Return user data without password hash
        user_data = {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'created_at': user['created_at'],
            'last_login': user['last_login']
        }
        
        return True, "Login successful!", user_data


# Singleton instance
_auth_instance = None

def get_auth_manager() -> AuthenticationManager:
    global _auth_instance
    if _auth_instance is None:
        _auth_instance = AuthenticationManager()
    return _auth_instance