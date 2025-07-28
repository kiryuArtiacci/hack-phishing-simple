import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from gui.components.FormularioBase import FormularioBase
import logic as db_manager
from styles import *

def crear_tabla(parent, cols, widths={}):
    tree = ttk.Treeview(parent, columns=cols, show="headings", style="Treeview")
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=widths.get(col, 120), anchor="w")
    return tree

class GestionCatalogoWindow(FormularioBase):
    def __init__(self, parent, controller, title, tabla, id_col, nombre_col, **kwargs):
        super().__init__(parent, controller, title)
        self.tabla, self.id_col, self.nombre_col = tabla, id_col, nombre_col
        add_frame = ctk.CTkFrame(self.main_frame, fg_color=FRAME_BG_COLOR)
        add_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(
            add_frame,
            text=f"Agregar Nuevo/a {title.split(' ')[-1]}",
            font=FONT_BOLD,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(pady=(5, 10))
        entry_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        entry_frame.pack(fill="x", padx=10)
        ctk.CTkLabel(
            entry_frame, text="Nombre:", font=FONT_NORMAL, text_color=TEXT_COLOR
        ).pack(  # CORREGIDO
            side=tk.LEFT, padx=5
        )
        self.new_entry = ctk.CTkEntry(
            entry_frame,
            fg_color=ENTRY_BG_COLOR,
            border_color=BUTTON_SECONDARY_COLOR,
            text_color=TEXT_COLOR,
        )
        self.new_entry.pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        ctk.CTkButton(
            entry_frame,
            text="Agregar",
            command=self.agregar,
            width=80,
            fg_color=BUTTON_SECONDARY_COLOR,
            hover_color=BUTTON_SECONDARY_HOVER,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(side=tk.LEFT, padx=5)
        tree_frame = ctk.CTkFrame(self.main_frame, fg_color=FRAME_BG_COLOR)
        tree_frame.pack(fill="both", expand=True, pady=10)
        self.tree = crear_tabla(
            tree_frame, ("ID", "Nombre"), widths={"ID": 50, "Nombre": 400}
        )
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        action_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        action_frame.pack(fill="x", pady=5, padx=10, anchor="e")
        ctk.CTkButton(
            action_frame,
            text="Editar",
            command=self.editar,
            width=80,
            fg_color=BUTTON_SECONDARY_COLOR,
            hover_color=BUTTON_SECONDARY_HOVER,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(side="right", padx=5)
        ctk.CTkButton(
            action_frame,
            text="Eliminar",
            command=self.eliminar,
            width=80,
            fg_color=ACCENT_PINK,
            hover_color=ACCENT_PURPLE,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(side="right")
        self.populate_tree()

    def populate_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in db_manager.get_catalogo(self.tabla, self.id_col, self.nombre_col):
            self.tree.insert(
                "", "end", values=(item[self.id_col], item[self.nombre_col])
            )

    def agregar(self):
        new_val = self.new_entry.get()
        if not new_val:
            messagebox.showwarning("Campo Vacío", "Introduce un nombre.", parent=self)
            return
        success, msg = db_manager.crear_item_catalogo(
            self.tabla, self.nombre_col, new_val
        )
        if success:
            self.new_entry.delete(0, tk.END)
            self.populate_tree()
        messagebox.showinfo("Resultado", msg, parent=self)

    def editar(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Selección Requerida",
                "Selecciona un elemento para editar.",
                parent=self,
            )
            return
        item_id, nombre_actual = self.tree.item(selected[0])["values"]
        dialog = ctk.CTkInputDialog(text="Introduce el nuevo nombre:", title="Editar")
        nuevo_nombre = dialog.get_input()
        if nuevo_nombre and nuevo_nombre.strip() and nuevo_nombre != nombre_actual:
            success, msg = db_manager.actualizar_item_catalogo(
                self.tabla, self.id_col, self.nombre_col, item_id, nuevo_nombre
            )
            if success:
                self.populate_tree()
            messagebox.showinfo("Resultado", msg, parent=self)

    def eliminar(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Selección Requerida",
                "Selecciona un elemento para eliminar.",
                parent=self,
            )
            return
        item_id, nombre = self.tree.item(selected[0])["values"]
        if messagebox.askyesno(
            "Confirmar", f"¿Seguro que quieres eliminar '{nombre}'?", parent=self
        ):
            success, msg = db_manager.eliminar_item_catalogo(
                self.tabla, self.id_col, item_id
            )
            if success:
                self.populate_tree()
            messagebox.showinfo("Resultado", msg, parent=self)
