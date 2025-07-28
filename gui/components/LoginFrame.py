import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import logic as db_manager
from styles import *
from gui.components.CrearUsuarioWindow import CrearUsuarioWindow

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        login_container = ctk.CTkFrame(self, fg_color="transparent")
        login_container.grid(row=0, column=0)
        ctk.CTkLabel(
            login_container,
            text="Login del Sistema",
            font=FONT_TITLE,
            text_color=TEXT_COLOR,
        ).pack(pady=20)
        ctk.CTkLabel(
            login_container, text="Email", font=FONT_NORMAL, text_color=TEXT_COLOR
        ).pack(anchor="w", padx=40)
        self.email_entry = ctk.CTkEntry(
            login_container,
            width=300,
            height=35,
            placeholder_text="correo@ejemplo.com",
            fg_color=ENTRY_BG_COLOR,
            border_color=BUTTON_SECONDARY_COLOR,
            text_color=TEXT_COLOR,
            placeholder_text_color=TEXT_COLOR,
        )
        self.email_entry.pack(pady=(0, 10))
        self.email_entry.focus()
        ctk.CTkLabel(
            login_container, text="Contraseña", font=FONT_NORMAL, text_color=TEXT_COLOR
        ).pack(anchor="w", padx=40)
        self.pass_entry = ctk.CTkEntry(
            login_container,
            width=300,
            height=35,
            show="*",
            fg_color=ENTRY_BG_COLOR,
            border_color=BUTTON_SECONDARY_COLOR,
            text_color=TEXT_COLOR,
        )
        self.pass_entry.pack()
        self.pass_entry.bind("<Return>", self.attempt_login)
        ctk.CTkButton(
            login_container,
            text="Ingresar",
            command=self.attempt_login,
            height=40,
            corner_radius=10,
            fg_color=ACCENT_PURPLE,
            hover_color=ACCENT_PINK,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(pady=20, ipady=5)
        if self.controller.is_first_run:
            ctk.CTkButton(
                login_container,
                text="Crear Primer Usuario (Admin)",
                command=self.crear_primer_usuario,
                height=35,
                corner_radius=10,
                fg_color=BUTTON_SECONDARY_COLOR,
                hover_color=BUTTON_SECONDARY_HOVER,
                text_color=TEXT_COLOR,  # CORREGIDO
            ).pack(pady=10)

    def crear_primer_usuario(self):
        CrearUsuarioWindow(
            self.controller,
            self.controller,
            is_first_user=True,
            on_success_callback=self.refresh_login,
        )

    def refresh_login(self):
        self.controller.is_first_run = False
        self.controller.show_frame(LoginFrame)

    def attempt_login(self, event=None):
        email, password = self.email_entry.get(), self.pass_entry.get()
        if not email or not password:
            messagebox.showwarning(
                "Campos Vacíos", "Por favor, ingrese email y contraseña."
            )
            return
        self.controller.config(cursor="watch")
        self.controller.update_idletasks()
        usuario, rol = db_manager.login_usuario(email, password)
        self.controller.config(cursor="")
        if usuario:
            self.controller.usuario_actual, self.controller.rol_actual = usuario, rol
            from gui.components.MainFrame import MainFrame
            self.controller.show_frame(MainFrame)
        else:
            messagebox.showerror(
                "Login Fallido", "Email, contraseña incorrectos o usuario inactivo."
            )
