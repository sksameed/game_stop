# database/db_manager.py
import sqlite3
from datetime import datetime
from typing import Optional, List, Tuple, Dict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import DATABASE_PATH
from database import models


class DatabaseManager:
    
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self.initialize_database()
    
    
    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.Connection(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    
    def initialize_database(self) -> None:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(models.CREATE_USERS_TABLE)
                cursor.execute(models.CREATE_GAME_SCORES_TABLE)
                cursor.execute(models.CREATE_USER_STATS_TABLE)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
            raise
    
    
    def create_user(self, username: str, password_hash: str, email: str = None) -> Optional[int]:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(models.INSERT_USER, (username, password_hash, email))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None  # Username or email already exists
        except sqlite3.Error as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(models.GET_USER_BY_USERNAME, (username,))
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
        except sqlite3.Error as e:
            print(f"Error retrieving user: {e}")
            return None
    
    def update_last_login(self, user_id: int) -> bool:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(models.UPDATE_LAST_LOGIN, (user_id,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error updating last login: {e}")
            return False
    
    
    def save_game_score(self, user_id: int, game_name: str, score: int,
                       difficulty: str = None, time_taken: float = None,
                       moves_count: int = None) -> bool:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute(models.INSERT_GAME_SCORE,
                             (user_id, game_name, score, difficulty, time_taken, moves_count))
                
                cursor.execute(models.UPDATE_USER_STATS,
                             (user_id, game_name, score, score, score))
                
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error saving game score: {e}")
            return False
    
    def get_user_high_scores(self, user_id: int) -> List[Dict]:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(models.GET_USER_HIGH_SCORES, (user_id,))
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error retrieving high scores: {e}")
            return []
    
    def get_user_game_stats(self, user_id: int) -> List[Dict]:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(models.GET_USER_GAME_STATS, (user_id,))
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error retrieving game stats: {e}")
            return []
    
    def get_leaderboard(self, game_name: str, limit: int = 10) -> List[Dict]:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                query = models.GET_LEADERBOARD.replace('LIMIT 10', f'LIMIT {limit}')
                cursor.execute(query, (game_name,))
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error retrieving leaderboard: {e}")
            return []


_db_instance = None

def get_db_manager() -> DatabaseManager:
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager()
    return _db_instance