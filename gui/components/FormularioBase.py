import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import logic as db_manager
from styles import *

class FormularioBase(ctk.CTkToplevel):
    def __init__(self, parent, controller, title):
        super().__init__(parent, fg_color=APP_BG_COLOR)
        self.title(title)
        self.transient(parent)
        self.grab_set()
        self.controller = controller
        self.entries = {}
        self.resizable(False, False)
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    def crear_campo(self, frame, texto_label, tipo="entry", **kwargs):
        row = ctk.CTkFrame(frame, fg_color="transparent")
        label = ctk.CTkLabel(
            row,
            width=150,
            text=f"{texto_label}:",
            anchor="w",
            font=FONT_NORMAL,
            text_color=TEXT_COLOR,  # CORREGIDO
        )
        widget = None
        if tipo == "entry":
            widget = ctk.CTkEntry(
                row,
                width=300,
                font=FONT_NORMAL,
                fg_color=ENTRY_BG_COLOR,
                border_color=BUTTON_SECONDARY_COLOR,
                text_color=TEXT_COLOR,
            )
            if "Contraseña" in texto_label:
                widget.configure(show="*")
        elif tipo == "combobox":
            widget = ctk.CTkComboBox(
                row,
                width=300,
                state="readonly",
                font=FONT_NORMAL,
                values=kwargs.get("values", []),
                fg_color=ENTRY_BG_COLOR,
                border_color=BUTTON_SECONDARY_COLOR,
                button_color=BUTTON_SECONDARY_COLOR,
                button_hover_color=BUTTON_SECONDARY_HOVER,
                
                text_color=TEXT_COLOR,
                
                dropdown_fg_color=APP_BG_COLOR,
                dropdown_text_color=TEXT_COLOR,
            )
        elif tipo == "textbox":
            widget = ctk.CTkTextbox(
                row,
                width=300,
                height=80,
                font=FONT_NORMAL,
                fg_color=ENTRY_BG_COLOR,
                border_color=BUTTON_SECONDARY_COLOR,
                text_color=TEXT_COLOR,
            )
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=8)
        label.pack(side=tk.LEFT)
        if widget:
            widget.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        self.entries[texto_label.replace(":", "")] = widget
        return widget
