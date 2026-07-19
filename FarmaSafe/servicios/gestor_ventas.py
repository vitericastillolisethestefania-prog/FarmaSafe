#biblioteca para identificar las ventas del dia
from datetime import date

#conecta las ventas con el archivo y el inventario
from modelos.venta import Venta
from servicios.gestor_datos import GestorDatos


#controla la canasta y el historial de ventas
class GestorVentas:
    def __init__(self):
        self.ventas = []
        self.errores_carga = []

        GestorDatos.inicializar_archivos()
        self.cargar_desde_archivo()

    #recupera las ventas guardadas al iniciar
    def cargar_desde_archivo(self):
        self.ventas = []
        self.errores_carga = []

        registros = GestorDatos.leer_ventas()

        for numero_fila, registro in enumerate(
            registros,
            start=2
        ):
            try:
                venta = Venta.desde_diccionario(
                    registro
                )

                if self.buscar_venta(
                    venta.codigo_venta
                ) is not None:
                    self.errores_carga.append(
                        f"Fila {numero_fila}: código repetido."
                    )
                    continue

                self.ventas.append(venta)

            except (
                ValueError,
                TypeError,
                KeyError
            ) as error:
                self.errores_carga.append(
                    f"Fila {numero_fila}: {error}"
                )

    #busca una venta por su codigo
    def buscar_venta(self, codigo_venta):
        codigo_venta = int(codigo_venta)

        for venta in self.ventas:
            if venta.codigo_venta == codigo_venta:
                return venta

        return None

    #obtiene el siguiente codigo disponible
    def obtener_siguiente_codigo(self):
        siguiente_codigo = 1

        for venta in self.ventas:
            if venta.codigo_venta >= siguiente_codigo:
                siguiente_codigo = venta.codigo_venta + 1

        return siguiente_codigo

    #crea una canasta nueva antes de realizar la venta
    def crear_venta(
        self,
        cliente="Consumidor final"
    ):
        return Venta(
            codigo_venta=self.obtener_siguiente_codigo(),
            cliente=cliente
        )

    #agrega un producto despues de revisar sus condiciones
    def agregar_producto(
        self,
        venta,
        gestor_inventario,
        codigo_medicamento,
        cantidad
    ):
        if not isinstance(venta, Venta):
            raise TypeError(
                "Se necesita una venta válida."
            )

        codigo_medicamento = int(
            codigo_medicamento
        )
        cantidad = int(cantidad)

        if cantidad <= 0:
            raise ValueError(
                "La cantidad debe ser mayor que cero."
            )

        medicamento = gestor_inventario.buscar_por_codigo(
            codigo_medicamento
        )

        if medicamento is None:
            raise ValueError(
                "El medicamento no existe."
            )

        if medicamento.esta_vencido():
            raise ValueError(
                "No se puede vender un medicamento vencido."
            )

        cantidad_actual = 0

        for producto in venta.productos:
            if (
                producto["CodigoMedicamento"]
                == codigo_medicamento
            ):
                cantidad_actual = producto["Cantidad"]
                break

        if cantidad_actual + cantidad > medicamento.stock:
            raise ValueError(
                "No existe stock suficiente para la venta."
            )

        venta.agregar_producto(
            codigo_medicamento=medicamento.codigo,
            nombre_medicamento=medicamento.nombre,
            cantidad=cantidad,
            precio_unitario=medicamento.precio
        )

        return venta

    #elimina un producto antes de confirmar la venta
    def eliminar_producto(
        self,
        venta,
        codigo_medicamento
    ):
        if not isinstance(venta, Venta):
            raise TypeError(
                "Se necesita una venta válida."
            )

        return venta.eliminar_producto(
            codigo_medicamento
        )

    #confirma la venta y descuenta las existencias
    def finalizar_venta(
        self,
        venta,
        gestor_inventario
    ):
        if not isinstance(venta, Venta):
            raise TypeError(
                "Se necesita una venta válida."
            )

        if venta.esta_vacia():
            raise ValueError(
                "No se puede finalizar una venta vacía."
            )

        if self.buscar_venta(
            venta.codigo_venta
        ) is not None:
            raise ValueError(
                "La venta ya fue registrada."
            )

        #revisa todos los productos antes de cambiar el stock
        for producto in venta.productos:
            medicamento = (
                gestor_inventario.buscar_por_codigo(
                    producto["CodigoMedicamento"]
                )
            )

            if medicamento is None:
                raise ValueError(
                    "Uno de los medicamentos ya no existe."
                )

            if medicamento.esta_vencido():
                raise ValueError(
                    f"{medicamento.nombre} está vencido."
                )

            if producto["Cantidad"] > medicamento.stock:
                raise ValueError(
                    f"No existe stock suficiente de "
                    f"{medicamento.nombre}."
                )

        #descuenta los productos despues de revisar la venta
        for producto in venta.productos:
            medicamento = (
                gestor_inventario.buscar_por_codigo(
                    producto["CodigoMedicamento"]
                )
            )

            cantidad = int(
                producto["Cantidad"]
            )

            medicamento.stock = (
                medicamento.stock - cantidad
            )

        gestor_inventario.guardar_inventario()

        self.ventas.append(venta)
        GestorDatos.agregar_venta(venta)

        return venta
    
        #registra como venta un pedido que ya fue atendido
    def registrar_pedido_atendido(
        self,
        pedido,
        gestor_inventario
    ):
        medicamento = (
            gestor_inventario.buscar_por_codigo(
                pedido.codigo_medicamento
            )
        )

        if medicamento is None:
            raise ValueError(
                "El medicamento del pedido ya no existe."
            )

        venta = self.crear_venta(
            cliente=pedido.cliente
        )

        venta.agregar_producto(
            codigo_medicamento=medicamento.codigo,
            nombre_medicamento=medicamento.nombre,
            cantidad=pedido.cantidad,
            precio_unitario=medicamento.precio
        )

        self.ventas.append(venta)
        GestorDatos.agregar_venta(venta)

        return venta

    #devuelve el historial completo de ventas
    def obtener_ventas(self):
        return list(self.ventas)

    #devuelve solamente las ventas realizadas hoy
    def obtener_ventas_hoy(self):
        ventas_hoy = []

        for venta in self.ventas:
            if venta.fecha_venta.date() == date.today():
                ventas_hoy.append(venta)

        return ventas_hoy

    #encuentra el producto con mas unidades vendidas
    def obtener_producto_mas_vendido(self):
        cantidades = {}

        for venta in self.ventas:
            for producto in venta.productos:
                codigo = producto["CodigoMedicamento"]

                if codigo not in cantidades:
                    cantidades[codigo] = {
                        "nombre": producto[
                            "NombreMedicamento"
                        ],
                        "cantidad": 0
                    }

                cantidades[codigo]["cantidad"] += producto[
                    "Cantidad"
                ]

        producto_mayor = None

        for producto in cantidades.values():
            if (
                producto_mayor is None
                or producto["cantidad"]
                > producto_mayor["cantidad"]
            ):
                producto_mayor = producto

        return producto_mayor

    #prepara los datos principales de las ventas
    def obtener_resumen(self):
        total_ingresos = 0.0
        total_unidades = 0

        for venta in self.ventas:
            total_ingresos += venta.total
            total_unidades += venta.cantidad_unidades()

        producto_mayor = (
            self.obtener_producto_mas_vendido()
        )

        return {
            "cantidad_ventas": len(self.ventas),
            "ingresos": round(total_ingresos, 2),
            "unidades": total_unidades,
            "ventas_hoy": len(
                self.obtener_ventas_hoy()
            ),
            "producto_mas_vendido": producto_mayor
        }