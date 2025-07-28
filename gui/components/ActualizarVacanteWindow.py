import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from gui.components.FormularioBase import FormularioBase
import logic as db_manager
from styles import *

class ActualizarVacanteWindow(FormularioBase):
    def __init__(self, parent, controller, datos_vacante, **kwargs):
        super().__init__(parent, controller, "Editar Vacante")
        self.on_success_callback = kwargs.get("on_success_callback")
        self.id_vacante = datos_vacante["ID_Vacante"]
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.crear_campo(frame, "Cargo Vacante")
        self.crear_campo(frame, "Descripción del Perfil", "textbox")
        self.crear_campo(frame, "Salario Ofrecido")
        self.crear_campo(
            frame, "Estatus", tipo="combobox", values=["Activa", "Inactiva", "Cerrada"]
        )
        frame.pack(pady=10, fill="x")
        self.entries["Cargo Vacante"].insert(0, datos_vacante["Cargo_Vacante"])
        self.entries["Descripción del Perfil"].insert(
            "1.0", datos_vacante["Descripcion_Perfil"]
        )
        self.entries["Salario Ofrecido"].insert(
            0, f"{float(datos_vacante['Salario_Ofrecido']):.2f}"
        )
        self.entries["Estatus"].set(datos_vacante["Estatus"])
        ctk.CTkButton(
            self.main_frame,
            text="Guardar Cambios",
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
        if not all(datos.values()):
            messagebox.showerror(
                "Error", "Todos los campos son obligatorios.", parent=self
            )
            return
        success, message = db_manager.actualizar_vacante_db(
            self.id_vacante,
            datos["Cargo Vacante"],
            datos["Descripción del Perfil"],
            salario,
            datos["Estatus"],
        )
        if success:
            messagebox.showinfo("Éxito", message, parent=self)
            if self.on_success_callback:
                self.on_success_callback()
            self.destroy()
        else:
            messagebox.showerror("Error al Guardar", message, parent=self)
