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


class VistaPedidos(ctk.CTkFrame):

    def __init__(
        self,
        master,
        gestor_pedidos,
        gestor_inventario,
        gestor_ventas
    ):
        super().__init__(
            master,
            corner_radius=0,
            fg_color="transparent"
        )

        #conecta la vista con la cola y el inventario
        self.gestor_pedidos = gestor_pedidos
        self.gestor_inventario = gestor_inventario
        self.gestor_ventas = gestor_ventas

        self.variable_busqueda = tk.StringVar()
        self.variable_estado = tk.StringVar(value="Todos")
        self.variable_cliente = tk.StringVar()
        self.variable_cantidad = tk.StringVar(value="1")
        self.variable_historial = tk.StringVar()
        self.variable_estado_historial = tk.StringVar(value="Todos")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.crear_resumen()
        self.crear_pestanas()
        self.actualizar_vista()

    #crea los indicadores generales de los pedidos guardados
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
            ("total", "Pedidos registrados", COLOR_AZUL),
            ("pendientes", "Pendientes", COLOR_ADVERTENCIA),
            ("atendidos", "Atendidos", COLOR_PRIMARIO),
            ("rechazados", "Rechazados", COLOR_PELIGRO),
            ("frente", "Frente de la cola", COLOR_PRIMARIO)
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

    #separa la cola pendiente del historial completo
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

        pestana_cola = self.pestanas.add("Cola de pedidos")
        pestana_historial = self.pestanas.add("Historial de pedidos")

        self.crear_pestana_cola(pestana_cola)
        self.crear_pestana_historial(pestana_historial)

    #crea la zona para registrar y atender solicitudes
    def crear_pestana_cola(self, contenedor):
        contenedor.configure(fg_color=COLOR_FONDO)
        contenedor.grid_rowconfigure(0, weight=1)
        contenedor.grid_columnconfigure(0, weight=3)
        contenedor.grid_columnconfigure(1, weight=2)

        self.crear_nuevo_pedido(contenedor)
        self.crear_cola(contenedor)

    #crea el formulario y la tabla para elegir medicamentos
    def crear_nuevo_pedido(self, contenedor):
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
            pady=(15, 8)
        )
        encabezado.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            encabezado,
            text="Registrar nuevo pedido",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=16,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).grid(row=0, column=0, sticky="w")

        self.etiqueta_codigo = ctk.CTkLabel(
            encabezado,
            text="Pedido 1",
            height=28,
            corner_radius=7,
            fg_color=COLOR_SELECCION,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=9,
                weight="bold"
            ),
            text_color=COLOR_PRIMARIO
        )
        self.etiqueta_codigo.grid(row=0, column=1, sticky="e")

        datos_cliente = ctk.CTkFrame(
            panel,
            corner_radius=0,
            fg_color="transparent"
        )
        datos_cliente.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=18,
            pady=(0, 8)
        )
        datos_cliente.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            datos_cliente,
            text="Cliente",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=9,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).grid(row=0, column=0, sticky="w", padx=(0, 10))

        self.entrada_cliente = ctk.CTkEntry(
            datos_cliente,
            textvariable=self.variable_cliente,
            height=36,
            corner_radius=8,
            border_color=COLOR_BORDE,
            fg_color=COLOR_PANEL,
            text_color=COLOR_TEXTO,
            placeholder_text="Nombre del cliente"
        )
        self.entrada_cliente.grid(row=0, column=1, sticky="ew")

        acciones = ctk.CTkFrame(
            panel,
            corner_radius=0,
            fg_color="transparent"
        )
        acciones.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=18,
            pady=(0, 8)
        )
        acciones.grid_columnconfigure(0, weight=1)

        entrada_busqueda = ctk.CTkEntry(
            acciones,
            textvariable=self.variable_busqueda,
            height=38,
            corner_radius=9,
            border_color=COLOR_BORDE,
            fg_color=COLOR_PANEL,
            text_color=COLOR_TEXTO,
            placeholder_text="Buscar por codigo, nombre o categoria"
        )
        entrada_busqueda.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 8)
        )
        entrada_busqueda.bind(
            "<KeyRelease>",
            lambda evento: self.cargar_medicamentos()
        )

        menu_estado = ctk.CTkOptionMenu(
            acciones,
            variable=self.variable_estado,
            values=[
                "Todos",
                "Disponibles",
                "Stock bajo",
                "Sin stock",
                "Vencidos"
            ],
            width=145,
            height=38,
            corner_radius=9,
            fg_color=COLOR_PANEL,
            button_color=COLOR_PRIMARIO,
            button_hover_color="#176B57",
            text_color=COLOR_TEXTO,
            command=lambda valor: self.cargar_medicamentos()
        )
        menu_estado.grid(row=0, column=1, padx=(0, 8))

        ctk.CTkLabel(
            acciones,
            text="Cantidad",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=8,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).grid(row=0, column=2, padx=(0, 5))

        ctk.CTkEntry(
            acciones,
            textvariable=self.variable_cantidad,
            width=58,
            height=38,
            corner_radius=9,
            justify="center",
            border_color=COLOR_BORDE,
            fg_color=COLOR_PANEL,
            text_color=COLOR_TEXTO
        ).grid(row=0, column=3)

        ctk.CTkButton(
            acciones,
            text="Crear pedido",
            width=112,
            height=38,
            corner_radius=9,
            fg_color=COLOR_PRIMARIO,
            hover_color="#176B57",
            command=self.crear_pedido
        ).grid(row=0, column=4, padx=(8, 0))

        zona_tabla = ctk.CTkFrame(
            panel,
            corner_radius=0,
            fg_color="transparent"
        )
        zona_tabla.grid(
            row=3,
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
            "estado"
        )
        self.tabla_medicamentos = ttk.Treeview(
            zona_tabla,
            columns=columnas,
            show="headings",
            style="PedidosMedicamentos.Treeview",
            selectmode="browse"
        )

        encabezados = {
            "codigo": "Codigo",
            "medicamento": "Medicamento",
            "categoria": "Categoria",
            "stock": "Stock",
            "estado": "Estado"
        }
        anchos = {
            "codigo": 65,
            "medicamento": 200,
            "categoria": 135,
            "stock": 70,
            "estado": 135
        }

        for columna in columnas:
            self.tabla_medicamentos.heading(
                columna,
                text=encabezados[columna]
            )
            self.tabla_medicamentos.column(
                columna,
                width=anchos[columna],
                minwidth=55,
                anchor="center" if columna != "medicamento" else "w"
            )

        self.tabla_medicamentos.tag_configure(
            "normal",
            foreground=COLOR_TEXTO
        )
        self.tabla_medicamentos.tag_configure(
            "advertencia",
            foreground="#C87900"
        )
        self.tabla_medicamentos.tag_configure(
            "peligro",
            foreground=COLOR_PELIGRO
        )
        self.tabla_medicamentos.bind(
            "<Double-1>",
            lambda evento: self.crear_pedido()
        )

        barra_vertical = ttk.Scrollbar(
            zona_tabla,
            orient="vertical",
            command=self.tabla_medicamentos.yview
        )
        barra_horizontal = ttk.Scrollbar(
            zona_tabla,
            orient="horizontal",
            command=self.tabla_medicamentos.xview
        )
        self.tabla_medicamentos.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set
        )

        self.tabla_medicamentos.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        barra_vertical.grid(row=0, column=1, sticky="ns")
        barra_horizontal.grid(row=1, column=0, sticky="ew")

    #crea el panel que representa el orden de la cola fifo
    def crear_cola(self, contenedor):
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
            pady=(15, 8)
        )
        encabezado.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            encabezado,
            text="Cola de atencion FIFO",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=16,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).grid(row=0, column=0, sticky="w")

        self.etiqueta_pendientes = ctk.CTkLabel(
            encabezado,
            text="0 pendientes",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=9
            ),
            text_color=COLOR_TEXTO_SUAVE
        )
        self.etiqueta_pendientes.grid(row=0, column=1, sticky="e")

        ctk.CTkLabel(
            panel,
            text="El primero en entrar es el primero en salir",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=9
            ),
            text_color=COLOR_TEXTO_SUAVE
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=18,
            pady=(0, 8)
        )

        self.tarjeta_frente = ctk.CTkFrame(
            panel,
            height=112,
            corner_radius=10,
            fg_color=COLOR_FILA,
            border_width=1,
            border_color=COLOR_BORDE
        )
        self.tarjeta_frente.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=18,
            pady=(0, 10)
        )
        self.tarjeta_frente.grid_propagate(False)
        self.tarjeta_frente.grid_columnconfigure(1, weight=1)

        insignia = ctk.CTkLabel(
            self.tarjeta_frente,
            text="1",
            width=48,
            height=48,
            corner_radius=24,
            fg_color=COLOR_SELECCION,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=19,
                weight="bold"
            ),
            text_color=COLOR_PRIMARIO
        )
        insignia.grid(
            row=0,
            column=0,
            rowspan=3,
            padx=(15, 12),
            pady=16
        )

        self.etiqueta_frente_titulo = ctk.CTkLabel(
            self.tarjeta_frente,
            text="Cola vacia",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        )
        self.etiqueta_frente_titulo.grid(
            row=0,
            column=1,
            sticky="sw",
            pady=(14, 0)
        )

        self.etiqueta_frente_cliente = ctk.CTkLabel(
            self.tarjeta_frente,
            text="No existen pedidos pendientes",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=9
            ),
            text_color=COLOR_TEXTO_SUAVE
        )
        self.etiqueta_frente_cliente.grid(
            row=1,
            column=1,
            sticky="w"
        )

        self.etiqueta_frente_producto = ctk.CTkLabel(
            self.tarjeta_frente,
            text="",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=9
            ),
            text_color=COLOR_PRIMARIO
        )
        self.etiqueta_frente_producto.grid(
            row=2,
            column=1,
            sticky="nw",
            pady=(0, 13)
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
            padx=18,
            pady=(0, 10)
        )
        zona_tabla.grid_rowconfigure(0, weight=1)
        zona_tabla.grid_columnconfigure(0, weight=1)

        columnas = (
            "posicion",
            "pedido",
            "cliente",
            "medicamento",
            "cantidad"
        )
        self.tabla_cola = ttk.Treeview(
            zona_tabla,
            columns=columnas,
            show="headings",
            style="PedidosCola.Treeview",
            selectmode="browse"
        )

        encabezados = {
            "posicion": "Pos.",
            "pedido": "Pedido",
            "cliente": "Cliente",
            "medicamento": "Medicamento",
            "cantidad": "Cant."
        }
        anchos = {
            "posicion": 50,
            "pedido": 65,
            "cliente": 130,
            "medicamento": 165,
            "cantidad": 55
        }

        for columna in columnas:
            self.tabla_cola.heading(
                columna,
                text=encabezados[columna]
            )
            self.tabla_cola.column(
                columna,
                width=anchos[columna],
                minwidth=45,
                anchor=(
                    "w"
                    if columna in ("cliente", "medicamento")
                    else "center"
                )
            )

        self.tabla_cola.tag_configure(
            "frente",
            background=COLOR_SELECCION,
            foreground=COLOR_TEXTO
        )

        barra_vertical = ttk.Scrollbar(
            zona_tabla,
            orient="vertical",
            command=self.tabla_cola.yview
        )
        barra_horizontal = ttk.Scrollbar(
            zona_tabla,
            orient="horizontal",
            command=self.tabla_cola.xview
        )
        self.tabla_cola.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set
        )

        self.tabla_cola.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        barra_vertical.grid(row=0, column=1, sticky="ns")
        barra_horizontal.grid(row=1, column=0, sticky="ew")

        botones = ctk.CTkFrame(
            panel,
            corner_radius=0,
            fg_color="transparent"
        )
        botones.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=18,
            pady=(0, 18)
        )
        botones.grid_columnconfigure(0, weight=1)
        botones.grid_columnconfigure(1, weight=2)

        ctk.CTkButton(
            botones,
            text="Actualizar",
            height=40,
            corner_radius=9,
            fg_color=COLOR_PANEL,
            hover_color=COLOR_SELECCION,
            border_width=1,
            border_color=COLOR_PRIMARIO,
            text_color=COLOR_PRIMARIO,
            command=self.actualizar_vista
        ).grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.boton_atender = ctk.CTkButton(
            botones,
            text="Atender siguiente",
            height=40,
            corner_radius=9,
            fg_color=COLOR_PRIMARIO,
            hover_color="#176B57",
            command=self.atender_siguiente
        )
        self.boton_atender.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(5, 0)
        )

    #crea la tabla que conserva todos los estados de los pedidos
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
            padx=10,
            pady=(8, 10)
        )
        encabezado.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            encabezado,
            text="Historial completo de pedidos",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=16,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).grid(row=0, column=0, sticky="w")

        entrada = ctk.CTkEntry(
            encabezado,
            textvariable=self.variable_historial,
            width=250,
            height=36,
            corner_radius=8,
            border_color=COLOR_BORDE,
            fg_color=COLOR_PANEL,
            text_color=COLOR_TEXTO,
            placeholder_text="Buscar pedido o cliente"
        )
        entrada.grid(row=0, column=1, padx=(10, 8))
        entrada.bind(
            "<KeyRelease>",
            lambda evento: self.cargar_historial()
        )

        menu = ctk.CTkOptionMenu(
            encabezado,
            variable=self.variable_estado_historial,
            values=[
                "Todos",
                "PENDIENTE",
                "ATENDIDO",
                "RECHAZADO"
            ],
            width=135,
            height=36,
            corner_radius=8,
            fg_color=COLOR_PANEL,
            button_color=COLOR_PRIMARIO,
            button_hover_color="#176B57",
            text_color=COLOR_TEXTO,
            command=lambda valor: self.cargar_historial()
        )
        menu.grid(row=0, column=2, padx=(0, 8))

        self.etiqueta_historial = ctk.CTkLabel(
            encabezado,
            text="0 pedidos",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=9
            ),
            text_color=COLOR_TEXTO_SUAVE
        )
        self.etiqueta_historial.grid(row=0, column=3, padx=(0, 10))

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
        ).grid(row=0, column=4)

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
            sticky="nsew"
        )
        panel.grid_rowconfigure(0, weight=1)
        panel.grid_columnconfigure(0, weight=1)

        columnas = (
            "codigo",
            "fecha",
            "cliente",
            "medicamento",
            "cantidad",
            "estado"
        )
        self.tabla_historial = ttk.Treeview(
            panel,
            columns=columnas,
            show="headings",
            style="PedidosHistorial.Treeview",
            selectmode="browse"
        )

        encabezados = {
            "codigo": "Pedido",
            "fecha": "Fecha de registro",
            "cliente": "Cliente",
            "medicamento": "Medicamento",
            "cantidad": "Cantidad",
            "estado": "Estado"
        }
        anchos = {
            "codigo": 80,
            "fecha": 170,
            "cliente": 230,
            "medicamento": 260,
            "cantidad": 90,
            "estado": 130
        }

        for columna in columnas:
            self.tabla_historial.heading(
                columna,
                text=encabezados[columna]
            )
            self.tabla_historial.column(
                columna,
                width=anchos[columna],
                minwidth=65,
                anchor=(
                    "w"
                    if columna in ("cliente", "medicamento")
                    else "center"
                )
            )

        self.tabla_historial.tag_configure(
            "pendiente",
            foreground="#C87900"
        )
        self.tabla_historial.tag_configure(
            "atendido",
            foreground=COLOR_PRIMARIO
        )
        self.tabla_historial.tag_configure(
            "rechazado",
            foreground=COLOR_PELIGRO
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

    #prepara el estilo claro de las tablas
    def configurar_estilo_tablas(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")

        for nombre in (
            "PedidosMedicamentos.Treeview",
            "PedidosCola.Treeview",
            "PedidosHistorial.Treeview"
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

    #carga los medicamentos que se pueden solicitar
    def cargar_medicamentos(self):
        seleccion_anterior = self.tabla_medicamentos.selection()

        for elemento in self.tabla_medicamentos.get_children():
            self.tabla_medicamentos.delete(elemento)

        texto = self.variable_busqueda.get().strip().lower()
        estado = self.variable_estado.get()

        for medicamento in self.gestor_inventario.obtener_todos():
            if not self.medicamento_coincide(
                medicamento,
                texto,
                estado
            ):
                continue

            if medicamento.esta_vencido() or medicamento.stock == 0:
                etiqueta = "peligro"
            elif medicamento.tiene_stock_bajo():
                etiqueta = "advertencia"
            else:
                etiqueta = "normal"

            self.tabla_medicamentos.insert(
                "",
                "end",
                iid=str(medicamento.codigo),
                values=(
                    medicamento.codigo,
                    medicamento.nombre,
                    medicamento.categoria,
                    medicamento.stock,
                    medicamento.obtener_estado()
                ),
                tags=(etiqueta,)
            )

        if seleccion_anterior:
            codigo = seleccion_anterior[0]

            if self.tabla_medicamentos.exists(codigo):
                self.tabla_medicamentos.selection_set(codigo)

    #valida el formulario y agrega el pedido al final de la cola
    def crear_pedido(self):
        seleccion = self.tabla_medicamentos.selection()

        if not seleccion:
            messagebox.showwarning(
                "Seleccione un medicamento",
                "Seleccione el medicamento solicitado por el cliente."
            )
            return

        cliente = self.variable_cliente.get().strip()

        if not cliente:
            messagebox.showwarning(
                "Cliente obligatorio",
                "Escriba el nombre del cliente antes de crear el pedido."
            )
            self.entrada_cliente.focus_set()
            return

        try:
            cantidad = int(self.variable_cantidad.get())

            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Cantidad incorrecta",
                "La cantidad debe ser un numero entero mayor que cero."
            )
            return

        codigo_medicamento = int(seleccion[0])
        medicamento = self.gestor_inventario.buscar_por_codigo(
            codigo_medicamento
        )

        if medicamento is None:
            messagebox.showerror(
                "Medicamento no encontrado",
                "El medicamento seleccionado ya no existe."
            )
            self.actualizar_vista()
            return

        codigo_pedido = self.gestor_pedidos.obtener_siguiente_codigo()
        datos = {
            "codigo_pedido": codigo_pedido,
            "cliente": cliente,
            "codigo_medicamento": medicamento.codigo,
            "nombre_medicamento": medicamento.nombre,
            "cantidad": cantidad,
            "fecha_registro": None,
            "estado": "PENDIENTE"
        }

        confirmar = messagebox.askyesno(
            "Crear pedido",
            (
                f"¿Desea colocar el pedido {codigo_pedido} "
                "al final de la cola?"
            )
        )

        if not confirmar:
            return

        try:
            pedido = self.gestor_pedidos.crear_pedido(datos)
            posicion = len(self.gestor_pedidos.obtener_pendientes())

            messagebox.showinfo(
                "Pedido registrado",
                (
                    f"El pedido {pedido.codigo_pedido} se guardo "
                    f"en la posicion {posicion} de la cola."
                )
            )

            self.variable_cliente.set("")
            self.variable_cantidad.set("1")
            self.actualizar_vista()
        except (ValueError, TypeError) as error:
            messagebox.showerror(
                "No se pudo crear",
                str(error)
            )

    #carga los pedidos pendientes en el orden de llegada
    def cargar_cola(self):
        for elemento in self.tabla_cola.get_children():
            self.tabla_cola.delete(elemento)

        pendientes = self.gestor_pedidos.obtener_pendientes()

        for posicion, pedido in enumerate(pendientes, start=1):
            etiqueta = "frente" if posicion == 1 else ""
            self.tabla_cola.insert(
                "",
                "end",
                iid=str(pedido.codigo_pedido),
                values=(
                    posicion,
                    pedido.codigo_pedido,
                    pedido.cliente,
                    pedido.nombre_medicamento,
                    pedido.cantidad
                ),
                tags=(etiqueta,) if etiqueta else ()
            )

        self.etiqueta_pendientes.configure(
            text=f"{len(pendientes)} pendientes"
        )

        if pendientes:
            frente = pendientes[0]
            self.etiqueta_frente_titulo.configure(
                text=f"Pedido {frente.codigo_pedido}"
            )
            self.etiqueta_frente_cliente.configure(
                text=frente.cliente
            )
            self.etiqueta_frente_producto.configure(
                text=(
                    f"{frente.nombre_medicamento}  x{frente.cantidad}"
                )
            )
            self.boton_atender.configure(state="normal")
        else:
            self.etiqueta_frente_titulo.configure(text="Cola vacia")
            self.etiqueta_frente_cliente.configure(
                text="No existen pedidos pendientes"
            )
            self.etiqueta_frente_producto.configure(text="")
            self.boton_atender.configure(state="disabled")

    #atiende solamente el pedido ubicado al frente de la cola
    def atender_siguiente(self):
        pendientes = self.gestor_pedidos.obtener_pendientes()

        if not pendientes:
            messagebox.showwarning(
                "Cola vacia",
                "No existen pedidos pendientes para atender."
            )
            return

        frente = pendientes[0]
        confirmar = messagebox.askyesno(
            "Atender siguiente",
            (
                f"¿Desea procesar el pedido {frente.codigo_pedido} "
                f"de {frente.cliente}?"
            )
        )

        if not confirmar:
            return

        try:
            resultado = self.gestor_pedidos.atender_siguiente(
                self.gestor_inventario
            )
            pedido = resultado["pedido"]
            mensaje = resultado["mensaje"]

            if resultado["exito"]:
                venta = (
                    self.gestor_ventas.registrar_pedido_atendido(
                        pedido,
                        self.gestor_inventario
                    )
                )

                messagebox.showinfo(
                    "Pedido atendido",
                    (
                        f"Pedido {pedido.codigo_pedido}\n\n"
                        f"{mensaje}\n\n"
                        f"Venta {venta.codigo_venta} registrada."
                    )
                )
                
            else:
                messagebox.showwarning(
                    "Pedido rechazado",
                    (
                        f"Pedido {pedido.codigo_pedido}\n\n"
                        f"{mensaje}"
                    )
                )

            self.actualizar_vista()
        except (ValueError, TypeError, KeyError) as error:
            messagebox.showerror(
                "No se pudo atender",
                str(error)
            )

    #revisa si un pedido coincide con la busqueda del historial
    def pedido_coincide_historial(self, pedido, texto, estado):
        contenido = (
            f"{pedido.codigo_pedido} "
            f"{pedido.cliente} "
            f"{pedido.codigo_medicamento} "
            f"{pedido.nombre_medicamento} "
            f"{pedido.estado}"
        ).lower()

        if texto and texto not in contenido:
            return False

        if estado != "Todos" and pedido.estado != estado:
            return False

        return True

    #carga todos los pedidos y conserva su estado final
    def cargar_historial(self):
        for elemento in self.tabla_historial.get_children():
            self.tabla_historial.delete(elemento)

        texto = self.variable_historial.get().strip().lower()
        estado = self.variable_estado_historial.get()
        cantidad = 0

        for pedido in self.gestor_pedidos.obtener_historial():
            if not self.pedido_coincide_historial(
                pedido,
                texto,
                estado
            ):
                continue

            fecha = pedido.fecha_registro.strftime(
                pedido.FORMATO_FECHA
            )
            etiqueta = pedido.estado.lower()

            self.tabla_historial.insert(
                "",
                "end",
                values=(
                    pedido.codigo_pedido,
                    fecha,
                    pedido.cliente,
                    pedido.nombre_medicamento,
                    pedido.cantidad,
                    pedido.estado
                ),
                tags=(etiqueta,)
            )
            cantidad += 1

        self.etiqueta_historial.configure(
            text=f"{cantidad} pedidos"
        )

    #muestra los valores actuales y el pedido del frente
    def actualizar_resumen(self):
        resumen = self.gestor_pedidos.obtener_resumen()
        pendientes = self.gestor_pedidos.obtener_pendientes()

        self.etiquetas_resumen["total"].configure(
            text=str(resumen.get("total", 0))
        )
        self.etiquetas_resumen["pendientes"].configure(
            text=str(resumen.get("pendientes", 0))
        )
        self.etiquetas_resumen["atendidos"].configure(
            text=str(resumen.get("atendidos", 0))
        )
        self.etiquetas_resumen["rechazados"].configure(
            text=str(resumen.get("rechazados", 0))
        )

        if pendientes:
            texto_frente = f"Pedido {pendientes[0].codigo_pedido}"
        else:
            texto_frente = "Cola vacia"

        self.etiquetas_resumen["frente"].configure(
            text=texto_frente
        )
        self.etiqueta_codigo.configure(
            text=(
                "Pedido "
                f"{self.gestor_pedidos.obtener_siguiente_codigo()}"
            )
        )

    #actualiza las tablas y los indicadores de la vista
    def actualizar_vista(self):
        self.cargar_medicamentos()
        self.cargar_cola()
        self.cargar_historial()
        self.actualizar_resumen()