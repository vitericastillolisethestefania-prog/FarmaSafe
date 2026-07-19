#biblioteca para guardar la fecha y hora del pedido
from datetime import datetime


#guarda la informacion de cada pedido que entrara en la cola
class Pedido:
    FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"
    ESTADOS_VALIDOS = ("PENDIENTE", "ATENDIDO", "RECHAZADO")

    def __init__(
        self,
        codigo_pedido,
        cliente,
        codigo_medicamento,
        nombre_medicamento,
        cantidad,
        fecha_registro=None,
        estado="PENDIENTE"
    ):
        self.codigo_pedido = int(codigo_pedido)
        self.cliente = str(cliente).strip()
        self.codigo_medicamento = int(codigo_medicamento)
        self.nombre_medicamento = str(nombre_medicamento).strip()
        self.cantidad = int(cantidad)
        self.fecha_registro = self._convertir_fecha(fecha_registro)
        self.estado = str(estado).strip().upper()

        self._validar_datos()

    #convierte la fecha para poder guardarla y mostrarla
    @staticmethod
    def _convertir_fecha(fecha):
        if fecha is None:
            return datetime.now()

        if isinstance(fecha, datetime):
            return fecha

        try:
            return datetime.strptime(
                str(fecha),
                Pedido.FORMATO_FECHA
            )
        except ValueError as error:
            raise ValueError(
                "La fecha debe tener el formato AAAA-MM-DD HH:MM:SS."
            ) from error

    #evita guardar pedidos con datos incorrectos
    def _validar_datos(self):
        if self.codigo_pedido <= 0:
            raise ValueError(
                "El código del pedido debe ser mayor que cero."
            )

        if not self.cliente:
            raise ValueError("El nombre del cliente es obligatorio.")

        if self.codigo_medicamento <= 0:
            raise ValueError(
                "El código del medicamento debe ser mayor que cero."
            )

        if not self.nombre_medicamento:
            raise ValueError(
                "El nombre del medicamento es obligatorio."
            )

        if self.cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        if self.estado not in self.ESTADOS_VALIDOS:
            raise ValueError("El estado del pedido no es válido.")

    #revisa si el pedido todavia espera ser atendido
    def esta_pendiente(self):
        return self.estado == "PENDIENTE"

    #cambia el estado cuando el pedido fue entregado
    def marcar_atendido(self):
        self.estado = "ATENDIDO"

    #cambia el estado cuando el pedido no puede completarse
    def marcar_rechazado(self):
        self.estado = "RECHAZADO"

    #prepara los datos para guardarlos en el archivo csv
    def a_diccionario(self):
        return {
            "CodigoPedido": self.codigo_pedido,
            "Cliente": self.cliente,
            "CodigoMedicamento": self.codigo_medicamento,
            "NombreMedicamento": self.nombre_medicamento,
            "Cantidad": self.cantidad,
            "FechaRegistro": self.fecha_registro.strftime(
                self.FORMATO_FECHA
            ),
            "Estado": self.estado
        }

    #crea un pedido con los datos leidos del archivo csv
    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            codigo_pedido=datos["CodigoPedido"],
            cliente=datos["Cliente"],
            codigo_medicamento=datos["CodigoMedicamento"],
            nombre_medicamento=datos["NombreMedicamento"],
            cantidad=datos["Cantidad"],
            fecha_registro=datos["FechaRegistro"],
            estado=datos["Estado"]
        )

    #muestra un resumen del pedido dentro de la cola
    def __str__(self):
        return (
            f"Pedido {self.codigo_pedido} | "
            f"{self.cliente} | "
            f"{self.nombre_medicamento} x{self.cantidad} | "
            f"{self.estado}"
        )