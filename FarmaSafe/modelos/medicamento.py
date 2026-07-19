#biblioteca para trabajar con fechas
from datetime import date, datetime


#guarda la informacion y los controles de cada medicamento
class Medicamento:
    FORMATO_FECHA = "%Y-%m-%d"

    def __init__(
        self,
        codigo,
        nombre,
        categoria,
        lote,
        fecha_vencimiento,
        stock,
        stock_minimo,
        precio,
        imagen="default.png"
    ):
        self.codigo = int(codigo)
        self.nombre = str(nombre).strip()
        self.categoria = str(categoria).strip()
        self.lote = str(lote).strip().upper()
        self.fecha_vencimiento = self._convertir_fecha(fecha_vencimiento)
        self.stock = int(stock)
        self.stock_minimo = int(stock_minimo)
        self.precio = float(precio)
        self.imagen = imagen if imagen else "default.png"

        self._validar_datos()

    #convierte la fecha para poder revisar el vencimiento
    @staticmethod
    def _convertir_fecha(fecha):
        if isinstance(fecha, datetime):
            return fecha.date()

        if isinstance(fecha, date):
            return fecha

        try:
            return datetime.strptime(
                str(fecha),
                Medicamento.FORMATO_FECHA
            ).date()
        except ValueError as error:
            raise ValueError(
                "La fecha debe tener el formato AAAA-MM-DD."
            ) from error

    #evita guardar cantidades o datos incorrectos
    def _validar_datos(self):
        if self.codigo <= 0:
            raise ValueError("El código debe ser mayor que cero.")

        if not self.nombre:
            raise ValueError("El nombre del medicamento es obligatorio.")

        if not self.categoria:
            raise ValueError("La categoría es obligatoria.")

        if not self.lote:
            raise ValueError("El lote es obligatorio.")

        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo.")

        if self.stock_minimo < 0:
            raise ValueError("El stock mínimo no puede ser negativo.")

        if self.precio <= 0:
            raise ValueError("El precio debe ser mayor que cero.")

    #calcula los dias que faltan para el vencimiento
    def dias_para_vencer(self, fecha_actual=None):
        if fecha_actual is None:
            fecha_actual = date.today()

        return (self.fecha_vencimiento - fecha_actual).days

    #revisa si el medicamento ya se encuentra vencido
    def esta_vencido(self):
        return self.dias_para_vencer() < 0

    #revisa si el medicamento esta cerca de vencer
    def proximo_a_vencer(self, dias_alerta=30):
        dias = self.dias_para_vencer()
        return 0 <= dias <= dias_alerta

    #revisa si quedan pocas unidades disponibles
    def tiene_stock_bajo(self):
        return self.stock <= self.stock_minimo

    #aumenta las unidades cuando llega nuevo stock
    def aumentar_stock(self, cantidad):
        cantidad = int(cantidad)

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        self.stock += cantidad

    #descuenta las unidades vendidas del inventario
    def disminuir_stock(self, cantidad):
        cantidad = int(cantidad)

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        if cantidad > self.stock:
            raise ValueError("No existe stock suficiente.")

        self.stock -= cantidad

    #define el estado que se mostrara en las alertas
    def obtener_estado(self):
        if self.esta_vencido():
            return "VENCIDO"

        if self.stock == 0:
            return "SIN STOCK"

        if self.proximo_a_vencer():
            return "PRÓXIMO A VENCER"

        if self.tiene_stock_bajo():
            return "STOCK BAJO"

        return "NORMAL"

    #prepara los datos para guardarlos en el archivo csv
    def a_diccionario(self):
        return {
            "Codigo": self.codigo,
            "Nombre": self.nombre,
            "Categoria": self.categoria,
            "Lote": self.lote,
            "FechaVencimiento": self.fecha_vencimiento.strftime(
                self.FORMATO_FECHA
            ),
            "Stock": self.stock,
            "StockMinimo": self.stock_minimo,
            "Precio": self.precio,
            "Imagen": self.imagen
        }

    #crea un medicamento con los datos leidos del archivo csv
    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            codigo=datos["Codigo"],
            nombre=datos["Nombre"],
            categoria=datos["Categoria"],
            lote=datos["Lote"],
            fecha_vencimiento=datos["FechaVencimiento"],
            stock=datos["Stock"],
            stock_minimo=datos["StockMinimo"],
            precio=datos["Precio"],
            imagen=datos.get("Imagen", "default.png")
        )

    #muestra un resumen sencillo del medicamento
    def __str__(self):
        return (
            f"{self.codigo} - {self.nombre} | "
            f"Stock: {self.stock} | "
            f"Estado: {self.obtener_estado()}"
        )
        