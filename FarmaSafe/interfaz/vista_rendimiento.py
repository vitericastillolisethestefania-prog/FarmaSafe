import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

import customtkinter as ctk

from algoritmos.busquedas import comparar_busquedas
from algoritmos.ordenamientos import (
    comparar_ordenamientos,
    ordenamiento_quick_sort
)


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
COLOR_MORADO = "#8B5CF6"
COLOR_GRIS = "#94A3B8"


class VistaRendimiento(ctk.CTkFrame):

    CAMPOS = {
        "Código": ("codigo", "entero"),
        "Nombre": ("nombre", "texto"),
        "Categoría": ("categoria", "texto"),
        "Stock": ("stock", "entero"),
        "Precio": ("precio", "decimal"),
        "Vencimiento": ("fecha_vencimiento", "fecha")
    }

    def __init__(self, master, gestor_inventario):
        super().__init__(
            master,
            corner_radius=0,
            fg_color="transparent"
        )

        #conecta las pruebas con los medicamentos del arbol avl
        self.gestor_inventario = gestor_inventario
        self.resultado_ordenamientos = None
        self.resultado_busquedas = None

        self.variable_campo_orden = tk.StringVar(value="Código")
        self.variable_direccion = tk.StringVar(value="Ascendente")
        self.variable_campo_busqueda = tk.StringVar(value="Código")
        self.variable_valor_busqueda = tk.StringVar()

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.crear_resumen()
        self.crear_pestanas()
        self.mostrar_ordenamientos()

    #crea los indicadores generales de la ultima prueba
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
            ("registros", "Registros analizados", COLOR_AZUL),
            ("prueba", "Prueba actual", COLOR_PRIMARIO),
            ("ganador", "Algoritmo más eficiente", COLOR_PRIMARIO),
            ("mejora", "Mejora observada", COLOR_MORADO),
            ("coincidencia", "Resultados correctos", COLOR_ADVERTENCIA)
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
                text="-",
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=17,
                    weight="bold"
                ),
                text_color=color
            )
            etiqueta.pack(anchor="w")
            self.etiquetas_resumen[clave] = etiqueta

        self.actualizar_resumen_inicial()

    #muestra la cantidad disponible antes de ejecutar una prueba
    def actualizar_resumen_inicial(self):
        cantidad = len(self.gestor_inventario.obtener_todos())
        self.etiquetas_resumen["registros"].configure(text=str(cantidad))
        self.etiquetas_resumen["prueba"].configure(text="Sin ejecutar")
        self.etiquetas_resumen["ganador"].configure(text="-")
        self.etiquetas_resumen["mejora"].configure(text="-")
        self.etiquetas_resumen["coincidencia"].configure(text="-")

    #crea los botones para cambiar entre las dos comparaciones
    def crear_pestanas(self):
        self.barra_pestanas = ctk.CTkFrame(
            self,
            height=38,
            corner_radius=10,
            fg_color=COLOR_PANEL
        )
        self.barra_pestanas.grid(
            row=1,
            column=0,
            sticky="n",
            pady=(0, 10)
        )

        self.boton_ordenamientos = ctk.CTkButton(
            self.barra_pestanas,
            width=150,
            height=30,
            corner_radius=9,
            text="Ordenamientos",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12
            ),
            command=self.mostrar_ordenamientos
        )
        self.boton_ordenamientos.pack(
            side="left",
            padx=(4, 0),
            pady=4
        )

        self.boton_busquedas = ctk.CTkButton(
            self.barra_pestanas,
            width=150,
            height=30,
            corner_radius=9,
            text="Búsquedas",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12
            ),
            command=self.mostrar_busquedas
        )
        self.boton_busquedas.pack(
            side="left",
            padx=(0, 4),
            pady=4
        )

        self.contenedor_vistas = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="transparent"
        )
        self.contenedor_vistas.grid(
            row=2,
            column=0,
            sticky="nsew"
        )
        self.grid_rowconfigure(2, weight=1)
        self.contenedor_vistas.grid_rowconfigure(0, weight=1)
        self.contenedor_vistas.grid_columnconfigure(0, weight=1)

    #elimina la seccion anterior antes de dibujar otra
    def limpiar_contenedor(self):
        for componente in self.contenedor_vistas.winfo_children():
            componente.destroy()

    #activa visualmente la pestana seleccionada
    def seleccionar_pestana(self, nombre):
        if nombre == "ordenamientos":
            self.boton_ordenamientos.configure(
                fg_color=COLOR_PRIMARIO,
                hover_color=COLOR_PRIMARIO,
                text_color="#FFFFFF"
            )
            self.boton_busquedas.configure(
                fg_color="transparent",
                hover_color=COLOR_SELECCION,
                text_color=COLOR_TEXTO
            )
        else:
            self.boton_busquedas.configure(
                fg_color=COLOR_PRIMARIO,
                hover_color=COLOR_PRIMARIO,
                text_color="#FFFFFF"
            )
            self.boton_ordenamientos.configure(
                fg_color="transparent",
                hover_color=COLOR_SELECCION,
                text_color=COLOR_TEXTO
            )

    #construye la seccion para bubblesort y quicksort
    def mostrar_ordenamientos(self):
        self.limpiar_contenedor()
        self.seleccionar_pestana("ordenamientos")

        vista = ctk.CTkFrame(
            self.contenedor_vistas,
            corner_radius=0,
            fg_color="transparent"
        )
        vista.grid(row=0, column=0, sticky="nsew")
        vista.grid_rowconfigure(1, weight=1)
        vista.grid_columnconfigure(0, weight=1)

        controles = ctk.CTkFrame(
            vista,
            height=64,
            corner_radius=12,
            fg_color=COLOR_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )
        controles.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 12)
        )
        controles.grid_propagate(False)
        controles.grid_columnconfigure(0, weight=1)

        textos = ctk.CTkFrame(
            controles,
            corner_radius=0,
            fg_color="transparent"
        )
        textos.grid(
            row=0,
            column=0,
            sticky="w",
            padx=18,
            pady=10
        )

        ctk.CTkLabel(
            textos,
            text="Comparación de ordenamientos",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=15,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).pack(anchor="w")

        ctk.CTkLabel(
            textos,
            text="BubbleSort y QuickSort reciben una copia de los mismos datos",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10
            ),
            text_color=COLOR_TEXTO_SUAVE
        ).pack(anchor="w")

        self.selector_campo_orden = ctk.CTkOptionMenu(
            controles,
            width=150,
            height=38,
            values=list(self.CAMPOS.keys()),
            variable=self.variable_campo_orden,
            fg_color=COLOR_PANEL,
            button_color=COLOR_PRIMARIO,
            button_hover_color=COLOR_SECUNDARIO,
            text_color=COLOR_TEXTO,
            dropdown_fg_color=COLOR_PANEL,
            dropdown_text_color=COLOR_TEXTO,
            font=ctk.CTkFont(family="Segoe UI", size=11)
        )
        self.selector_campo_orden.grid(
            row=0,
            column=1,
            padx=(8, 6),
            pady=12
        )

        self.selector_direccion = ctk.CTkOptionMenu(
            controles,
            width=140,
            height=38,
            values=["Ascendente", "Descendente"],
            variable=self.variable_direccion,
            fg_color=COLOR_PANEL,
            button_color=COLOR_PRIMARIO,
            button_hover_color=COLOR_SECUNDARIO,
            text_color=COLOR_TEXTO,
            dropdown_fg_color=COLOR_PANEL,
            dropdown_text_color=COLOR_TEXTO,
            font=ctk.CTkFont(family="Segoe UI", size=11)
        )
        self.selector_direccion.grid(
            row=0,
            column=2,
            padx=6,
            pady=12
        )

        ctk.CTkButton(
            controles,
            width=178,
            height=38,
            corner_radius=9,
            text="Ejecutar comparación",
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_SECUNDARIO,
            text_color="#FFFFFF",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=11,
                weight="bold"
            ),
            command=self.ejecutar_ordenamientos
        ).grid(
            row=0,
            column=3,
            padx=(6, 16),
            pady=12
        )

        cuerpo = ctk.CTkFrame(
            vista,
            corner_radius=0,
            fg_color="transparent"
        )
        cuerpo.grid(row=1, column=0, sticky="nsew")
        cuerpo.grid_columnconfigure(0, weight=5)
        cuerpo.grid_columnconfigure(1, weight=4)
        cuerpo.grid_rowconfigure(0, weight=1)

        izquierda = ctk.CTkFrame(
            cuerpo,
            corner_radius=12,
            fg_color=COLOR_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )
        izquierda.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 6)
        )
        izquierda.grid_columnconfigure(0, weight=1)
        izquierda.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            izquierda,
            text="Resultados de la comparación",
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
            padx=18,
            pady=(16, 10)
        )

        tarjetas = ctk.CTkFrame(
            izquierda,
            corner_radius=0,
            fg_color="transparent"
        )
        tarjetas.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=14,
            pady=(0, 10)
        )
        tarjetas.grid_columnconfigure(0, weight=1)
        tarjetas.grid_columnconfigure(1, weight=1)

        self.etiquetas_orden = {}
        self.crear_tarjeta_algoritmo(
            tarjetas,
            0,
            "burbuja",
            "BubbleSort",
            COLOR_ADVERTENCIA
        )
        self.crear_tarjeta_algoritmo(
            tarjetas,
            1,
            "quick_sort",
            "QuickSort",
            COLOR_AZUL
        )

        grafico_marco = ctk.CTkFrame(
            izquierda,
            corner_radius=10,
            fg_color=COLOR_FILA
        )
        grafico_marco.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=14,
            pady=(0, 14)
        )
        grafico_marco.grid_rowconfigure(1, weight=1)
        grafico_marco.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            grafico_marco,
            text="Comparación visual",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=14,
            pady=(12, 2)
        )

        self.grafico_orden = tk.Canvas(
            grafico_marco,
            bg=COLOR_FILA,
            highlightthickness=0,
            height=245
        )
        self.grafico_orden.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=8,
            pady=(0, 8)
        )

        derecha = ctk.CTkFrame(
            cuerpo,
            corner_radius=12,
            fg_color=COLOR_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )
        derecha.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(6, 0)
        )
        derecha.grid_columnconfigure(0, weight=1)
        derecha.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            derecha,
            text="Vista previa del resultado",
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
            padx=18,
            pady=(16, 2)
        )

        self.etiqueta_detalle_orden = ctk.CTkLabel(
            derecha,
            text="Ejecute la comparación para observar la lista ordenada",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=COLOR_TEXTO_SUAVE
        )
        self.etiqueta_detalle_orden.grid(
            row=1,
            column=0,
            sticky="w",
            padx=18,
            pady=(0, 10)
        )

        marco_tabla = ctk.CTkFrame(
            derecha,
            corner_radius=8,
            fg_color=COLOR_PANEL
        )
        marco_tabla.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=14,
            pady=(0, 14)
        )
        marco_tabla.grid_rowconfigure(0, weight=1)
        marco_tabla.grid_columnconfigure(0, weight=1)

        columnas = (
            "posicion",
            "codigo",
            "medicamento",
            "categoria",
            "stock",
            "precio"
        )
        self.tabla_orden = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            style="Rendimiento.Treeview"
        )

        encabezados = {
            "posicion": "Pos.",
            "codigo": "Código",
            "medicamento": "Medicamento",
            "categoria": "Categoría",
            "stock": "Stock",
            "precio": "Precio"
        }
        anchos = {
            "posicion": 45,
            "codigo": 65,
            "medicamento": 165,
            "categoria": 120,
            "stock": 65,
            "precio": 70
        }

        for columna in columnas:
            self.tabla_orden.heading(
                columna,
                text=encabezados[columna]
            )
            self.tabla_orden.column(
                columna,
                width=anchos[columna],
                minwidth=anchos[columna],
                anchor="center" if columna != "medicamento" else "w"
            )

        barra_vertical = ttk.Scrollbar(
            marco_tabla,
            orient="vertical",
            command=self.tabla_orden.yview
        )
        barra_horizontal = ttk.Scrollbar(
            marco_tabla,
            orient="horizontal",
            command=self.tabla_orden.xview
        )
        self.tabla_orden.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set
        )
        self.tabla_orden.grid(row=0, column=0, sticky="nsew")
        barra_vertical.grid(row=0, column=1, sticky="ns")
        barra_horizontal.grid(row=1, column=0, sticky="ew")

        self.configurar_estilo_tablas()
        self.dibujar_grafico_vacio(
            self.grafico_orden,
            "Ejecute una comparación para generar el gráfico"
        )

    #crea una tarjeta con las metricas de un algoritmo
    def crear_tarjeta_algoritmo(
        self,
        master,
        columna,
        clave,
        titulo,
        color
    ):
        tarjeta = ctk.CTkFrame(
            master,
            corner_radius=10,
            fg_color=COLOR_FILA,
            border_width=1,
            border_color=COLOR_BORDE
        )
        tarjeta.grid(
            row=0,
            column=columna,
            sticky="nsew",
            padx=(0, 5) if columna == 0 else (5, 0)
        )

        titulo_marco = ctk.CTkFrame(
            tarjeta,
            corner_radius=0,
            fg_color="transparent"
        )
        titulo_marco.pack(fill="x", padx=12, pady=(10, 4))

        ctk.CTkLabel(
            titulo_marco,
            text="●",
            font=ctk.CTkFont(size=13),
            text_color=color
        ).pack(side="left")

        ctk.CTkLabel(
            titulo_marco,
            text=titulo,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).pack(side="left", padx=(6, 0))

        valores = {}

        for nombre, texto in (
            ("tiempo", "Tiempo"),
            ("comparaciones", "Comparaciones"),
            ("intercambios", "Intercambios")
        ):
            fila = ctk.CTkFrame(
                tarjeta,
                corner_radius=0,
                fg_color="transparent"
            )
            fila.pack(fill="x", padx=12, pady=2)

            ctk.CTkLabel(
                fila,
                text=texto,
                font=ctk.CTkFont(family="Segoe UI", size=9),
                text_color=COLOR_TEXTO_SUAVE
            ).pack(side="left")

            valor = ctk.CTkLabel(
                fila,
                text="-",
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=10,
                    weight="bold"
                ),
                text_color=color
            )
            valor.pack(side="right")
            valores[nombre] = valor

        ctk.CTkLabel(
            tarjeta,
            text="",
            height=4
        ).pack()
        self.etiquetas_orden[clave] = valores

    #ejecuta los dos ordenamientos usando la misma lista original
    def ejecutar_ordenamientos(self):
        datos = self.gestor_inventario.obtener_todos()

        if not datos:
            messagebox.showwarning(
                "Sin datos",
                "No existen medicamentos para realizar la comparación."
            )
            return

        campo = self.variable_campo_orden.get()
        atributo = self.CAMPOS[campo][0]
        ascendente = self.variable_direccion.get() == "Ascendente"

        try:
            resultados = comparar_ordenamientos(
                datos,
                atributo,
                ascendente
            )
        except (ValueError, TypeError, RecursionError) as error:
            messagebox.showerror(
                "No se pudo ordenar",
                str(error)
            )
            return

        self.resultado_ordenamientos = resultados
        burbuja = resultados["burbuja"]
        quick = resultados["quick_sort"]

        for clave, resultado in (
            ("burbuja", burbuja),
            ("quick_sort", quick)
        ):
            etiquetas = self.etiquetas_orden[clave]
            etiquetas["tiempo"].configure(
                text=self.formatear_tiempo(resultado["tiempo_ms"])
            )
            etiquetas["comparaciones"].configure(
                text=f"{resultado['comparaciones']:,}"
            )
            etiquetas["intercambios"].configure(
                text=f"{resultado['intercambios']:,}"
            )

        valores_burbuja = [
            getattr(elemento, atributo)
            for elemento in burbuja["lista"]
        ]
        valores_quick = [
            getattr(elemento, atributo)
            for elemento in quick["lista"]
        ]
        coinciden = valores_burbuja == valores_quick

        ganador = self.obtener_ganador(
            burbuja["tiempo_ms"],
            quick["tiempo_ms"],
            "BubbleSort",
            "QuickSort"
        )
        mejora = self.calcular_mejora(
            burbuja["tiempo_ms"],
            quick["tiempo_ms"]
        )

        self.etiquetas_resumen["registros"].configure(
            text=str(len(datos))
        )
        self.etiquetas_resumen["prueba"].configure(
            text=f"Ordenar por {campo.lower()}"
        )
        self.etiquetas_resumen["ganador"].configure(text=ganador)
        self.etiquetas_resumen["mejora"].configure(text=mejora)
        self.etiquetas_resumen["coincidencia"].configure(
            text="Sí" if coinciden else "No",
            text_color=COLOR_PRIMARIO if coinciden else COLOR_PELIGRO
        )

        self.etiqueta_detalle_orden.configure(
            text=(
                f"{len(datos)} registros por {campo.lower()} · "
                f"{self.variable_direccion.get()} · resultados iguales: "
                f"{'sí' if coinciden else 'no'}"
            )
        )

        self.cargar_tabla_orden(quick["lista"])
        self.dibujar_grafico_ordenamientos(burbuja, quick)

    #carga la lista ordenada sin modificar el arbol avl
    def cargar_tabla_orden(self, datos):
        for item in self.tabla_orden.get_children():
            self.tabla_orden.delete(item)

        for posicion, medicamento in enumerate(datos, start=1):
            self.tabla_orden.insert(
                "",
                "end",
                values=(
                    posicion,
                    medicamento.codigo,
                    medicamento.nombre,
                    medicamento.categoria,
                    medicamento.stock,
                    f"${medicamento.precio:.2f}"
                )
            )

    #dibuja barras normalizadas para las tres metricas
    def dibujar_grafico_ordenamientos(self, burbuja, quick):
        canvas = self.grafico_orden
        canvas.delete("all")
        canvas.update_idletasks()

        ancho = max(canvas.winfo_width(), 520)
        margen_x = 145
        ancho_util = max(ancho - margen_x - 28, 100)

        metricas = [
            (
                "Tiempo (ms)",
                burbuja["tiempo_ms"],
                quick["tiempo_ms"]
            ),
            (
                "Comparaciones",
                burbuja["comparaciones"],
                quick["comparaciones"]
            ),
            (
                "Intercambios",
                burbuja["intercambios"],
                quick["intercambios"]
            )
        ]

        for indice, (titulo, valor_burbuja, valor_quick) in enumerate(metricas):
            base_y = 28 + indice * 72
            maximo = max(valor_burbuja, valor_quick, 0.0000001)
            ancho_burbuja = (valor_burbuja / maximo) * ancho_util
            ancho_quick = (valor_quick / maximo) * ancho_util

            canvas.create_text(
                12,
                base_y,
                text=titulo,
                anchor="w",
                fill=COLOR_TEXTO,
                font=("Segoe UI", 9, "bold")
            )
            canvas.create_text(
                margen_x - 8,
                base_y + 20,
                text="BubbleSort",
                anchor="e",
                fill=COLOR_TEXTO_SUAVE,
                font=("Segoe UI", 8)
            )
            canvas.create_rectangle(
                margen_x,
                base_y + 13,
                margen_x + max(ancho_burbuja, 2),
                base_y + 25,
                fill=COLOR_ADVERTENCIA,
                outline=""
            )
            canvas.create_text(
                margen_x - 8,
                base_y + 40,
                text="QuickSort",
                anchor="e",
                fill=COLOR_TEXTO_SUAVE,
                font=("Segoe UI", 8)
            )
            canvas.create_rectangle(
                margen_x,
                base_y + 33,
                margen_x + max(ancho_quick, 2),
                base_y + 45,
                fill=COLOR_AZUL,
                outline=""
            )

    #construye la seccion para busqueda lineal y binaria
    def mostrar_busquedas(self):
        self.limpiar_contenedor()
        self.seleccionar_pestana("busquedas")

        vista = ctk.CTkFrame(
            self.contenedor_vistas,
            corner_radius=0,
            fg_color="transparent"
        )
        vista.grid(row=0, column=0, sticky="nsew")
        vista.grid_rowconfigure(1, weight=1)
        vista.grid_columnconfigure(0, weight=1)

        controles = ctk.CTkFrame(
            vista,
            height=64,
            corner_radius=12,
            fg_color=COLOR_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )
        controles.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 12)
        )
        controles.grid_propagate(False)
        controles.grid_columnconfigure(0, weight=1)

        textos = ctk.CTkFrame(
            controles,
            corner_radius=0,
            fg_color="transparent"
        )
        textos.grid(
            row=0,
            column=0,
            sticky="w",
            padx=18,
            pady=10
        )

        ctk.CTkLabel(
            textos,
            text="Comparación de búsquedas",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=15,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).pack(anchor="w")

        ctk.CTkLabel(
            textos,
            text="La búsqueda binaria utiliza una copia ordenada previamente",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=COLOR_TEXTO_SUAVE
        ).pack(anchor="w")

        self.selector_campo_busqueda = ctk.CTkOptionMenu(
            controles,
            width=145,
            height=38,
            values=list(self.CAMPOS.keys()),
            variable=self.variable_campo_busqueda,
            fg_color=COLOR_PANEL,
            button_color=COLOR_PRIMARIO,
            button_hover_color=COLOR_SECUNDARIO,
            text_color=COLOR_TEXTO,
            dropdown_fg_color=COLOR_PANEL,
            dropdown_text_color=COLOR_TEXTO,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            command=self.actualizar_ayuda_busqueda
        )
        self.selector_campo_busqueda.grid(
            row=0,
            column=1,
            padx=(8, 6),
            pady=12
        )

        self.entrada_busqueda = ctk.CTkEntry(
            controles,
            width=230,
            height=38,
            corner_radius=9,
            placeholder_text="Código del medicamento",
            textvariable=self.variable_valor_busqueda,
            fg_color=COLOR_PANEL,
            border_color=COLOR_BORDE,
            text_color=COLOR_TEXTO,
            font=ctk.CTkFont(family="Segoe UI", size=11)
        )
        self.entrada_busqueda.grid(
            row=0,
            column=2,
            padx=6,
            pady=12
        )
        self.entrada_busqueda.bind(
            "<Return>",
            lambda evento: self.ejecutar_busquedas()
        )

        ctk.CTkButton(
            controles,
            width=178,
            height=38,
            corner_radius=9,
            text="Ejecutar comparación",
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_SECUNDARIO,
            text_color="#FFFFFF",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=11,
                weight="bold"
            ),
            command=self.ejecutar_busquedas
        ).grid(
            row=0,
            column=3,
            padx=(6, 16),
            pady=12
        )

        cuerpo = ctk.CTkFrame(
            vista,
            corner_radius=0,
            fg_color="transparent"
        )
        cuerpo.grid(row=1, column=0, sticky="nsew")
        cuerpo.grid_columnconfigure(0, weight=5)
        cuerpo.grid_columnconfigure(1, weight=4)
        cuerpo.grid_rowconfigure(0, weight=1)

        izquierda = ctk.CTkFrame(
            cuerpo,
            corner_radius=12,
            fg_color=COLOR_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )
        izquierda.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 6)
        )
        izquierda.grid_columnconfigure(0, weight=1)
        izquierda.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            izquierda,
            text="Eficiencia de las búsquedas",
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
            padx=18,
            pady=(16, 10)
        )

        tarjetas = ctk.CTkFrame(
            izquierda,
            corner_radius=0,
            fg_color="transparent"
        )
        tarjetas.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=14,
            pady=(0, 10)
        )
        tarjetas.grid_columnconfigure(0, weight=1)
        tarjetas.grid_columnconfigure(1, weight=1)

        self.etiquetas_busqueda = {}
        self.crear_tarjeta_busqueda(
            tarjetas,
            0,
            "lineal",
            "Búsqueda lineal",
            COLOR_ADVERTENCIA
        )
        self.crear_tarjeta_busqueda(
            tarjetas,
            1,
            "binaria",
            "Búsqueda binaria",
            COLOR_PRIMARIO
        )

        grafico_marco = ctk.CTkFrame(
            izquierda,
            corner_radius=10,
            fg_color=COLOR_FILA
        )
        grafico_marco.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=14,
            pady=(0, 14)
        )
        grafico_marco.grid_rowconfigure(1, weight=1)
        grafico_marco.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            grafico_marco,
            text="Comparaciones realizadas",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=14,
            pady=(12, 2)
        )

        self.grafico_busqueda = tk.Canvas(
            grafico_marco,
            bg=COLOR_FILA,
            highlightthickness=0,
            height=245
        )
        self.grafico_busqueda.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=8,
            pady=(0, 8)
        )

        derecha = ctk.CTkFrame(
            cuerpo,
            corner_radius=12,
            fg_color=COLOR_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )
        derecha.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(6, 0)
        )
        derecha.grid_columnconfigure(0, weight=1)
        derecha.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            derecha,
            text="Resultado localizado",
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
            padx=18,
            pady=(16, 2)
        )

        self.etiqueta_preparacion = ctk.CTkLabel(
            derecha,
            text="La preparación de la lista binaria se mostrará por separado",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=COLOR_TEXTO_SUAVE
        )
        self.etiqueta_preparacion.grid(
            row=1,
            column=0,
            sticky="w",
            padx=18,
            pady=(0, 10)
        )

        self.panel_resultado_busqueda = ctk.CTkFrame(
            derecha,
            corner_radius=10,
            fg_color=COLOR_FILA
        )
        self.panel_resultado_busqueda.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=14,
            pady=(0, 14)
        )
        self.panel_resultado_busqueda.grid_columnconfigure(0, weight=1)

        self.etiqueta_estado_busqueda = ctk.CTkLabel(
            self.panel_resultado_busqueda,
            text="Sin búsqueda",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12,
                weight="bold"
            ),
            text_color=COLOR_TEXTO_SUAVE
        )
        self.etiqueta_estado_busqueda.pack(
            anchor="w",
            padx=18,
            pady=(18, 8)
        )

        self.etiqueta_nombre_resultado = ctk.CTkLabel(
            self.panel_resultado_busqueda,
            text="Ingrese un valor para comparar los métodos",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=20,
                weight="bold"
            ),
            text_color=COLOR_TEXTO,
            wraplength=390,
            justify="left"
        )
        self.etiqueta_nombre_resultado.pack(
            anchor="w",
            padx=18,
            pady=(0, 12)
        )

        self.etiqueta_datos_resultado = ctk.CTkLabel(
            self.panel_resultado_busqueda,
            text=(
                "La búsqueda lineal recorrerá la lista original y la "
                "binaria descartará la mitad en cada paso."
            ),
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=COLOR_TEXTO_SUAVE,
            justify="left",
            wraplength=390
        )
        self.etiqueta_datos_resultado.pack(
            anchor="w",
            padx=18,
            pady=(0, 18)
        )

        self.dibujar_grafico_vacio(
            self.grafico_busqueda,
            "Ejecute una búsqueda para comparar los recorridos"
        )
        self.entrada_busqueda.focus_set()

    #crea una tarjeta para mostrar tiempo y comparaciones
    def crear_tarjeta_busqueda(
        self,
        master,
        columna,
        clave,
        titulo,
        color
    ):
        tarjeta = ctk.CTkFrame(
            master,
            corner_radius=10,
            fg_color=COLOR_FILA,
            border_width=1,
            border_color=COLOR_BORDE
        )
        tarjeta.grid(
            row=0,
            column=columna,
            sticky="nsew",
            padx=(0, 5) if columna == 0 else (5, 0)
        )

        ctk.CTkLabel(
            tarjeta,
            text=titulo,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="bold"
            ),
            text_color=color
        ).pack(anchor="w", padx=12, pady=(10, 4))

        valores = {}

        for nombre, texto in (
            ("tiempo", "Tiempo"),
            ("comparaciones", "Comparaciones"),
            ("posicion", "Posición")
        ):
            fila = ctk.CTkFrame(
                tarjeta,
                corner_radius=0,
                fg_color="transparent"
            )
            fila.pack(fill="x", padx=12, pady=2)

            ctk.CTkLabel(
                fila,
                text=texto,
                font=ctk.CTkFont(family="Segoe UI", size=9),
                text_color=COLOR_TEXTO_SUAVE
            ).pack(side="left")

            valor = ctk.CTkLabel(
                fila,
                text="-",
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=10,
                    weight="bold"
                ),
                text_color=color
            )
            valor.pack(side="right")
            valores[nombre] = valor

        ctk.CTkLabel(tarjeta, text="", height=4).pack()
        self.etiquetas_busqueda[clave] = valores

    #cambia el ejemplo segun el tipo del campo seleccionado
    def actualizar_ayuda_busqueda(self, campo=None):
        campo = campo or self.variable_campo_busqueda.get()
        ejemplos = {
            "Código": "Ejemplo: 15",
            "Nombre": "Ejemplo: Complejo B",
            "Categoría": "Ejemplo: Analgésico",
            "Stock": "Ejemplo: 40",
            "Precio": "Ejemplo: 4.50",
            "Vencimiento": "Formato: AAAA-MM-DD"
        }
        self.entrada_busqueda.configure(
            placeholder_text=ejemplos.get(campo, "Valor buscado")
        )

    #convierte el valor escrito al tipo usado por el modelo
    def convertir_valor_busqueda(self, texto, tipo):
        texto = texto.strip()

        if not texto:
            raise ValueError("Escriba el valor que desea buscar.")

        if tipo == "entero":
            return int(texto)

        if tipo == "decimal":
            return float(texto.replace(",", "."))

        if tipo == "fecha":
            try:
                return datetime.strptime(texto, "%Y-%m-%d").date()
            except ValueError as error:
                raise ValueError(
                    "La fecha debe tener el formato AAAA-MM-DD."
                ) from error

        return texto

    #ejecuta las dos busquedas y separa el costo de ordenar
    def ejecutar_busquedas(self):
        datos = self.gestor_inventario.obtener_todos()

        if not datos:
            messagebox.showwarning(
                "Sin datos",
                "No existen medicamentos para realizar la comparación."
            )
            return

        campo = self.variable_campo_busqueda.get()
        atributo, tipo = self.CAMPOS[campo]

        try:
            valor = self.convertir_valor_busqueda(
                self.variable_valor_busqueda.get(),
                tipo
            )
            preparacion = ordenamiento_quick_sort(
                datos,
                atributo,
                True
            )
            resultados = comparar_busquedas(
                datos,
                preparacion["lista"],
                valor,
                atributo
            )
        except (ValueError, TypeError) as error:
            messagebox.showerror(
                "Valor no válido",
                str(error)
            )
            return

        self.resultado_busquedas = resultados
        lineal = resultados["lineal"]
        binaria = resultados["binaria"]

        for clave, resultado in (
            ("lineal", lineal),
            ("binaria", binaria)
        ):
            etiquetas = self.etiquetas_busqueda[clave]
            etiquetas["tiempo"].configure(
                text=self.formatear_tiempo(resultado["tiempo_ms"])
            )
            etiquetas["comparaciones"].configure(
                text=f"{resultado['comparaciones']:,}"
            )
            posicion = resultado["posicion"]
            etiquetas["posicion"].configure(
                text=str(posicion + 1) if posicion >= 0 else "No encontrado"
            )

        encontrado_lineal = lineal["resultado"] is not None
        encontrado_binario = binaria["resultado"] is not None
        coinciden = encontrado_lineal == encontrado_binario

        if encontrado_lineal and encontrado_binario:
            valor_lineal = getattr(lineal["resultado"], atributo)
            valor_binario = getattr(binaria["resultado"], atributo)
            coinciden = valor_lineal == valor_binario

        ganador = self.obtener_ganador(
            lineal["tiempo_ms"],
            binaria["tiempo_ms"],
            "Lineal",
            "Binaria"
        )
        mejora = self.calcular_mejora(
            lineal["tiempo_ms"],
            binaria["tiempo_ms"]
        )

        self.etiquetas_resumen["registros"].configure(
            text=str(len(datos))
        )
        self.etiquetas_resumen["prueba"].configure(
            text=f"Buscar por {campo.lower()}"
        )
        self.etiquetas_resumen["ganador"].configure(text=ganador)
        self.etiquetas_resumen["mejora"].configure(text=mejora)
        self.etiquetas_resumen["coincidencia"].configure(
            text="Sí" if coinciden else "No",
            text_color=COLOR_PRIMARIO if coinciden else COLOR_PELIGRO
        )

        self.etiqueta_preparacion.configure(
            text=(
                "Preparación de la lista binaria con QuickSort: "
                f"{self.formatear_tiempo(preparacion['tiempo_ms'])}. "
                "Este tiempo no se suma a la búsqueda."
            )
        )

        resultado = lineal["resultado"] or binaria["resultado"]
        self.mostrar_resultado_busqueda(resultado, valor)
        self.dibujar_grafico_busquedas(lineal, binaria)

    #muestra los datos del medicamento encontrado
    def mostrar_resultado_busqueda(self, medicamento, valor):
        if medicamento is None:
            self.etiqueta_estado_busqueda.configure(
                text="NO ENCONTRADO",
                text_color=COLOR_PELIGRO
            )
            self.etiqueta_nombre_resultado.configure(
                text=f"No existe una coincidencia para “{valor}”"
            )
            self.etiqueta_datos_resultado.configure(
                text=(
                    "Ambos algoritmos terminaron sin encontrar el valor. "
                    "Las comparaciones realizadas permanecen disponibles "
                    "para el análisis."
                )
            )
            return

        self.etiqueta_estado_busqueda.configure(
            text="MEDICAMENTO ENCONTRADO",
            text_color=COLOR_PRIMARIO
        )
        self.etiqueta_nombre_resultado.configure(
            text=medicamento.nombre
        )
        self.etiqueta_datos_resultado.configure(
            text=(
                f"Código: {medicamento.codigo}\n"
                f"Categoría: {medicamento.categoria}\n"
                f"Lote: {medicamento.lote}\n"
                f"Vencimiento: {medicamento.fecha_vencimiento}\n"
                f"Stock: {medicamento.stock} unidades\n"
                f"Precio: ${medicamento.precio:.2f}\n"
                f"Estado: {medicamento.obtener_estado()}"
            )
        )

    #dibuja el numero de comparaciones de cada busqueda
    def dibujar_grafico_busquedas(self, lineal, binaria):
        canvas = self.grafico_busqueda
        canvas.delete("all")
        canvas.update_idletasks()

        ancho = max(canvas.winfo_width(), 520)
        alto = max(canvas.winfo_height(), 230)
        valores = [
            ("Búsqueda lineal", lineal["comparaciones"], COLOR_ADVERTENCIA),
            ("Búsqueda binaria", binaria["comparaciones"], COLOR_PRIMARIO)
        ]
        maximo = max(lineal["comparaciones"], binaria["comparaciones"], 1)
        ancho_barra = 110
        espacio = 90
        centro = ancho / 2
        inicio_x = centro - ancho_barra - espacio / 2
        base_y = alto - 42
        alto_util = max(alto - 90, 80)

        for indice, (nombre, valor, color) in enumerate(valores):
            x1 = inicio_x + indice * (ancho_barra + espacio)
            altura = max((valor / maximo) * alto_util, 3)
            y1 = base_y - altura

            canvas.create_rectangle(
                x1,
                y1,
                x1 + ancho_barra,
                base_y,
                fill=color,
                outline=""
            )
            canvas.create_text(
                x1 + ancho_barra / 2,
                y1 - 12,
                text=f"{valor:,}",
                fill=COLOR_TEXTO,
                font=("Segoe UI", 11, "bold")
            )
            canvas.create_text(
                x1 + ancho_barra / 2,
                base_y + 16,
                text=nombre,
                fill=COLOR_TEXTO_SUAVE,
                font=("Segoe UI", 8)
            )

    #muestra una indicacion antes de tener resultados
    def dibujar_grafico_vacio(self, canvas, mensaje):
        canvas.delete("all")
        canvas.update_idletasks()
        ancho = max(canvas.winfo_width(), 500)
        alto = max(canvas.winfo_height(), 220)
        canvas.create_text(
            ancho / 2,
            alto / 2,
            text=mensaje,
            fill=COLOR_TEXTO_SUAVE,
            font=("Segoe UI", 10)
        )

    #prepara el estilo de las tablas para el tema claro
    def configurar_estilo_tablas(self):
        estilo = ttk.Style()
        estilo.configure(
            "Rendimiento.Treeview",
            background=COLOR_PANEL,
            fieldbackground=COLOR_PANEL,
            foreground=COLOR_TEXTO,
            rowheight=29,
            borderwidth=0,
            font=("Segoe UI", 9)
        )
        estilo.configure(
            "Rendimiento.Treeview.Heading",
            background=COLOR_FILA,
            foreground=COLOR_TEXTO,
            relief="flat",
            font=("Segoe UI", 9, "bold")
        )
        estilo.map(
            "Rendimiento.Treeview",
            background=[("selected", COLOR_SELECCION)],
            foreground=[("selected", COLOR_TEXTO)]
        )

    #presenta tiempos pequenos sin perder precision
    @staticmethod
    def formatear_tiempo(tiempo_ms):
        return f"{tiempo_ms:.6f} ms"

    #elige el menor tiempo sin alterar los resultados
    @staticmethod
    def obtener_ganador(tiempo_a, tiempo_b, nombre_a, nombre_b):
        if tiempo_a < tiempo_b:
            return nombre_a

        if tiempo_b < tiempo_a:
            return nombre_b

        return "Empate"

    #calcula la diferencia porcentual entre los tiempos medidos
    @staticmethod
    def calcular_mejora(tiempo_a, tiempo_b):
        mayor = max(tiempo_a, tiempo_b)
        menor = min(tiempo_a, tiempo_b)

        if mayor <= 0:
            return "0.00%"

        mejora = ((mayor - menor) / mayor) * 100
        return f"{mejora:.2f}%"