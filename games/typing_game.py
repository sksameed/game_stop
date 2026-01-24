import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import random
import time
import sys
import os
import json
import math
from typing import List, Dict, Any, Callable, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from games.base_game import BaseGame
from ui.styles import Colors, Fonts, ButtonStyles

class TypingGame(BaseGame):
    """
    Typing Defense Game.
    Players must type falling words before they hit the bottom.
    """
    
    def __init__(self, root: ctk.CTk, user_data: Dict[str, Any], on_close_callback: Callable[[], None]):
        """Initialize the Typing Game."""
        self.active_words: List[Dict[str, Any]] = [] 
        # List of {"word": str, "x": int, "y": int, "id": canvas_id}
        
        self.falling_speed: int = 1
        self.spawn_rate: int = 2000 # ms
        self.game_loop_id: Optional[str] = None
        self.spawn_loop_id: Optional[str] = None
        self.lives: int = 3
        self.current_input: str = ""
        self.canvas: Optional[tk.Canvas] = None
        
        # Stats
        self.correct_words: int = 0
        self.start_time: float = 0
        self.wpm: int = 0
        
        self.load_words()
        
        super().__init__(root, user_data, on_close_callback, "Typing Defense")
        self.create_game_ui()

    def load_words(self) -> None:
        """Loads words from JSON asset file."""
        try:
            asset_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'words.json')
            with open(asset_path, 'r') as f:
                self.words_list = json.load(f)
        except Exception as e:
            print(f"Error loading words: {e}")
            # Fallback list
            self.words_list = ["error", "loading", "words", "fallback", "mode"]

    def create_game_ui(self) -> None:
        """Creates the UI elements."""
        # Difficulty selection
        self.difficulty_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.difficulty_frame.pack(pady=20)
        
        ctk.CTkLabel(self.difficulty_frame, text="Select Difficulty:", font=Fonts.large()).pack(pady=10)
        
        btn_frame = ctk.CTkFrame(self.difficulty_frame, fg_color="transparent")
        btn_frame.pack()
        
        for diff in ["Easy", "Medium", "Hard"]:
            btn = ctk.CTkButton(btn_frame, text=diff,
                               command=lambda d=diff: self.start_game(d),
                               width=120, height=40)
            btn.pack(side='left', padx=10)
            
        # Instructions
        instructions = ("Type the words before they hit the bottom!\n"
                       "Just type the letters.\n"
                       "You have 3 lives.")
        ctk.CTkLabel(self.difficulty_frame, text=instructions, font=Fonts.small(),
                    text_color="gray").pack(pady=20)

        # Game Container (Hidden initially)
        self.game_container = ctk.CTkFrame(self.root, fg_color="transparent")
        
        # Stats bar
        self.stats_label = ctk.CTkLabel(self.game_container, text="", font=Fonts.normal())
        self.stats_label.pack(pady=5)
        
        # Use standard canvas for game rendering as it's more flexible for moving text
        self.canvas = tk.Canvas(self.game_container, width=800, height=500,
                               bg='#2C3E50', highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Current input display
        self.input_label = ctk.CTkLabel(self.game_container, text="Type here...", font=Fonts.large(),
                                      fg_color=Colors.SECONDARY, text_color='white', width=300, height=50,
                                      corner_radius=10)
        self.input_label.pack(pady=10)

    def start_game(self, difficulty: str = "Medium") -> None:
        """
        Starts the game with selected difficulty.
        
        Args:
            difficulty: "Easy", "Medium", or "Hard".
        """
        self.difficulty = difficulty
        self.difficulty_frame.pack_forget()
        self.game_container.pack(fill='both', expand=True)
        
        # Setup difficulty params
        if difficulty == "Easy":
            self.falling_speed = 1
            self.spawn_rate = 2000
        elif difficulty == "Medium":
            self.falling_speed = 2
            self.spawn_rate = 1500
        else:
            self.falling_speed = 3
            self.spawn_rate = 1000
            
        self.score = 0
        self.lives = 3
        self.active_words = []
        self.current_input = ""
        self.correct_words = 0
        self.start_time = time.time()
        
        self.update_stats()
        self.update_input_display()
        
        # Bind keys
        self.root.bind('<Key>', self.handle_keypress)
        self.root.bind('<BackSpace>', lambda e: self.handle_backspace())
        self.root.focus_set()
        
        # Start loops
        self.spawn_word()
        self.game_loop()

    def spawn_word(self) -> None:
        """Spawns a new random word at the top of the canvas."""
        # Pick random word
        word = random.choice(self.words_list)
        x_pos = random.randint(50, 750)
        y_pos = 0
        
        text_id = self.canvas.create_text(x_pos, y_pos, text=word, fill='white',
                                        font=("Courier", 16, "bold"), anchor='n')
        
        self.active_words.append({
            "word": word,
            "id": text_id,
            "x": x_pos,
            "y": y_pos
        })
        
        # Schedule next spawn
        self.spawn_loop_id = self.root.after(self.spawn_rate, self.spawn_word)

    def game_loop(self) -> None:
        """Main game loop for updating positions and checking collisions."""
        # Move words down
        to_remove = []
        canvas_height = 500
        
        for w in self.active_words:
            w['y'] += self.falling_speed
            self.canvas.coords(w['id'], w['x'], w['y'])
            
            # Check collision with bottom
            if w['y'] > canvas_height:
                self.lives -= 1
                self.canvas.delete(w['id'])
                to_remove.append(w)
                self.flash_damage()
        
        for w in to_remove:
            if w in self.active_words:
                self.active_words.remove(w)
        
        self.update_wpm()
        self.update_stats()
        
        if self.lives <= 0:
            self.end_game()
            return
            
        self.game_loop_id = self.root.after(30, self.game_loop)

    def handle_keypress(self, event: tk.Event) -> None:
        """Handles character input."""
        if not event.char or len(event.char) > 1:
            return
        
        # Add char to input
        if event.char.isalpha():
            self.current_input += event.char.lower()
            self.update_input_display()
            self.check_input_match()

    def handle_backspace(self) -> None:
        """Handles backspace input."""
        self.current_input = self.current_input[:-1]
        self.update_input_display()

    def check_input_match(self) -> None:
        """Checks if the typed input matches any active word."""
        # Check if current input matches any active word
        matched_word = None
        
        for w in self.active_words:
            if w['word'] == self.current_input:
                matched_word = w
                break
        
        if matched_word:
            # Success!
            self.score += len(matched_word['word']) * 10
            self.correct_words += 1
            self.canvas.delete(matched_word['id'])
            self.active_words.remove(matched_word)
            self.current_input = ""
            self.update_input_display()
            
            self.show_success_effect(matched_word['x'], matched_word['y'])

    def show_success_effect(self, x: int, y: int) -> None:
        """
        Shows a particle explosion effect at given coordinates.
        
        Args:
            x: X coordinate.
            y: Y coordinate.
        """
        # Particle explosion effect
        particles = []
        for _ in range(8):
            dx = random.randint(-20, 20)
            dy = random.randint(-20, 20)
            p = self.canvas.create_oval(x, y, x+4, y+4, fill=Colors.SUCCESS, outline="")
            particles.append((p, dx, dy))
            
        def update_particles(step=0):
            if step > 10:
                for p, _, _ in particles:
                    self.canvas.delete(p)
                return
            
            for p, dx, dy in particles:
                self.canvas.move(p, dx/2, dy/2)
                
            self.root.after(50, lambda: update_particles(step+1))
            
        update_particles()

    def flash_damage(self) -> None:
        """Flashes the screen red to indicate damage."""
        original_bg = self.canvas.cget('bg')
        self.canvas.configure(bg=Colors.DANGER)
        self.root.after(100, lambda: self.canvas.configure(bg=original_bg))

    def update_input_display(self) -> None:
        """Updates the input label with current text and validation color."""
        self.input_label.configure(text=self.current_input or "Type here...")
        
        # Highlight logic
        is_prefix = any(w['word'].startswith(self.current_input) for w in self.active_words)
        if self.current_input and not is_prefix:
            self.input_label.configure(fg_color=Colors.DANGER)
        else:
            self.input_label.configure(fg_color=Colors.SECONDARY)

    def update_wpm(self) -> None:
        """Calculates and updates WPM."""
        elapsed_min = (time.time() - self.start_time) / 60
        if elapsed_min > 0:
            self.wpm = int(self.correct_words / elapsed_min)

    def update_stats(self) -> None:
        """Updates the status bar."""
        self.stats_label.configure(text=f"Score: {self.score}  |  Lives: {'❤️' * self.lives}  |  WPM: {self.wpm}")
        self.score_label.configure(text=f"Score: {self.score}")

    def end_game(self) -> None:
        """Ends the game, stops loops and saves score."""
        # Stop loops
        if self.spawn_loop_id:
            self.root.after_cancel(self.spawn_loop_id)
        if self.game_loop_id:
            self.root.after_cancel(self.game_loop_id)
            
        self.update_stats()
        try:
            self.root.unbind('<Key>')
        except:
            pass
        
        time_taken = time.time() - self.start_time
        self.save_score(self.difficulty, time_taken, self.score)
        
        msg = f"Game Over!\n\nScore: {self.score}\nWPM: {self.wpm}\nTime: {int(time_taken)}s"
        messagebox.showinfo("Game Over", msg)
        self.on_close()

    def on_close(self) -> None:
        """Cleanup on close."""
        if self.spawn_loop_id:
            self.root.after_cancel(self.spawn_loop_id)
        if self.game_loop_id:
            self.root.after_cancel(self.game_loop_id)
        super().on_close()
