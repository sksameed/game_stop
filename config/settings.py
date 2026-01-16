# config/settings.py
import os

# Application Information
APP_NAME = "Mini Game Hub"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Your Name"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "game_hub.db")

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
DASHBOARD_WIDTH = 900
DASHBOARD_HEIGHT = 650

COLOR_PRIMARY = "#2C3E50"
COLOR_SECONDARY = "#3498DB"
COLOR_SUCCESS = "#27AE60"
COLOR_DANGER = "#E74C3C"
COLOR_WARNING = "#F39C12"
COLOR_BACKGROUND = "#ECF0F1"
COLOR_TEXT = "#2C3E50"
COLOR_TEXT_LIGHT = "#7F8C8D"

FONT_FAMILY = "Segoe UI"
FONT_SIZE_SMALL = 10
FONT_SIZE_NORMAL = 12
FONT_SIZE_LARGE = 14
FONT_SIZE_TITLE = 18
FONT_SIZE_HEADER = 24
MAZE_SIZES = {
    "Easy": (10, 10),
    "Medium": (15, 15),
    "Hard": (20, 20)
}

MEMORY_CARD_COUNTS = {
    "Easy": 8,
    "Medium": 12,
    "Hard": 16
}

HANGMAN_CATEGORIES = {
    "Animals": ["elephant", "giraffe", "penguin", "dolphin", "kangaroo", "cheetah"],
    "Countries": ["australia", "brazil", "canada", "germany", "japan", "mexico"],
    "Fruits": ["strawberry", "blueberry", "pineapple", "watermelon", "banana", "orange"],
    "Sports": ["basketball", "football", "tennis", "swimming", "cricket", "volleyball"]
}

HANGMAN_MAX_ATTEMPTS = 6

# Security Configuration
PASSWORD_MIN_LENGTH = 6
PASSWORD_HASH_ROUNDS = 12