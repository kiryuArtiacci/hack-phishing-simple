import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from gui.components.FormularioBase import FormularioBase
import logic as db_manager
from setup import *

class CrearVacanteWindow(FormularioBase):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, controller, "Crear Nueva Vacante")
        self.on_success_callback = kwargs.get("on_success_callback")
        self.profesiones = db_manager.get_catalogo(
            "Profesiones", "ID_Profesion", "Nombre_Profesion"
        )
        self.prof_map = {
            p["Nombre_Profesion"]: p["ID_Profesion"] for p in self.profesiones or []
        }
        if not self.profesiones:
            messagebox.showwarning(
                "Advertencia", "No hay profesiones registradas.", parent=self
            )
            self.destroy()
            return
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.crear_campo(frame, "Cargo Vacante")
        self.crear_campo(frame, "Descripción del Perfil", "textbox")
        self.crear_campo(frame, "Salario Ofrecido")
        self.crear_campo(
            frame,
            "Profesión Requerida",
            tipo="combobox",
            values=list(self.prof_map.keys()),
        )
        frame.pack(pady=10, fill="x")
        ctk.CTkButton(
            self.main_frame,
            text="Guardar Vacante",
            command=self.guardar,
            height=40,
            corner_radius=10,
            fg_color=ACCENT_PURPLE,
            hover_color=ACCENT_PINK,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(pady=15)

    def guardar(self):
        datos = {
            k: v.get("1.0", "end-1c").strip()
            if isinstance(v, ctk.CTkTextbox)
            else v.get()
            for k, v in self.entries.items()
        }
        try:
            salario = float(datos.get("Salario Ofrecido", 0))
            if salario <= 0:
                raise ValueError
        except (ValueError, TypeError):
            messagebox.showerror(
                "Entrada no válida",
                "El salario debe ser un número positivo.",
                parent=self,
            )
            return
        id_profesion = self.prof_map.get(datos.get("Profesión Requerida"))
        if not all([datos.get("Cargo Vacante"), id_profesion]):
            messagebox.showerror(
                "Error", "Cargo y Profesión son obligatorios.", parent=self
            )
            return
        success, message = db_manager.crear_vacante_db(
            self.controller.usuario_actual["ID_Usuario"],
            datos["Cargo Vacante"],
            datos["Descripción del Perfil"],
            salario,
            id_profesion,
        )
        if success:
            messagebox.showinfo("Éxito", message, parent=self)
            if self.on_success_callback:
                self.on_success_callback()
            self.destroy()
        else:
            messagebox.showerror("Error al Guardar", message, parent=self)
