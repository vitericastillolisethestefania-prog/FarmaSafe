import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

import customtkinter as ctk

from utilidades.gestor_imagenes import (
    cargar_imagen_ctk,
    cargar_imagen_interfaz_ctk,
    cargar_imagen_medicamento_ctk
)


#aplica los colores claros usados en el panel principal
COLOR_FONDO = "#F6F8FA"
COLOR_MENU = "#FFFFFF"
COLOR_PANEL = "#FFFFFF"
COLOR_PRIMARIO = "#21866B"
COLOR_SECUNDARIO = "#76C3AF"
COLOR_ADVERTENCIA = "#F3A712"
COLOR_PELIGRO = "#EF4444"
COLOR_TEXTO = "#102A40"
COLOR_TEXTO_SUAVE = "#64748B"
COLOR_BORDE = "#DCE7E4"
COLOR_FILA = "#F4F8F7"
COLOR_SELECCION = "#EAF5F1"
COLOR_AZUL = "#3B82F6"


class VistaInventario(ctk.CTkFrame):

    def __init__(self, master, gestor_inventario):
        super().__init__(
            master,
            corner_radius=0,
            fg_color="transparent"
        )

        #conecta la vista con el gestor que contiene el arbol avl
        self.gestor = gestor_inventario
        self.medicamento_seleccionado = None
        self.imagen_detalle = None

        self.variable_busqueda = tk.StringVar()
        self.variable_estado = tk.StringVar(value="Todos")

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.crear_barra_acciones()
        self.crear_resumen()
        self.crear_zona_inventario()
        self.cargar_tabla()

    #crea los controles para buscar y administrar los registros
    def crear_barra_acciones(self):
        barra = ctk.CTkFrame(
            self,
            height=52,
            corner_radius=0,
            fg_color="transparent"
        )
        barra.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 12)
        )
        barra.grid_columnconfigure(0, weight=1)

        buscador = ctk.CTkEntry(
            barra,
            width=330,
            height=40,
            corner_radius=9,
            border_color=COLOR_BORDE,
            fg_color=COLOR_PANEL,
            text_color=COLOR_TEXTO,
            placeholder_text="Buscar por código, nombre, categoría o lote",
            textvariable=self.variable_busqueda
        )
        buscador.grid(
            row=0,
            column=0,
            sticky="w"
        )
        buscador.bind(
            "<Return>",
            lambda evento: self.cargar_tabla()
        )

        filtro = ctk.CTkComboBox(
            barra,
            width=175,
            height=40,
            corner_radius=9,
            border_color=COLOR_BORDE,
            fg_color=COLOR_PANEL,
            button_color=COLOR_PRIMARIO,
            button_hover_color=COLOR_SECUNDARIO,
            text_color=COLOR_TEXTO,
            dropdown_fg_color=COLOR_PANEL,
            dropdown_text_color=COLOR_TEXTO,
            variable=self.variable_estado,
            values=[
                "Todos",
                "Normal",
                "Stock bajo",
                "Sin stock",
                "Próximo a vencer",
                "Vencido"
            ],
            state="readonly",
            command=lambda opcion: self.cargar_tabla()
        )
        filtro.grid(
            row=0,
            column=1,
            padx=(10, 0)
        )

        ctk.CTkButton(
            barra,
            text="Buscar",
            width=90,
            height=40,
            corner_radius=9,
            fg_color=COLOR_AZUL,
            hover_color="#2563EB",
            command=self.cargar_tabla
        ).grid(
            row=0,
            column=2,
            padx=(10, 0)
        )

        ctk.CTkButton(
            barra,
            text="Limpiar",
            width=90,
            height=40,
            corner_radius=9,
            fg_color=COLOR_PANEL,
            hover_color=COLOR_SELECCION,
            border_width=1,
            border_color=COLOR_BORDE,
            text_color=COLOR_TEXTO,
            command=self.limpiar_busqueda
        ).grid(
            row=0,
            column=3,
            padx=(8, 0)
        )

        ctk.CTkButton(
            barra,
            text="Carga masiva",
            width=120,
            height=40,
            corner_radius=9,
            fg_color=COLOR_PANEL,
            hover_color=COLOR_SELECCION,
            border_width=1,
            border_color=COLOR_PRIMARIO,
            text_color=COLOR_PRIMARIO,
            command=self.generar_carga_masiva
        ).grid(
            row=0,
            column=4,
            padx=(18, 8)
        )

        ctk.CTkButton(
            barra,
            text="Nuevo medicamento",
            width=150,
            height=40,
            corner_radius=9,
            fg_color=COLOR_PRIMARIO,
            hover_color="#176B57",
            command=self.abrir_nuevo_medicamento
        ).grid(
            row=0,
            column=5
        )

    #muestra los principales valores del inventario
    def crear_resumen(self):
        self.resumen = ctk.CTkFrame(
            self,
            height=72,
            corner_radius=12,
            fg_color=COLOR_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )
        self.resumen.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 14)
        )
        self.resumen.grid_propagate(False)

        for columna in range(5):
            self.resumen.grid_columnconfigure(columna, weight=1)

        self.etiquetas_resumen = {}
        indicadores = [
            ("total", "Medicamentos", COLOR_AZUL),
            ("stock_bajo", "Stock bajo", COLOR_ADVERTENCIA),
            ("sin_stock", "Sin stock", COLOR_PELIGRO),
            ("proximos", "Próximos a vencer", COLOR_AZUL),
            ("vencidos", "Vencidos", COLOR_PELIGRO)
        ]

        for columna, (clave, texto, color) in enumerate(indicadores):
            bloque = ctk.CTkFrame(
                self.resumen,
                corner_radius=0,
                fg_color="transparent"
            )
            bloque.grid(
                row=0,
                column=columna,
                sticky="nsew",
                padx=14,
                pady=11
            )

            ctk.CTkLabel(
                bloque,
                text=texto,
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=9
                ),
                text_color=COLOR_TEXTO_SUAVE
            ).pack(anchor="w")

            etiqueta = ctk.CTkLabel(
                bloque,
                text="0",
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=18,
                    weight="bold"
                ),
                text_color=color
            )
            etiqueta.pack(anchor="w")
            self.etiquetas_resumen[clave] = etiqueta

    #divide la tabla y el detalle del medicamento seleccionado
    def crear_zona_inventario(self):
        zona = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="transparent"
        )
        zona.grid(
            row=2,
            column=0,
            sticky="nsew"
        )
        zona.grid_rowconfigure(0, weight=1)
        zona.grid_columnconfigure(0, weight=1)

        self.crear_panel_tabla(zona)
        self.crear_panel_detalle(zona)

    #crea la tabla donde se muestran los registros del arbol
    def crear_panel_tabla(self, contenedor):
        panel = ctk.CTkFrame(
            contenedor,
            corner_radius=12,
            fg_color=COLOR_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )
        panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 12)
        )
        panel.grid_rowconfigure(1, weight=1)
        panel.grid_columnconfigure(0, weight=1)

        encabezado = ctk.CTkFrame(
            panel,
            corner_radius=0,
            fg_color="transparent"
        )
        encabezado.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=18,
            pady=(16, 8)
        )
        encabezado.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            encabezado,
            text="Medicamentos registrados",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=15,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).grid(row=0, column=0, sticky="w")

        self.etiqueta_resultados = ctk.CTkLabel(
            encabezado,
            text="0 registros",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=9
            ),
            text_color=COLOR_TEXTO_SUAVE
        )
        self.etiqueta_resultados.grid(row=0, column=1, sticky="e")

        marco_tabla = tk.Frame(
            panel,
            bg=COLOR_PANEL
        )
        marco_tabla.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=16,
            pady=(4, 16)
        )
        marco_tabla.grid_rowconfigure(0, weight=1)
        marco_tabla.grid_columnconfigure(0, weight=1)

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "Inventario.Treeview",
            background=COLOR_PANEL,
            fieldbackground=COLOR_PANEL,
            foreground=COLOR_TEXTO,
            borderwidth=0,
            rowheight=32,
            font=("Segoe UI", 9)
        )
        estilo.configure(
            "Inventario.Treeview.Heading",
            background=COLOR_FILA,
            foreground=COLOR_TEXTO,
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 9, "bold")
        )
        estilo.map(
            "Inventario.Treeview",
            background=[("selected", COLOR_SELECCION)],
            foreground=[("selected", COLOR_TEXTO)]
        )

        columnas = (
            "codigo",
            "nombre",
            "categoria",
            "lote",
            "vencimiento",
            "stock",
            "minimo",
            "precio",
            "estado"
        )
        self.tabla = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            style="Inventario.Treeview",
            selectmode="browse"
        )

        encabezados = {
            "codigo": "Código",
            "nombre": "Medicamento",
            "categoria": "Categoría",
            "lote": "Lote",
            "vencimiento": "Vencimiento",
            "stock": "Stock",
            "minimo": "Mínimo",
            "precio": "Precio",
            "estado": "Estado"
        }
        anchos = {
            "codigo": 65,
            "nombre": 170,
            "categoria": 120,
            "lote": 85,
            "vencimiento": 105,
            "stock": 65,
            "minimo": 65,
            "precio": 75,
            "estado": 125
        }

        for columna in columnas:
            self.tabla.heading(
                columna,
                text=encabezados[columna]
            )
            self.tabla.column(
                columna,
                width=anchos[columna],
                minwidth=55,
                anchor="center"
            )

        self.tabla.column("nombre", anchor="w")
        self.tabla.column("categoria", anchor="w")

        desplazamiento_y = ttk.Scrollbar(
            marco_tabla,
            orient="vertical",
            command=self.tabla.yview
        )
        desplazamiento_x = ttk.Scrollbar(
            marco_tabla,
            orient="horizontal",
            command=self.tabla.xview
        )
        self.tabla.configure(
            yscrollcommand=desplazamiento_y.set,
            xscrollcommand=desplazamiento_x.set
        )

        self.tabla.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        desplazamiento_y.grid(
            row=0,
            column=1,
            sticky="ns"
        )
        desplazamiento_x.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        self.tabla.tag_configure(
            "vencido",
            foreground=COLOR_PELIGRO
        )
        self.tabla.tag_configure(
            "alerta",
            foreground="#B77900"
        )
        self.tabla.tag_configure(
            "normal",
            foreground=COLOR_TEXTO
        )
        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.seleccionar_medicamento
        )
        self.tabla.bind(
            "<Double-1>",
            lambda evento: self.editar_medicamento()
        )

    #crea el panel lateral con imagen y acciones del registro
    def crear_panel_detalle(self, contenedor):
        self.panel_detalle = ctk.CTkFrame(
            contenedor,
            width=300,
            corner_radius=12,
            fg_color=COLOR_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )
        self.panel_detalle.grid(
            row=0,
            column=1,
            sticky="nsew"
        )
        self.panel_detalle.grid_propagate(False)
        self.panel_detalle.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.panel_detalle,
            text="Detalle del medicamento",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=15,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(18, 12)
        )

        self.marco_imagen = ctk.CTkFrame(
            self.panel_detalle,
            width=260,
            height=180,
            corner_radius=10,
            fg_color=COLOR_FILA
        )
        self.marco_imagen.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 14)
        )
        self.marco_imagen.grid_propagate(False)

        self.etiqueta_imagen = ctk.CTkLabel(
            self.marco_imagen,
            text="Seleccione un medicamento",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10
            ),
            text_color=COLOR_TEXTO_SUAVE
        )
        self.etiqueta_imagen.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self.etiqueta_nombre = ctk.CTkLabel(
            self.panel_detalle,
            text="Ningún registro seleccionado",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=16,
                weight="bold"
            ),
            text_color=COLOR_TEXTO,
            wraplength=250,
            justify="left"
        )
        self.etiqueta_nombre.grid(
            row=2,
            column=0,
            sticky="w",
            padx=20
        )

        self.etiqueta_estado = ctk.CTkLabel(
            self.panel_detalle,
            text="Sin selección",
            height=28,
            corner_radius=7,
            fg_color=COLOR_FILA,
            text_color=COLOR_TEXTO_SUAVE,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=9,
                weight="bold"
            )
        )
        self.etiqueta_estado.grid(
            row=3,
            column=0,
            sticky="w",
            padx=20,
            pady=(8, 13)
        )

        self.etiqueta_datos = ctk.CTkLabel(
            self.panel_detalle,
            text="Código: -\nCategoría: -\nLote: -\nVencimiento: -\nStock: -\nPrecio: -",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10
            ),
            text_color=COLOR_TEXTO_SUAVE,
            justify="left"
        )
        self.etiqueta_datos.grid(
            row=4,
            column=0,
            sticky="w",
            padx=20
        )

        acciones = ctk.CTkFrame(
            self.panel_detalle,
            corner_radius=0,
            fg_color="transparent"
        )
        acciones.grid(
            row=5,
            column=0,
            sticky="sew",
            padx=20,
            pady=18
        )
        for columna in range(2):
            acciones.grid_columnconfigure(columna, weight=1)
        self.panel_detalle.grid_rowconfigure(5, weight=1)

        ctk.CTkButton(
            acciones,
            text="Editar",
            height=36,
            corner_radius=8,
            fg_color=COLOR_AZUL,
            hover_color="#2563EB",
            command=self.editar_medicamento
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 5),
            pady=4
        )

        ctk.CTkButton(
            acciones,
            text="Eliminar",
            height=36,
            corner_radius=8,
            fg_color=COLOR_PELIGRO,
            hover_color="#DC2626",
            command=self.eliminar_medicamento
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(5, 0),
            pady=4
        )

        ctk.CTkButton(
            acciones,
            text="Agregar stock",
            height=36,
            corner_radius=8,
            fg_color=COLOR_PRIMARIO,
            hover_color="#176B57",
            command=lambda: self.cambiar_stock("agregar")
        ).grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 5),
            pady=4
        )

        ctk.CTkButton(
            acciones,
            text="Retirar stock",
            height=36,
            corner_radius=8,
            fg_color=COLOR_PANEL,
            hover_color=COLOR_SELECCION,
            border_width=1,
            border_color=COLOR_ADVERTENCIA,
            text_color="#B77900",
            command=lambda: self.cambiar_stock("retirar")
        ).grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(5, 0),
            pady=4
        )

    #devuelve los registros que coinciden con la busqueda y el estado
    def obtener_registros_filtrados(self):
        texto = self.variable_busqueda.get().strip().lower()
        estado = self.variable_estado.get().strip().upper()
        registros = []

        for medicamento in self.gestor.obtener_todos():
            coincide_texto = (
                not texto
                or texto in str(medicamento.codigo)
                or texto in medicamento.nombre.lower()
                or texto in medicamento.categoria.lower()
                or texto in medicamento.lote.lower()
            )

            estado_medicamento = medicamento.obtener_estado()
            coincide_estado = (
                estado == "TODOS"
                or estado == estado_medicamento
            )

            if coincide_texto and coincide_estado:
                registros.append(medicamento)

        return registros

    #actualiza la tabla con el recorrido ordenado del arbol
    def cargar_tabla(self):
        seleccion_anterior = None

        if self.medicamento_seleccionado is not None:
            seleccion_anterior = self.medicamento_seleccionado.codigo

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        registros = self.obtener_registros_filtrados()

        for medicamento in registros:
            estado = medicamento.obtener_estado()

            if estado == "VENCIDO" or estado == "SIN STOCK":
                etiqueta = "vencido"
            elif estado in ("STOCK BAJO", "PRÓXIMO A VENCER"):
                etiqueta = "alerta"
            else:
                etiqueta = "normal"

            self.tabla.insert(
                "",
                "end",
                iid=str(medicamento.codigo),
                values=(
                    medicamento.codigo,
                    medicamento.nombre,
                    medicamento.categoria,
                    medicamento.lote,
                    medicamento.fecha_vencimiento.strftime("%Y-%m-%d"),
                    medicamento.stock,
                    medicamento.stock_minimo,
                    f"${medicamento.precio:.2f}",
                    estado
                ),
                tags=(etiqueta,)
            )

        self.etiqueta_resultados.configure(
            text=f"{len(registros)} registros"
        )
        self.actualizar_resumen()

        if (
            seleccion_anterior is not None
            and self.tabla.exists(str(seleccion_anterior))
        ):
            self.tabla.selection_set(str(seleccion_anterior))
            self.tabla.focus(str(seleccion_anterior))
            self.mostrar_detalle(
                self.gestor.buscar_por_codigo(seleccion_anterior)
            )
        elif not registros:
            self.limpiar_detalle()

    #actualiza los indicadores colocados sobre la tabla
    def actualizar_resumen(self):
        resumen = self.gestor.obtener_resumen()

        for clave, etiqueta in self.etiquetas_resumen.items():
            etiqueta.configure(
                text=str(resumen[clave])
            )

    #limpia el texto y el filtro del buscador
    def limpiar_busqueda(self):
        self.variable_busqueda.set("")
        self.variable_estado.set("Todos")
        self.cargar_tabla()

    #recupera el objeto relacionado con la fila seleccionada
    def seleccionar_medicamento(self, evento=None):
        seleccion = self.tabla.selection()

        if not seleccion:
            return

        codigo = int(seleccion[0])
        medicamento = self.gestor.buscar_por_codigo(codigo)
        self.mostrar_detalle(medicamento)

    #muestra la imagen y los datos del registro seleccionado
    def mostrar_detalle(self, medicamento):
        if medicamento is None:
            self.limpiar_detalle()
            return

        self.medicamento_seleccionado = medicamento
        estado = medicamento.obtener_estado()

        if estado in ("VENCIDO", "SIN STOCK"):
            color_estado = COLOR_PELIGRO
            fondo_estado = "#FDECEC"
        elif estado in ("STOCK BAJO", "PRÓXIMO A VENCER"):
            color_estado = "#B77900"
            fondo_estado = "#FFF5D9"
        else:
            color_estado = COLOR_PRIMARIO
            fondo_estado = COLOR_SELECCION

        self.etiqueta_nombre.configure(
            text=medicamento.nombre
        )
        self.etiqueta_estado.configure(
            text=f"  {estado}  ",
            text_color=color_estado,
            fg_color=fondo_estado
        )
        self.etiqueta_datos.configure(
            text=(
                f"Código: {medicamento.codigo}\n"
                f"Categoría: {medicamento.categoria}\n"
                f"Lote: {medicamento.lote}\n"
                "Vencimiento: "
                f"{medicamento.fecha_vencimiento.strftime('%Y-%m-%d')}\n"
                f"Stock: {medicamento.stock} unidades\n"
                f"Stock mínimo: {medicamento.stock_minimo}\n"
                f"Precio: ${medicamento.precio:.2f}"
            )
        )

        self.imagen_detalle = cargar_imagen_medicamento_ctk(
            medicamento.imagen,
            220,
            150
        )

        if self.imagen_detalle is None:
            self.imagen_detalle = cargar_imagen_interfaz_ctk(
                "logo_icono.png",
                100,
                120
            )

        if self.imagen_detalle is not None:
            self.etiqueta_imagen.configure(
                text="",
                image=self.imagen_detalle
            )
        else:
            self.etiqueta_imagen.configure(
                text="Imagen no disponible",
                image=None
            )

    #restablece el panel cuando no existe una seleccion
    def limpiar_detalle(self):
        self.medicamento_seleccionado = None
        self.imagen_detalle = None
        self.etiqueta_imagen.configure(
            text="Seleccione un medicamento",
            image=None
        )
        self.etiqueta_nombre.configure(
            text="Ningún registro seleccionado"
        )
        self.etiqueta_estado.configure(
            text="Sin selección",
            text_color=COLOR_TEXTO_SUAVE,
            fg_color=COLOR_FILA
        )
        self.etiqueta_datos.configure(
            text="Código: -\nCategoría: -\nLote: -\nVencimiento: -\nStock: -\nPrecio: -"
        )

    #abre el formulario para crear un registro nuevo
    def abrir_nuevo_medicamento(self):
        VentanaMedicamento(
            self,
            self.gestor,
            al_guardar=self.registro_guardado
        )

    #abre el formulario con los datos de la fila seleccionada
    def editar_medicamento(self):
        if self.medicamento_seleccionado is None:
            messagebox.showwarning(
                "Seleccionar medicamento",
                "Seleccione un medicamento para editarlo."
            )
            return

        VentanaMedicamento(
            self,
            self.gestor,
            medicamento=self.medicamento_seleccionado,
            al_guardar=self.registro_guardado
        )

    #actualiza la vista despues de guardar un medicamento
    def registro_guardado(self, medicamento):
        self.medicamento_seleccionado = medicamento
        self.cargar_tabla()

        if self.tabla.exists(str(medicamento.codigo)):
            self.tabla.selection_set(str(medicamento.codigo))
            self.tabla.focus(str(medicamento.codigo))
            self.tabla.see(str(medicamento.codigo))
            self.mostrar_detalle(medicamento)

    #elimina el registro seleccionado despues de confirmarlo
    def eliminar_medicamento(self):
        medicamento = self.medicamento_seleccionado

        if medicamento is None:
            messagebox.showwarning(
                "Seleccionar medicamento",
                "Seleccione un medicamento para eliminarlo."
            )
            return

        confirmar = messagebox.askyesno(
            "Eliminar medicamento",
            f"¿Desea eliminar {medicamento.nombre}?"
        )

        if not confirmar:
            return

        eliminado = self.gestor.eliminar_medicamento(
            medicamento.codigo
        )

        if eliminado:
            self.limpiar_detalle()
            self.cargar_tabla()
            messagebox.showinfo(
                "Medicamento eliminado",
                "El medicamento fue eliminado del árbol y del archivo CSV."
            )

    #agrega o retira unidades del medicamento seleccionado
    def cambiar_stock(self, operacion):
        medicamento = self.medicamento_seleccionado

        if medicamento is None:
            messagebox.showwarning(
                "Seleccionar medicamento",
                "Seleccione un medicamento para actualizar el stock."
            )
            return

        cantidad = simpledialog.askinteger(
            "Actualizar stock",
            "Ingrese la cantidad de unidades:",
            parent=self,
            minvalue=1
        )

        if cantidad is None:
            return

        try:
            if operacion == "agregar":
                actualizado = self.gestor.agregar_stock(
                    medicamento.codigo,
                    cantidad
                )
            else:
                actualizado = self.gestor.retirar_stock(
                    medicamento.codigo,
                    cantidad
                )

            self.medicamento_seleccionado = actualizado
            self.cargar_tabla()
            self.mostrar_detalle(actualizado)
        except ValueError as error:
            messagebox.showerror(
                "No se pudo actualizar",
                str(error)
            )

    #genera varios registros y los inserta dentro del arbol
    def generar_carga_masiva(self):
        cantidad = simpledialog.askinteger(
            "Carga masiva",
            "Cantidad de medicamentos que se generarán:",
            parent=self,
            initialvalue=1000,
            minvalue=1,
            maxvalue=5000
        )

        if cantidad is None:
            return

        confirmar = messagebox.askyesno(
            "Confirmar carga masiva",
            f"¿Desea generar {cantidad} medicamentos de prueba?"
        )

        if not confirmar:
            return

        try:
            nuevos = self.gestor.generar_carga_masiva(
                cantidad=cantidad
            )
            self.cargar_tabla()
            messagebox.showinfo(
                "Carga masiva completada",
                f"Se insertaron {len(nuevos)} registros con nombres "
                "sintéticos únicos en el árbol AVL."
            )
        except (ValueError, OSError) as error:
            messagebox.showerror(
                "No se pudo completar la carga",
                str(error)
            )


