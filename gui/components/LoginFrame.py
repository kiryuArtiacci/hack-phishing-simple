import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from logic.users import login_usuario
from styles import *

import os
from PIL import Image


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        login_container = ctk.CTkFrame(self, fg_color="transparent")
        login_container.grid(row=0, column=0)

        card_frame = ctk.CTkFrame(
            login_container, fg_color=FRAME_BG_COLOR, corner_radius=15
        )
        card_frame.pack(pady=10, padx=40)
        card_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card_frame,
            text="Login del Sistema",
            font=FONT_TITLE,
            text_color=TEXT_COLOR,
        ).grid(row=0, column=0, pady=(30, 25), padx=30)

        ctk.CTkLabel(
            card_frame, text="Email", font=FONT_NORMAL, text_color=TEXT_COLOR
        ).grid(row=1, column=0, sticky="w", padx=20, pady=(0, 5))

        email_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        email_frame.grid(row=2, column=0, sticky="ew", padx=20)
        email_frame.grid_columnconfigure(0, weight=1)

        self.email_entry = ctk.CTkEntry(
            email_frame,
            height=35,
            placeholder_text="correo@ejemplo.com",
            fg_color=ENTRY_BG_COLOR,
            border_color=BUTTON_SECONDARY_COLOR,
            text_color=TEXT_COLOR,
            placeholder_text_color=TEXT_COLOR,
        )
        self.email_entry.grid(row=0, column=0, sticky="ew")
        self.email_entry.focus()

        spacer_frame = ctk.CTkFrame(
            email_frame, fg_color="transparent", width=31, height=28
        )
        spacer_frame.grid(row=0, column=1, padx=(5, 0))

        ctk.CTkLabel(
            card_frame, text="Contraseña", font=FONT_NORMAL, text_color=TEXT_COLOR
        ).grid(row=3, column=0, sticky="w", padx=20, pady=(15, 5))

        password_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        password_frame.grid(row=4, column=0, sticky="ew", padx=20)
        password_frame.grid_columnconfigure(0, weight=1)

        self.pass_entry = ctk.CTkEntry(
            password_frame,
            height=35,
            show="*",
            fg_color=ENTRY_BG_COLOR,
            border_color=BUTTON_SECONDARY_COLOR,
            text_color=TEXT_COLOR,
        )
        self.pass_entry.grid(row=0, column=0, sticky="ew")
        self.pass_entry.bind("<Return>", self.attempt_login)

        try:
            script_dir = os.path.dirname(__file__)
            image_path = os.path.join(script_dir, "../../assets/scan-eye.png")
            eye_icon = ctk.CTkImage(Image.open(image_path), size=(20, 20))

            self.toggle_pass_button = ctk.CTkButton(
                password_frame,
                image=eye_icon,
                text="",
                width=28,
                height=28,
                fg_color="transparent",
                hover_color=BUTTON_SECONDARY_HOVER,
                command=self.toggle_password_visibility,
            )
            self.toggle_pass_button.grid(row=0, column=1, padx=(5, 0))
        except FileNotFoundError:
            print("Advertencia: No se encontró 'assets/scan-eye.png'.")

        ctk.CTkButton(
            card_frame,
            text="Ingresar",
            command=self.attempt_login,
            height=40,
            corner_radius=10,
            fg_color=ACCENT_PURPLE,
            hover_color=ACCENT_PINK,
            text_color=TEXT_COLOR,
        ).grid(row=5, column=0, pady=30, padx=20, ipady=5)

        if self.controller.is_first_run:
            ctk.CTkButton(
                login_container,
                text="Crear Primer Usuario (Admin)",
                command=self.crear_primer_usuario,
                height=35,
                corner_radius=10,
                fg_color=BUTTON_SECONDARY_COLOR,
                hover_color=BUTTON_SECONDARY_HOVER,
                text_color=TEXT_COLOR,
            ).pack(pady=20)

    def toggle_password_visibility(self):
        if self.pass_entry.cget("show") == "*":
            self.pass_entry.configure(show="")
        else:
            self.pass_entry.configure(show="*")

    def crear_primer_usuario(self):
        from gui.components.CrearUsuarioWindow import CrearUsuarioWindow

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

        usuario, rol = login_usuario(email, password)

        self.controller.config(cursor="")

        if usuario:
            self.controller.usuario_actual = usuario
            self.controller.rol_actual = rol
            from gui.components.MainFrame import MainFrame

            self.controller.show_frame(MainFrame)
        else:
            messagebox.showerror(
                "Login Fallido", "Email, contraseña incorrectos o usuario inactivo."
            )
