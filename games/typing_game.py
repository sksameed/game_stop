import tkinter as tk
from tkinter import messagebox
import random
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from games.base_game import BaseGame
from ui.styles import Colors, Fonts, ButtonStyles

# Word list for the game
WORDS = [
    "python", "coding", "game", "loop", "canvas", "thread", "async", "await",
    "class", "object", "system", "memory", "storage", "network", "server",
    "client", "socket", "packet", "data", "value", "input", "output",
    "mouse", "keyboard", "monitor", "screen", "pixel", "vector", "array",
    "list", "tuple", "string", "integer", "float", "double", "boolean",
    "logic", "syntax", "error", "debug", "trace", "stack", "heap", "queue",
    "deque", "graph", "tree", "node", "edge", "audit", "login", "user",
    "pass", "token", "session", "cookie", "cache", "proxy", "router",
    "switch", "bridge", "gateway", "firewall", "subnet", "domain", "host",
    "algorithm", "function", "variable", "constant", "import", "export",
    "module", "package", "library", "framework", "django", "flask", "fastapi",
    "react", "angular", "vue", "node", "deno", "bun", "rust", "go", "java",
    "cpp", "csharp", "ruby", "perl", "php", "swift", "kotlin", "scala"
]

class TypingGame(BaseGame):
    def __init__(self, root, user_data, on_close_callback):
        self.active_words = [] # List of {"word": str, "x": int, "y": int, "id": canvas_id}
        self.falling_speed = 1
        self.spawn_rate = 2000 # ms
        self.game_loop_id = None
        self.spawn_loop_id = None
        self.lives = 3
        self.current_input = ""
        self.canvas = None
        
        super().__init__(root, user_data, on_close_callback, "Typing Defense")
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
            btn = tk.Button(btn_frame, text=diff, width=12,
                           command=lambda d=diff: self.start_game(d),
                           **ButtonStyles.SECONDARY)
            btn.pack(side='left', padx=5)
            
        # Instructions
        instructions = ("Type the words before they hit the bottom!\n"
                       "Press Enter or Space isn't needed, just type.\n"
                       "You have 3 lives.")
        tk.Label(self.difficulty_frame, text=instructions, font=Fonts.small(),
                fg=Colors.TEXT_LIGHT, bg=Colors.BACKGROUND).pack(pady=10)

        # Game Canvas (Hidden initially)
        self.game_container = tk.Frame(self.root, bg=Colors.BACKGROUND)
        
        # Stats bar
        self.stats_label = tk.Label(self.game_container, text="", font=Fonts.normal(),
                                   bg=Colors.BACKGROUND, fg=Colors.TEXT)
        self.stats_label.pack(pady=5)
        
        self.canvas = tk.Canvas(self.game_container, width=800, height=500,
                               bg='#2C3E50', highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Current input display
        self.input_label = tk.Label(self.game_container, text="Type here...", font=Fonts.large(),
                                   bg=Colors.SECONDARY, fg='white', width=30, height=2)
        self.input_label.pack(pady=10)

    def start_game(self, difficulty="Medium"):
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
        self.last_spawn_time = time.time()
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

    def spawn_word(self):
        # Pick random word
        word = random.choice(WORDS)
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

    def game_loop(self):
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
        
        self.update_stats()
        
        if self.lives <= 0:
            self.end_game()
            return
            
        self.game_loop_id = self.root.after(30, self.game_loop)

    def handle_keypress(self, event):
        if not event.char or len(event.char) > 1:
            return
        
        # Add char to input
        # Validation: valid chars only (letters)
        if event.char.isalpha():
            self.current_input += event.char.lower()
            self.update_input_display()
            self.check_input_match()

    def handle_backspace(self):
        self.current_input = self.current_input[:-1]
        self.update_input_display()

    def check_input_match(self):
        # Check if current input matches any active word
        matched_word = None
        
        for w in self.active_words:
            if w['word'] == self.current_input:
                matched_word = w
                break
        
        if matched_word:
            # Success!
            self.score += len(matched_word['word']) * 10
            self.canvas.delete(matched_word['id'])
            self.active_words.remove(matched_word)
            self.current_input = ""
            self.update_input_display()
            
            # Create particle effect or color flash on word position? (Optional polish)
            self.show_success_effect(matched_word['x'], matched_word['y'])

    def show_success_effect(self, x, y):
        # Quick flash effect
        effect_id = self.canvas.create_text(x, y, text="+10", fill=Colors.SUCCESS, font=("Arial", 14, "bold"))
        self.root.after(500, lambda: self.canvas.delete(effect_id))

    def flash_damage(self):
        original_bg = self.canvas.cget('bg')
        self.canvas.configure(bg=Colors.DANGER)
        self.root.after(100, lambda: self.canvas.configure(bg=original_bg))

    def update_input_display(self):
        self.input_label.config(text=self.current_input or "Type here...")
        
        # Highlight logic - Check if input is a prefix of any active word
        is_prefix = any(w['word'].startswith(self.current_input) for w in self.active_words)
        if self.current_input and not is_prefix:
            self.input_label.config(fg=Colors.DANGER)
        else:
            self.input_label.config(fg='white')

    def update_stats(self):
        self.stats_label.config(text=f"Score: {self.score}  |  Lives: {'❤️' * self.lives}")
        self.score_label.configure(text=f"Score: {self.score}")

    def end_game(self):
        # Stop loops
        if self.spawn_loop_id:
            self.root.after_cancel(self.spawn_loop_id)
        if self.game_loop_id:
            self.root.after_cancel(self.game_loop_id)
            
        self.update_stats()
        self.root.unbind('<Key>')
        
        time_taken = time.time() - self.start_time
        
        # Save score
        self.save_score(self.difficulty, time_taken, self.score)
        
        msg = f"Game Over!\n\nScore: {self.score}\nTime: {int(time_taken)}s"
        messagebox.showinfo("Game Over", msg)
        self.on_close()

    def on_close(self):
        if self.spawn_loop_id:
            self.root.after_cancel(self.spawn_loop_id)
        if self.game_loop_id:
            self.root.after_cancel(self.game_loop_id)
        super().on_close()