class VentanaMedicamento(ctk.CTkToplevel):

    def __init__(
        self,
        master,
        gestor_inventario,
        medicamento=None,
        al_guardar=None
    ):
        super().__init__(master)

        #prepara el formulario para crear o actualizar un registro
        self.gestor = gestor_inventario
        self.medicamento = medicamento
        self.al_guardar = al_guardar
        self.ruta_imagen = ""
        self.imagen_previa = None

        self.title(
            "Nuevo medicamento"
            if medicamento is None
            else "Editar medicamento"
        )
        self.geometry("720x680")
        self.minsize(680, 640)
        self.configure(fg_color=COLOR_FONDO)
        self.transient(master.winfo_toplevel())
        self.grab_set()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.variables = {
            "codigo": tk.StringVar(),
            "nombre": tk.StringVar(),
            "categoria": tk.StringVar(),
            "lote": tk.StringVar(),
            "fecha_vencimiento": tk.StringVar(),
            "stock": tk.StringVar(),
            "stock_minimo": tk.StringVar(),
            "precio": tk.StringVar()
        }

        self.crear_encabezado()
        self.crear_formulario()
        self.cargar_datos_iniciales()

    #crea el titulo colocado sobre los campos
    def crear_encabezado(self):
        encabezado = ctk.CTkFrame(
            self,
            height=82,
            corner_radius=0,
            fg_color=COLOR_PANEL
        )
        encabezado.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        titulo = (
            "Registrar medicamento"
            if self.medicamento is None
            else "Actualizar medicamento"
        )
        descripcion = (
            "Complete los datos que se insertarán en el árbol AVL"
            if self.medicamento is None
            else "Modifique los datos conservando el código principal"
        )

        ctk.CTkLabel(
            encabezado,
            text=titulo,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=21,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).pack(
            anchor="w",
            padx=28,
            pady=(15, 1)
        )

        ctk.CTkLabel(
            encabezado,
            text=descripcion,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10
            ),
            text_color=COLOR_TEXTO_SUAVE
        ).pack(anchor="w", padx=28)

    #crea los campos y botones del formulario
    def crear_formulario(self):
        contenido = ctk.CTkScrollableFrame(
            self,
            corner_radius=0,
            fg_color=COLOR_FONDO
        )
        contenido.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=22,
            pady=18
        )
        for columna in range(2):
            contenido.grid_columnconfigure(columna, weight=1)

        self.entradas = {}
        campos = [
            ("codigo", "Código", "Ejemplo: 101"),
            ("nombre", "Nombre", "Ejemplo: Paracetamol 500mg"),
            ("categoria", "Categoría", "Seleccione una categoría"),
            ("lote", "Lote", "Ejemplo: PAR-001"),
            (
                "fecha_vencimiento",
                "Fecha de vencimiento",
                "Formato: AAAA-MM-DD"
            ),
            ("stock", "Stock inicial", "Ejemplo: 50"),
            ("stock_minimo", "Stock mínimo", "Ejemplo: 10"),
            ("precio", "Precio", "Ejemplo: 3.50")
        ]

        for indice, (clave, texto, ayuda) in enumerate(campos):
            fila = indice // 2
            columna = indice % 2

            grupo = ctk.CTkFrame(
                contenido,
                corner_radius=0,
                fg_color="transparent"
            )
            grupo.grid(
                row=fila,
                column=columna,
                sticky="ew",
                padx=7,
                pady=7
            )
            grupo.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                grupo,
                text=texto,
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=10,
                    weight="bold"
                ),
                text_color=COLOR_TEXTO
            ).grid(row=0, column=0, sticky="w", pady=(0, 5))

            if clave == "categoria":
                entrada = ctk.CTkComboBox(
                    grupo,
                    height=39,
                    corner_radius=8,
                    border_color=COLOR_BORDE,
                    fg_color=COLOR_PANEL,
                    button_color=COLOR_PRIMARIO,
                    button_hover_color=COLOR_SECUNDARIO,
                    text_color=COLOR_TEXTO,
                    dropdown_fg_color=COLOR_PANEL,
                    dropdown_text_color=COLOR_TEXTO,
                    variable=self.variables[clave],
                    values=[
                        "Analgésico",
                        "Antibiótico",
                        "Antihistamínico",
                        "Antiinflamatorio",
                        "Antihipertensivo",
                        "Antidiabético",
                        "Antifúngico",
                        "Cardiovascular",
                        "Corticoide",
                        "Gastrointestinal",
                        "Neurológico",
                        "Respiratorio",
                        "Vitaminas",
                        "General"
                    ]
                )
            else:
                entrada = ctk.CTkEntry(
                    grupo,
                    height=39,
                    corner_radius=8,
                    border_color=COLOR_BORDE,
                    fg_color=COLOR_PANEL,
                    text_color=COLOR_TEXTO,
                    placeholder_text=ayuda,
                    textvariable=self.variables[clave]
                )

            entrada.grid(row=1, column=0, sticky="ew")
            self.entradas[clave] = entrada

        imagen = ctk.CTkFrame(
            contenido,
            corner_radius=10,
            fg_color=COLOR_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )
        imagen.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=7,
            pady=(14, 8)
        )
        imagen.grid_columnconfigure(1, weight=1)

        self.marco_previo = ctk.CTkFrame(
            imagen,
            width=135,
            height=115,
            corner_radius=8,
            fg_color=COLOR_FILA
        )
        self.marco_previo.grid(
            row=0,
            column=0,
            rowspan=3,
            padx=14,
            pady=14
        )
        self.marco_previo.grid_propagate(False)

        self.etiqueta_previa = ctk.CTkLabel(
            self.marco_previo,
            text="Sin imagen",
            font=ctk.CTkFont(size=9),
            text_color=COLOR_TEXTO_SUAVE
        )
        self.etiqueta_previa.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        ctk.CTkLabel(
            imagen,
            text="Imagen del medicamento",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=11,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).grid(
            row=0,
            column=1,
            sticky="sw",
            padx=(0, 14),
            pady=(16, 2)
        )

        self.etiqueta_ruta = ctk.CTkLabel(
            imagen,
            text="Se usará la imagen predeterminada",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=9
            ),
            text_color=COLOR_TEXTO_SUAVE,
            wraplength=390,
            justify="left"
        )
        self.etiqueta_ruta.grid(
            row=1,
            column=1,
            sticky="nw",
            padx=(0, 14)
        )

        ctk.CTkButton(
            imagen,
            text="Seleccionar imagen",
            width=145,
            height=34,
            corner_radius=8,
            fg_color=COLOR_PANEL,
            hover_color=COLOR_SELECCION,
            border_width=1,
            border_color=COLOR_PRIMARIO,
            text_color=COLOR_PRIMARIO,
            command=self.seleccionar_imagen
        ).grid(
            row=2,
            column=1,
            sticky="nw",
            padx=(0, 14),
            pady=(7, 14)
        )

        botones = ctk.CTkFrame(
            contenido,
            corner_radius=0,
            fg_color="transparent"
        )
        botones.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="e",
            padx=7,
            pady=(14, 6)
        )

        ctk.CTkButton(
            botones,
            text="Cancelar",
            width=110,
            height=40,
            corner_radius=8,
            fg_color=COLOR_PANEL,
            hover_color=COLOR_SELECCION,
            border_width=1,
            border_color=COLOR_BORDE,
            text_color=COLOR_TEXTO,
            command=self.destroy
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            botones,
            text="Guardar medicamento",
            width=165,
            height=40,
            corner_radius=8,
            fg_color=COLOR_PRIMARIO,
            hover_color="#176B57",
            command=self.guardar
        ).pack(side="left")

    #carga los datos del registro o prepara el siguiente codigo
    def cargar_datos_iniciales(self):
        if self.medicamento is None:
            self.variables["codigo"].set(
                str(self.gestor.obtener_siguiente_codigo())
            )
            self.variables["categoria"].set("General")
            self.variables["stock"].set("0")
            self.variables["stock_minimo"].set("10")
            return

        medicamento = self.medicamento
        valores = {
            "codigo": medicamento.codigo,
            "nombre": medicamento.nombre,
            "categoria": medicamento.categoria,
            "lote": medicamento.lote,
            "fecha_vencimiento": medicamento.fecha_vencimiento.strftime(
                "%Y-%m-%d"
            ),
            "stock": medicamento.stock,
            "stock_minimo": medicamento.stock_minimo,
            "precio": medicamento.precio
        }

        for clave, valor in valores.items():
            self.variables[clave].set(str(valor))

        self.entradas["codigo"].configure(state="disabled")
        self.mostrar_imagen_guardada(medicamento.imagen)

    #muestra la imagen que ya se encuentra dentro del proyecto
    def mostrar_imagen_guardada(self, nombre):
        self.imagen_previa = cargar_imagen_medicamento_ctk(
            nombre,
            115,
            95
        )

        if self.imagen_previa is not None:
            self.etiqueta_previa.configure(
                text="",
                image=self.imagen_previa
            )
            self.etiqueta_ruta.configure(
                text=f"Imagen actual: {nombre}"
            )

    #permite escoger una imagen desde el equipo
    def seleccionar_imagen(self):
        ruta = filedialog.askopenfilename(
            parent=self,
            title="Seleccionar imagen del medicamento",
            filetypes=[
                ("Archivos de imagen", "*.png *.jpg *.jpeg *.webp"),
                ("Todos los archivos", "*.*")
            ]
        )

        if not ruta:
            return

        imagen = cargar_imagen_ctk(
            ruta,
            115,
            95
        )

        if imagen is None:
            messagebox.showerror(
                "Imagen no válida",
                "No se pudo abrir la imagen seleccionada.",
                parent=self
            )
            return

        self.ruta_imagen = ruta
        self.imagen_previa = imagen
        self.etiqueta_previa.configure(
            text="",
            image=self.imagen_previa
        )
        self.etiqueta_ruta.configure(
            text=ruta
        )

    #envia los campos al gestor para validar y guardar
    def guardar(self):
        datos = {
            "codigo": self.variables["codigo"].get(),
            "nombre": self.variables["nombre"].get(),
            "categoria": self.variables["categoria"].get(),
            "lote": self.variables["lote"].get(),
            "fecha_vencimiento": self.variables["fecha_vencimiento"].get(),
            "stock": self.variables["stock"].get(),
            "stock_minimo": self.variables["stock_minimo"].get(),
            "precio": self.variables["precio"].get(),
            "imagen": self.ruta_imagen
        }

        try:
            if self.medicamento is None:
                guardado = self.gestor.crear_medicamento(
                    datos
                )
                mensaje = "El medicamento fue registrado correctamente."
            else:
                guardado = self.gestor.actualizar_medicamento(
                    self.medicamento.codigo,
                    datos
                )
                mensaje = "El medicamento fue actualizado correctamente."

            if self.al_guardar is not None:
                self.al_guardar(guardado)

            messagebox.showinfo(
                "Datos guardados",
                mensaje,
                parent=self
            )
            self.destroy()
        except (ValueError, TypeError, OSError) as error:
            messagebox.showerror(
                "No se pudo guardar",
                str(error),
                parent=self
            )