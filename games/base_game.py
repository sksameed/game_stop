# games/base_game.py
import tkinter as tk # Standard tk for Canvas
from tkinter import messagebox
import customtkinter as ctk
from abc import ABC, abstractmethod
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.styles import Fonts
from database.db_manager import get_db_manager


class BaseGame(ABC):
    
    def __init__(self, root, user_data, on_close_callback, game_name):
        self.root = root
        self.user_data = user_data
        self.on_close_callback = on_close_callback
        self.game_name = game_name
        self.db = get_db_manager()
        
        self.score = 0
        self.moves = 0
        self.start_time = None
        
        self.setup_window()
        self.create_header()
        
        # Protocol for window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    
    def setup_window(self):
        self.root.title(self.game_name)
        # self.root.geometry("800x600")
        # self.root.resizable(False, False)
        self.root.after(0, lambda: self.root.state('zoomed'))
        # self.root.configure(bg=...) # Handled by CTk theme
    
    
    def create_header(self):
        header_frame = ctk.CTkFrame(self.root, height=60, corner_radius=0)
        header_frame.pack(fill='x')
        # header_frame.pack_propagate(False) # CTk Frames don't always need this, but good for fixed height
        
        # Game title
        title_label = ctk.CTkLabel(header_frame, text=self.game_name, font=Fonts.title())
        title_label.pack(side='left', padx=20, pady=10)
        
        # Close button
        close_btn = ctk.CTkButton(header_frame, text="Exit", command=self.on_close,
                                 fg_color="#C0392B", hover_color="#922B21", width=80)
        close_btn.pack(side='right', padx=10, pady=10)

        # Score display
        self.score_label = ctk.CTkLabel(header_frame, text="Score: 0", font=Fonts.normal())
        self.score_label.pack(side='right', padx=20, pady=10)
        
        
    def update_score_display(self):
        self.score_label.configure(text=f"Score: {self.score}")
    
    def save_score(self, difficulty=None, time_taken=None, moves_count=None):
        success = self.db.save_game_score(
            user_id=self.user_data['id'],
            game_name=self.game_name,
            score=self.score,
            difficulty=difficulty,
            time_taken=time_taken,
            moves_count=moves_count
        )
        return success
    
    def on_close(self):
        if self.on_close_callback:
            self.on_close_callback()
        self.root.destroy()
    
    @abstractmethod
    def create_game_ui(self):
        pass
    
    @abstractmethod
    def start_game(self):
        pass
    
    @abstractmethod
    def end_game(self):
        pass