# games/maze_game.py
import tkinter as tk
from tkinter import messagebox
import random
import time
from collections import deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from games.base_game import BaseGame
from ui.styles import Colors, ButtonStyles, Fonts
from config.settings import MAZE_SIZES


class MazeGame(BaseGame):
    
    def __init__(self, root, user_data, on_close_callback):
        self.difficulty = None
        self.maze = None
        self.player_pos = None
        self.end_pos = None
        self.canvas = None
        self.cell_size = 30
        
        super().__init__(root, user_data, on_close_callback, "Maze Path Game")
        self.create_game_ui()
    
    
    def create_game_ui(self):
        self.difficulty_frame = tk.Frame(self.root, bg=Colors.BACKGROUND)
        self.difficulty_frame.pack(pady=20)
        
        tk.Label(self.difficulty_frame, text="Select Difficulty:", font=Fonts.large(),
                bg=Colors.BACKGROUND, fg=Colors.PRIMARY).pack(pady=10)
        
        btn_frame = tk.Frame(self.difficulty_frame, bg=Colors.BACKGROUND)
        btn_frame.pack()
        
        for diff in ["Easy", "Medium", "Hard"]:
            btn = tk.Button(btn_frame, text=diff, width=12,
                           command=lambda d=diff: self.select_difficulty(d),
                           **ButtonStyles.SECONDARY)
            btn.pack(side='left', padx=5)
        
        # Game canvas (hidden initially)
        self.canvas_frame = tk.Frame(self.root, bg=Colors.BACKGROUND)
        
        # Instructions
        instructions = ("Use arrow keys to move\n"
                       "🟢 = Start  🔴 = End\n"
                       "Find the shortest path!")
        tk.Label(self.difficulty_frame, text=instructions, font=Fonts.small(),
                fg=Colors.TEXT_LIGHT, bg=Colors.BACKGROUND, justify='left').pack(pady=10)
        
        # Stats display
        self.stats_label = tk.Label(self.root, text="", font=Fonts.normal(),
                                    bg=Colors.BACKGROUND, fg=Colors.TEXT)
    
    
    def select_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.difficulty_frame.pack_forget()
        self.canvas_frame.pack(pady=20)
        self.stats_label.pack(pady=10)
        self.root.after(100, self.root.focus_set)  # Ensure window gets focus
        self.start_game()
    
    def start_game(self):
        self.moves = 0
        self.start_time = time.time()
        
        # Get maze size
        rows, cols = MAZE_SIZES[self.difficulty]
        
        # Generate maze
        self.maze = self.generate_maze(rows, cols)
        
        # Set start and end positions
        self.player_pos = [0, 0]
        self.end_pos = [rows-1, cols-1]
        
        # Create canvas
        canvas_width = cols * self.cell_size
        canvas_height = rows * self.cell_size
        
        if self.canvas:
            self.canvas.destroy()
        
        self.canvas = tk.Canvas(self.canvas_frame, width=canvas_width, height=canvas_height,
                               bg='white', highlightthickness=1, highlightbackground=Colors.PRIMARY)
        self.canvas.pack()
        
        # Draw maze
        self.draw_maze()
        
        # Bind keys
        self.root.bind('<Up>', lambda e: self.move_player(-1, 0))
        self.root.bind('<Down>', lambda e: self.move_player(1, 0))
        self.root.bind('<Left>', lambda e: self.move_player(0, -1))
        self.root.bind('<Right>', lambda e: self.move_player(0, 1))
        
        self.update_stats()
    
    def generate_maze(self, rows, cols):
        # Initialize maze with all walls
        maze = [[1 for _ in range(cols)] for _ in range(rows)]
        
        # Carve paths using DFS
        def carve_path(r, c):
            maze[r][c] = 0
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(directions)
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 1:
                    maze[r + dr//2][c + dc//2] = 0
                    carve_path(nr, nc)
        
        carve_path(0, 0)
        
        # Ensure start and end are clear
        # Ensure start and end are clear
        maze[0][0] = 0
        maze[rows-1][cols-1] = 0
        
        # Ensure end is reachable (fix for even-sized grids)
        # DFS nodes are at (even, even), so if end is at (odd, odd), it might be isolated.
        # We clear adjacent cells to connect it to the nearest DFS visited nodes.
        if rows > 1:
            maze[rows-2][cols-1] = 0  # Top neighbor
        if cols > 1:
            maze[rows-1][cols-2] = 0  # Left neighbor
        
        return maze
    
    def draw_maze(self):
        self.canvas.delete('all')
        rows = len(self.maze)
        cols = len(self.maze[0])
        
        for r in range(rows):
            for c in range(cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                if self.maze[r][c] == 1:
                    # Wall
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=Colors.PRIMARY, outline='')
                else:
                    # Path
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline=Colors.TEXT_LIGHT)
        
        # Draw start (green)
        self.draw_circle(0, 0, Colors.SUCCESS)
        
        # Draw end (red)
        self.draw_circle(self.end_pos[0], self.end_pos[1], Colors.DANGER)
        
        # Draw player (blue)
        self.draw_player()
    
    def draw_circle(self, row, col, color):
        x = col * self.cell_size + self.cell_size // 2
        y = row * self.cell_size + self.cell_size // 2
        r = self.cell_size // 3
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline='')
    
    def draw_player(self):
        self.canvas.delete('player')
        x = self.player_pos[1] * self.cell_size + self.cell_size // 2
        y = self.player_pos[0] * self.cell_size + self.cell_size // 2
        r = self.cell_size // 3
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=Colors.SECONDARY, 
                               outline='', tags='player')
    
    def move_player(self, dr, dc):
        new_r = self.player_pos[0] + dr
        new_c = self.player_pos[1] + dc
        
        # Check bounds and walls
        if (0 <= new_r < len(self.maze) and 
            0 <= new_c < len(self.maze[0]) and 
            self.maze[new_r][new_c] == 0):
            
            self.player_pos = [new_r, new_c]
            self.moves += 1
            self.draw_player()
            self.update_stats()
            
            # Check if reached end
            if self.player_pos == self.end_pos:
                self.end_game()
    
    def update_stats(self):
        elapsed = int(time.time() - self.start_time)
        self.stats_label.config(text=f"Moves: {self.moves}  |  Time: {elapsed}s")
    
    def end_game(self):
        time_taken = time.time() - self.start_time
        
        # Calculate score (higher is better)
        # Base score by difficulty
        base_scores = {"Easy": 100, "Medium": 200, "Hard": 300}
        base_score = base_scores[self.difficulty]
        
        # Calculate optimal path
        optimal_moves = self.calculate_optimal_path()
        
        # Penalty for extra moves and time
        move_penalty = max(0, (self.moves - optimal_moves) * 5)
        time_penalty = int(time_taken * 2)
        
        self.score = max(10, base_score - move_penalty - time_penalty)
        
        # Save score
        self.save_score(self.difficulty, time_taken, self.moves)
        
        # Show results
        message = (f"Congratulations! You completed the maze!\n\n"
                  f"Moves: {self.moves} (Optimal: {optimal_moves})\n"
                  f"Time: {int(time_taken)}s\n"
                  f"Score: {self.score}")
        
        messagebox.showinfo("Game Complete", message)
        self.on_close()
    
    def calculate_optimal_path(self):
        rows, cols = len(self.maze), len(self.maze[0])
        queue = deque([(0, 0, 0)])  # (row, col, distance)
        visited = set([(0, 0)])
        
        while queue:
            r, c, dist = queue.popleft()
            
            if [r, c] == self.end_pos:
                return dist
            
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols and 
                    self.maze[nr][nc] == 0 and (nr, nc) not in visited):
                    visited.add((nr, nc))
                    queue.append((nr, nc, dist + 1))
        
        return float('inf')