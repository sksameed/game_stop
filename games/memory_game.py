# games/memory_game.py
import tkinter as tk
from tkinter import messagebox
import random
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from games.base_game import BaseGame
from ui.styles import Colors, ButtonStyles, Fonts
from config.settings import MEMORY_CARD_COUNTS


class MemoryGame(BaseGame):
    
    def __init__(self, root, user_data, on_close_callback):
        self.difficulty = None
        self.cards = []
        self.card_buttons = []
        self.revealed = []
        self.matched = []
        self.first_card = None
        self.second_card = None
        self.can_click = True
        
        # Card symbols
        self.symbols = ['🎮', '🎯', '🎨', '🎭', '🎪', '🎸', '🎺', '🎹',
                       '⚽', '🏀', '🏈', '⚾', '🎾', '🏐', '🏓', '🏸',
                       '🚗', '🚕', '🚙', '🚌', '🚎', '🏎️', '🚓', '🚑']
        
        super().__init__(root, user_data, on_close_callback, "Memory Card Game")
        self.create_game_ui()
    
    def create_game_ui(self):
        # Difficulty selection
        self.difficulty_frame = tk.Frame(self.root, bg=Colors.BACKGROUND)
        self.difficulty_frame.pack(pady=20)
        
        tk.Label(self.difficulty_frame, text="Select Difficulty:", font=Fonts.large(),
                bg=Colors.BACKGROUND, fg=Colors.PRIMARY).pack(pady=10)
        
        btn_frame = tk.Frame(self.difficulty_frame, bg=Colors.BACKGROUND)
        btn_frame.pack()
        
        for diff in ["Easy", "Medium", "Hard"]:
            pairs = MEMORY_CARD_COUNTS[diff] // 2
            btn = tk.Button(btn_frame, text=f"{diff}\n({pairs} pairs)", width=12,
                           command=lambda d=diff: self.select_difficulty(d),
                           **ButtonStyles.SECONDARY)
            btn.pack(side='left', padx=5)
        
        # Game frame (hidden initially)
        self.game_frame = tk.Frame(self.root, bg=Colors.BACKGROUND)
        
        # Stats display
        self.stats_label = tk.Label(self.root, text="", font=Fonts.normal(),
                                    bg=Colors.BACKGROUND, fg=Colors.TEXT)
        
        # Instructions
        instructions = "Click cards to reveal\nFind matching pairs!"
        tk.Label(self.difficulty_frame, text=instructions, font=Fonts.small(),
                fg=Colors.TEXT_LIGHT, bg=Colors.BACKGROUND).pack(pady=10)
    
    def select_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.difficulty_frame.pack_forget()
        self.game_frame.pack(pady=20)
        self.stats_label.pack(pady=10)
        self.start_game()
    
    def start_game(self):
        self.moves = 0
        self.start_time = time.time()
        self.matched = []
        self.first_card = None
        self.second_card = None
        
        # Get number of pairs
        num_cards = MEMORY_CARD_COUNTS[self.difficulty]
        num_pairs = num_cards // 2
        
        # Create card deck
        self.cards = self.symbols[:num_pairs] * 2
        random.shuffle(self.cards)
        
        # Create card grid
        cols = 4
        rows = (num_cards + cols - 1) // cols
        
        # Clear previous buttons
        for btn in self.card_buttons:
            btn.destroy()
        self.card_buttons = []
        
        # Create buttons
        for i, symbol in enumerate(self.cards):
            row = i // cols
            col = i % cols
            
            btn = tk.Button(self.game_frame, text="?", width=8, height=4,
                           font=('Arial', 20), bg=Colors.SECONDARY, fg='white',
                           command=lambda idx=i: self.reveal_card(idx))
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.card_buttons.append(btn)
        
        self.update_stats()
    
    def reveal_card(self, index):
        if not self.can_click or index in self.matched or index in self.revealed:
            return
        
        # Reveal the card
        self.revealed.append(index)
        self.card_buttons[index].config(text=self.cards[index], bg='white', fg='black')
        
        if self.first_card is None:
            # First card revealed
            self.first_card = index
        elif self.second_card is None:
            # Second card revealed
            self.second_card = index
            self.moves += 1
            self.update_stats()
            
            # Check for match
            self.can_click = False
            self.root.after(1000, self.check_match)
    
    def check_match(self):
        if self.cards[self.first_card] == self.cards[self.second_card]:
            # Match found
            self.matched.extend([self.first_card, self.second_card])
            self.card_buttons[self.first_card].config(state='disabled', bg=Colors.SUCCESS)
            self.card_buttons[self.second_card].config(state='disabled', bg=Colors.SUCCESS)
            
            # Check if game is complete
            if len(self.matched) == len(self.cards):
                self.end_game()
        else:
            # No match - hide cards
            self.card_buttons[self.first_card].config(text="?", bg=Colors.SECONDARY, fg='white')
            self.card_buttons[self.second_card].config(text="?", bg=Colors.SECONDARY, fg='white')
        
        # Reset for next turn
        self.revealed = []
        self.first_card = None
        self.second_card = None
        self.can_click = True
    
    def update_stats(self):
        elapsed = int(time.time() - self.start_time)
        pairs_found = len(self.matched) // 2
        total_pairs = len(self.cards) // 2
        self.stats_label.config(text=f"Moves: {self.moves}  |  Pairs: {pairs_found}/{total_pairs}  |  Time: {elapsed}s")
    
    def end_game(self):
        time_taken = time.time() - self.start_time
        
        # Calculate score
        base_scores = {"Easy": 200, "Medium": 400, "Hard": 600}
        base_score = base_scores[self.difficulty]
        
        # Optimal moves (one per pair)
        optimal_moves = len(self.cards) // 2
        move_penalty = (self.moves - optimal_moves) * 10
        time_penalty = int(time_taken * 3)
        
        self.score = max(50, base_score - move_penalty - time_penalty)
        
        # Save score
        self.save_score(self.difficulty, time_taken, self.moves)
        
        # Show results
        message = (f"Congratulations! You matched all pairs!\n\n"
                  f"Moves: {self.moves}\n"
                  f"Time: {int(time_taken)}s\n"
                  f"Score: {self.score}")
        
        messagebox.showinfo("Game Complete", message)
        self.on_close()