#bibliotecas para guardar los productos y la fecha de venta
import json
from datetime import datetime


#guarda los productos y el total de cada venta
class Venta:
    FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"

    def __init__(
        self,
        codigo_venta,
        cliente="Consumidor final",
        fecha_venta=None,
        productos=None
    ):
        self.codigo_venta = int(codigo_venta)
        self.cliente = str(cliente).strip()
        self.fecha_venta = self._convertir_fecha(fecha_venta)
        self.productos = list(productos) if productos else []
        self.total = 0.0

        self._validar_datos()
        self._calcular_total()

    #convierte la fecha para guardarla en el historial
    @staticmethod
    def _convertir_fecha(fecha):
        if fecha is None:
            return datetime.now()

        if isinstance(fecha, datetime):
            return fecha

        try:
            return datetime.strptime(
                str(fecha),
                Venta.FORMATO_FECHA
            )
        except ValueError as error:
            raise ValueError(
                "La fecha debe tener el formato AAAA-MM-DD HH:MM:SS."
            ) from error

    #evita crear ventas con datos incorrectos
    def _validar_datos(self):
        if self.codigo_venta <= 0:
            raise ValueError(
                "El código de la venta debe ser mayor que cero."
            )

        if not self.cliente:
            raise ValueError("El nombre del cliente es obligatorio.")

    #agrega un medicamento a la canasta de venta
    def agregar_producto(
        self,
        codigo_medicamento,
        nombre_medicamento,
        cantidad,
        precio_unitario
    ):
        codigo_medicamento = int(codigo_medicamento)
        nombre_medicamento = str(nombre_medicamento).strip()
        cantidad = int(cantidad)
        precio_unitario = float(precio_unitario)

        if codigo_medicamento <= 0:
            raise ValueError(
                "El código del medicamento debe ser mayor que cero."
            )

        if not nombre_medicamento:
            raise ValueError(
                "El nombre del medicamento es obligatorio."
            )

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        if precio_unitario <= 0:
            raise ValueError(
                "El precio unitario debe ser mayor que cero."
            )

        #aumenta la cantidad cuando el producto ya esta en la canasta
        for producto in self.productos:
            if producto["CodigoMedicamento"] == codigo_medicamento:
                producto["Cantidad"] += cantidad
                producto["Subtotal"] = round(
                    producto["Cantidad"]
                    * producto["PrecioUnitario"],
                    2
                )
                self._calcular_total()
                return

        subtotal = round(cantidad * precio_unitario, 2)

        self.productos.append({
            "CodigoMedicamento": codigo_medicamento,
            "NombreMedicamento": nombre_medicamento,
            "Cantidad": cantidad,
            "PrecioUnitario": precio_unitario,
            "Subtotal": subtotal
        })

        self._calcular_total()

    #retira un medicamento de la canasta
    def eliminar_producto(self, codigo_medicamento):
        codigo_medicamento = int(codigo_medicamento)

        for posicion, producto in enumerate(self.productos):
            if producto["CodigoMedicamento"] == codigo_medicamento:
                self.productos.pop(posicion)
                self._calcular_total()
                return True

        return False

    #suma los subtotales para obtener el valor de la venta
    def _calcular_total(self):
        total = 0.0

        for producto in self.productos:
            total += float(producto["Subtotal"])

        self.total = round(total, 2)

    #revisa si todavia no se agregaron productos
    def esta_vacia(self):
        return len(self.productos) == 0

    #cuenta todas las unidades agregadas a la venta
    def cantidad_unidades(self):
        cantidad = 0

        for producto in self.productos:
            cantidad += int(producto["Cantidad"])

        return cantidad

    #prepara la venta para guardarla en el archivo csv
    def a_diccionario(self):
        return {
            "CodigoVenta": self.codigo_venta,
            "Cliente": self.cliente,
            "FechaVenta": self.fecha_venta.strftime(
                self.FORMATO_FECHA
            ),
            "Productos": json.dumps(
                self.productos,
                ensure_ascii=False
            ),
            "Total": self.total
        }

    #crea una venta con los datos leidos del archivo csv
    @classmethod
    def desde_diccionario(cls, datos):
        productos = datos.get("Productos", [])

        if isinstance(productos, str):
            productos = json.loads(productos) if productos else []

        return cls(
            codigo_venta=datos["CodigoVenta"],
            cliente=datos["Cliente"],
            fecha_venta=datos["FechaVenta"],
            productos=productos
        )

    #muestra un resumen de la venta realizada
    def __str__(self):
        return (
            f"Venta {self.codigo_venta} | "
            f"{self.cliente} | "
            f"Unidades: {self.cantidad_unidades()} | "
            f"Total: ${self.total:.2f}"
        )