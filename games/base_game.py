# games/base_game.py
import tkinter as tk # Standard tk for Canvas
import customtkinter as ctk
from abc import ABC, abstractmethod
import sys
import os
from typing import Any, Optional, Callable, Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.styles import Fonts
from database.db_manager import get_db_manager


class BaseGame(ABC):
    """
    Abstract base class for all mini-games.
    Handles common window setup, header creation, and score saving.
    """
    
    def __init__(self, root: ctk.CTk, user_data: Dict[str, Any], on_close_callback: Callable[[], None], game_name: str):
        """
        Initialize the base game.

        Args:
            root: The root window (CTk instance).
            user_data: Dictionary containing user information (id, username, etc.).
            on_close_callback: Function to call when the game is closed.
            game_name: Display name of the game.
        """
        self.root = root
        self.user_data = user_data
        self.on_close_callback = on_close_callback
        self.game_name = game_name
        self.db = get_db_manager()
        
        self.score: int = 0
        self.moves: int = 0
        self.start_time: Optional[float] = None
        self.score_label: Optional[ctk.CTkLabel] = None
        
        self.setup_window()
        self.create_header()
        
        # Protocol for window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    
    def setup_window(self) -> None:
        """Configures the game window properties."""
        self.root.title(self.game_name)
        self.root.after(0, lambda: self.root.state('zoomed'))
    
    
    def create_header(self) -> None:
        """Creates the common header with title, score, and exit button."""
        header_frame = ctk.CTkFrame(self.root, height=60, corner_radius=0)
        header_frame.pack(fill='x')
        
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
        
        
    def update_score_display(self) -> None:
        """Updates the score label text."""
        if self.score_label:
            self.score_label.configure(text=f"Score: {self.score}")
    
    def save_score(self, difficulty: str = None, time_taken: float = None, moves_count: int = None) -> bool:
        """
        Saves the game score to the database.

        Args:
            difficulty: Difficulty level (e.g., "Easy", "Hard").
            time_taken: Time taken to complete the game/round in seconds.
            moves_count: Number of moves made (if applicable).

        Returns:
            bool: True if save was successful, False otherwise.
        """
        success = self.db.save_game_score(
            user_id=self.user_data['id'],
            game_name=self.game_name,
            score=self.score,
            difficulty=difficulty,
            time_taken=time_taken,
            moves_count=moves_count
        )
        return success
    
    def on_close(self) -> None:
        """Handles game closure and cleanup."""
        if self.on_close_callback:
            self.on_close_callback()
        self.root.destroy()
    
    @abstractmethod
    def create_game_ui(self) -> None:
        """Create the specific UI elements for the game."""
        pass
    
    @abstractmethod
    def start_game(self) -> None:
        """Start the game logic."""
        pass
    
    @abstractmethod
    def end_game(self) -> None:
        """End the game logic and handle game over state."""
        pass
