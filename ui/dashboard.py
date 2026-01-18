# ui/dashboard.py
import tkinter as tk  # Needed for some constants or mixins if any
from tkinter import messagebox
import customtkinter as ctk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.styles import Fonts
from config.settings import DASHBOARD_WIDTH, DASHBOARD_HEIGHT, APP_NAME
from database.db_manager import get_db_manager
from utils.helpers import format_score

class Dashboard:
    """Main application dashboard."""
    
    def __init__(self, root, user_data, on_logout):
        """
        Initialize the dashboard.
        
        Args:
            root: Parent CustomTkinter window (CTk)
            user_data: Dictionary containing user information
            on_logout: Callback function when user logs out
        """
        self.root = root
        self.user_data = user_data
        self.on_logout = on_logout
        self.db = get_db_manager()
        
        self.setup_window()
        self.create_widgets()
        self.load_user_stats()
    
    def setup_window(self):
        """Configure the dashboard window."""
        self.root.title(f"{APP_NAME} - Dashboard")
        # self.root.geometry(f"{DASHBOARD_WIDTH}x{DASHBOARD_HEIGHT}")
        # self.root.configure(bg=Colors.BACKGROUND) # Handled by CTk theme
    
    def create_widgets(self):
        """Create all dashboard widgets."""
        # Grid layout for root
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # Header Frame
        # Using sticky='ew' to stretch horizontally
        header_frame = ctk.CTkFrame(self.root, height=80, corner_radius=0)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        # User info in header
        user_label = ctk.CTkLabel(header_frame, text=f"Welcome, {self.user_data['username']}!",
                                 font=Fonts.title())
        user_label.pack(side='left', padx=20, pady=20)
        
        # Logout button
        logout_btn = ctk.CTkButton(header_frame, text="Logout", command=self.handle_logout,
                                  fg_color="#C0392B", hover_color="#922B21") # Danger red
        logout_btn.pack(side='right', padx=20, pady=20)
        
        # Refresh button
        refresh_btn = ctk.CTkButton(header_frame, text="Refresh Stats", command=self.load_user_stats)
        refresh_btn.pack(side='right', padx=10, pady=20)
        
        # Main content area
        # Left side - Games
        games_frame = ctk.CTkFrame(self.root)
        games_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        games_label = ctk.CTkLabel(games_frame, text="Available Games", font=Fonts.large())
        games_label.pack(pady=10)
        
        self.create_game_buttons(games_frame)
        
        # Right side - Statistics
        stats_frame = ctk.CTkFrame(self.root)
        stats_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
        
        stats_label = ctk.CTkLabel(stats_frame, text="Your Statistics", font=Fonts.large())
        stats_label.pack(pady=10)
        
        # Scrollable frame for stats
        self.stats_scroll = ctk.CTkScrollableFrame(stats_frame, label_text="Stats History")
        self.stats_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.create_stats_display() # Initializes the container structure (already done by ScrollableFrame)
    
    def create_game_buttons(self, parent):
        """Create buttons for each game."""
        games = [
            {
                'name': 'Maze Path Game',
                'description': 'Navigate through mazes',
                'icon': '🎯',
                'command': self.launch_maze_game
            },
            {
                'name': 'Memory Card Game',
                'description': 'Match pairs of cards',
                'icon': '🃏',
                'command': self.launch_memory_game
            },
            {
                'name': 'Hangman Game',
                'description': 'Guess the word',
                'icon': '📝',
                'command': self.launch_hangman_game
            },
            {
                'name': 'Typing Defense',
                'description': 'Type fast to survive',
                'icon': '⌨️',
                'command': self.launch_typing_game
            },
            {
                'name': 'Simon Says',
                'description': 'Follow the sequence',
                'icon': '🔴',
                'command': self.launch_simon_game
            }
        ]
        
        for game in games:
            card = ctk.CTkFrame(parent)
            card.pack(fill='x', padx=10, pady=10)
            
            # Icon
            ctk.CTkLabel(card, text=game['icon'], font=("Arial", 30)).pack(side='left', padx=10)
            
            # Info
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side='left', fill='both', expand=True)
            
            ctk.CTkLabel(info_frame, text=game['name'], font=Fonts.normal(), anchor="w").pack(fill='x')
            ctk.CTkLabel(info_frame, text=game['description'], font=Fonts.small(), text_color="gray", anchor="w").pack(fill='x')
            
            # Play button
            ctk.CTkButton(card, text="Play", command=game['command'], width=60).pack(side='right', padx=10)
    
    def create_stats_display(self):
        """Setup stats display."""
        # CustomTkinter ScrollableFrame handles the scrolling automatically.
        # We just add children to self.stats_scroll
        pass

    def load_user_stats(self):
        """Load and display user statistics."""
        # Clear existing stats
        for widget in self.stats_scroll.winfo_children():
            widget.destroy()
        
        # Get stats from database
        stats = self.db.get_user_game_stats(self.user_data['id'])
        
        if not stats:
            ctk.CTkLabel(self.stats_scroll, text="No games played yet!").pack(pady=20)
            return
        
        # Display stats for each game
        for stat in stats:
            self.create_stat_card(stat)
    
    def create_stat_card(self, stat):
        """Create a card displaying stats for one game."""
        card = ctk.CTkFrame(self.stats_scroll)
        card.pack(fill='x', padx=5, pady=5)
        
        # Header
        ctk.CTkLabel(card, text=stat['game_name'], font=Fonts.normal()).pack(pady=5)
        
        # Stats Grid
        grid_frame = ctk.CTkFrame(card, fg_color="transparent")
        grid_frame.pack(fill='x', padx=10, pady=5)
        
        ctk.CTkLabel(grid_frame, text=f"Played: {stat['games_played']}").pack(side='left', padx=10)
        ctk.CTkLabel(grid_frame, text=f"Best: {format_score(stat['best_score'])}").pack(side='right', padx=10)
        # Avg could go on a new line or middle, but this is fine for now

    def launch_maze_game(self):
        """Launch the Maze Path Game."""
        try:
            from games.maze_game import MazeGame
            # For games, we might want a new Toplevel, CTk has CTkToplevel
            game_window = ctk.CTkToplevel(self.root)
            # Ensure it comes to front
            game_window.attributes('-topmost', True)
            game_window.after(100, lambda: game_window.attributes('-topmost', False))
            
            MazeGame(game_window, self.user_data, self.on_game_close)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch game: {str(e)}")
    
    def launch_memory_game(self):
        """Launch the Memory Card Game."""
        try:
            from games.memory_game import MemoryGame
            game_window = ctk.CTkToplevel(self.root)
            game_window.attributes('-topmost', True)
            game_window.after(100, lambda: game_window.attributes('-topmost', False))
            
            MemoryGame(game_window, self.user_data, self.on_game_close)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch game: {str(e)}")
    
    def launch_hangman_game(self):
        """Launch the Hangman Game."""
        try:
            from games.hangman_game import HangmanGame
            game_window = ctk.CTkToplevel(self.root)
            game_window.attributes('-topmost', True)
            game_window.after(100, lambda: game_window.attributes('-topmost', False))
            
            HangmanGame(game_window, self.user_data, self.on_game_close)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch game: {str(e)}")
    
    def launch_typing_game(self):
        """Launch the Typing Defense Game."""
        try:
            from games.typing_game import TypingGame
            game_window = ctk.CTkToplevel(self.root)
            game_window.attributes('-topmost', True)
            game_window.after(100, lambda: game_window.attributes('-topmost', False))
            
            TypingGame(game_window, self.user_data, self.on_game_close)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch game: {str(e)}")

    def launch_simon_game(self):
        """Launch Simon Says Game."""
        try:
            from games.simon_game import SimonGame
            game_window = ctk.CTkToplevel(self.root)
            game_window.attributes('-topmost', True)
            game_window.after(100, lambda: game_window.attributes('-topmost', False))
            
            SimonGame(game_window, self.user_data, self.on_game_close)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch game: {str(e)}")

    def on_game_close(self):
        """Callback when a game is closed."""
        self.load_user_stats()  # Refresh stats
    
    def handle_logout(self):
        """Handle logout button click."""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.on_logout()