import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from logic.users import login_usuario
from styles import *  # Asegúrate de que esto importe las fuentes actualizadas de styles.py

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

        # --- CAMBIO DRÁSTICO: Tarjeta mucho más ancha y alta ---
        card_frame = ctk.CTkFrame(
            login_container,
            fg_color=FRAME_BG_COLOR,
            corner_radius=20,  # Radio aumentado
        )
        card_frame.pack(pady=30, padx=200)  # Padding aumentado drásticamente
        card_frame.grid_columnconfigure(0, weight=1)

        # --- CAMBIO DRÁSTICO: Título más grande y con más espaciado ---
        ctk.CTkLabel(
            card_frame,
            text="Login del Sistema",
            font=FONT_TITLE,  # Usa la fuente de título más grande
            text_color=TEXT_COLOR,
        ).grid(row=0, column=0, pady=(50, 45), padx=50)  # Espaciado aumentado

        # --- CAMBIO DRÁSTICO: Label con más espaciado ---
        ctk.CTkLabel(
            card_frame, text="Email", font=FONT_NORMAL, text_color=TEXT_COLOR
        ).grid(
            row=1, column=0, sticky="w", padx=40, pady=(0, 10)
        )  # Espaciado aumentado

        # --- CAMBIO DRÁSTICO: Entry mucho más alto y con fuente más grande ---
        self.email_entry = ctk.CTkEntry(
            card_frame,
            height=50,  # Altura aumentada
            placeholder_text="correo@ejemplo.com",
            fg_color=ENTRY_BG_COLOR,
            border_color=BORDER_COLOR_SKY_BLUE,
            text_color=TEXT_COLOR,
            placeholder_text_color=TEXT_COLOR,
            font=FONT_NORMAL,  # Fuente interna aumentada
            corner_radius=8,
        )
        self.email_entry.grid(
            row=2, column=0, sticky="ew", padx=40
        )  # Padding aumentado
        self.email_entry.focus()

        # --- CAMBIO DRÁSTICO: Label con más espaciado ---
        ctk.CTkLabel(
            card_frame, text="Contraseña", font=FONT_NORMAL, text_color=TEXT_COLOR
        ).grid(
            row=3, column=0, sticky="w", padx=40, pady=(25, 10)
        )  # Espaciado aumentado

        # --- CAMBIO DRÁSTICO: Contenedor de contraseña más alto ---
        password_container = ctk.CTkFrame(
            card_frame,
            height=50,  # Altura aumentada
            fg_color=ENTRY_BG_COLOR,
            border_color=BORDER_COLOR_SKY_BLUE,
            border_width=1,
            corner_radius=8,
        )
        password_container.grid(
            row=4, column=0, sticky="ew", padx=40
        )  # Padding aumentado

        self.pass_entry = ctk.CTkEntry(
            password_container,
            show="*",
            fg_color="transparent",
            border_width=0,
            text_color=TEXT_COLOR,
            font=FONT_NORMAL,  # Fuente interna aumentada
        )
        self.pass_entry.pack(
            side="left", fill="both", expand=True, padx=(15, 0), pady=5
        )
        self.pass_entry.bind("<Return>", self.attempt_login)

        try:
            # --- CAMBIO DRÁSTICO: Ícono del ojo más grande ---
            script_dir = os.path.dirname(__file__)
            image_path = os.path.join(script_dir, "../../assets/scan-eye.png")
            eye_icon = ctk.CTkImage(
                Image.open(image_path), size=(26, 26)
            )  # Tamaño del ícono aumentado

            self.toggle_pass_button = ctk.CTkButton(
                password_container,
                image=eye_icon,
                text="",
                width=36,  # Ancho del botón aumentado
                height=36,  # Alto del botón aumentado
                fg_color="transparent",
                hover_color=BUTTON_SECONDARY_HOVER,
                command=self.toggle_password_visibility,
            )
            self.toggle_pass_button.pack(side="right", padx=(5, 10))
        except FileNotFoundError:
            print("Advertencia: No se encontró 'assets/scan-eye.png'.")

        # --- CAMBIO DRÁSTICO: Botón de Ingresar mucho más grande y con más espaciado ---
        ctk.CTkButton(
            card_frame,
            text="Ingresar",
            command=self.attempt_login,
            height=55,  # Altura aumentada
            corner_radius=12,
            fg_color=ACCENT_PURPLE,
            hover_color=ACCENT_PINK,
            text_color=TEXT_COLOR,
            font=FONT_BOLD,  # Fuente del botón aumentada
        ).grid(
            row=5, column=0, pady=50, padx=40, ipady=10
        )  # Espaciado y padding interno aumentados

        if self.controller.is_first_run:
            ctk.CTkButton(
                login_container,
                text="Crear Primer Usuario (Admin)",
                command=self.crear_primer_usuario,
                height=40,  # Altura aumentada
                corner_radius=10,
                fg_color=BUTTON_SECONDARY_COLOR,
                hover_color=BUTTON_SECONDARY_HOVER,
                text_color=TEXT_COLOR,
                font=FONT_NORMAL,
            ).pack(pady=30)

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
