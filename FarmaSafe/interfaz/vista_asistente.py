import tkinter as tk
import unicodedata

import customtkinter as ctk

from utilidades.gestor_imagenes import cargar_imagen_interfaz_ctk


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


class MotorAsistenteFarmi:

    def __init__(
        self,
        gestor_inventario,
        gestor_pedidos,
        gestor_ventas
    ):
        #conecta las respuestas con los datos actuales del sistema
        self.gestor_inventario = gestor_inventario
        self.gestor_pedidos = gestor_pedidos
        self.gestor_ventas = gestor_ventas

    #elimina diferencias de mayusculas y tildes
    @staticmethod
    def normalizar(texto):
        texto = str(texto).strip().lower()
        texto = unicodedata.normalize("NFD", texto)
        return "".join(
            caracter
            for caracter in texto
            if unicodedata.category(caracter) != "Mn"
        )

    #prepara una respuesta con texto y expresion de farmi
    @staticmethod
    def respuesta(texto, emocion="normal", titulo="FARMI"):
        return {
            "texto": texto,
            "emocion": emocion,
            "titulo": titulo
        }

    #elige la consulta correspondiente sin modificar ningun registro
    def responder(self, mensaje):
        texto = str(mensaje).strip()
        consulta = self.normalizar(texto)

        if not consulta:
            return self.respuesta(
                "Escribe una consulta para que pueda ayudarte."
            )

        if self.contiene_alguna(
            consulta,
            ("hola", "buenos dias", "buenas tardes", "buenas noches")
        ):
            return self.respuesta(
                "¡Hola! Soy FARMI, el asistente local de FarmaSafe. "
                "Puedo consultar el inventario, las alertas, las ventas "
                "y la cola de pedidos."
            )

        if self.contiene_alguna(
            consulta,
            (
                "ayuda",
                "que puedes hacer",
                "como funcionas",
                "comandos",
                "opciones"
            )
        ):
            return self.responder_ayuda()

        if self.contiene_alguna(
            consulta,
            ("resumen general", "resumen del sistema", "estado del sistema")
        ):
            return self.responder_resumen_general()

        if self.contiene_alguna(
            consulta,
            ("stock bajo", "poco stock", "reponer", "reposicion")
        ):
            return self.responder_stock_bajo()

        if self.contiene_alguna(
            consulta,
            ("sin stock", "agotados", "agotado")
        ):
            return self.responder_sin_stock()

        if self.contiene_alguna(
            consulta,
            ("proximos a vencer", "proximo a vencer", "por vencer")
        ):
            return self.responder_proximos()

        if self.contiene_alguna(
            consulta,
            ("vencidos", "medicamento vencido", "medicamentos vencidos")
        ):
            return self.responder_vencidos()

        if self.contiene_alguna(
            consulta,
            ("pedidos", "cola", "pendientes")
        ):
            return self.responder_pedidos()

        if self.contiene_alguna(
            consulta,
            ("ventas", "ingresos", "producto mas vendido")
        ):
            return self.responder_ventas()

        if consulta.startswith("categoria "):
            valor = texto[len("categoria "):].strip()
            return self.responder_categoria(valor)

        for patron, tipo in (
            ("precio de ", "precio"),
            ("cuanto cuesta ", "precio"),
            ("stock de ", "stock"),
            ("estado de ", "estado"),
            ("buscar ", "buscar"),
            ("busca ", "buscar")
        ):
            if consulta.startswith(patron):
                valor = texto[len(patron):].strip()
                return self.responder_medicamento(valor, tipo)

        if consulta.isdigit():
            return self.responder_medicamento(consulta, "buscar")

        if self.contiene_alguna(
            consulta,
            ("inventario", "medicamentos", "cuantos medicamentos")
        ):
            return self.responder_inventario()

        #intenta localizar el texto como nombre antes de mostrar la ayuda
        encontrados = self.gestor_inventario.buscar_por_nombre(texto)

        if encontrados:
            return self.responder_resultados(encontrados, "buscar")

        return self.respuesta(
            "No pude relacionar esa consulta con los datos del sistema. "
            "Prueba con “stock bajo”, “ventas”, “pedidos pendientes”, "
            "“buscar paracetamol” o “qué puedes hacer”.",
            "normal",
            "Consulta no reconocida"
        )

    #revisa si alguna expresion se encuentra en la consulta
    @staticmethod
    def contiene_alguna(texto, expresiones):
        return any(expresion in texto for expresion in expresiones)

    #explica las consultas disponibles
    def responder_ayuda(self):
        return self.respuesta(
            "Puedo ayudarte con estas consultas:\n\n"
            "• Resumen general del sistema\n"
            "• Medicamentos con stock bajo\n"
            "• Medicamentos vencidos o próximos a vencer\n"
            "• Medicamentos sin stock\n"
            "• Buscar paracetamol\n"
            "• Precio de ibuprofeno\n"
            "• Stock de vitamina C\n"
            "• Categoría antibiótico\n"
            "• Pedidos pendientes\n"
            "• Resumen de ventas\n\n"
            "Las consultas son locales y no necesitan conexión a internet.",
            "presentacion",
            "¿Qué puede hacer FARMI?"
        )

    #resume inventario, pedidos y ventas en una respuesta
    def responder_resumen_general(self):
        inventario = self.gestor_inventario.obtener_resumen()
        pedidos = self.gestor_pedidos.obtener_resumen()
        ventas = self.gestor_ventas.obtener_resumen()
        cantidad_ventas = ventas.get("cantidad_ventas", 0)
        ingresos = float(ventas.get("ingresos", 0))

        hay_alertas = (
            inventario.get("vencidos", 0) > 0
            or inventario.get("stock_bajo", 0) > 0
            or pedidos.get("pendientes", 0) > 0
        )

        return self.respuesta(
            "Este es el estado actual de FarmaSafe:\n\n"
            f"• Medicamentos registrados: {inventario.get('total', 0)}\n"
            f"• Stock bajo: {inventario.get('stock_bajo', 0)}\n"
            f"• Vencidos: {inventario.get('vencidos', 0)}\n"
            f"• Próximos a vencer: {inventario.get('proximos', 0)}\n"
            f"• Pedidos pendientes: {pedidos.get('pendientes', 0)}\n"
            f"• Ventas registradas: {cantidad_ventas}\n"
            f"• Ingresos acumulados: ${ingresos:.2f}",
            "advertencia" if hay_alertas else "exito",
            "Resumen general"
        )

    #muestra la cantidad de medicamentos y la altura del arbol
    def responder_inventario(self):
        resumen = self.gestor_inventario.obtener_resumen()
        return self.respuesta(
            f"El inventario contiene {resumen.get('total', 0)} "
            "medicamentos organizados en el árbol AVL. "
            f"La altura actual del árbol es {resumen.get('altura_arbol', 0)}.",
            "normal",
            "Inventario"
        )

    #lista los productos que llegaron al minimo permitido
    def responder_stock_bajo(self):
        alertas = self.gestor_inventario.obtener_alertas()
        medicamentos = alertas.get("stock_bajo", [])

        if not medicamentos:
            return self.respuesta(
                "No hay medicamentos con stock bajo. El inventario se "
                "encuentra por encima de los mínimos establecidos.",
                "exito",
                "Stock controlado"
            )

        return self.respuesta(
            f"Encontré {len(medicamentos)} medicamentos que requieren "
            "reposición:\n\n"
            + self.formatear_medicamentos(medicamentos, "stock"),
            "advertencia",
            "Alerta de stock bajo"
        )

    #lista los productos que ya no tienen unidades
    def responder_sin_stock(self):
        alertas = self.gestor_inventario.obtener_alertas()
        medicamentos = alertas.get("sin_stock", [])

        if not medicamentos:
            return self.respuesta(
                "No existen medicamentos agotados en este momento.",
                "exito",
                "Sin productos agotados"
            )

        return self.respuesta(
            f"Hay {len(medicamentos)} medicamentos sin unidades:\n\n"
            + self.formatear_medicamentos(medicamentos, "stock"),
            "peligro",
            "Medicamentos agotados"
        )

    #lista los medicamentos que ya superaron su fecha
    def responder_vencidos(self):
        alertas = self.gestor_inventario.obtener_alertas()
        medicamentos = alertas.get("vencidos", [])

        if not medicamentos:
            return self.respuesta(
                "No hay medicamentos vencidos registrados.",
                "exito",
                "Inventario seguro"
            )

        return self.respuesta(
            f"Detecté {len(medicamentos)} medicamentos vencidos. No deben "
            "dispensarse:\n\n"
            + self.formatear_medicamentos(medicamentos, "fecha"),
            "peligro",
            "Alerta de vencimiento"
        )

    #lista los medicamentos dentro del periodo preventivo
    def responder_proximos(self):
        alertas = self.gestor_inventario.obtener_alertas()
        medicamentos = alertas.get("proximos", [])

        if not medicamentos:
            return self.respuesta(
                "No existen medicamentos próximos a vencer durante los "
                "siguientes 30 días.",
                "exito",
                "Sin vencimientos cercanos"
            )

        return self.respuesta(
            f"Hay {len(medicamentos)} medicamentos próximos a vencer:\n\n"
            + self.formatear_medicamentos(medicamentos, "dias"),
            "advertencia",
            "Vencimientos próximos"
        )

    #resume la cola fifo y muestra el frente actual
    def responder_pedidos(self):
        resumen = self.gestor_pedidos.obtener_resumen()
        pendientes = self.gestor_pedidos.obtener_pendientes()

        if pendientes:
            frente = pendientes[0]
            detalle_frente = (
                f"\n\nEl frente es el pedido {frente.codigo_pedido} de "
                f"{frente.cliente}: {frente.nombre_medicamento} "
                f"x{frente.cantidad}."
            )
        else:
            detalle_frente = "\n\nLa cola FIFO se encuentra vacía."

        return self.respuesta(
            "Resumen de pedidos:\n\n"
            f"• Total: {resumen.get('total', 0)}\n"
            f"• Pendientes: {resumen.get('pendientes', 0)}\n"
            f"• Atendidos: {resumen.get('atendidos', 0)}\n"
            f"• Rechazados: {resumen.get('rechazados', 0)}"
            + detalle_frente,
            "advertencia" if pendientes else "exito",
            "Cola de pedidos"
        )

    #resume las operaciones de venta guardadas
    def responder_ventas(self):
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

        return self.respuesta(
            "Resumen de ventas:\n\n"
            f"• Ventas registradas: {cantidad}\n"
            f"• Ventas de hoy: {ventas_hoy}\n"
            f"• Unidades vendidas: {unidades}\n"
            f"• Ingresos: ${ingresos:.2f}\n"
            f"• Producto más vendido: {nombre_producto}",
            "exito" if cantidad else "normal",
            "Ventas"
        )

    #busca los medicamentos pertenecientes a una categoria
    def responder_categoria(self, categoria):
        categoria_normalizada = self.normalizar(categoria)
        encontrados = []

        for medicamento in self.gestor_inventario.obtener_todos():
            if self.normalizar(medicamento.categoria) == categoria_normalizada:
                encontrados.append(medicamento)

        if not encontrados:
            return self.respuesta(
                f"No encontré medicamentos en la categoría “{categoria}”.",
                "normal",
                "Categoría sin resultados"
            )

        return self.respuesta(
            f"Encontré {len(encontrados)} medicamentos en la categoría "
            f"{categoria}:\n\n"
            + self.formatear_medicamentos(encontrados, "stock"),
            "normal",
            "Consulta por categoría"
        )

    #busca por codigo o por una parte del nombre
    def responder_medicamento(self, valor, tipo):
        valor = str(valor).strip()

        if not valor:
            return self.respuesta(
                "Indica el código o el nombre del medicamento que deseas "
                "consultar. Por ejemplo: buscar paracetamol."
            )

        if valor.isdigit():
            medicamento = self.gestor_inventario.buscar_por_codigo(
                int(valor)
            )
            encontrados = [medicamento] if medicamento is not None else []
        else:
            encontrados = self.gestor_inventario.buscar_por_nombre(valor)

        if not encontrados:
            return self.respuesta(
                f"No encontré medicamentos relacionados con “{valor}”.",
                "normal",
                "Sin coincidencias"
            )

        return self.responder_resultados(encontrados, tipo)

    #presenta uno o varios resultados encontrados
    def responder_resultados(self, medicamentos, tipo):
        if len(medicamentos) > 1:
            return self.respuesta(
                f"Encontré {len(medicamentos)} coincidencias:\n\n"
                + self.formatear_medicamentos(medicamentos, "stock"),
                "normal",
                "Resultados de la búsqueda"
            )

        medicamento = medicamentos[0]

        if tipo == "precio":
            texto = (
                f"{medicamento.nombre} tiene un precio de "
                f"${medicamento.precio:.2f}."
            )
        elif tipo == "stock":
            texto = (
                f"{medicamento.nombre} tiene {medicamento.stock} unidades. "
                f"Su stock mínimo es {medicamento.stock_minimo}."
            )
        elif tipo == "estado":
            texto = (
                f"El estado de {medicamento.nombre} es "
                f"{medicamento.obtener_estado()}."
            )
        else:
            texto = (
                f"{medicamento.nombre}\n\n"
                f"• Código: {medicamento.codigo}\n"
                f"• Categoría: {medicamento.categoria}\n"
                f"• Lote: {medicamento.lote}\n"
                f"• Vencimiento: {medicamento.fecha_vencimiento}\n"
                f"• Stock: {medicamento.stock} unidades\n"
                f"• Precio: ${medicamento.precio:.2f}\n"
                f"• Estado: {medicamento.obtener_estado()}"
            )

        estado = medicamento.obtener_estado()

        if estado in ("VENCIDO", "SIN STOCK"):
            emocion = "peligro"
        elif estado in ("PRÓXIMO A VENCER", "STOCK BAJO"):
            emocion = "advertencia"
        else:
            emocion = "exito"

        return self.respuesta(
            texto,
            emocion,
            "Medicamento localizado"
        )

    #limita las listas largas para conservar una respuesta legible
    @staticmethod
    def formatear_medicamentos(medicamentos, modo):
        lineas = []
        limite = 8

        for medicamento in medicamentos[:limite]:
            if modo == "fecha":
                detalle = f"vence {medicamento.fecha_vencimiento}"
            elif modo == "dias":
                detalle = f"faltan {medicamento.dias_para_vencer()} días"
            else:
                detalle = (
                    f"stock {medicamento.stock}/"
                    f"mínimo {medicamento.stock_minimo}"
                )

            lineas.append(
                f"• {medicamento.codigo} - {medicamento.nombre}: {detalle}"
            )

        if len(medicamentos) > limite:
            lineas.append(
                f"• ... y {len(medicamentos) - limite} resultados más"
            )

        return "\n".join(lineas)


