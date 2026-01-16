# ui/login_window.py
import customtkinter as ctk
from tkinter import messagebox  # We still use standard messagebox for generic popups
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.authentication import get_auth_manager
from ui.styles import Fonts
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, APP_NAME


class LoginWindow:
    """Login and registration window."""
    
    def __init__(self, root, on_login_success):
        """
        Initialize the login window.
        
        Args:
            root: Parent CustomTkinter window (CTk)
            on_login_success: Callback function when login succeeds
        """
        self.root = root
        self.on_login_success = on_login_success
        self.auth_manager = get_auth_manager()
        
        self.setup_window()
        self.create_widgets()
    
    def setup_window(self):
        """Configure the main window."""
        self.root.title(f"{APP_NAME} - Login")
        # Geometry handled by main.py (maximized)
        # self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}") 
        # self.root.resizable(False, False)
        
        # Center window logic is handled by OS usually with CTk, but we can force it if needed.
        # CTk usually centers by default on creation.
    
    def create_widgets(self):
        """Create all UI widgets."""
        # Main container
        # Use a central frame for the card-like look
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Padding inside the frame
        inner_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        inner_frame.pack(padx=40, pady=40)
        
        # Header
        header_label = ctk.CTkLabel(inner_frame, text=APP_NAME, font=Fonts.header())
        header_label.pack(pady=(0, 10))
        
        subtitle_label = ctk.CTkLabel(inner_frame, text="Welcome! Please login or register",
                                     font=Fonts.small(), text_color="gray")
        subtitle_label.pack(pady=(0, 30))
        
        # Tab view for Login/Register
        self.tab_view = ctk.CTkTabview(inner_frame, width=300)
        self.tab_view.pack(pady=10)
        
        self.tab_view.add("Login")
        self.tab_view.add("Register")
        
        # Create forms in tabs
        self.create_login_form(self.tab_view.tab("Login"))
        self.create_register_form(self.tab_view.tab("Register"))

    def create_login_form(self, parent_frame):
        """Create the login form."""
        # Username
        ctk.CTkLabel(parent_frame, text="Username", font=Fonts.normal()).pack(anchor='w', pady=(10, 0))
        self.login_username = ctk.CTkEntry(parent_frame, width=250, placeholder_text="Enter username")
        self.login_username.pack(pady=(5, 10))
        
        # Password
        ctk.CTkLabel(parent_frame, text="Password", font=Fonts.normal()).pack(anchor='w', pady=(10, 0))
        self.login_password = ctk.CTkEntry(parent_frame, width=250, show='*', placeholder_text="Enter password")
        self.login_password.pack(pady=(5, 20))
        
        # Login button
        login_btn = ctk.CTkButton(parent_frame, text="Login", width=250,
                                 command=self.handle_login, font=Fonts.normal())
        login_btn.pack(pady=20)
        
        # Bind Enter key
        self.login_password.bind('<Return>', lambda e: self.handle_login())
    
    def create_register_form(self, parent_frame):
        """Create the registration form."""
        # Username
        self.reg_username = ctk.CTkEntry(parent_frame, width=250, placeholder_text="Username")
        self.reg_username.pack(pady=5)
        
        # Email
        self.reg_email = ctk.CTkEntry(parent_frame, width=250, placeholder_text="Email (optional)")
        self.reg_email.pack(pady=5)
        
        # Password
        self.reg_password = ctk.CTkEntry(parent_frame, width=250, show='*', placeholder_text="Password")
        self.reg_password.pack(pady=5)
        
        # Confirm Password
        self.reg_confirm = ctk.CTkEntry(parent_frame, width=250, show='*', placeholder_text="Confirm Password")
        self.reg_confirm.pack(pady=5)
        
        # Register button
        register_btn = ctk.CTkButton(parent_frame, text="Register", width=250,
                                    command=self.handle_register, fg_color="#2CC985", hover_color="#229954")
        register_btn.pack(pady=20)
        
        # Bind Enter key
        self.reg_confirm.bind('<Return>', lambda e: self.handle_register())
    
    def handle_login(self):
        """Handle login button click."""
        username = self.login_username.get().strip()
        password = self.login_password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        success, message, user_data = self.auth_manager.login_user(username, password)
        
        if success:
            # messagebox.showinfo("Success", message) # Optional, maybe just proceed
            self.on_login_success(user_data)
        else:
            messagebox.showerror("Error", message)
    
    def handle_register(self):
        """Handle register button click."""
        username = self.reg_username.get().strip()
        email = self.reg_email.get().strip() or None
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()
        
        if not username or not password:
             messagebox.showerror("Error", "Username and Password are required")
             return

        # Validate passwords match
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        success, message = self.auth_manager.register_user(username, password, email)
        
        if success:
            messagebox.showinfo("Success", message)
            # Switch to login tab
            self.tab_view.set("Login")
            
            # Pre-fill username
            self.login_username.delete(0, 'end')
            self.login_username.insert(0, username)
            self.login_password.focus()
            
            # Clear register inputs
            self.reg_username.delete(0, 'end')
            self.reg_password.delete(0, 'end')
            self.reg_confirm.delete(0, 'end')
            self.reg_email.delete(0, 'end')
        else:
            messagebox.showerror("Error", message)