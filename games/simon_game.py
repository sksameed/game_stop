import tkinter as tk
from tkinter import messagebox
import random
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from games.base_game import BaseGame
from ui.styles import Colors, Fonts, ButtonStyles

class SimonGame(BaseGame):
    def __init__(self, root, user_data, on_close_callback):
        self.sequence = []
        self.player_sequence = []
        self.buttons = {} # key: color_name, value: widget
        self.game_active = False
        self.showing_sequence = False
        
        # Colors: (Normal, Active/Bright)
        self.color_map = {
            "green": ("#27AE60", "#00FF00"),  # Normal -> Lime
            "red": ("#C0392B", "#FF0000"),    # Normal -> Pure Red
            "blue": ("#2980B9", "#00BFFF"),   # Normal -> Deep Sky Blue
            "yellow": ("#F39C12", "#FFFF00")  # Normal -> Yellow
        }
        
        super().__init__(root, user_data, on_close_callback, "Simon Says")
        self.create_game_ui()

    def create_game_ui(self):
        # Top frame for controls
        self.top_frame = tk.Frame(self.root, bg=Colors.BACKGROUND)
        self.top_frame.pack(pady=20)
        
        self.status_label = tk.Label(self.top_frame, text="Watch the sequence...", font=Fonts.large(),
                                   bg=Colors.BACKGROUND, fg=Colors.TEXT)
        self.status_label.pack(pady=10)
        
        self.start_btn = tk.Button(self.top_frame, text="Start Game", command=self.start_game,
                                  **ButtonStyles.PRIMARY)
        self.start_btn.pack(pady=5)
        
        # Game board (2x2 grid)
        self.board_frame = tk.Frame(self.root, bg=Colors.BACKGROUND)
        self.board_frame.pack(expand=True)
        
        positions = [
            ("green", 0, 0), ("red", 0, 1),
            ("yellow", 1, 0), ("blue", 1, 1)
        ]
        
        for color, row, col in positions:
            # Using Canvas for circular buttons feeling or just colored frames
            # Let's use simple Frames or Labels used as buttons for filling space
            btn = tk.Canvas(self.board_frame, width=200, height=200, 
                           bg=self.color_map[color][0], highlightthickness=0)
            btn.grid(row=row, column=col, padx=10, pady=10)
            
            # Bind click
            btn.bind("<Button-1>", lambda e, c=color: self.handle_click(c))
            
            self.buttons[color] = btn

    def start_game(self):
        self.sequence = []
        self.player_sequence = []
        self.score = 0
        self.game_active = True
        self.start_btn.config(state='disabled')
        self.start_time = time.time()
        self.update_score_display()
        
        self.next_round()

    def next_round(self):
        self.player_sequence = []
        self.score = len(self.sequence)
        self.update_score_display()
        
        # Add random color to sequence
        colors = list(self.color_map.keys())
        self.sequence.append(random.choice(colors))
        
        self.status_label.config(text=f"Round {len(self.sequence)}")
        
        # Play sequence
        self.root.after(1000, self.play_sequence)

    def play_sequence(self):
        self.showing_sequence = True
        delay = 0
        
        for color in self.sequence:
            self.root.after(delay, lambda c=color: self.flash_button(c))
            delay += 800 # 600ms flash + 200ms gap
            
        self.root.after(delay, self.enable_input)

    def flash_button(self, color):
        if not self.root: return
        btn = self.buttons[color]
        original_color = self.color_map[color][0]
        bright_color = self.color_map[color][1]
        
        btn.config(bg=bright_color)
        # Optional: Sound beep here
        
        self.root.after(500, lambda: btn.config(bg=original_color))

    def enable_input(self):
        self.showing_sequence = False
        self.status_label.config(text="Your Turn!")

    def handle_click(self, color):
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
            self.status_label.config(text="Good Job!")
            self.root.after(1000, self.next_round)

    def end_game(self):
        self.game_active = False
        self.start_btn.config(state='normal')
        self.status_label.config(text="Game Over!", fg=Colors.DANGER)
        
        time_taken = time.time() - self.start_time
        self.save_score("Standard", time_taken, len(self.sequence))
        
        messagebox.showinfo("Game Over", f"Game Over!\nRounds completed: {len(self.sequence) - 1}")
        self.on_close()

    def on_close(self):
        self.game_active = False
        super().on_close()
