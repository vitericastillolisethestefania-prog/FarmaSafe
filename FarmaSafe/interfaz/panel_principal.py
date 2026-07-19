import tkinter as tk
from collections import Counter
from tkinter import messagebox

import customtkinter as ctk

from config import (
    NOMBRE_APLICACION,
    TAMANO_VENTANA
)
from servicios.gestor_inventario import GestorInventario
from servicios.gestor_pedidos import GestorPedidos
from servicios.gestor_ventas import GestorVentas
from interfaz.vista_asistente import VistaAsistente
from interfaz.vista_inventario import VistaInventario
from interfaz.vista_pedidos import VistaPedidos
from interfaz.vista_rendimiento import VistaRendimiento
from interfaz.vista_ventas import VistaVentas
from utilidades.gestor_imagenes import (
    cargar_imagen_interfaz,
    cargar_imagen_interfaz_ctk
)


#aplica la paleta clara definida en el branding de farmasafe
ctk.set_appearance_mode("light")

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
COLOR_MORADO = "#8B5CF6"
COLOR_GRIS_GRAFICO = "#94A3B8"


class PanelPrincipal(ctk.CTk):

    def __init__(self):
        super().__init__()

        #configura la ventana que contiene todo el sistema
        self.title(NOMBRE_APLICACION)
        self.geometry(TAMANO_VENTANA)
        self.minsize(1100, 680)
        self.configure(fg_color=COLOR_FONDO)

        #coloca el logo pequeno como icono de la ventana
        self.icono_aplicacion = cargar_imagen_interfaz(
            "logo_icono.png",
            64,
            64
        )

        if self.icono_aplicacion is not None:
            self.iconphoto(True, self.icono_aplicacion)

        #carga los gestores que conectan la interfaz con los archivos csv
        self.gestor_inventario = GestorInventario()
        self.gestor_pedidos = GestorPedidos()
        self.gestor_ventas = GestorVentas()

        #guarda las imagenes mientras la ventana permanece abierta
        self.imagenes_interfaz = {}
        self.botones_menu = {}
        self.opcion_actual = ""

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.crear_menu_lateral()
        self.crear_contenedor_principal()
        self.mostrar_inicio()

    #crea el menu que permite cambiar entre las vistas
    def crear_menu_lateral(self):
        self.menu_lateral = ctk.CTkFrame(
            self,
            width=235,
            corner_radius=0,
            fg_color=COLOR_MENU
        )
        self.menu_lateral.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        self.menu_lateral.grid_propagate(False)
        self.menu_lateral.grid_rowconfigure(8, weight=1)

        marca = ctk.CTkFrame(
            self.menu_lateral,
            height=112,
            corner_radius=0,
            fg_color="transparent"
        )
        marca.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=18,
            pady=(18, 6)
        )
        marca.grid_propagate(False)

        #usa la version del logo preparada para fondos claros
        logo = cargar_imagen_interfaz_ctk(
            "logo_icono.png",
            58,
            70
        )

        if logo is None:
            logo = cargar_imagen_interfaz_ctk(
                "logo_icono_ver2.png",
                58,
                70
            )

        self.imagenes_interfaz["logo_menu"] = logo

        if logo is not None:
            ctk.CTkLabel(
                marca,
                text="",
                image=logo,
                width=58
            ).grid(
                row=0,
                column=0,
                rowspan=2,
                padx=(0, 10),
                pady=12
            )

        textos_marca = ctk.CTkFrame(
            marca,
            fg_color="transparent"
        )
        textos_marca.grid(
            row=0,
            column=1,
            rowspan=2,
            sticky="w"
        )

        ctk.CTkLabel(
            textos_marca,
            text="FarmaSafe",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=19,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).pack(anchor="w")

        ctk.CTkLabel(
            textos_marca,
            text="Control farmacéutico",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10
            ),
            text_color=COLOR_TEXTO_SUAVE
        ).pack(anchor="w", pady=(1, 0))

        ctk.CTkLabel(
            self.menu_lateral,
            text="MENÚ PRINCIPAL",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10,
                weight="bold"
            ),
            text_color=COLOR_TEXTO_SUAVE
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=24,
            pady=(18, 8)
        )

        opciones = [
            ("inicio", "⌂   Panel principal", self.mostrar_inicio),
            ("inventario", "▦   Inventario", self.mostrar_inventario),
            ("ventas", "$   Ventas", self.mostrar_ventas),
            ("pedidos", "≡   Pedidos", self.mostrar_pedidos),
            ("rendimiento", "↗   Rendimiento", self.mostrar_rendimiento),
            ("asistente", "?   Asistente", self.mostrar_asistente)
        ]

        for fila, (codigo, texto, comando) in enumerate(opciones, start=2):
            boton = ctk.CTkButton(
                self.menu_lateral,
                text=texto,
                command=comando,
                height=48,
                corner_radius=8,
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=12
                ),
                fg_color="transparent",
                hover_color=COLOR_SELECCION,
                text_color=COLOR_TEXTO_SUAVE,
                anchor="w",
                cursor="hand2"
            )
            boton.grid(
                row=fila,
                column=0,
                sticky="ew",
                padx=10,
                pady=2
            )
            self.botones_menu[codigo] = boton

        pie = ctk.CTkFrame(
            self.menu_lateral,
            fg_color="transparent"
        )
        pie.grid(
            row=9,
            column=0,
            sticky="sew",
            padx=20,
            pady=20
        )

        ctk.CTkLabel(
            pie,
            text="Sistema local",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10,
                weight="bold"
            ),
            text_color=COLOR_PRIMARIO
        ).pack(anchor="w")

        ctk.CTkLabel(
            pie,
            text="Datos guardados en CSV",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=9
            ),
            text_color=COLOR_TEXTO_SUAVE
        ).pack(anchor="w", pady=(2, 0))

    #crea el espacio donde se mostrara cada modulo
    def crear_contenedor_principal(self):
        self.contenedor_principal = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=COLOR_FONDO
        )
        self.contenedor_principal.grid(
            row=0,
            column=1,
            sticky="nsew"
        )
        self.contenedor_principal.grid_rowconfigure(1, weight=1)
        self.contenedor_principal.grid_columnconfigure(0, weight=1)

        self.encabezado = ctk.CTkFrame(
            self.contenedor_principal,
            height=98,
            corner_radius=0,
            fg_color="transparent"
        )
        self.encabezado.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=36,
            pady=(18, 0)
        )
        self.encabezado.grid_propagate(False)
        self.encabezado.grid_columnconfigure(0, weight=1)

        self.textos_encabezado = ctk.CTkFrame(
            self.encabezado,
            fg_color="transparent"
        )
        self.textos_encabezado.grid(
            row=0,
            column=0,
            sticky="nw"
        )

        self.titulo = ctk.CTkLabel(
            self.textos_encabezado,
            text="",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=27,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        )
        self.titulo.pack(anchor="w")

        self.subtitulo = ctk.CTkLabel(
            self.textos_encabezado,
            text="",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=11
            ),
            text_color=COLOR_TEXTO_SUAVE
        )
        self.subtitulo.pack(anchor="w", pady=(5, 0))

        self.estado_sistema = ctk.CTkLabel(
            self.encabezado,
            text="●  Sistema activo",
            height=38,
            corner_radius=8,
            fg_color=COLOR_PANEL,
            text_color=COLOR_PRIMARIO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10,
                weight="bold"
            )
        )
        self.estado_sistema.grid(
            row=0,
            column=1,
            sticky="ne",
            padx=(20, 0),
            pady=4
        )

        self.contenido = ctk.CTkFrame(
            self.contenedor_principal,
            corner_radius=0,
            fg_color="transparent"
        )
        self.contenido.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=36,
            pady=(0, 26)
        )

    #elimina los elementos de la vista anterior
    def limpiar_contenido(self):
        for elemento in self.contenido.winfo_children():
            elemento.destroy()

    #cambia el color del boton seleccionado
    def seleccionar_opcion(self, codigo):
        self.opcion_actual = codigo

        for clave, boton in self.botones_menu.items():
            if clave == codigo:
                boton.configure(
                    fg_color=COLOR_SELECCION,
                    text_color=COLOR_TEXTO
                )
            else:
                boton.configure(
                    fg_color="transparent",
                    text_color=COLOR_TEXTO_SUAVE
                )

    #actualiza el titulo que aparece sobre cada vista
    def cambiar_encabezado(self, titulo, subtitulo):
        self.titulo.configure(text=titulo)
        self.subtitulo.configure(text=subtitulo)

    #carga el icono creado para cada indicador del panel
    def colocar_icono_tarjeta(self, contenedor, archivo_icono, color):
        clave_imagen = f"tarjeta_{archivo_icono}"
        imagen = cargar_imagen_interfaz_ctk(
            archivo_icono,
            58,
            58
        )
        self.imagenes_interfaz[clave_imagen] = imagen

        if imagen is not None:
            ctk.CTkLabel(
                contenedor,
                text="",
                image=imagen,
                fg_color="transparent"
            ).place(
                relx=0.5,
                rely=0.5,
                anchor="center"
            )
            return

        #mantiene la tarjeta visible si falta un archivo de imagen
        ctk.CTkLabel(
            contenedor,
            text="●",
            font=ctk.CTkFont(size=26),
            text_color=color,
            fg_color="transparent"
        ).place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

    #crea una tarjeta para mostrar un dato del sistema
    def crear_tarjeta(
        self,
        contenedor,
        columna,
        titulo,
        valor,
        detalle,
        color,
        archivo_icono
    ):
        tarjeta = ctk.CTkFrame(
            contenedor,
            height=145,
            corner_radius=12,
            fg_color=COLOR_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )
        tarjeta.grid(
            row=0,
            column=columna,
            sticky="nsew",
            padx=7
        )
        tarjeta.grid_propagate(False)
        tarjeta.grid_columnconfigure(1, weight=1)

        #marca cada indicador con el color relacionado con su estado
        linea_color = ctk.CTkFrame(
            tarjeta,
            width=5,
            height=117,
            corner_radius=3,
            fg_color=color
        )
        linea_color.place(
            x=0,
            y=14
        )

        icono = ctk.CTkFrame(
            tarjeta,
            width=58,
            height=58,
            corner_radius=10,
            fg_color="transparent"
        )
        icono.grid(
            row=0,
            column=0,
            rowspan=3,
            padx=(18, 13),
            pady=20
        )
        icono.grid_propagate(False)
        self.colocar_icono_tarjeta(
            icono,
            archivo_icono,
            color
        )

        ctk.CTkLabel(
            tarjeta,
            text=titulo,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10,
                weight="bold"
            ),
            text_color=color
        ).grid(
            row=0,
            column=1,
            sticky="sw",
            pady=(19, 0)
        )

        ctk.CTkLabel(
            tarjeta,
            text=str(valor),
            font=ctk.CTkFont(
                family="Segoe UI",
                size=28,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).grid(
            row=1,
            column=1,
            sticky="w",
            pady=(0, 0)
        )

        ctk.CTkLabel(
            tarjeta,
            text=detalle,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=9
            ),
            text_color=COLOR_TEXTO_SUAVE,
            wraplength=170,
            justify="left"
        ).grid(
            row=2,
            column=1,
            sticky="nw",
            padx=(0, 10),
            pady=(0, 15)
        )

    #crea una fila con una alerta y su cantidad
    def crear_fila_alerta(self, contenedor, fila, nombre, cantidad, color):
        bloque = ctk.CTkFrame(
            contenedor,
            height=46,
            corner_radius=8,
            fg_color=COLOR_FILA
        )
        bloque.grid(
            row=fila,
            column=0,
            sticky="ew",
            padx=20,
            pady=4
        )
        bloque.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            bloque,
            text="●",
            font=ctk.CTkFont(size=12),
            text_color=color
        ).grid(row=0, column=0, padx=(13, 9), pady=10)

        ctk.CTkLabel(
            bloque,
            text=nombre,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10
            ),
            text_color=COLOR_TEXTO
        ).grid(row=0, column=1, sticky="w")

        ctk.CTkLabel(
            bloque,
            text=str(cantidad),
            font=ctk.CTkFont(
                family="Segoe UI",
                size=11,
                weight="bold"
            ),
            text_color=color
        ).grid(row=0, column=2, padx=14)

    #prepara las categorias que se mostraran en el grafico
    def obtener_categorias_grafico(self, medicamentos):
        conteo = Counter(
            medicamento.categoria
            for medicamento in medicamentos
        )
        principales = conteo.most_common(4)
        cantidad_principales = sum(
            cantidad
            for _, cantidad in principales
        )
        cantidad_otros = len(medicamentos) - cantidad_principales

        if cantidad_otros > 0:
            principales.append(("Otros", cantidad_otros))

        return principales

    #dibuja la distribucion del inventario por categoria
    def crear_grafico_categorias(self, contenedor, medicamentos):
        categorias = self.obtener_categorias_grafico(medicamentos)
        colores = [
            COLOR_PRIMARIO,
            COLOR_AZUL,
            COLOR_ADVERTENCIA,
            COLOR_MORADO,
            COLOR_GRIS_GRAFICO
        ]

        zona = ctk.CTkFrame(
            contenedor,
            corner_radius=10,
            fg_color=COLOR_FILA
        )
        zona.grid(
            row=7,
            column=0,
            sticky="nsew",
            padx=20,
            pady=(13, 20)
        )
        zona.grid_columnconfigure(1, weight=1)

        lienzo = tk.Canvas(
            zona,
            width=170,
            height=160,
            bg=COLOR_FILA,
            highlightthickness=0
        )
        lienzo.grid(
            row=0,
            column=0,
            padx=(14, 8),
            pady=8
        )

        total = sum(
            cantidad
            for _, cantidad in categorias
        )

        if total == 0:
            lienzo.create_text(
                85,
                80,
                text="Sin datos",
                fill=COLOR_TEXTO_SUAVE,
                font=("Segoe UI", 10)
            )
        else:
            inicio = 90

            for indice, (_, cantidad) in enumerate(categorias):
                extension = 360 * cantidad / total
                lienzo.create_arc(
                    15,
                    10,
                    155,
                    150,
                    start=inicio,
                    extent=-extension,
                    fill=colores[indice],
                    outline=COLOR_FILA,
                    width=2
                )
                inicio -= extension

            lienzo.create_oval(
                52,
                47,
                118,
                113,
                fill=COLOR_FILA,
                outline=COLOR_FILA
            )
            lienzo.create_text(
                85,
                71,
                text=str(total),
                fill=COLOR_TEXTO,
                font=("Segoe UI", 17, "bold")
            )
            lienzo.create_text(
                85,
                92,
                text="registros",
                fill=COLOR_TEXTO_SUAVE,
                font=("Segoe UI", 8)
            )

        leyenda = ctk.CTkFrame(
            zona,
            fg_color="transparent"
        )
        leyenda.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(4, 16),
            pady=14
        )
        leyenda.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            leyenda,
            text="Inventario por categoría",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=11,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="w",
            pady=(0, 7)
        )

        for fila, (nombre, cantidad) in enumerate(categorias, start=1):
            porcentaje = 0 if total == 0 else cantidad * 100 / total

            ctk.CTkLabel(
                leyenda,
                text="●",
                text_color=colores[fila - 1]
            ).grid(row=fila, column=0, sticky="w", padx=(0, 6))

            ctk.CTkLabel(
                leyenda,
                text=nombre,
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=9
                ),
                text_color=COLOR_TEXTO_SUAVE
            ).grid(row=fila, column=1, sticky="w")

            ctk.CTkLabel(
                leyenda,
                text=f"{porcentaje:.0f}%",
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=9,
                    weight="bold"
                ),
                text_color=COLOR_TEXTO
            ).grid(row=fila, column=2, sticky="e")

    #muestra las estructuras y la presencia del asistente
    def crear_panel_informacion(self, contenedor):
        panel = ctk.CTkFrame(
            contenedor,
            width=285,
            corner_radius=12,
            fg_color=COLOR_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )
        panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(9, 7)
        )
        panel.grid_propagate(False)
        panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            panel,
            text="Estructuras utilizadas",
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
            pady=(19, 12)
        )

        estructuras = [
            ("Árbol AVL", "inventario y búsquedas"),
            ("Cola enlazada", "atención FIFO de pedidos"),
            ("QuickSort", "ordenamiento eficiente"),
            ("Búsqueda binaria", "localización de productos")
        ]

        for fila, (nombre, uso) in enumerate(estructuras, start=1):
            bloque = ctk.CTkFrame(
                panel,
                fg_color="transparent"
            )
            bloque.grid(
                row=fila,
                column=0,
                sticky="ew",
                padx=20,
                pady=7
            )

            ctk.CTkLabel(
                bloque,
                text=nombre,
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=10,
                    weight="bold"
                ),
                text_color=COLOR_PRIMARIO
            ).pack(anchor="w")

            ctk.CTkLabel(
                bloque,
                text=uso,
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=8
                ),
                text_color=COLOR_TEXTO_SUAVE
            ).pack(anchor="w", pady=(1, 0))

        farma = cargar_imagen_interfaz_ctk(
            "farmi_normal.png",
            135,
            82
        )
        self.imagenes_interfaz["farmi_inicio"] = farma

        tarjeta_farmi = ctk.CTkFrame(
            panel,
            corner_radius=10,
            fg_color=COLOR_FILA
        )
        tarjeta_farmi.grid(
            row=6,
            column=0,
            sticky="sew",
            padx=18,
            pady=(18, 18)
        )
        panel.grid_rowconfigure(6, weight=1)

        if farma is not None:
            ctk.CTkLabel(
                tarjeta_farmi,
                text="",
                image=farma
            ).pack(pady=(10, 2))

        ctk.CTkLabel(
            tarjeta_farmi,
            text="FARMI está supervisando",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=9,
                weight="bold"
            ),
            text_color=COLOR_PRIMARIO
        ).pack(pady=(2, 1))

        ctk.CTkLabel(
            tarjeta_farmi,
            text="Alertas y registros del sistema",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=8
            ),
            text_color=COLOR_TEXTO_SUAVE
        ).pack(pady=(0, 10))

    #muestra el resumen general del inventario y las operaciones
    def mostrar_inicio(self):
        self.limpiar_contenido()
        self.seleccionar_opcion("inicio")
        self.cambiar_encabezado(
            "Panel principal",
            "Resumen preventivo del inventario y las operaciones"
        )

        resumen_inventario = self.gestor_inventario.obtener_resumen()
        resumen_pedidos = self.gestor_pedidos.obtener_resumen()
        resumen_ventas = self.gestor_ventas.obtener_resumen()
        medicamentos = self.gestor_inventario.obtener_todos()

        #cuenta los medicamentos que se encuentran proximos a vencer
        proximos_vencer = sum(
            1
            for medicamento in medicamentos
            if medicamento.proximo_a_vencer()
        )

        tarjetas = ctk.CTkFrame(
            self.contenido,
            height=145,
            corner_radius=0,
            fg_color="transparent"
        )
        tarjetas.pack(fill="x")
        tarjetas.pack_propagate(False)

        for columna in range(4):
            tarjetas.grid_columnconfigure(columna, weight=1)

        datos_tarjetas = [
            (
                "MEDICAMENTOS",
                resumen_inventario["total"],
                "registros en el árbol AVL",
                COLOR_AZUL,
                "medicamentos_icon.png"
            ),
            (
                "STOCK BAJO",
                resumen_inventario["stock_bajo"],
                "productos que requieren reposición",
                COLOR_ADVERTENCIA,
                "stock_bajo_icon.png"
            ),
            (
                "VENCIDOS",
                resumen_inventario["vencidos"],
                "productos que no deben dispensarse",
                COLOR_PELIGRO,
                "vencidos_icon.png"
            ),
            (
                "VENTAS",
                resumen_ventas["cantidad_ventas"],
                "operaciones registradas",
                COLOR_PRIMARIO,
                "ventas_icon.png"
            )
        ]

        for columna, datos in enumerate(datos_tarjetas):
            self.crear_tarjeta(
                tarjetas,
                columna,
                *datos
            )

        zona_inferior = ctk.CTkFrame(
            self.contenido,
            corner_radius=0,
            fg_color="transparent"
        )
        zona_inferior.pack(
            fill="both",
            expand=True,
            pady=(18, 0)
        )
        zona_inferior.grid_rowconfigure(0, weight=1)
        zona_inferior.grid_columnconfigure(0, weight=1)

        panel_alertas = ctk.CTkFrame(
            zona_inferior,
            corner_radius=12,
            fg_color=COLOR_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )
        panel_alertas.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(7, 9)
        )
        panel_alertas.grid_columnconfigure(0, weight=1)
        panel_alertas.grid_rowconfigure(7, weight=1)

        ctk.CTkLabel(
            panel_alertas,
            text="Alertas preventivas",
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
            pady=(18, 2)
        )

        ctk.CTkLabel(
            panel_alertas,
            text="Situaciones que necesitan revisión",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=9
            ),
            text_color=COLOR_TEXTO_SUAVE
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 9)
        )

        alertas = [
            (
                "Stock bajo",
                resumen_inventario["stock_bajo"],
                COLOR_ADVERTENCIA
            ),
            (
                "Medicamentos vencidos",
                resumen_inventario["vencidos"],
                COLOR_PELIGRO
            ),
            (
                "Próximos a vencer",
                proximos_vencer,
                COLOR_AZUL
            ),
            (
                "Pedidos pendientes",
                resumen_pedidos["pendientes"],
                COLOR_PRIMARIO
            )
        ]

        for fila, (nombre, cantidad, color) in enumerate(
            alertas,
            start=2
        ):
            self.crear_fila_alerta(
                panel_alertas,
                fila,
                nombre,
                cantidad,
                color
            )

        self.crear_grafico_categorias(
            panel_alertas,
            medicamentos
        )
        self.crear_panel_informacion(zona_inferior)

    #muestra temporalmente el nombre del modulo seleccionado
    def mostrar_modulo_pendiente(self, codigo, titulo, descripcion):
        self.limpiar_contenido()
        self.seleccionar_opcion(codigo)
        self.cambiar_encabezado(titulo, descripcion)

        panel = ctk.CTkFrame(
            self.contenido,
            corner_radius=12,
            fg_color=COLOR_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )
        panel.pack(
            fill="both",
            expand=True,
            padx=7
        )

        ctk.CTkLabel(
            panel,
            text=titulo,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=27,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).pack(pady=(130, 10))

        ctk.CTkLabel(
            panel,
            text="La conexión de esta vista se agregará en el siguiente paso.",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=11
            ),
            text_color=COLOR_TEXTO_SUAVE
        ).pack()

        ctk.CTkButton(
            panel,
            text="Volver al panel",
            command=self.mostrar_inicio,
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10,
                weight="bold"
            ),
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_SECUNDARIO,
            text_color=COLOR_TEXTO,
            cursor="hand2"
        ).pack(pady=24)

    def mostrar_inventario(self):
        self.limpiar_contenido()
        self.seleccionar_opcion("inventario")
        self.cambiar_encabezado(
            "Inventario",
            "Administración y control preventivo de medicamentos"
        )

        vista = VistaInventario(
            self.contenido,
            self.gestor_inventario
        )
        vista.pack(
            fill="both",
            expand=True
        )

    def mostrar_ventas(self):
        self.limpiar_contenido()
        self.seleccionar_opcion("ventas")
        self.cambiar_encabezado(
            "Ventas",
            "Registro de ventas y actualización automática del stock"
        )

        vista = VistaVentas(
            self.contenido,
            self.gestor_ventas,
            self.gestor_inventario
        )
        vista.pack(
            fill="both",
            expand=True
        )

    def mostrar_pedidos(self):
        self.limpiar_contenido()
        self.seleccionar_opcion("pedidos")
        self.cambiar_encabezado(
            "Pedidos",
            "Atención de solicitudes mediante una cola FIFO"
        )

        vista = VistaPedidos(
            self.contenido,
            self.gestor_pedidos,
            self.gestor_inventario,
            self.gestor_ventas
        )
        vista.pack(
            fill="both",
            expand=True
        )

    def mostrar_rendimiento(self):
        self.limpiar_contenido()
        self.seleccionar_opcion("rendimiento")
        self.cambiar_encabezado(
            "Rendimiento",
            "Comparación de ordenamientos y métodos de búsqueda"
        )

        vista = VistaRendimiento(
            self.contenido,
            self.gestor_inventario
        )
        vista.pack(
            fill="both",
            expand=True
        )

    def mostrar_asistente(self):
        self.limpiar_contenido()
        self.seleccionar_opcion("asistente")
        self.cambiar_encabezado(
            "Asistente FARMI",
            "Consultas locales sobre inventario, ventas y pedidos"
        )

        vista = VistaAsistente(
            self.contenido,
            self.gestor_inventario,
            self.gestor_pedidos,
            self.gestor_ventas
        )
        vista.pack(
            fill="both",
            expand=True
        )

    #muestra un mensaje antes de cerrar el programa
    def cerrar_aplicacion(self):
        cerrar = messagebox.askyesno(
            "Cerrar FarmaSafe",
            "¿Desea cerrar el sistema?"
        )

        if cerrar:
            self.destroy()