import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from gui.components.LoginFrame import LoginFrame

# import logic as db_manager
from logic.users import hay_usuarios_registrados
from styles import *


# --- FUNCIÓN DE UTILIDAD (PARA EL TREEVIEW) ---
def crear_tabla(parent, cols, widths={}):
    tree = ttk.Treeview(parent, columns=cols, show="headings", style="Treeview")
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=widths.get(col, 120), anchor="w")
    return tree


class App(ctk.CTk):
    def __init__(self, is_first_run=False):
        super().__init__(fg_color=APP_BG_COLOR)
        self.title("Sistema de Gestión Nexus Talents")
        self.geometry("1100x700")
        self.minsize(800, 600)
        self.is_first_run = is_first_run
        self.usuario_actual = None
        self.rol_actual = None
        self.setup_styles()
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.show_frame(LoginFrame)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background=ENTRY_BG_COLOR,
            foreground=TEXT_COLOR,
            fieldbackground=ENTRY_BG_COLOR,
            rowheight=25,
            font=FONT_NORMAL,
            borderwidth=0,
        )
        style.map("Treeview", background=[("selected", ACCENT_PURPLE)])
        style.configure(
            "Treeview.Heading",
            background=FRAME_BG_COLOR,
            foreground=TEXT_COLOR,
            font=FONT_BOLD,
            relief="flat",
            padding=5,
        )
        style.map("Treeview.Heading", background=[("active", BUTTON_SECONDARY_HOVER)])

    def show_frame(self, FrameClass):
        for widget in self.container.winfo_children():
            widget.destroy()
        frame = FrameClass(parent=self.container, controller=self)
        frame.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    first_run = not hay_usuarios_registrados()
    app = App(is_first_run=first_run)
    app.mainloop()
