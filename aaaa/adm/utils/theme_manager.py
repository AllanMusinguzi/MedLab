class ThemeManager:
    def __init__(self):
        self.current_theme = "dark"
        
    def apply_theme(self, theme_name):
        import customtkinter as ctk
        self.current_theme = theme_name
        ctk.set_appearance_mode(theme_name)
        ctk.set_default_color_theme("blue")