class VistaAsistente(ctk.CTkFrame):

    IMAGENES_EMOCION = {
        "normal": "farmi_normal.png",
        "presentacion": "farmi_presentacion.png",
        "exito": "farmi_exito.png",
        "advertencia": "farmi_advertencia.png",
        "peligro": "farmi_peligro.png"
    }

    def __init__(
        self,
        master,
        gestor_inventario,
        gestor_pedidos,
        gestor_ventas
    ):
        super().__init__(
            master,
            corner_radius=0,
            fg_color="transparent"
        )

        #crea el motor local que interpreta las consultas
        self.motor = MotorAsistenteFarmi(
            gestor_inventario,
            gestor_pedidos,
            gestor_ventas
        )
        self.gestor_inventario = gestor_inventario
        self.gestor_pedidos = gestor_pedidos
        self.gestor_ventas = gestor_ventas
        self.variable_mensaje = tk.StringVar()
        self.imagenes = {}

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.cargar_imagenes()
        self.crear_resumen()
        self.crear_contenido()
        self.agregar_mensaje_farmi(
            "¡Hola! Soy FARMI. Estoy conectado con los datos locales de "
            "FarmaSafe y listo para ayudarte. Puedes usar una sugerencia "
            "o escribir tu propia consulta.",
            "presentacion",
            "Bienvenido"
        )

    #carga todas las expresiones creadas para farmi
    def cargar_imagenes(self):
        for emocion, archivo in self.IMAGENES_EMOCION.items():
            if emocion == "presentacion":
                ancho = 145
                alto = 185
            else:
                ancho = 112
                alto = 96

            self.imagenes[emocion] = cargar_imagen_interfaz_ctk(
                archivo,
                ancho,
                alto
            )

    #muestra un resumen rapido sobre el chat
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

        for columna in range(4):
            self.resumen.grid_columnconfigure(columna, weight=1)

        datos = [
            ("medicamentos", "Medicamentos", COLOR_AZUL),
            ("alertas", "Alertas de inventario", COLOR_ADVERTENCIA),
            ("pedidos", "Pedidos pendientes", COLOR_PRIMARIO),
            ("ventas", "Ventas registradas", COLOR_PRIMARIO)
        ]
        self.etiquetas_resumen = {}

        for columna, (clave, titulo, color) in enumerate(datos):
            bloque = ctk.CTkFrame(
                self.resumen,
                corner_radius=0,
                fg_color="transparent"
            )
            bloque.grid(
                row=0,
                column=columna,
                sticky="nsew",
                padx=16,
                pady=10
            )

            ctk.CTkLabel(
                bloque,
                text=titulo,
                font=ctk.CTkFont(family="Segoe UI", size=9),
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

        self.actualizar_resumen()

    #organiza la presentacion lateral y el area de conversacion
    def crear_contenido(self):
        cuerpo = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="transparent"
        )
        cuerpo.grid(row=1, column=0, sticky="nsew")
        cuerpo.grid_rowconfigure(0, weight=1)
        cuerpo.grid_columnconfigure(1, weight=1)

        self.crear_panel_farmi(cuerpo)
        self.crear_panel_chat(cuerpo)

    #crea la tarjeta de identidad y las consultas sugeridas
    def crear_panel_farmi(self, master):
        panel = ctk.CTkFrame(
            master,
            width=300,
            corner_radius=12,
            fg_color=COLOR_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )
        panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 6)
        )
        panel.grid_propagate(False)
        panel.grid_columnconfigure(0, weight=1)

        self.etiqueta_imagen_farmi = ctk.CTkLabel(
            panel,
            text="FARMI" if self.imagenes["presentacion"] is None else "",
            image=self.imagenes["presentacion"],
            font=ctk.CTkFont(
                family="Segoe UI",
                size=24,
                weight="bold"
            ),
            text_color=COLOR_PRIMARIO
        )
        self.etiqueta_imagen_farmi.grid(
            row=0,
            column=0,
            pady=(18, 4)
        )

        ctk.CTkLabel(
            panel,
            text="FARMI",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=20,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).grid(row=1, column=0)

        self.etiqueta_estado_farmi = ctk.CTkLabel(
            panel,
            text="Asistente local activo",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=COLOR_PRIMARIO
        )
        self.etiqueta_estado_farmi.grid(
            row=2,
            column=0,
            pady=(2, 16)
        )

        ctk.CTkLabel(
            panel,
            text="CONSULTAS RÁPIDAS",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=9,
                weight="bold"
            ),
            text_color=COLOR_TEXTO_SUAVE
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=18,
            pady=(4, 8)
        )

        sugerencias = [
            "Resumen general",
            "Stock bajo",
            "Medicamentos vencidos",
            "Próximos a vencer",
            "Pedidos pendientes",
            "Resumen de ventas",
            "¿Qué puedes hacer?"
        ]

        for fila, sugerencia in enumerate(sugerencias, start=4):
            ctk.CTkButton(
                panel,
                height=36,
                corner_radius=8,
                anchor="w",
                text=sugerencia,
                fg_color=COLOR_FILA,
                hover_color=COLOR_SELECCION,
                text_color=COLOR_TEXTO,
                font=ctk.CTkFont(family="Segoe UI", size=10),
                command=lambda texto=sugerencia: self.enviar_sugerencia(texto)
            ).grid(
                row=fila,
                column=0,
                sticky="ew",
                padx=14,
                pady=3
            )

        panel.grid_rowconfigure(11, weight=1)

        ctk.CTkLabel(
            panel,
            text="Consulta segura y de solo lectura\nDatos obtenidos desde CSV",
            font=ctk.CTkFont(family="Segoe UI", size=8),
            text_color=COLOR_TEXTO_SUAVE,
            justify="center"
        ).grid(
            row=12,
            column=0,
            pady=(10, 16)
        )

    #crea la conversacion y el campo para escribir
    def crear_panel_chat(self, master):
        panel = ctk.CTkFrame(
            master,
            corner_radius=12,
            fg_color=COLOR_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )
        panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(6, 0)
        )
        panel.grid_rowconfigure(1, weight=1)
        panel.grid_columnconfigure(0, weight=1)

        encabezado = ctk.CTkFrame(
            panel,
            height=58,
            corner_radius=0,
            fg_color="transparent"
        )
        encabezado.grid(row=0, column=0, sticky="ew")
        encabezado.grid_propagate(False)
        encabezado.grid_columnconfigure(0, weight=1)

        textos = ctk.CTkFrame(
            encabezado,
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
            text="Conversación con FARMI",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=15,
                weight="bold"
            ),
            text_color=COLOR_TEXTO
        ).pack(anchor="w")

        ctk.CTkLabel(
            textos,
            text="Consultas sobre el estado actual de FarmaSafe",
            font=ctk.CTkFont(family="Segoe UI", size=9),
            text_color=COLOR_TEXTO_SUAVE
        ).pack(anchor="w")

        ctk.CTkButton(
            encabezado,
            width=105,
            height=32,
            corner_radius=8,
            text="Limpiar chat",
            fg_color=COLOR_PANEL,
            hover_color=COLOR_SELECCION,
            border_width=1,
            border_color=COLOR_BORDE,
            text_color=COLOR_TEXTO,
            font=ctk.CTkFont(family="Segoe UI", size=10),
            command=self.limpiar_chat
        ).grid(
            row=0,
            column=1,
            padx=16,
            pady=12
        )

        self.area_chat = ctk.CTkScrollableFrame(
            panel,
            corner_radius=10,
            fg_color=COLOR_FILA,
            scrollbar_button_color=COLOR_SECUNDARIO,
            scrollbar_button_hover_color=COLOR_PRIMARIO
        )
        self.area_chat.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=14,
            pady=(0, 10)
        )
        self.area_chat.grid_columnconfigure(0, weight=1)

        entrada_marco = ctk.CTkFrame(
            panel,
            height=62,
            corner_radius=0,
            fg_color="transparent"
        )
        entrada_marco.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=14,
            pady=(0, 12)
        )
        entrada_marco.grid_columnconfigure(0, weight=1)

        self.entrada_mensaje = ctk.CTkEntry(
            entrada_marco,
            height=42,
            corner_radius=10,
            placeholder_text=(
                "Ejemplo: buscar paracetamol o mostrar stock bajo"
            ),
            textvariable=self.variable_mensaje,
            fg_color=COLOR_PANEL,
            border_color=COLOR_BORDE,
            text_color=COLOR_TEXTO,
            font=ctk.CTkFont(family="Segoe UI", size=11)
        )
        self.entrada_mensaje.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 8)
        )
        self.entrada_mensaje.bind(
            "<Return>",
            lambda evento: self.enviar_mensaje()
        )

        ctk.CTkButton(
            entrada_marco,
            width=125,
            height=42,
            corner_radius=10,
            text="Enviar",
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_SECUNDARIO,
            text_color="#FFFFFF",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=11,
                weight="bold"
            ),
            command=self.enviar_mensaje
        ).grid(row=0, column=1)

        self.entrada_mensaje.focus_set()

    #envia el texto escrito y agrega la respuesta obtenida
    def enviar_mensaje(self):
        mensaje = self.variable_mensaje.get().strip()

        if not mensaje:
            return

        self.variable_mensaje.set("")
        self.agregar_mensaje_usuario(mensaje)
        respuesta = self.motor.responder(mensaje)
        self.agregar_mensaje_farmi(
            respuesta["texto"],
            respuesta["emocion"],
            respuesta["titulo"]
        )
        self.actualizar_resumen()
        self.entrada_mensaje.focus_set()

    #envia una consulta elegida desde el panel lateral
    def enviar_sugerencia(self, texto):
        self.variable_mensaje.set(texto)
        self.enviar_mensaje()

    #agrega una burbuja alineada a la derecha
    def agregar_mensaje_usuario(self, texto):
        fila = ctk.CTkFrame(
            self.area_chat,
            corner_radius=0,
            fg_color="transparent"
        )
        fila.grid(sticky="ew", padx=8, pady=5)
        fila.grid_columnconfigure(0, weight=1)

        burbuja = ctk.CTkFrame(
            fila,
            corner_radius=12,
            fg_color=COLOR_PRIMARIO
        )
        burbuja.grid(row=0, column=1, sticky="e")

        ctk.CTkLabel(
            burbuja,
            text="Tú",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=9,
                weight="bold"
            ),
            text_color="#DDF5EE"
        ).pack(anchor="e", padx=14, pady=(8, 0))

        ctk.CTkLabel(
            burbuja,
            text=texto,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#FFFFFF",
            wraplength=560,
            justify="left"
        ).pack(anchor="w", padx=14, pady=(2, 9))

        self.desplazar_chat()

    #agrega una respuesta con la expresion correspondiente
    def agregar_mensaje_farmi(self, texto, emocion, titulo):
        fila = ctk.CTkFrame(
            self.area_chat,
            corner_radius=0,
            fg_color="transparent"
        )
        fila.grid(sticky="ew", padx=8, pady=5)
        fila.grid_columnconfigure(1, weight=1)

        #evita colocar la ilustracion completa dentro de una burbuja pequena
        emocion_imagen = "normal" if emocion == "presentacion" else emocion
        imagen = (
            self.imagenes.get(emocion_imagen)
            or self.imagenes.get("normal")
        )
        ctk.CTkLabel(
            fila,
            width=58,
            height=58,
            text="F" if imagen is None else "",
            image=imagen,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=18,
                weight="bold"
            ),
            text_color=COLOR_PRIMARIO,
            fg_color=COLOR_PANEL,
            corner_radius=29
        ).grid(
            row=0,
            column=0,
            sticky="nw",
            padx=(0, 8)
        )

        burbuja = ctk.CTkFrame(
            fila,
            corner_radius=12,
            fg_color=COLOR_PANEL,
            border_width=1,
            border_color=self.color_emocion(emocion)
        )
        burbuja.grid(row=0, column=1, sticky="w")

        ctk.CTkLabel(
            burbuja,
            text=titulo,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10,
                weight="bold"
            ),
            text_color=self.color_emocion(emocion)
        ).pack(anchor="w", padx=14, pady=(9, 0))

        ctk.CTkLabel(
            burbuja,
            text=texto,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=COLOR_TEXTO,
            wraplength=690,
            justify="left"
        ).pack(anchor="w", padx=14, pady=(4, 10))

        self.cambiar_expresion(emocion)
        self.desplazar_chat()

    #actualiza la imagen principal segun el resultado
    def cambiar_expresion(self, emocion):
        imagen = self.imagenes.get(emocion) or self.imagenes.get("normal")
        self.etiqueta_imagen_farmi.configure(
            image=imagen,
            text="FARMI" if imagen is None else ""
        )

        estados = {
            "normal": "Listo para consultar",
            "presentacion": "Asistente local activo",
            "exito": "Información verificada",
            "advertencia": "Situación que requiere atención",
            "peligro": "Alerta preventiva detectada"
        }
        self.etiqueta_estado_farmi.configure(
            text=estados.get(emocion, "Asistente local activo"),
            text_color=self.color_emocion(emocion)
        )

    #devuelve el color relacionado con cada expresion
    @staticmethod
    def color_emocion(emocion):
        colores = {
            "normal": COLOR_AZUL,
            "presentacion": COLOR_PRIMARIO,
            "exito": COLOR_PRIMARIO,
            "advertencia": COLOR_ADVERTENCIA,
            "peligro": COLOR_PELIGRO
        }
        return colores.get(emocion, COLOR_PRIMARIO)

    #lleva la conversacion hasta el mensaje mas reciente
    def desplazar_chat(self):
        def mover():
            canvas = getattr(self.area_chat, "_parent_canvas", None)

            if canvas is not None:
                canvas.yview_moveto(1.0)

        self.after(30, mover)

    #reinicia la conversacion sin modificar los datos
    def limpiar_chat(self):
        for componente in self.area_chat.winfo_children():
            componente.destroy()

        self.agregar_mensaje_farmi(
            "La conversación se limpió. ¿Qué deseas consultar ahora?",
            "normal",
            "Nueva conversación"
        )

    #refresca los indicadores usando los gestores actuales
    def actualizar_resumen(self):
        inventario = self.gestor_inventario.obtener_resumen()
        pedidos = self.gestor_pedidos.obtener_resumen()
        ventas = self.gestor_ventas.obtener_resumen()
        alertas = (
            inventario.get("stock_bajo", 0)
            + inventario.get("vencidos", 0)
            + inventario.get("proximos", 0)
        )

        self.etiquetas_resumen["medicamentos"].configure(
            text=str(inventario.get("total", 0))
        )
        self.etiquetas_resumen["alertas"].configure(text=str(alertas))
        self.etiquetas_resumen["pedidos"].configure(
            text=str(pedidos.get("pendientes", 0))
        )
        self.etiquetas_resumen["ventas"].configure(
            text=str(ventas.get("cantidad_ventas", 0))
        )