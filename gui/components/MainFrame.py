import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import logic as db_manager
from styles import *

from gui.components.ActualizarUsuarioWindow import ActualizarUsuarioWindow
from gui.components.CrearUsuarioWindow import CrearUsuarioWindow
from gui.components.CrearVacanteWindow import CrearVacanteWindow
from gui.components.GestionarExperienciaWindow import GestionarExperienciaWindow
from gui.components.GestionCatalogoWindow import GestionCatalogoWindow
from gui.components.ActualizarVacanteWindow import ActualizarVacanteWindow


def crear_tabla(parent, cols, widths={}):
    tree = ttk.Treeview(parent, columns=cols, show="headings", style="Treeview")
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=widths.get(col, 120), anchor="w")
    return tree


class MainFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        menu_frame = ctk.CTkFrame(
            self, width=220, corner_radius=0, fg_color=FRAME_BG_COLOR
        )
        menu_frame.grid(row=0, column=0, sticky="nsw")
        self.content_frame = ctk.CTkScrollableFrame(
            self,
            corner_radius=0,
            fg_color="transparent",
            scrollbar_button_color=BUTTON_SKY_BLUE_COLOR,
            scrollbar_button_hover_color=BUTTON_SKY_BLUE_HOVER,
        )
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        rol = self.controller.rol_actual
        ctk.CTkLabel(
            menu_frame,
            text=f"Menú - {rol}",
            font=FONT_MENU_TITLE,
            text_color=TEXT_COLOR,
        ).pack(pady=20)
        botones = {
            "HiringGroup": [
                ("Crear Usuario", lambda: self.open_form_window(CrearUsuarioWindow)),
                ("Gestionar Empresas", self.show_gestionar_empresas),
                ("Gestionar Catálogos", self.show_menu_catalogos),
                ("Contratar Postulante", self.show_contratar_form),
                ("Ejecutar Nómina", self.show_nomina_form),
                ("Reportes de Nómina", self.show_reportes_nomina),
            ],
            "Empresa": [
                (
                    "Crear Vacante",
                    lambda: self.open_form_window(
                        CrearVacanteWindow, on_success_callback=self.show_mis_vacantes
                    ),
                ),
                ("Ver Mis Vacantes", self.show_mis_vacantes),
                (
                    "Editar Mi Perfil",
                    lambda: self.open_form_window(ActualizarUsuarioWindow),
                ),
            ],
            "Postulante": [
                ("Buscar Vacantes", self.show_buscar_vacantes),
                ("Mis Postulaciones", self.show_mis_postulaciones),
                (
                    "Editar Mi Perfil",
                    lambda: self.open_form_window(ActualizarUsuarioWindow),
                ),
                (
                    "Gestionar Experiencia",
                    lambda: self.open_form_window(GestionarExperienciaWindow),
                ),
            ],
            "Contratado": [
                ("Ver Vacantes", lambda: self.show_buscar_vacantes(read_only=True)),
                ("Mis Recibos de Pago", self.show_recibos_pago),
                ("Generar Constancia", self.show_constancia),
                (
                    "Editar Mi Perfil",
                    lambda: self.open_form_window(ActualizarUsuarioWindow),
                ),
            ],
        }
        for texto, comando in botones.get(rol, []):
            ctk.CTkButton(
                menu_frame,
                text=texto,
                command=comando,
                height=35,
                corner_radius=8,
                fg_color=BUTTON_SECONDARY_COLOR,
                hover_color=BUTTON_SECONDARY_HOVER,
                text_color=TEXT_COLOR,  # CORREGIDO
            ).pack(pady=4, padx=20, fill="x")
        ctk.CTkButton(
            menu_frame,
            text="Salir (Logout)",
            command=self.logout,
            height=35,
            corner_radius=8,
            fg_color=BUTTON_SKY_BLUE_COLOR,
            hover_color=BUTTON_SKY_BLUE_HOVER,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(side="bottom", pady=20, padx=20, fill="x")
        self.show_welcome_message()

    def open_form_window(self, WindowClass, *args, **kwargs):
        WindowClass(self.controller, self.controller, *args, **kwargs)

    def show_welcome_message(self):
        self.clear_content_frame()
        ctk.CTkLabel(
            self.content_frame,
            text=f"Bienvenido/a, {self.controller.usuario_actual['Email']}",
            font=FONT_TITLE,
            text_color=TEXT_COLOR,
        ).pack(anchor="w", pady=(0, 10))

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def logout(self):
        self.controller.usuario_actual, self.controller.rol_actual = None, None
        from gui.components.LoginFrame import LoginFrame

        self.controller.show_frame(LoginFrame)

    def show_gestionar_empresas(self):
        self.show_welcome_message()
        ctk.CTkLabel(
            self.content_frame,
            text="Gestionar Empresas",
            font=FONT_TITLE,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(pady=10, anchor="w")
        empresas = db_manager.get_catalogo(
            "Empresas",
            "ID_Empresa",
            [
                "Nombre_Empresa",
                "RIF",
                "Sector_Industrial",
                "Persona_Contacto",
                "Telefono_Contacto",
                "Email_Contacto",
            ],
        )
        if not empresas:
            ctk.CTkLabel(
                self.content_frame,
                text="No hay empresas registradas.",
                text_color=TEXT_COLOR,
            ).pack()  # CORREGIDO
            return
        tree_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, pady=5)
        tree = crear_tabla(
            tree_frame,
            ("ID", "Nombre", "RIF", "Sector", "Contacto", "Teléfono", "Email"),
            widths={"ID": 40, "Nombre": 150, "RIF": 80},
        )
        for e in empresas:
            tree.insert(
                "",
                "end",
                values=(
                    e["ID_Empresa"],
                    e["Nombre_Empresa"],
                    e["RIF"],
                    e["Sector_Industrial"],
                    e["Persona_Contacto"],
                    e["Telefono_Contacto"],
                    e["Email_Contacto"],
                ),
            )
        tree.pack(fill="both", expand=True)

    def show_menu_catalogos(self):
        self.show_welcome_message()
        ctk.CTkLabel(
            self.content_frame,
            text="Gestionar Catálogos",
            font=FONT_TITLE,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(pady=10, anchor="w")
        catalogos = {
            "Áreas de Conocimiento": (
                "Areas_Conocimiento",
                "ID_Area_Conocimiento",
                "Nombre_Area",
            ),
            "Profesiones": ("Profesiones", "ID_Profesion", "Nombre_Profesion"),
            "Universidades": ("Universidades", "ID_Universidad", "Nombre_Universidad"),
            "Bancos": ("Bancos", "ID_Banco", "Nombre_Banco"),
        }
        for title, args in catalogos.items():
            ctk.CTkButton(
                self.content_frame,
                text=f"Gestionar {title}",
                command=lambda t=title, a=args: self.open_form_window(
                    GestionCatalogoWindow,
                    title=f"Gestionar {t}",
                    tabla=a[0],
                    id_col=a[1],
                    nombre_col=a[2],
                ),
                fg_color=BUTTON_SECONDARY_COLOR,
                hover_color=BUTTON_SECONDARY_HOVER,
                corner_radius=8,
                text_color=TEXT_COLOR,  # CORREGIDO
            ).pack(fill="x", padx=20, pady=5)

    def show_contratar_form(self):
        self.show_welcome_message()
        ctk.CTkLabel(
            self.content_frame,
            text="Contratar Postulante",
            font=FONT_TITLE,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(pady=10, anchor="w")
        postulaciones = db_manager.get_postulaciones_para_contratar()
        bancos = db_manager.get_catalogo("Bancos", "ID_Banco", "Nombre_Banco")
        if not postulaciones:
            ctk.CTkLabel(
                self.content_frame,
                text="No hay postulaciones recibidas.",
                text_color=TEXT_COLOR,  # CORREGIDO
            ).pack()
            return
        tree_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        tree_frame.pack(fill="x", expand=True, pady=5)
        tree = crear_tabla(tree_frame, ("ID", "Nombre", "Cargo"))
        for p in postulaciones:
            tree.insert(
                "",
                "end",
                values=(
                    p["ID_Postulacion"],
                    f"{p['Nombres']} {p['Apellidos']}",
                    p["Cargo_Vacante"],
                ),
            )
        tree.pack(fill="x")
        form_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        form_frame.pack(anchor="w", fill="x", pady=(10, 0))
        entries = {}
        bancos_map = {b["Nombre_Banco"]: b["ID_Banco"] for b in bancos or []}
        fields = [
            ("Salario", "entry"),
            ("Tipo Contrato", "combo_contrato"),
            ("Tipo de Sangre", "entry"),
            ("Nombre Contacto Emergencia", "entry"),
            ("Teléfono Contacto Emergencia", "entry"),
            ("Número de Cuenta", "entry"),
            ("Banco", "combo_banco"),
        ]
        for i, (label_text, widget_type) in enumerate(fields):
            label = ctk.CTkLabel(
                form_frame,
                text=f"{label_text}:",
                font=FONT_NORMAL,
                text_color=TEXT_COLOR,
            )  # CORREGIDO
            label.grid(row=i, column=0, padx=5, pady=8, sticky="w")
            widget = None
            if widget_type == "entry":
                widget = ctk.CTkEntry(
                    form_frame,
                    width=250,
                    text_color=TEXT_COLOR,
                    fg_color=ENTRY_BG_COLOR,
                    border_color=BUTTON_SECONDARY_COLOR,
                )
            elif (
                widget_type == "combo_contrato" or widget_type == "combo_banco"
            ):  # CORREGIDO (Agrupado)
                widget = ctk.CTkComboBox(
                    form_frame,
                    width=250,
                    values=(
                        ["Un mes", "Seis meses", "Un año", "Indefinido"]
                        if widget_type == "combo_contrato"
                        else list(bancos_map.keys())
                    ),
                    state="readonly",
                    text_color=TEXT_COLOR,
                    fg_color=ENTRY_BG_COLOR,
                    border_color=BUTTON_SECONDARY_COLOR,
                    button_color=BUTTON_SECONDARY_COLOR,
                    button_hover_color=BUTTON_SECONDARY_HOVER,
                )
            if widget:
                widget.grid(row=i, column=1, padx=5, pady=8, sticky="ew")
                entries[label_text] = widget

        def contratar():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning(
                    "Selección Requerida", "Por favor, selecciona una postulación."
                )
                return
            try:
                salario_val = float(entries["Salario"].get())
                if salario_val <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                messagebox.showerror(
                    "Entrada no válida", "El salario debe ser un número positivo."
                )
                return
            id_postulacion = tree.item(selected[0])["values"][0]
            datos_contrato = {
                "Salario_Acordado": salario_val,
                "Tipo_Contrato": entries["Tipo Contrato"].get(),
                "Tipo_Sangre": entries["Tipo de Sangre"].get(),
                "Contacto_Emergencia_Nombre": entries[
                    "Nombre Contacto Emergencia"
                ].get(),
                "Contacto_Emergencia_Telefono": entries[
                    "Teléfono Contacto Emergencia"
                ].get(),
                "Numero_Cuenta": entries["Número de Cuenta"].get(),
                "ID_Banco": bancos_map.get(entries["Banco"].get()),
            }
            if not all(
                v is not None if k == "ID_Banco" else v
                for k, v in datos_contrato.items()
            ):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            success, msg = db_manager.contratar_postulante_db(
                id_postulacion, datos_contrato
            )
            if success:
                messagebox.showinfo("Resultado", msg)
                self.show_contratar_form()
            else:
                messagebox.showerror("Error", msg)

        ctk.CTkButton(
            self.content_frame,
            text="Contratar y Aceptar",
            command=contratar,
            height=40,
            corner_radius=10,
            fg_color=ACCENT_PURPLE,
            hover_color=ACCENT_PINK,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(pady=20, anchor="w")

    def show_buscar_vacantes(self, read_only=False):
        self.show_welcome_message()
        title = "Vacantes Disponibles" if not read_only else "Visualizar Vacantes"
        ctk.CTkLabel(
            self.content_frame, text=title, font=FONT_TITLE, text_color=TEXT_COLOR
        ).pack(  # CORREGIDO
            pady=10, anchor="w"
        )
        filter_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        filter_frame.pack(fill="x", pady=5)
        areas = db_manager.get_catalogo(
            "Areas_Conocimiento", "ID_Area_Conocimiento", "Nombre_Area"
        )
        area_map = {"Todas": None}
        area_map.update(
            {a["Nombre_Area"]: a["ID_Area_Conocimiento"] for a in areas or []}
        )
        ctk.CTkLabel(
            filter_frame, text="Área:", font=FONT_NORMAL, text_color=TEXT_COLOR
        ).pack(  # CORREGIDO
            side=tk.LEFT, padx=(0, 5)
        )
        area_combo = ctk.CTkComboBox(
            filter_frame,
            values=list(area_map.keys()),
            state="readonly",
            width=180,
            text_color=TEXT_COLOR,  # CORREGIDO
            fg_color=ENTRY_BG_COLOR,  # CORREGIDO
            border_color=BUTTON_SECONDARY_COLOR,  # CORREGIDO
            button_color=BUTTON_SECONDARY_COLOR,  # CORREGIDO
            button_hover_color=BUTTON_SECONDARY_HOVER,  # CORREGIDO
        )
        area_combo.pack(side=tk.LEFT, padx=5)
        area_combo.set("Todas")
        ctk.CTkLabel(
            filter_frame, text="Salario:", font=FONT_NORMAL, text_color=TEXT_COLOR
        ).pack(  # CORREGIDO
            side=tk.LEFT, padx=(10, 5)
        )
        salary_combo = ctk.CTkComboBox(
            filter_frame,
            values=["Sin Orden", "Mayor a Menor", "Menor a Mayor"],
            state="readonly",
            width=150,
            text_color=TEXT_COLOR,  # CORREGIDO
            fg_color=ENTRY_BG_COLOR,  # CORREGIDO
            border_color=BUTTON_SECONDARY_COLOR,  # CORREGIDO
            button_color=BUTTON_SECONDARY_COLOR,  # CORREGIDO
            button_hover_color=BUTTON_SECONDARY_HOVER,  # CORREGIDO
        )
        salary_combo.pack(side=tk.LEFT, padx=5)
        salary_combo.set("Sin Orden")
        tree_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, pady=10)
        tree = crear_tabla(
            tree_frame,
            ("ID", "Cargo", "Empresa", "Área", "Profesión", "Salario"),
            widths={"ID": 40, "Salario": 80},
        )
        tree.pack(fill="both", expand=True)

        def populate_tree():
            for i in tree.get_children():
                tree.delete(i)
            filtro_area = area_map[area_combo.get()]
            sort_map = {"Mayor a Menor": "DESC", "Menor a Mayor": "ASC"}
            sort_salary = sort_map.get(salary_combo.get())
            vacantes = db_manager.get_active_vacantes(
                filtro_area=filtro_area, sort_salary=sort_salary
            )
            for v in vacantes or []:
                tree.insert(
                    "",
                    "end",
                    values=(
                        v["ID_Vacante"],
                        v["Cargo_Vacante"],
                        v["Nombre_Empresa"],
                        v["Nombre_Area"] or "No Asignada",
                        v["Nombre_Profesion"],
                        f"{float(v['Salario_Ofrecido']):.2f}",
                    ),
                )

        ctk.CTkButton(
            filter_frame,
            text="Filtrar",
            command=populate_tree,
            width=80,
            corner_radius=8,
            fg_color=BUTTON_SECONDARY_COLOR,
            hover_color=BUTTON_SECONDARY_HOVER,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(side=tk.LEFT, padx=10)
        if not read_only:
            ctk.CTkButton(
                self.content_frame,
                text="Aplicar a Vacante",
                command=lambda: self.aplicar(tree),
                height=40,
                corner_radius=10,
                fg_color=ACCENT_PURPLE,
                hover_color=ACCENT_PINK,
                text_color=TEXT_COLOR,  # CORREGIDO
            ).pack(pady=10, anchor="e")
        populate_tree()

    def aplicar(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning(
                "Selección Requerida", "Selecciona una vacante para aplicar."
            )
            return
        id_vacante = tree.item(selected[0])["values"][0]
        success, msg = db_manager.aplicar_a_vacante_db(
            self.controller.usuario_actual["ID_Usuario"], id_vacante
        )
        messagebox.showinfo("Resultado", msg)

    def show_recibos_pago(self):
        self.show_welcome_message()
        ctk.CTkLabel(
            self.content_frame,
            text="Mis Recibos de Pago",
            font=FONT_TITLE,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(pady=10, anchor="w")
        filter_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        filter_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(filter_frame, text="Mes (opc):", text_color=TEXT_COLOR).pack(
            side=tk.LEFT, padx=5
        )  # CORREGIDO
        mes_entry = ctk.CTkEntry(
            filter_frame,
            width=50,
            text_color=TEXT_COLOR,
            fg_color=ENTRY_BG_COLOR,
            border_color=BUTTON_SECONDARY_COLOR,
        )
        mes_entry.pack(side=tk.LEFT, padx=5)
        ctk.CTkLabel(filter_frame, text="Año (opc):", text_color=TEXT_COLOR).pack(
            side=tk.LEFT, padx=5
        )  # CORREGIDO
        anio_entry = ctk.CTkEntry(
            filter_frame,
            width=70,
            text_color=TEXT_COLOR,
            fg_color=ENTRY_BG_COLOR,
            border_color=BUTTON_SECONDARY_COLOR,
        )
        anio_entry.pack(side=tk.LEFT, padx=5)
        tree_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, pady=10)
        tree = crear_tabla(
            tree_frame, ("Periodo", "Fecha Pago", "Salario Base", "Salario Neto")
        )
        tree.pack(fill="both", expand=True)

        def populate_recibos():
            for i in tree.get_children():
                tree.delete(i)
            recibos = db_manager.get_recibos_por_contratado(
                self.controller.usuario_actual["ID_Usuario"],
                mes_entry.get() or None,
                anio_entry.get() or None,
            )
            for r in recibos or []:
                tree.insert(
                    "",
                    "end",
                    values=(
                        f"{r['Mes']}/{r['Anio']}",
                        r["Fecha_Pago"],
                        f"{r['Salario_Base']:.2f}",
                        f"{r['Salario_Neto_Pagado']:.2f}",
                    ),
                )

        ctk.CTkButton(
            filter_frame,
            text="Filtrar",
            command=populate_recibos,
            width=80,
            corner_radius=8,
            fg_color=BUTTON_SECONDARY_COLOR,
            hover_color=BUTTON_SECONDARY_HOVER,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(side=tk.LEFT, padx=10)
        populate_recibos()

    def show_mis_vacantes(self):
        self.show_welcome_message()
        ctk.CTkLabel(
            self.content_frame,
            text="Mis Vacantes Publicadas",
            font=FONT_TITLE,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(pady=10, anchor="w")
        vacantes = db_manager.get_vacantes_por_empresa(
            self.controller.usuario_actual["ID_Usuario"]
        )
        if not vacantes:
            ctk.CTkLabel(
                self.content_frame,
                text="No tienes vacantes publicadas.",
                text_color=TEXT_COLOR,  # CORREGIDO
            ).pack()
            return
        tree_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, pady=10)
        tree = crear_tabla(
            tree_frame,
            ("ID", "Cargo", "Salario", "Estatus"),
            widths={"ID": 50, "Estatus": 80},
        )
        for v in vacantes:
            salario = (
                f"{float(v['Salario_Ofrecido']):.2f}"
                if v["Salario_Ofrecido"]
                else "N/A"
            )
            tree.insert(
                "",
                "end",
                values=(v["ID_Vacante"], v["Cargo_Vacante"], salario, v["Estatus"]),
            )
        tree.pack(fill="both", expand=True)
        buttons_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=5, anchor="e")

        def editar_vacante():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning(
                    "Selección Requerida",
                    "Selecciona una vacante para editar.",
                    parent=self.controller,
                )
                return
            id_vacante = tree.item(selected[0])["values"][0]
            datos_vacante = next(
                (v for v in vacantes if v["ID_Vacante"] == id_vacante), None
            )
            if datos_vacante:
                self.open_form_window(
                    ActualizarVacanteWindow,
                    datos_vacante=datos_vacante,
                    on_success_callback=self.show_mis_vacantes,
                )

        def eliminar_vacante():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning(
                    "Selección Requerida",
                    "Selecciona una vacante para eliminar.",
                    parent=self.controller,
                )
                return
            id_vacante, cargo = tree.item(selected[0])["values"][:2]
            if messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Estás seguro de que quieres eliminar la vacante '{cargo}'?",
                parent=self.controller,
            ):
                success, msg = db_manager.eliminar_vacante_db(id_vacante)
                if success:
                    messagebox.showinfo("Resultado", msg, parent=self.controller)
                    self.show_mis_vacantes()
                else:
                    messagebox.showerror("Error", msg, parent=self.controller)

        ctk.CTkButton(
            buttons_frame,
            text="Editar Vacante",
            command=editar_vacante,
            fg_color=BUTTON_SECONDARY_COLOR,
            hover_color=BUTTON_SECONDARY_HOVER,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(side="right", padx=10)
        ctk.CTkButton(
            buttons_frame,
            text="Eliminar Vacante",
            command=eliminar_vacante,
            fg_color=ACCENT_PINK,
            hover_color=ACCENT_PURPLE,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(side="right")

    def show_reportes_nomina(self):
        self.show_welcome_message()
        ctk.CTkLabel(
            self.content_frame,
            text="Reportes de Nómina",
            font=FONT_TITLE,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(pady=10, anchor="w")
        rep1_frame = ctk.CTkFrame(self.content_frame, fg_color=FRAME_BG_COLOR)
        rep1_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(
            rep1_frame, text="Nómina por Empresa", font=FONT_BOLD, text_color=TEXT_COLOR
        ).pack(  # CORREGIDO
            pady=10
        )
        empresas = db_manager.get_catalogo("Empresas", "ID_Empresa", "Nombre_Empresa")
        empresa_map = {e["Nombre_Empresa"]: e["ID_Empresa"] for e in empresas or []}
        filter_controls = ctk.CTkFrame(rep1_frame, fg_color="transparent")
        filter_controls.pack(fill="x", padx=10)
        ctk.CTkLabel(filter_controls, text="Empresa:", text_color=TEXT_COLOR).pack(
            side=tk.LEFT
        )  # CORREGIDO
        empresa_combo = ctk.CTkComboBox(
            filter_controls,
            values=list(empresa_map.keys()),
            state="readonly",
            width=200,
            text_color=TEXT_COLOR,  # CORREGIDO
            fg_color=ENTRY_BG_COLOR,  # CORREGIDO
            border_color=BUTTON_SECONDARY_COLOR,  # CORREGIDO
            button_color=BUTTON_SECONDARY_COLOR,  # CORREGIDO
            button_hover_color=BUTTON_SECONDARY_HOVER,  # CORREGIDO
        )
        empresa_combo.pack(side=tk.LEFT, padx=5)
        ctk.CTkLabel(filter_controls, text="Mes:", text_color=TEXT_COLOR).pack(
            side=tk.LEFT
        )  # CORREGIDO
        mes_entry = ctk.CTkEntry(
            filter_controls,
            width=50,
            text_color=TEXT_COLOR,
            fg_color=ENTRY_BG_COLOR,
            border_color=BUTTON_SECONDARY_COLOR,
        )
        mes_entry.pack(side=tk.LEFT, padx=5)
        ctk.CTkLabel(filter_controls, text="Año:", text_color=TEXT_COLOR).pack(
            side=tk.LEFT
        )  # CORREGIDO
        anio_entry = ctk.CTkEntry(
            filter_controls,
            width=70,
            text_color=TEXT_COLOR,
            fg_color=ENTRY_BG_COLOR,
            border_color=BUTTON_SECONDARY_COLOR,
        )
        anio_entry.pack(side=tk.LEFT, padx=5)
        tree1_frame = ctk.CTkFrame(rep1_frame, fg_color="transparent")
        tree1_frame.pack(fill="both", expand=True, pady=10, padx=10)
        tree1 = crear_tabla(tree1_frame, ("Empleado", "Cédula", "Salario Base"))
        tree1.pack(fill="both", expand=True)

        def buscar_nomina():
            id_empresa = empresa_map.get(empresa_combo.get())
            try:
                mes, anio = int(mes_entry.get()), int(anio_entry.get())
            except (ValueError, TypeError):
                messagebox.showerror(
                    "Entrada no válida",
                    "Por favor, introduce un mes (1-12) y año válidos.",
                )
                return
            if not id_empresa:
                messagebox.showerror("Error", "Debes seleccionar una empresa")
                return
            for i in tree1.get_children():
                tree1.delete(i)
            reporte = db_manager.get_nomina_reporte_db(id_empresa, mes, anio)
            for row in reporte or []:
                tree1.insert(
                    "",
                    "end",
                    values=(
                        row["Empleado"],
                        row["Cedula_Identidad"],
                        f"{row['Salario_Base']:.2f}",
                    ),
                )

        ctk.CTkButton(
            filter_controls,
            text="Buscar",
            command=buscar_nomina,
            width=80,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(side=tk.LEFT, padx=10)
        rep2_frame = ctk.CTkFrame(self.content_frame, fg_color=FRAME_BG_COLOR)
        rep2_frame.pack(fill="both", pady=10, expand=True)
        ctk.CTkLabel(
            rep2_frame,
            text="Nómina General por Empresa",
            font=FONT_BOLD,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(pady=10)
        tree2_frame = ctk.CTkFrame(rep2_frame, fg_color="transparent")
        tree2_frame.pack(fill="both", expand=True, padx=10, pady=10)
        tree2 = crear_tabla(tree2_frame, ("Empresa", "Periodo", "Total Nómina"))
        tree2.pack(fill="both", expand=True)
        reporte_total = db_manager.get_toda_nomina_reporte_db()
        for row in reporte_total or []:
            tree2.insert(
                "",
                "end",
                values=(
                    row["Nombre_Empresa"],
                    f"{row['Mes']}/{row['Anio']}",
                    f"{row['Total_Nomina']:.2f}",
                ),
            )

    def show_nomina_form(self):
        self.show_welcome_message()
        ctk.CTkLabel(
            self.content_frame,
            text="Ejecutar Nómina Mensual",
            font=FONT_TITLE,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(pady=10, anchor="w")
        form_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        form_container.pack(fill="x", pady=5, anchor="w")
        empresas = db_manager.get_catalogo("Empresas", "ID_Empresa", "Nombre_Empresa")
        if not empresas:
            ctk.CTkLabel(
                self.content_frame,
                text="No hay empresas registradas.",
                text_color=TEXT_COLOR,
            ).pack()  # CORREGIDO
            return
        empresa_map = {e["Nombre_Empresa"]: e["ID_Empresa"] for e in empresas or []}
        ctk.CTkLabel(form_container, text="Empresa:", text_color=TEXT_COLOR).pack(
            anchor="w"
        )  # CORREGIDO
        empresa_combo = ctk.CTkComboBox(
            form_container,
            values=list(empresa_map.keys()),
            state="readonly",
            width=300,
            text_color=TEXT_COLOR,  # CORREGIDO
            fg_color=ENTRY_BG_COLOR,  # CORREGIDO
            border_color=BUTTON_SECONDARY_COLOR,  # CORREGIDO
            button_color=BUTTON_SECONDARY_COLOR,  # CORREGIDO
            button_hover_color=BUTTON_SECONDARY_HOVER,  # CORREGIDO
        )
        empresa_combo.pack(fill="x")
        ctk.CTkLabel(form_container, text="Mes (1-12):", text_color=TEXT_COLOR).pack(
            anchor="w", pady=(10, 0)
        )  # CORREGIDO
        mes_entry = ctk.CTkEntry(
            form_container,
            width=300,
            text_color=TEXT_COLOR,
            fg_color=ENTRY_BG_COLOR,
            border_color=BUTTON_SECONDARY_COLOR,
        )
        mes_entry.pack(fill="x")
        ctk.CTkLabel(form_container, text="Año (YYYY):", text_color=TEXT_COLOR).pack(
            anchor="w", pady=(10, 0)
        )  # CORREGIDO
        anio_entry = ctk.CTkEntry(
            form_container,
            width=300,
            text_color=TEXT_COLOR,
            fg_color=ENTRY_BG_COLOR,
            border_color=BUTTON_SECONDARY_COLOR,
        )
        anio_entry.pack(fill="x")
        resultado_frame = ctk.CTkFrame(self.content_frame, fg_color=FRAME_BG_COLOR)
        resultado_frame.pack(fill="both", pady=20, expand=True)
        ctk.CTkLabel(
            resultado_frame,
            text="Resultado de la Nómina Generada",
            font=FONT_BOLD,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(pady=10)
        tree_resultado = crear_tabla(
            resultado_frame,
            ("Empleado", "Cédula", "Salario Base", "Deducciones", "Salario Neto"),
            widths={
                "Empleado": 200,
                "Cédula": 100,
                "Salario Base": 100,
                "Deducciones": 100,
                "Salario Neto": 100,
            },
        )
        tree_resultado.pack(fill="both", expand=True, padx=10, pady=10)

        def generar():
            for i in tree_resultado.get_children():
                tree_resultado.delete(i)
            nombre_empresa = empresa_combo.get()
            try:
                mes, anio = int(mes_entry.get()), int(anio_entry.get())
            except (ValueError, TypeError):
                messagebox.showerror(
                    "Entrada no válida", "Mes y año deben ser números."
                )
                return
            if not (1 <= mes <= 12 and 2000 <= anio <= 2100):
                messagebox.showerror(
                    "Entrada no válida",
                    "Por favor, introduce un mes (1-12) y año válidos.",
                )
                return
            if not nombre_empresa:
                messagebox.showerror("Error", "Debes seleccionar una empresa")
                return
            id_empresa = empresa_map.get(nombre_empresa)
            success, msg, id_nomina = db_manager.ejecutar_nomina_db(
                id_empresa, mes, anio
            )
            messagebox.showinfo("Resultado", msg)
            if success and id_nomina:
                detalles_nomina = db_manager.get_nomina_generada_detalle_db(id_nomina)
                for detalle in detalles_nomina or []:
                    tree_resultado.insert(
                        "",
                        "end",
                        values=(
                            detalle["Empleado"],
                            detalle["Cedula_Identidad"],
                            f"{detalle['Salario_Base']:.2f}",
                            f"{detalle['Total_Deducciones']:.2f}",
                            f"{detalle['Salario_Neto_Pagado']:.2f}",
                        ),
                    )

        ctk.CTkButton(
            form_container,
            text="Generar Nómina",
            command=generar,
            height=40,
            corner_radius=10,
            fg_color=ACCENT_PURPLE,
            hover_color=ACCENT_PINK,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(pady=20, anchor="w")

    def show_mis_postulaciones(self):
        self.show_welcome_message()
        ctk.CTkLabel(
            self.content_frame,
            text="Mis Postulaciones Realizadas",
            font=FONT_TITLE,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(pady=10, anchor="w")
        postulaciones = db_manager.get_postulaciones_por_postulante(
            self.controller.usuario_actual["ID_Usuario"]
        )
        if not postulaciones:
            ctk.CTkLabel(
                self.content_frame,
                text="No has realizado ninguna postulación.",
                text_color=TEXT_COLOR,  # CORREGIDO
            ).pack()
            return
        tree_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, pady=10)
        tree = crear_tabla(
            tree_frame, ("Cargo", "Empresa", "Salario", "Fecha", "Estatus")
        )
        for p in postulaciones:
            salario = (
                f"{float(p['Salario_Ofrecido']):.2f}"
                if p["Salario_Ofrecido"]
                else "N/A"
            )
            fecha = p["Fecha_Postulacion"] if p["Fecha_Postulacion"] else "N/A"
            tree.insert(
                "",
                "end",
                values=(
                    p["Cargo_Vacante"],
                    p["Nombre_Empresa"],
                    salario,
                    fecha,
                    p["Estatus"],
                ),
            )
        tree.pack(fill="both", expand=True)

    def show_constancia(self):
        self.show_welcome_message()
        ctk.CTkLabel(
            self.content_frame,
            text="Constancia de Trabajo",
            font=FONT_TITLE,
            text_color=TEXT_COLOR,  # CORREGIDO
        ).pack(pady=10, anchor="w")
        texto_constancia = db_manager.get_datos_constancia(
            self.controller.usuario_actual["ID_Usuario"]
        )
        if texto_constancia:
            textbox = ctk.CTkTextbox(
                self.content_frame,
                height=250,
                font=("Courier", 12),
                wrap="word",
                fg_color=ENTRY_BG_COLOR,
                border_color=BUTTON_SECONDARY_COLOR,
                text_color=TEXT_COLOR,
            )
            textbox.pack(pady=10, fill="x", expand=True)
            textbox.insert(tk.END, texto_constancia)
            textbox.configure(state="disabled")
        else:
            ctk.CTkLabel(
                self.content_frame,
                text="No se pudo generar la constancia. No se encontró un contrato activo.",
                text_color=TEXT_COLOR,  # CORREGIDO
            ).pack()
