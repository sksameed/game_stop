import tkinter as tk
from tkinter import messagebox
import win32api
import winsound
import random
import time
import sys
import os
import customtkinter as ctk
from typing import List, Dict, Any, Callable, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from games.base_game import BaseGame
from ui.styles import Colors, Fonts, ButtonStyles

class SimonGame(BaseGame):
    """
    Simon Says Game Implementation.
    Players must memorize and repeat a sequence of colors/sounds.
    """
    
    def __init__(self, root: ctk.CTk, user_data: Dict[str, Any], on_close_callback: Callable[[], None]):
        """Initialize the Simon Game."""
        self.sequence: List[str] = []
        self.player_sequence: List[str] = []
        self.buttons: Dict[str, ctk.CTkButton] = {} 
        self.game_active: bool = False
        self.showing_sequence: bool = False
        
        # Colors: (Normal, Active/Bright, Frequency)
        self.color_map: Dict[str, Dict[str, Any]] = {
            "green":  {"normal": "#1E8449", "bright": "#2ECC71", "freq": 300},
            "red":    {"normal": "#922B21", "bright": "#E74C3C", "freq": 400},
            "blue":   {"normal": "#2874A6", "bright": "#3498DB", "freq": 500},
            "yellow": {"normal": "#D4AC0D", "bright": "#F1C40F", "freq": 600}
        }
        
        super().__init__(root, user_data, on_close_callback, "Simon Says")
        self.create_game_ui()

    def create_game_ui(self) -> None:
        """Sets up the visual elements for the game."""
        # Top frame for controls
        self.top_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.top_frame.pack(pady=20)
        
        self.status_label = ctk.CTkLabel(self.top_frame, text="Watch the sequence...", 
                                       font=Fonts.large())
        self.status_label.pack(pady=10)
        
        self.start_btn = ctk.CTkButton(self.top_frame, text="Start Game", command=self.start_game,
                                      font=Fonts.normal(), height=40)
        self.start_btn.pack(pady=5)
        
        # Game board (2x2 grid)
        self.board_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.board_frame.pack(expand=True)
        
        positions = [
            ("green", 0, 0), ("red", 0, 1),
            ("yellow", 1, 0), ("blue", 1, 1)
        ]
        
        for color, row, col in positions:
            # Using CTkButton with large corner radius for circular look
            btn = ctk.CTkButton(self.board_frame, text="", width=200, height=200,
                               fg_color=self.color_map[color]["normal"],
                               hover_color=self.color_map[color]["bright"],
                               corner_radius=20)
            btn.grid(row=row, column=col, padx=20, pady=20)
            
            # Bind click
            btn.bind("<Button-1>", lambda e, c=color: self.handle_click(c))
            
            self.buttons[color] = btn

    def start_game(self) -> None:
        """Starts a new game session."""
        self.sequence = []
        self.player_sequence = []
        self.score = 0
        self.game_active = True
        self.start_btn.configure(state='disabled')
        self.start_time = time.time()
        self.update_score_display()
        
        self.next_round()

    def next_round(self) -> None:
        """Proceeds to the next round by adding a step to the sequence."""
        self.player_sequence = []
        self.score = len(self.sequence)
        self.update_score_display()
        
        # Add random color to sequence
        colors = list(self.color_map.keys())
        self.sequence.append(random.choice(colors))
        
        self.status_label.configure(text=f"Round {len(self.sequence)}")
        
        # Play sequence
        self.root.after(1000, self.play_sequence)

    def play_sequence(self) -> None:
        """Plays back the current sequence to the player."""
        self.showing_sequence = True
        delay = 0
        
        for color in self.sequence:
            self.root.after(delay, lambda c=color: self.flash_button(c))
            delay += 800 # 600ms flash + 200ms gap
            
        self.root.after(delay, self.enable_input)

    def flash_button(self, color: str) -> None:
        """
        Visually flashes a button and plays a sound.
        
        Args:
            color: The color key of the button to flash.
        """
        if not self.root: return
        btn = self.buttons[color]
        original_color = self.color_map[color]["normal"]
        bright_color = self.color_map[color]["bright"]
        frequency = self.color_map[color]["freq"]
        
        btn.configure(fg_color=bright_color)
        
        # Sound beep
        try:
            winsound.Beep(frequency, 300)
        except:
            pass
        
        self.root.after(500, lambda: btn.configure(fg_color=original_color))

    def enable_input(self) -> None:
        """Enables player input after sequence display."""
        self.showing_sequence = False
        self.status_label.configure(text="Your Turn!")

    def handle_click(self, color: str) -> None:
        """
        Handle player button click.
        
        Args:
            color: The color clicked.
        """
        if not self.game_active or self.showing_sequence:
            return
        
        self.flash_button(color)
        self.player_sequence.append(color)
        
        # Check correctness
        idx = len(self.player_sequence) - 1
        if self.player_sequence[idx] != self.sequence[idx]:
            self.end_game()
            return
            
        # Check if round complete
        if len(self.player_sequence) == len(self.sequence):
            self.status_label.configure(text="Good Job!")
            self.root.after(1000, self.next_round)

    def end_game(self) -> None:
        """Ends the game and saves score."""
        self.game_active = False
        self.start_btn.configure(state='normal')
        self.status_label.configure(text="Game Over!", text_color=Colors.DANGER)
        
        time_taken = time.time() - self.start_time
        self.save_score("Standard", time_taken, len(self.sequence))
        
        try:
            winsound.Beep(150, 500) # Fail sound
        except:
            pass

        messagebox.showinfo("Game Over", f"Game Over!\nRounds completed: {len(self.sequence) - 1}")
        self.on_close()

    def on_close(self) -> None:
        """Cleanup on close."""
        self.game_active = False
        super().on_close()
