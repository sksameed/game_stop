# games/hangman_game.py
import tkinter as tk
from tkinter import messagebox
import random
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from games.base_game import BaseGame
from ui.styles import Colors, ButtonStyles, Fonts
from config.settings import HANGMAN_CATEGORIES, HANGMAN_MAX_ATTEMPTS


class HangmanGame(BaseGame):
    
    def __init__(self, root, user_data, on_close_callback):
        self.category = None
        self.word = None
        self.guessed_letters = set()
        self.attempts_left = HANGMAN_MAX_ATTEMPTS
        self.letter_buttons = []
        
        super().__init__(root, user_data, on_close_callback, "Hangman Game")
        self.create_game_ui()
    
    
    def create_game_ui(self):
        self.category_frame = tk.Frame(self.root, bg=Colors.BACKGROUND)
        self.category_frame.pack(pady=20)
        
        tk.Label(self.category_frame, text="Select Category:", font=Fonts.large(),
                bg=Colors.BACKGROUND, fg=Colors.PRIMARY).pack(pady=10)
        
        btn_frame = tk.Frame(self.category_frame, bg=Colors.BACKGROUND)
        btn_frame.pack()
        
        for category in HANGMAN_CATEGORIES.keys():
            btn = tk.Button(btn_frame, text=category, width=12,
                           command=lambda c=category: self.select_category(c),
                           **ButtonStyles.SECONDARY)
            btn.pack(side='left', padx=5)
        
        # Game frame (hidden initially)
        self.game_frame = tk.Frame(self.root, bg=Colors.BACKGROUND)
        
        # Hangman drawing area
        self.canvas = tk.Canvas(self.game_frame, width=200, height=250,
                               bg='white', highlightthickness=1,
                               highlightbackground=Colors.PRIMARY)
        self.canvas.pack(pady=10)
        
        # Word display
        self.word_label = tk.Label(self.game_frame, text="", font=('Courier', 24, 'bold'),
                                   bg=Colors.BACKGROUND, fg=Colors.PRIMARY)
        self.word_label.pack(pady=10)
        
        # Category display
        self.category_label = tk.Label(self.game_frame, text="", font=Fonts.normal(),
                                       bg=Colors.BACKGROUND, fg=Colors.TEXT_LIGHT)
        self.category_label.pack()
        
        # Attempts display
        self.attempts_label = tk.Label(self.game_frame, text="", font=Fonts.large(),
                                       bg=Colors.BACKGROUND, fg=Colors.DANGER)
        self.attempts_label.pack(pady=10)
        
        # Letter buttons
        self.letters_frame = tk.Frame(self.game_frame, bg=Colors.BACKGROUND)
        self.letters_frame.pack(pady=10)
        
        # Instructions
        instructions = "Click letters to guess\nGuess the word before running out of attempts!"
        tk.Label(self.category_frame, text=instructions, font=Fonts.small(),
                fg=Colors.TEXT_LIGHT, bg=Colors.BACKGROUND).pack(pady=10)
    
    
    def select_category(self, category):
        self.category = category
        self.category_frame.pack_forget()
        self.game_frame.pack(pady=20)
        self.start_game()
    
    def start_game(self):
        self.start_time = time.time()
        self.guessed_letters = set()
        self.attempts_left = HANGMAN_MAX_ATTEMPTS
        
        self.word = random.choice(HANGMAN_CATEGORIES[self.category]).upper()
        
        self.category_label.config(text=f"Category: {self.category}")
        self.update_word_display()
        self.update_attempts_display()
        self.draw_hangman()
        
        self.create_letter_buttons()
    
    def create_letter_buttons(self):
        for btn in self.letter_buttons:
            btn.destroy()
        self.letter_buttons = []
        
        # Create buttons for A-Z
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i, letter in enumerate(letters):
            row = i // 9
            col = i % 9
            
            btn = tk.Button(self.letters_frame, text=letter, width=3, height=1,
                           font=Fonts.normal(), bg=Colors.SECONDARY, fg='white',
                           command=lambda l=letter: self.guess_letter(l))
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.letter_buttons.append(btn)
    
    def guess_letter(self, letter):
        if letter in self.guessed_letters:
            return
        
        self.guessed_letters.add(letter)
        
        # Disable button
        for btn in self.letter_buttons:
            if btn.cget('text') == letter:
                btn.config(state='disabled', bg=Colors.TEXT_LIGHT)
                break
        
        # Check if letter is in word
        if letter not in self.word:
            self.attempts_left -= 1
            self.update_attempts_display()
            self.draw_hangman()
            
            if self.attempts_left == 0:
                self.end_game(won=False)
                return
        
        self.update_word_display()
        
        # Check if word is complete
        if all(letter in self.guessed_letters for letter in self.word):
            self.end_game(won=True)
    
    def update_word_display(self):
        display = ' '.join(letter if letter in self.guessed_letters else '_' 
                          for letter in self.word)
        self.word_label.config(text=display)
    
    def update_attempts_display(self):
        self.attempts_label.config(text=f"Attempts Left: {self.attempts_left}")
    
    def draw_hangman(self):
        self.canvas.delete('all')
        
        # Base
        self.canvas.create_line(20, 230, 180, 230, width=3)
        
        # Pole
        self.canvas.create_line(50, 230, 50, 20, width=3)
        self.canvas.create_line(50, 20, 130, 20, width=3)
        self.canvas.create_line(130, 20, 130, 50, width=3)
        
        # Draw body parts based on wrong guesses
        wrong_guesses = HANGMAN_MAX_ATTEMPTS - self.attempts_left
        
        if wrong_guesses >= 1:
            # Head
            self.canvas.create_oval(110, 50, 150, 90, width=3)
        if wrong_guesses >= 2:
            # Body
            self.canvas.create_line(130, 90, 130, 150, width=3)
        if wrong_guesses >= 3:
            # Left arm
            self.canvas.create_line(130, 110, 100, 130, width=3)
        if wrong_guesses >= 4:
            # Right arm
            self.canvas.create_line(130, 110, 160, 130, width=3)
        if wrong_guesses >= 5:
            # Left leg
            self.canvas.create_line(130, 150, 110, 190, width=3)
        if wrong_guesses >= 6:
            # Right leg
            self.canvas.create_line(130, 150, 150, 190, width=3)
    
    def end_game(self, won):
        time_taken = time.time() - self.start_time
        
        if won:
            # Calculate score
            base_score = 500
            time_bonus = max(0, 200 - int(time_taken * 2))
            attempts_bonus = self.attempts_left * 50
            self.score = base_score + time_bonus + attempts_bonus
            
            message = (f"Congratulations! You won!\n\n"
                      f"Word: {self.word}\n"
                      f"Time: {int(time_taken)}s\n"
                      f"Attempts Left: {self.attempts_left}\n"
                      f"Score: {self.score}")
            title = "Victory!"
        else:
            self.score = 0
            message = (f"Game Over!\n\n"
                      f"The word was: {self.word}\n"
                      f"Better luck next time!")
            title = "Game Over"
        
        # Save score
        self.save_score(self.category, time_taken, HANGMAN_MAX_ATTEMPTS - self.attempts_left)
        
        # Show results
        messagebox.showinfo(title, message)
        self.on_close()