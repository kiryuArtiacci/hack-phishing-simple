import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from gui.components.FormularioBase import FormularioBase
import logic as db_manager
from setup import *


# --- CLASES DE FORMULARIO (ESPECÍFICAS) ---
class CrearUsuarioWindow(FormularioBase):
    def __init__(
        self,
        parent,
        controller,
        is_first_user=False,
        on_success_callback=None,
        **kwargs,
    ):
        super().__init__(parent, controller, "Crear Nuevo Usuario")
        self.campos_especificos = {
            "Postulante": ["Nombres", "Apellidos", "Cédula", "Teléfono", "Universidad"],
            "Empresa": [
                "Nombre Empresa",
                "RIF",
                "Sector",
                "Persona de Contacto",
                "Teléfono de Contacto",
                "Email de Contacto",
            ],
            "HiringGroup": [],
        }
        self.on_success_callback = on_success_callback
        self.universidades = db_manager.get_catalogo(
            "Universidades", "ID_Universidad", "Nombre_Universidad"
        )
        self.uni_map = {
            u["Nombre_Universidad"]: u["ID_Universidad"]
            for u in self.universidades or []
        }
        top_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        tipo_usuario_combo = self.crear_campo(
            top_frame,
            "Tipo de Usuario",
            "combobox",
            values=list(self.campos_especificos.keys()),
        )
        tipo_usuario_combo.configure(command=self.actualizar_campos)
        top_frame.pack(fill="x")
        if is_first_user:
            self.title("Crear Primer Usuario Administrador")
            tipo_usuario_combo.set("HiringGroup")
            tipo_usuario_combo.configure(state="disabled")
        self.form_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.form_frame.pack(pady=10, fill="x")
        ctk.CTkButton(
            self.main_frame,
            text="Crear Usuario",
            command=self.crear,
            corner_radius=10,
            height=40,
            fg_color=ACCENT_PURPLE,
            text_color=TEXT_COLOR,
            hover_color=ACCENT_PINK,
        ).pack(pady=15)
        self.actualizar_campos(None)

    def actualizar_campos(self, event=None):
        for widget in self.form_frame.winfo_children():
            widget.destroy()
        keys_to_remove = [
            k for k in self.entries.keys() if k not in ["Tipo de Usuario"]
        ]
        [self.entries.pop(k, None) for k in keys_to_remove]
        self.crear_campo(self.form_frame, "Email")
        self.crear_campo(self.form_frame, "Contraseña")
        tipo_usuario = self.entries["Tipo de Usuario"].get()
        for field in self.campos_especificos.get(tipo_usuario, []):
            if field == "Universidad":
                self.crear_campo(
                    self.form_frame, field, "combobox", values=list(self.uni_map.keys())
                )
            else:
                self.crear_campo(self.form_frame, field)

    def crear(self):
        tipo_usuario = self.entries["Tipo de Usuario"].get()
        if not tipo_usuario:
            messagebox.showerror(
                "Error", "Debes seleccionar un tipo de usuario.", parent=self
            )
            return
        datos = {
            k: v.get("1.0", "end-1c").strip()
            if isinstance(v, ctk.CTkTextbox)
            else v.get()
            for k, v in self.entries.items()
        }
        datos_db = {
            "Email": datos.get("Email"),
            "Contraseña": datos.get("Contraseña"),
            "Nombres": datos.get("Nombres"),
            "Apellidos": datos.get("Apellidos"),
            "Cédula": datos.get("Cédula"),
            "Teléfono": datos.get("Teléfono"),
            "ID_Universidad": self.uni_map.get(datos.get("Universidad")),
            "Nombre Empresa": datos.get("Nombre Empresa"),
            "RIF": datos.get("RIF"),
            "Sector": datos.get("Sector"),
            "Persona de Contacto": datos.get("Persona de Contacto"),
            "Teléfono de Contacto": datos.get("Teléfono de Contacto"),
            "Email de Contacto": datos.get("Email de Contacto"),
        }
        self.controller.config(cursor="watch")
        self.controller.update_idletasks()
        success, message = db_manager.registrar_usuario_db(tipo_usuario, datos_db)
        self.controller.config(cursor="")
        if success:
            messagebox.showinfo("Éxito", message, parent=self)
            if self.on_success_callback:
                self.on_success_callback()
            self.destroy()
        else:
            messagebox.showerror("Error al Crear", message, parent=self)
