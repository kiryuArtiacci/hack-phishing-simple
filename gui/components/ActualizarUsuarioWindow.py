import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from gui.components.FormularioBase import FormularioBase
import logic as db_manager
from setup import *

class ActualizarUsuarioWindow(FormularioBase):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, controller, "Editar Mi Perfil")
        self.tipo_usuario = self.controller.rol_actual
        self.id_usuario = self.controller.usuario_actual["ID_Usuario"]
        form_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        if self.tipo_usuario in ["Postulante", "Contratado"]:
            self.universidades = db_manager.get_catalogo(
                "Universidades", "ID_Universidad", "Nombre_Universidad"
            )
            self.uni_map = {
                u["Nombre_Universidad"]: u["ID_Universidad"]
                for u in self.universidades or []
            }
            self.inv_uni_map = {v: k for k, v in self.uni_map.items()}
            self.crear_campo(form_frame, "Nombres")
            self.crear_campo(form_frame, "Apellidos")
            self.crear_campo(form_frame, "Teléfono")
            self.crear_campo(
                form_frame, "Universidad", "combobox", values=list(self.uni_map.keys())
            )
            self.populate_postulante()
        elif self.tipo_usuario == "Empresa":
            self.crear_campo(form_frame, "Nombre Empresa")
            self.crear_campo(form_frame, "Sector")
            self.crear_campo(form_frame, "Persona de Contacto")
            self.crear_campo(form_frame, "Teléfono de Contacto")
            self.crear_campo(form_frame, "Email de Contacto")
            self.populate_empresa()
        self.crear_campo(form_frame, "Nueva Contraseña (opcional)")
        form_frame.pack(pady=10, fill="x")
        ctk.CTkButton(
            self.main_frame,
            text="Guardar Cambios",
            command=self.actualizar,
            corner_radius=10,
            height=40,
            fg_color=ACCENT_PURPLE,
            hover_color=ACCENT_PINK,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(pady=15)

    def populate_postulante(self):
        datos = db_manager.get_single_postulante(self.id_usuario)
        if not datos:
            return
        self.entries["Nombres"].insert(0, datos["Nombres"] or "")
        self.entries["Apellidos"].insert(0, datos["Apellidos"] or "")
        self.entries["Teléfono"].insert(0, datos["Telefono"] or "")
        self.entries["Universidad"].set(
            self.inv_uni_map.get(datos["ID_Universidad"], "")
        )

    def populate_empresa(self):
        datos = db_manager.get_single_empresa(self.id_usuario)
        if not datos:
            return
        self.entries["Nombre Empresa"].insert(0, datos["Nombre_Empresa"] or "")
        self.entries["Sector"].insert(0, datos["Sector_Industrial"] or "")
        self.entries["Persona de Contacto"].insert(0, datos["Persona_Contacto"] or "")
        self.entries["Teléfono de Contacto"].insert(0, datos["Telefono_Contacto"] or "")
        self.entries["Email de Contacto"].insert(0, datos["Email_Contacto"] or "")

    def actualizar(self):
        datos = {
            k: v.get("1.0", "end-1c").strip()
            if isinstance(v, ctk.CTkTextbox)
            else v.get()
            for k, v in self.entries.items()
        }
        datos_db = {k.strip().replace(" (opcional)", ""): v for k, v in datos.items()}
        if self.tipo_usuario in ["Postulante", "Contratado"]:
            datos_db["ID_Universidad"] = self.uni_map.get(datos_db.get("Universidad"))
        if "Nueva Contraseña" in datos_db and datos_db["Nueva Contraseña"]:
            datos_db["Contraseña"] = datos_db.pop("Nueva Contraseña")
        self.controller.config(cursor="watch")
        self.controller.update_idletasks()
        success, message = db_manager.actualizar_usuario_db(
            self.id_usuario, self.tipo_usuario, datos_db
        )
        self.controller.config(cursor="")
        if success:
            messagebox.showinfo("Éxito", message, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Error al Actualizar", message, parent=self)

