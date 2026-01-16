# main.py
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.login_window import LoginWindow
from ui.dashboard import Dashboard
from config.settings import APP_NAME, APP_VERSION


class MiniGameHub:
    
    def __init__(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        
        self.root = ctk.CTk()
        self.root.title(APP_NAME)
        # self.root.geometry("800x600") # Removed fixed geometry
        self.root.after(0, lambda: self.root.state('zoomed')) # Maximize window
        
        self.current_user = None
        self.current_window = None
        
        self.show_login()
    
    def show_login(self):
        self.clear_window()
        self.current_window = LoginWindow(self.root, self.on_login_success)
    
    def show_dashboard(self):
        self.clear_window()
        self.current_window = Dashboard(self.root, self.current_user, self.on_logout)
    
    def on_login_success(self, user_data):
        self.current_user = user_data
        self.show_dashboard()
    
    def on_logout(self):
        self.current_user = None
        self.show_login()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def run(self):
        self.root.mainloop()


def main():
    try:
        print(f"Starting {APP_NAME} v{APP_VERSION}")
        print("=" * 50)
        
        # Create and run application
        app = MiniGameHub()
        app.run()
        
    except Exception as e:
        print(f"Fatal error: {e}")
        messagebox.showerror("Error", f"Application failed to start:\n{str(e)}")
        sys.exit(1)



if __name__ == "__main__":
    main()