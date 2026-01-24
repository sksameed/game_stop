# main.py
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import sys
import os
from typing import Optional, Dict, Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.login_window import LoginWindow
from ui.dashboard import Dashboard
from config.settings import APP_NAME, APP_VERSION


class MiniGameHub:
    """
    Main Application Class.
    Manages the root window, navigation between login and dashboard, and user session.
    """
    
    def __init__(self):
        """Initialize the application, setup options and creates the main window."""
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        
        self.root = ctk.CTk()
        self.root.title(APP_NAME)
        # self.root.geometry("800x600") # Removed fixed geometry
        self.root.after(0, lambda: self.root.state('zoomed')) # Maximize window
        
        self.current_user: Optional[Dict[str, Any]] = None
        self.current_window: Any = None
        
        self.show_login()
    
    def show_login(self) -> None:
        """Switches to the Login screen."""
        self.clear_window()
        self.current_window = LoginWindow(self.root, self.on_login_success)
    
    def show_dashboard(self) -> None:
        """Switches to the Dashboard screen."""
        self.clear_window()
        self.current_window = Dashboard(self.root, self.current_user, self.on_logout)
    
    def on_login_success(self, user_data: Dict[str, Any]) -> None:
        """
        Callback for successful login.
        
        Args:
            user_data: Dictionary containing user details.
        """
        self.current_user = user_data
        self.show_dashboard()
    
    def on_logout(self) -> None:
        """Callback for logout action."""
        self.current_user = None
        self.show_login()
    
    def clear_window(self) -> None:
        """Destroys all child widgets in the root window."""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def run(self) -> None:
        """Starts the main event loop."""
        self.root.mainloop()


def main() -> None:
    """Entry point of the application."""
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