import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from gui.components.FormularioBase import FormularioBase
import logic as db_manager
from setup import *

def crear_tabla(parent, cols, widths={}):
    tree = ttk.Treeview(parent, columns=cols, show="headings", style="Treeview")
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=widths.get(col, 120), anchor="w")
    return tree

class GestionarExperienciaWindow(FormularioBase):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, controller, "Gestionar Mi Experiencia Laboral")
        self.id_postulante = self.controller.usuario_actual["ID_Usuario"]
        add_frame = ctk.CTkFrame(self.main_frame, fg_color=FRAME_BG_COLOR)
        add_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(
            add_frame,
            text="Añadir/Editar Experiencia",
            font=FONT_BOLD,
            text_color=TEXT_COLOR,
        ).pack(  # CORREGIDO
            pady=(5, 10)
        )
        self.crear_campo(add_frame, "Empresa")
        self.crear_campo(add_frame, "Cargo")
        self.crear_campo(add_frame, "Fecha Inicio (YYYY-MM-DD)")
        self.crear_campo(add_frame, "Fecha Fin (YYYY-MM-DD, opcional)")
        self.crear_campo(add_frame, "Descripción", "textbox")
        ctk.CTkButton(
            add_frame,
            text="Agregar Experiencia",
            command=self.agregar,
            corner_radius=10,
            fg_color=ACCENT_PURPLE,
            hover_color=ACCENT_PINK,
            text_color=TEXT_COLOR,
        ).pack(pady=10)
        tree_frame = ctk.CTkFrame(self.main_frame, fg_color=FRAME_BG_COLOR)
        tree_frame.pack(fill="both", expand=True, pady=10)
        ctk.CTkLabel(
            tree_frame, text="Mis Experiencias", font=FONT_BOLD, text_color=TEXT_COLOR
        ).pack(  # CORREGIDO
            pady=(5, 10)
        )
        self.tree = crear_tabla(
            tree_frame, ("ID", "Empresa", "Cargo", "Inicio", "Fin"), widths={"ID": 30}
        )
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkButton(
            tree_frame,
            text="Eliminar Seleccionada",
            command=self.eliminar,
            corner_radius=10,
            fg_color=BUTTON_SECONDARY_COLOR,
            hover_color=BUTTON_SECONDARY_HOVER,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(pady=10, anchor="e", padx=10)
        self.populate_tree()

    def populate_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for exp in db_manager.get_experiencias_db(self.id_postulante) or []:
            self.tree.insert(
                "",
                "end",
                values=(
                    exp["ID_Experiencia"],
                    exp["Empresa"],
                    exp["Cargo_Ocupado"],
                    exp["Fecha_Inicio"],
                    exp["Fecha_Fin"] or "Actual",
                ),
            )

    def agregar(self):
        datos = {
            k: v.get("1.0", "end-1c").strip()
            if isinstance(v, ctk.CTkTextbox)
            else v.get()
            for k, v in self.entries.items()
        }
        if (
            not datos["Empresa"]
            or not datos["Cargo"]
            or not datos["Fecha Inicio (YYYY-MM-DD)"]
        ):
            messagebox.showerror(
                "Error",
                "Empresa, Cargo y Fecha de Inicio son obligatorios.",
                parent=self,
            )
            return
        self.controller.config(cursor="watch")
        self.controller.update_idletasks()
        success, msg = db_manager.crear_experiencia_db(self.id_postulante, datos)
        self.controller.config(cursor="")
        if success:
            self.populate_tree()
        else:
            messagebox.showerror("Error", msg, parent=self)

    def eliminar(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Selección Requerida",
                "Selecciona una experiencia para eliminar.",
                parent=self,
            )
            return
        id_exp = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno(
            "Confirmar", "¿Seguro que quieres eliminar esta experiencia?", parent=self
        ):
            self.controller.config(cursor="watch")
            self.controller.update_idletasks()
            success, msg = db_manager.eliminar_experiencia_db(id_exp)
            self.controller.config(cursor="")
            if success:
                self.populate_tree()
            else:
                messagebox.showerror("Error", msg, parent=self)
