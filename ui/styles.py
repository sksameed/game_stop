# ui/styles.py
from config import settings

class Colors:
    PRIMARY = settings.COLOR_PRIMARY
    SECONDARY = settings.COLOR_SECONDARY
    SUCCESS = settings.COLOR_SUCCESS
    DANGER = settings.COLOR_DANGER
    WARNING = settings.COLOR_WARNING
    BACKGROUND = settings.COLOR_BACKGROUND
    TEXT = settings.COLOR_TEXT
    TEXT_LIGHT = settings.COLOR_TEXT_LIGHT

class Fonts:
    FAMILY = "Roboto"
    
    @staticmethod
    def small():
        return (Fonts.FAMILY, 12)
    
    @staticmethod
    def normal():
        return (Fonts.FAMILY, 14)
    
    @staticmethod
    def large():
        return (Fonts.FAMILY, 18)
    
    @staticmethod
    def title():
        return (Fonts.FAMILY, 24, "bold")
    
    @staticmethod
    def header():
        return (Fonts.FAMILY, 32, "bold")

class ButtonStyles:
    PRIMARY = {
        'bg': Colors.PRIMARY,
        'fg': 'white',
        'activebackground': '#34495E',
        'relief': 'flat',
        'cursor': 'hand2',
        'font': (Fonts.FAMILY, 14)
    }
    
    SECONDARY = {
        'bg': Colors.SECONDARY,
        'fg': 'white',
        'activebackground': '#2980B9',
        'relief': 'flat',
        'cursor': 'hand2',
        'font': (Fonts.FAMILY, 14)
    }
    
    SUCCESS = {
        'bg': Colors.SUCCESS,
        'fg': 'white',
        'activebackground': '#229954',
        'relief': 'flat',
        'cursor': 'hand2',
        'font': (Fonts.FAMILY, 14)
    }

    DANGER = {
        'bg': Colors.DANGER,
        'fg': 'white',
        'activebackground': '#C0392B',
        'relief': 'flat',
        'cursor': 'hand2',
        'font': (Fonts.FAMILY, 14)
    }
