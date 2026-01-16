# auth/password_handler.py
import bcrypt
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import PASSWORD_HASH_ROUNDS


class PasswordHandler:
    
    @staticmethod
    def hash_password(password: str) -> str:
        password_bytes = password.encode('utf-8')
        
        salt = bcrypt.gensalt(rounds=PASSWORD_HASH_ROUNDS)
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        try:
            password_bytes = password.encode('utf-8')
            hash_bytes = password_hash.encode('utf-8')
            
            return bcrypt.checkpw(password_bytes, hash_bytes)
        except Exception as e:
            print(f"Password verification error: {e}")
            return False


def hash_password(password: str) -> str:
    return PasswordHandler.hash_password(password)


def verify_password(password: str, password_hash: str) -> bool:
    return PasswordHandler.verify_password(password, password_hash)