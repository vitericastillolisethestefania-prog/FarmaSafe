#conecta los pedidos con la cola y los archivos
from modelos.pedido import Pedido
from estructuras.cola_pedidos import ColaPedidos
from servicios.gestor_datos import GestorDatos
from utilidades.validaciones import validar_datos_pedido


#controla la cola y el historial de pedidos
class GestorPedidos:
    def __init__(self):
        self.cola = ColaPedidos()
        self.historial = []
        self.errores_carga = []

        GestorDatos.inicializar_archivos()
        self.cargar_desde_archivo()

    #recupera los pedidos guardados al iniciar el sistema
    def cargar_desde_archivo(self):
        self.cola = ColaPedidos()
        self.historial = []
        self.errores_carga = []

        registros = GestorDatos.leer_pedidos()

        for numero_fila, registro in enumerate(
            registros,
            start=2
        ):
            try:
                pedido = Pedido.desde_diccionario(
                    registro
                )

                if self.buscar_pedido(
                    pedido.codigo_pedido
                ) is not None:
                    self.errores_carga.append(
                        f"Fila {numero_fila}: código repetido."
                    )
                    continue

                self.historial.append(pedido)

                if pedido.esta_pendiente():
                    self.cola.encolar(pedido)

            except (
                ValueError,
                TypeError,
                KeyError
            ) as error:
                self.errores_carga.append(
                    f"Fila {numero_fila}: {error}"
                )

    #guarda todos los pedidos y sus estados
    def guardar_pedidos(self):
        GestorDatos.guardar_pedidos(
            self.historial
        )

    #busca un pedido dentro del historial
    def buscar_pedido(self, codigo_pedido):
        codigo_pedido = int(codigo_pedido)

        for pedido in self.historial:
            if pedido.codigo_pedido == codigo_pedido:
                return pedido

        return None

    #obtiene el siguiente codigo disponible
    def obtener_siguiente_codigo(self):
        siguiente_codigo = 1

        for pedido in self.historial:
            if pedido.codigo_pedido >= siguiente_codigo:
                siguiente_codigo = (
                    pedido.codigo_pedido + 1
                )

        return siguiente_codigo

    #crea un pedido y lo coloca al final de la cola
    def crear_pedido(self, datos):
        datos_validos = validar_datos_pedido(
            datos
        )

        if self.buscar_pedido(
            datos_validos["codigo_pedido"]
        ) is not None:
            raise ValueError(
                "Ya existe un pedido con ese código."
            )

        pedido = Pedido(**datos_validos)

        self.historial.append(pedido)
        self.cola.encolar(pedido)
        self.guardar_pedidos()

        return pedido

    #atiende el primer pedido y revisa el medicamento
    def atender_siguiente(self, gestor_inventario):
        pedido = self.cola.desencolar()

        if pedido is None:
            raise ValueError(
                "No existen pedidos pendientes."
            )

        medicamento = gestor_inventario.buscar_por_codigo(
            pedido.codigo_medicamento
        )

        if medicamento is None:
            pedido.marcar_rechazado()
            self.guardar_pedidos()

            return {
                "pedido": pedido,
                "exito": False,
                "mensaje": (
                    "El medicamento solicitado no existe."
                )
            }

        if medicamento.esta_vencido():
            pedido.marcar_rechazado()
            self.guardar_pedidos()

            return {
                "pedido": pedido,
                "exito": False,
                "mensaje": (
                    "El pedido fue rechazado porque "
                    "el medicamento está vencido."
                )
            }

        if pedido.cantidad > medicamento.stock:
            pedido.marcar_rechazado()
            self.guardar_pedidos()

            return {
                "pedido": pedido,
                "exito": False,
                "mensaje": (
                    "El pedido fue rechazado por falta de stock."
                )
            }

        gestor_inventario.retirar_stock(
            pedido.codigo_medicamento,
            pedido.cantidad
        )

        pedido.marcar_atendido()
        self.guardar_pedidos()

        return {
            "pedido": pedido,
            "exito": True,
            "mensaje": "El pedido fue atendido correctamente."
        }

    #devuelve los pedidos que todavia esperan atencion
    def obtener_pendientes(self):
        return self.cola.obtener_pedidos()

    #devuelve todos los pedidos registrados
    def obtener_historial(self):
        return list(self.historial)

    #cuenta los pedidos segun su estado
    def obtener_resumen(self):
        pendientes = 0
        atendidos = 0
        rechazados = 0

        for pedido in self.historial:
            if pedido.estado == "PENDIENTE":
                pendientes += 1
            elif pedido.estado == "ATENDIDO":
                atendidos += 1
            elif pedido.estado == "RECHAZADO":
                rechazados += 1

        return {
            "total": len(self.historial),
            "pendientes": pendientes,
            "atendidos": atendidos,
            "rechazados": rechazados
        }