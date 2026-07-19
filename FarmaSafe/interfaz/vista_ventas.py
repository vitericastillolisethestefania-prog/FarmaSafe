import tkinter as tk
from tkinter import messagebox, ttk

import customtkinter as ctk


#aplica los colores claros usados en el resto del sistema
COLOR_FONDO = "#F6F8FA"
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


class VistaVentas(ctk.CTkFrame):

    def __init__(
        self,
        master,
        gestor_ventas,
        gestor_inventario
    ):
        super().__init__(
            master,
            corner_radius=0,
            fg_color="transparent"
        )

        #conecta la vista con las ventas y el inventario
        self.gestor_ventas = gestor_ventas
        self.gestor_inventario = gestor_inventario
        self.venta_actual = self.gestor_ventas.crear_venta()

        self.variable_busqueda = tk.StringVar()
        self.variable_estado = tk.StringVar(value="Disponibles")
        self.variable_cantidad = tk.StringVar(value="1")
        self.variable_cliente = tk.StringVar(value="Consumidor final")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.crear_resumen()
        self.crear_pestanas()
        self.actualizar_vista()

    #crea los indicadores generales de las ventas guardadas
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
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 12)
        )
        self.resumen.grid_propagate(False)

        for columna in range(5):
            self.resumen.grid_columnconfigure(columna, weight=1)

        indicadores = [
            ("cantidad_ventas", "Ventas registradas", COLOR_AZUL),
            ("ingresos", "Ingresos", COLOR_PRIMARIO),
            ("unidades", "Unidades vendidas", COLOR_ADVERTENCIA),
            ("ventas_hoy", "Ventas de hoy", COLOR_AZUL),
            ("producto", "Producto más vendido", COLOR_PRIMARIO)
        ]

        self.etiquetas_resumen = {}

        for columna, (clave, titulo, color) in enumerate(indicadores):
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
                pady=10
            )

            ctk.CTkLabel(
                bloque,
                text=titulo,
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
                    size=17,
                    weight="bold"
                ),
                text_color=color
            )
            etiqueta.pack(anchor="w")
            self.etiquetas_resumen[clave] = etiqueta

    #separa la preparacion de una venta y el historial
    def crear_pestanas(self):
        self.pestanas = ctk.CTkTabview(
            self,
            corner_radius=12,
            fg_color=COLOR_FONDO,
            border_width=0,
            segmented_button_fg_color=COLOR_PANEL,
            segmented_button_selected_color=COLOR_PRIMARIO,
            segmented_button_selected_hover_color="#176B57",
            segmented_button_unselected_color=COLOR_PANEL,
            segmented_button_unselected_hover_color=COLOR_SELECCION,
            text_color=COLOR_TEXTO
        )
        self.pestanas.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        pestana_nueva = self.pestanas.add("Nueva venta")
        pestana_historial = self.pestanas.add("Historial de ventas")

        self.crear_pestana_nueva(pestana_nueva)
        self.crear_pestana_historial(pestana_historial)

    #crea la zona que muestra los productos y el carrito
    def crear_pestana_nueva(self, contenedor):
        contenedor.configure(fg_color=COLOR_FONDO)
        contenedor.grid_rowconfigure(0, weight=1)
        contenedor.grid_columnconfigure(0, weight=3)
        contenedor.grid_columnconfigure(1, weight=2)

        self.crear_catalogo(contenedor)
        self.crear_carrito(contenedor)

    #crea la tabla para seleccionar medicamentos del inventario
    def crear_catalogo(self, contenedor):
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
            padx=(0, 8),
            pady=(8, 0)
        )
        panel.grid_rowconfigure(2, weight=1)
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
            pady=(15, 8)
        )
        encabezado.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            encabezado,
            text="Medicamentos disponibles",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=16,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).grid(row=0, column=0, sticky="w")

        self.etiqueta_productos = ctk.CTkLabel(
            encabezado,
            text="0 productos",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=9
            ),
            text_color=COLOR_TEXTO_SUAVE
        )
        self.etiqueta_productos.grid(row=0, column=1, sticky="e")

        acciones = ctk.CTkFrame(
            panel,
            corner_radius=0,
            fg_color="transparent"
        )
        acciones.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=18,
            pady=(0, 10)
        )
        acciones.grid_columnconfigure(0, weight=1)

        buscador = ctk.CTkEntry(
            acciones,
            height=38,
            corner_radius=9,
            border_color=COLOR_BORDE,
            fg_color=COLOR_PANEL,
            text_color=COLOR_TEXTO,
            placeholder_text="Buscar por código, nombre o categoría",
            textvariable=self.variable_busqueda
        )
        buscador.grid(
            row=0,
            column=0,
            sticky="ew"
        )
        buscador.bind(
            "<Return>",
            lambda evento: self.cargar_productos()
        )

        filtro = ctk.CTkComboBox(
            acciones,
            width=145,
            height=38,
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
                "Disponibles",
                "Stock bajo",
                "Sin stock",
                "Vencidos"
            ],
            state="readonly",
            command=lambda opcion: self.cargar_productos()
        )
        filtro.grid(
            row=0,
            column=1,
            padx=(8, 0)
        )

        ctk.CTkLabel(
            acciones,
            text="Cantidad",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=9,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).grid(
            row=0,
            column=2,
            padx=(12, 5)
        )

        ctk.CTkEntry(
            acciones,
            width=58,
            height=38,
            corner_radius=9,
            border_color=COLOR_BORDE,
            fg_color=COLOR_PANEL,
            text_color=COLOR_TEXTO,
            justify="center",
            textvariable=self.variable_cantidad
        ).grid(row=0, column=3)

        ctk.CTkButton(
            acciones,
            text="Agregar",
            width=95,
            height=38,
            corner_radius=9,
            fg_color=COLOR_PRIMARIO,
            hover_color="#176B57",
            command=self.agregar_al_carrito
        ).grid(
            row=0,
            column=4,
            padx=(8, 0)
        )

        zona_tabla = ctk.CTkFrame(
            panel,
            corner_radius=0,
            fg_color="transparent"
        )
        zona_tabla.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=18,
            pady=(0, 18)
        )
        zona_tabla.grid_rowconfigure(0, weight=1)
        zona_tabla.grid_columnconfigure(0, weight=1)

        self.configurar_estilo_tablas()

        columnas = (
            "codigo",
            "medicamento",
            "categoria",
            "stock",
            "precio",
            "estado"
        )
        self.tabla_productos = ttk.Treeview(
            zona_tabla,
            columns=columnas,
            show="headings",
            style="VentasProductos.Treeview",
            selectmode="browse"
        )

        encabezados = {
            "codigo": "Código",
            "medicamento": "Medicamento",
            "categoria": "Categoría",
            "stock": "Stock",
            "precio": "Precio",
            "estado": "Estado"
        }
        anchos = {
            "codigo": 70,
            "medicamento": 190,
            "categoria": 135,
            "stock": 65,
            "precio": 75,
            "estado": 125
        }

        for columna in columnas:
            self.tabla_productos.heading(
                columna,
                text=encabezados[columna]
            )
            self.tabla_productos.column(
                columna,
                width=anchos[columna],
                minwidth=50,
                anchor="center" if columna != "medicamento" else "w"
            )

        self.tabla_productos.tag_configure(
            "normal",
            foreground=COLOR_TEXTO
        )
        self.tabla_productos.tag_configure(
            "advertencia",
            foreground="#C87900"
        )
        self.tabla_productos.tag_configure(
            "peligro",
            foreground=COLOR_PELIGRO
        )
        self.tabla_productos.bind(
            "<Double-1>",
            lambda evento: self.agregar_al_carrito()
        )

        barra_vertical = ttk.Scrollbar(
            zona_tabla,
            orient="vertical",
            command=self.tabla_productos.yview
        )
        barra_horizontal = ttk.Scrollbar(
            zona_tabla,
            orient="horizontal",
            command=self.tabla_productos.xview
        )
        self.tabla_productos.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set
        )

        self.tabla_productos.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        barra_vertical.grid(row=0, column=1, sticky="ns")
        barra_horizontal.grid(row=1, column=0, sticky="ew")

    #crea el carrito y el resumen de cobro
    def crear_carrito(self, contenedor):
        panel = ctk.CTkFrame(
            contenedor,
            corner_radius=12,
            fg_color=COLOR_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )
        panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0),
            pady=(8, 0)
        )
        panel.grid_rowconfigure(3, weight=1)
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
            pady=(15, 7)
        )
        encabezado.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            encabezado,
            text="Carrito de venta",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=16,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).grid(row=0, column=0, sticky="w")

        self.etiqueta_codigo_venta = ctk.CTkLabel(
            encabezado,
            text="Venta 1",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=9,
                weight="bold"
            ),
            text_color=COLOR_PRIMARIO,
            fg_color=COLOR_SELECCION,
            corner_radius=7,
            padx=10,
            pady=5
        )
        self.etiqueta_codigo_venta.grid(row=0, column=1, sticky="e")

        cliente = ctk.CTkFrame(
            panel,
            corner_radius=0,
            fg_color="transparent"
        )
        cliente.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=18,
            pady=(0, 10)
        )
        cliente.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            cliente,
            text="Cliente",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=9,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))

        ctk.CTkEntry(
            cliente,
            height=38,
            corner_radius=9,
            border_color=COLOR_BORDE,
            fg_color=COLOR_PANEL,
            text_color=COLOR_TEXTO,
            textvariable=self.variable_cliente
        ).grid(row=1, column=0, sticky="ew")

        ctk.CTkLabel(
            panel,
            text="Productos agregados",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=18,
            pady=(0, 6)
        )

        zona_tabla = ctk.CTkFrame(
            panel,
            corner_radius=0,
            fg_color="transparent"
        )
        zona_tabla.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=18
        )
        zona_tabla.grid_rowconfigure(0, weight=1)
        zona_tabla.grid_columnconfigure(0, weight=1)

        columnas = (
            "codigo",
            "producto",
            "cantidad",
            "subtotal"
        )
        self.tabla_carrito = ttk.Treeview(
            zona_tabla,
            columns=columnas,
            show="headings",
            style="VentasCarrito.Treeview",
            selectmode="browse"
        )

        encabezados = {
            "codigo": "Código",
            "producto": "Producto",
            "cantidad": "Cant.",
            "subtotal": "Subtotal"
        }
        anchos = {
            "codigo": 60,
            "producto": 170,
            "cantidad": 60,
            "subtotal": 85
        }

        for columna in columnas:
            self.tabla_carrito.heading(
                columna,
                text=encabezados[columna]
            )
            self.tabla_carrito.column(
                columna,
                width=anchos[columna],
                minwidth=50,
                anchor="center" if columna != "producto" else "w"
            )

        barra_vertical = ttk.Scrollbar(
            zona_tabla,
            orient="vertical",
            command=self.tabla_carrito.yview
        )
        self.tabla_carrito.configure(
            yscrollcommand=barra_vertical.set
        )
        self.tabla_carrito.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        barra_vertical.grid(row=0, column=1, sticky="ns")

        acciones = ctk.CTkFrame(
            panel,
            corner_radius=0,
            fg_color="transparent"
        )
        acciones.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=18,
            pady=(8, 0)
        )
        for columna in range(2):
            acciones.grid_columnconfigure(columna, weight=1)

        ctk.CTkButton(
            acciones,
            text="Quitar seleccionado",
            height=36,
            corner_radius=8,
            fg_color=COLOR_PANEL,
            hover_color="#FEE2E2",
            border_width=1,
            border_color=COLOR_PELIGRO,
            text_color=COLOR_PELIGRO,
            command=self.eliminar_del_carrito
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 5)
        )

        ctk.CTkButton(
            acciones,
            text="Vaciar carrito",
            height=36,
            corner_radius=8,
            fg_color=COLOR_PANEL,
            hover_color=COLOR_SELECCION,
            border_width=1,
            border_color=COLOR_BORDE,
            text_color=COLOR_TEXTO,
            command=self.vaciar_carrito
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(5, 0)
        )

        totales = ctk.CTkFrame(
            panel,
            corner_radius=10,
            fg_color=COLOR_FILA
        )
        totales.grid(
            row=5,
            column=0,
            sticky="ew",
            padx=18,
            pady=12
        )
        totales.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            totales,
            text="Unidades",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10
            ),
            text_color=COLOR_TEXTO_SUAVE
        ).grid(row=0, column=0, sticky="w", padx=14, pady=(11, 4))

        self.etiqueta_unidades = ctk.CTkLabel(
            totales,
            text="0",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        )
        self.etiqueta_unidades.grid(
            row=0,
            column=1,
            sticky="e",
            padx=14,
            pady=(11, 4)
        )

        ctk.CTkLabel(
            totales,
            text="Total a pagar",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=11,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).grid(row=1, column=0, sticky="w", padx=14, pady=(4, 12))

        self.etiqueta_total = ctk.CTkLabel(
            totales,
            text="$0.00",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=23,
                weight="bold"
            ),
            text_color=COLOR_PRIMARIO
        )
        self.etiqueta_total.grid(
            row=1,
            column=1,
            sticky="e",
            padx=14,
            pady=(4, 12)
        )

        ctk.CTkButton(
            panel,
            text="Finalizar venta",
            height=44,
            corner_radius=9,
            fg_color=COLOR_PRIMARIO,
            hover_color="#176B57",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=11,
                weight="bold"
            ),
            command=self.finalizar_venta
        ).grid(
            row=6,
            column=0,
            sticky="ew",
            padx=18,
            pady=(0, 18)
        )

    #crea la tabla de ventas que ya fueron finalizadas
    def crear_pestana_historial(self, contenedor):
        contenedor.configure(fg_color=COLOR_FONDO)
        contenedor.grid_rowconfigure(1, weight=1)
        contenedor.grid_columnconfigure(0, weight=1)

        encabezado = ctk.CTkFrame(
            contenedor,
            corner_radius=0,
            fg_color="transparent"
        )
        encabezado.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(8, 10)
        )
        encabezado.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            encabezado,
            text="Historial de ventas finalizadas",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=16,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).grid(row=0, column=0, sticky="w")

        self.etiqueta_historial = ctk.CTkLabel(
            encabezado,
            text="0 ventas",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=9
            ),
            text_color=COLOR_TEXTO_SUAVE
        )
        self.etiqueta_historial.grid(row=0, column=1, padx=(0, 10))

        ctk.CTkButton(
            encabezado,
            text="Actualizar",
            width=100,
            height=36,
            corner_radius=8,
            fg_color=COLOR_PANEL,
            hover_color=COLOR_SELECCION,
            border_width=1,
            border_color=COLOR_PRIMARIO,
            text_color=COLOR_PRIMARIO,
            command=self.actualizar_vista
        ).grid(row=0, column=2)

        panel = ctk.CTkFrame(
            contenedor,
            corner_radius=12,
            fg_color=COLOR_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )
        panel.grid(
            row=1,
            column=0,
            sticky="nsew",
            pady=(0, 0)
        )
        panel.grid_rowconfigure(0, weight=1)
        panel.grid_columnconfigure(0, weight=1)

        columnas = (
            "codigo",
            "fecha",
            "cliente",
            "unidades",
            "total"
        )
        self.tabla_historial = ttk.Treeview(
            panel,
            columns=columnas,
            show="headings",
            style="VentasHistorial.Treeview",
            selectmode="browse"
        )

        encabezados = {
            "codigo": "Venta",
            "fecha": "Fecha",
            "cliente": "Cliente",
            "unidades": "Unidades",
            "total": "Total"
        }
        anchos = {
            "codigo": 90,
            "fecha": 170,
            "cliente": 300,
            "unidades": 110,
            "total": 130
        }

        for columna in columnas:
            self.tabla_historial.heading(
                columna,
                text=encabezados[columna]
            )
            self.tabla_historial.column(
                columna,
                width=anchos[columna],
                minwidth=70,
                anchor="center" if columna != "cliente" else "w"
            )

        barra_vertical = ttk.Scrollbar(
            panel,
            orient="vertical",
            command=self.tabla_historial.yview
        )
        barra_horizontal = ttk.Scrollbar(
            panel,
            orient="horizontal",
            command=self.tabla_historial.xview
        )
        self.tabla_historial.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set
        )

        self.tabla_historial.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(14, 0),
            pady=(14, 0)
        )
        barra_vertical.grid(
            row=0,
            column=1,
            sticky="ns",
            pady=(14, 0),
            padx=(0, 14)
        )
        barra_horizontal.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(14, 0),
            pady=(0, 14)
        )

    #prepara el estilo claro de las tres tablas
    def configurar_estilo_tablas(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")

        for nombre in (
            "VentasProductos.Treeview",
            "VentasCarrito.Treeview",
            "VentasHistorial.Treeview"
        ):
            estilo.configure(
                nombre,
                background=COLOR_PANEL,
                fieldbackground=COLOR_PANEL,
                foreground=COLOR_TEXTO,
                rowheight=31,
                borderwidth=0,
                font=("Segoe UI", 9)
            )
            estilo.configure(
                f"{nombre}.Heading",
                background=COLOR_FILA,
                foreground=COLOR_TEXTO,
                relief="flat",
                font=("Segoe UI", 9, "bold")
            )
            estilo.map(
                nombre,
                background=[("selected", COLOR_SELECCION)],
                foreground=[("selected", COLOR_TEXTO)]
            )

    #revisa si un medicamento coincide con el filtro seleccionado
    def medicamento_coincide(self, medicamento, texto, estado):
        contenido = (
            f"{medicamento.codigo} "
            f"{medicamento.nombre} "
            f"{medicamento.categoria} "
            f"{medicamento.lote}"
        ).lower()

        if texto and texto not in contenido:
            return False

        if estado == "Todos":
            return True

        if estado == "Disponibles":
            return (
                medicamento.stock > 0
                and not medicamento.esta_vencido()
            )

        if estado == "Stock bajo":
            return medicamento.tiene_stock_bajo()

        if estado == "Sin stock":
            return medicamento.stock == 0

        if estado == "Vencidos":
            return medicamento.esta_vencido()

        return True

    #carga en la tabla los medicamentos que cumplen el filtro
    def cargar_productos(self):
        for elemento in self.tabla_productos.get_children():
            self.tabla_productos.delete(elemento)

        texto = self.variable_busqueda.get().strip().lower()
        estado = self.variable_estado.get()
        cantidad = 0

        for medicamento in self.gestor_inventario.obtener_todos():
            if not self.medicamento_coincide(
                medicamento,
                texto,
                estado
            ):
                continue

            estado_medicamento = medicamento.obtener_estado()

            if medicamento.esta_vencido() or medicamento.stock == 0:
                etiqueta = "peligro"
            elif medicamento.tiene_stock_bajo():
                etiqueta = "advertencia"
            else:
                etiqueta = "normal"

            self.tabla_productos.insert(
                "",
                "end",
                iid=str(medicamento.codigo),
                values=(
                    medicamento.codigo,
                    medicamento.nombre,
                    medicamento.categoria,
                    medicamento.stock,
                    f"${medicamento.precio:.2f}",
                    estado_medicamento
                ),
                tags=(etiqueta,)
            )
            cantidad += 1

        self.etiqueta_productos.configure(
            text=f"{cantidad} productos"
        )

    #obtiene un valor de los diccionarios guardados en el carrito
    def obtener_valor_producto(self, producto, claves, predeterminado=None):
        for clave in claves:
            if clave in producto:
                return producto[clave]

        return predeterminado

    #agrega el medicamento seleccionado a la venta actual
    def agregar_al_carrito(self):
        seleccion = self.tabla_productos.selection()

        if not seleccion:
            messagebox.showwarning(
                "Seleccione un medicamento",
                "Seleccione un medicamento antes de agregarlo."
            )
            return

        try:
            cantidad = int(self.variable_cantidad.get())

            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Cantidad incorrecta",
                "La cantidad debe ser un número entero mayor que cero."
            )
            return

        codigo = int(seleccion[0])

        try:
            self.gestor_ventas.agregar_producto(
                self.venta_actual,
                self.gestor_inventario,
                codigo,
                cantidad
            )
            self.variable_cantidad.set("1")
            self.cargar_carrito()
        except (ValueError, TypeError) as error:
            messagebox.showerror(
                "No se pudo agregar",
                str(error)
            )

    #muestra los productos de la venta y actualiza sus totales
    def cargar_carrito(self):
        for elemento in self.tabla_carrito.get_children():
            self.tabla_carrito.delete(elemento)

        productos = getattr(
            self.venta_actual,
            "productos",
            []
        )

        for producto in productos:
            codigo = self.obtener_valor_producto(
                producto,
                ("CodigoMedicamento", "codigo_medicamento", "codigo"),
                0
            )
            nombre = self.obtener_valor_producto(
                producto,
                ("NombreMedicamento", "nombre_medicamento", "nombre"),
                ""
            )
            cantidad = self.obtener_valor_producto(
                producto,
                ("Cantidad", "cantidad"),
                0
            )
            subtotal = self.obtener_valor_producto(
                producto,
                ("Subtotal", "subtotal"),
                0
            )

            self.tabla_carrito.insert(
                "",
                "end",
                iid=str(codigo),
                values=(
                    codigo,
                    nombre,
                    cantidad,
                    f"${float(subtotal):.2f}"
                )
            )

        unidades = self.obtener_unidades_venta(self.venta_actual)
        total = float(getattr(self.venta_actual, "total", 0))
        codigo_venta = getattr(
            self.venta_actual,
            "codigo_venta",
            "-"
        )

        self.etiqueta_unidades.configure(text=str(unidades))
        self.etiqueta_total.configure(text=f"${total:.2f}")
        self.etiqueta_codigo_venta.configure(
            text=f"Venta {codigo_venta}"
        )

    #elimina el producto marcado dentro del carrito
    def eliminar_del_carrito(self):
        seleccion = self.tabla_carrito.selection()

        if not seleccion:
            messagebox.showwarning(
                "Seleccione un producto",
                "Seleccione un producto del carrito para retirarlo."
            )
            return

        codigo = int(seleccion[0])

        try:
            self.gestor_ventas.eliminar_producto(
                self.venta_actual,
                codigo
            )
            self.cargar_carrito()
        except (ValueError, TypeError) as error:
            messagebox.showerror(
                "No se pudo retirar",
                str(error)
            )

    #crea un carrito nuevo sin modificar el inventario
    def vaciar_carrito(self):
        if self.venta_esta_vacia(self.venta_actual):
            return

        confirmar = messagebox.askyesno(
            "Vaciar carrito",
            "¿Desea retirar todos los productos del carrito?"
        )

        if not confirmar:
            return

        self.venta_actual = self.gestor_ventas.crear_venta(
            self.variable_cliente.get().strip() or "Consumidor final"
        )
        self.cargar_carrito()

    #finaliza la venta y descuenta las unidades del inventario
    def finalizar_venta(self):
        if self.venta_esta_vacia(self.venta_actual):
            messagebox.showwarning(
                "Carrito vacío",
                "Agregue al menos un medicamento antes de finalizar."
            )
            return

        cliente = self.variable_cliente.get().strip()

        if not cliente:
            cliente = "Consumidor final"

        self.venta_actual.cliente = cliente
        total = float(getattr(self.venta_actual, "total", 0))

        confirmar = messagebox.askyesno(
            "Finalizar venta",
            f"¿Desea registrar la venta por ${total:.2f}?"
        )

        if not confirmar:
            return

        try:
            venta_finalizada = self.gestor_ventas.finalizar_venta(
                self.venta_actual,
                self.gestor_inventario
            )

            codigo = getattr(
                venta_finalizada,
                "codigo_venta",
                getattr(self.venta_actual, "codigo_venta", "-")
            )

            messagebox.showinfo(
                "Venta registrada",
                f"La venta {codigo} se guardó correctamente."
            )

            self.variable_cliente.set("Consumidor final")
            self.venta_actual = self.gestor_ventas.crear_venta()
            self.actualizar_vista()
        except (ValueError, TypeError) as error:
            messagebox.showerror(
                "No se pudo finalizar",
                str(error)
            )

    #revisa si la venta no contiene productos
    def venta_esta_vacia(self, venta):
        metodo = getattr(venta, "esta_vacia", None)

        if callable(metodo):
            return metodo()

        return len(getattr(venta, "productos", [])) == 0

    #obtiene la cantidad total de unidades de una venta
    def obtener_unidades_venta(self, venta):
        metodo = getattr(venta, "cantidad_unidades", None)

        if callable(metodo):
            return metodo()

        cantidad = 0

        for producto in getattr(venta, "productos", []):
            cantidad += int(
                self.obtener_valor_producto(
                    producto,
                    ("Cantidad", "cantidad"),
                    0
                )
            )

        return cantidad

    #carga las ventas guardadas dentro del historial
    def cargar_historial(self):
        for elemento in self.tabla_historial.get_children():
            self.tabla_historial.delete(elemento)

        ventas = self.gestor_ventas.obtener_ventas()

        for venta in ventas:
            codigo = getattr(venta, "codigo_venta", "-")
            fecha = getattr(venta, "fecha_venta", "-")
            cliente = getattr(venta, "cliente", "Consumidor final")
            unidades = self.obtener_unidades_venta(venta)
            total = float(getattr(venta, "total", 0))

            self.tabla_historial.insert(
                "",
                "end",
                values=(
                    codigo,
                    str(fecha),
                    cliente,
                    unidades,
                    f"${total:.2f}"
                )
            )

        self.etiqueta_historial.configure(
            text=f"{len(ventas)} ventas"
        )

    #muestra los valores actuales de las ventas guardadas
    def actualizar_resumen(self):
        resumen = self.gestor_ventas.obtener_resumen()
        cantidad = resumen.get("cantidad_ventas", 0)
        ingresos = float(resumen.get("ingresos", 0))
        unidades = resumen.get(
            "unidades",
            resumen.get("unidades_vendidas", 0)
        )
        ventas_hoy = resumen.get("ventas_hoy", 0)
        producto = resumen.get("producto_mas_vendido")

        if isinstance(producto, dict):
            nombre_producto = producto.get(
                "nombre",
                producto.get("NombreMedicamento", "Sin ventas")
            )
        elif producto:
            nombre_producto = str(producto)
        else:
            nombre_producto = "Sin ventas"

        self.etiquetas_resumen["cantidad_ventas"].configure(
            text=str(cantidad)
        )
        self.etiquetas_resumen["ingresos"].configure(
            text=f"${ingresos:.2f}"
        )
        self.etiquetas_resumen["unidades"].configure(
            text=str(unidades)
        )
        self.etiquetas_resumen["ventas_hoy"].configure(
            text=str(ventas_hoy)
        )
        self.etiquetas_resumen["producto"].configure(
            text=nombre_producto
        )

    #actualiza las tablas y los indicadores de la vista
    def actualizar_vista(self):
        self.cargar_productos()
        self.cargar_carrito()
        self.cargar_historial()
        self.actualizar_resumen()