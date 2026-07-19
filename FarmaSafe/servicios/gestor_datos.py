#bibliotecas para trabajar con archivos csv
import csv
from pathlib import Path

#conecta el gestor con las rutas del proyecto
from config import (
    ARCHIVO_INVENTARIO,
    ARCHIVO_PEDIDOS,
    ARCHIVO_VENTAS
)


#columnas utilizadas por cada archivo
CAMPOS_INVENTARIO = [
    "Codigo",
    "Nombre",
    "Categoria",
    "Lote",
    "FechaVencimiento",
    "Stock",
    "StockMinimo",
    "Precio",
    "Imagen"
]

CAMPOS_PEDIDOS = [
    "CodigoPedido",
    "Cliente",
    "CodigoMedicamento",
    "NombreMedicamento",
    "Cantidad",
    "FechaRegistro",
    "Estado"
]

CAMPOS_VENTAS = [
    "CodigoVenta",
    "Cliente",
    "FechaVenta",
    "Productos",
    "Total"
]


#crea, lee y actualiza los archivos del sistema
class GestorDatos:
    #crea el archivo con sus columnas cuando esta vacio
    @staticmethod
    def _preparar_archivo(ruta, campos):
        ruta = Path(ruta)
        ruta.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not ruta.exists() or ruta.stat().st_size == 0:
            with open(
                ruta,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as archivo:
                escritor = csv.DictWriter(
                    archivo,
                    fieldnames=campos
                )
                escritor.writeheader()

    #lee todos los registros guardados en un archivo
    @classmethod
    def _leer_registros(cls, ruta, campos):
        cls._preparar_archivo(ruta, campos)
        registros = []

        with open(
            ruta,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as archivo:
            lector = csv.DictReader(archivo)

            for registro in lector:
                registros.append(registro)

        return registros

    #reemplaza el contenido sin dejar el archivo incompleto
    @classmethod
    def _guardar_registros(
        cls,
        ruta,
        campos,
        registros
    ):
        ruta = Path(ruta)
        ruta.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        archivo_temporal = ruta.with_suffix(".tmp")

        with open(
            archivo_temporal,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as archivo:
            escritor = csv.DictWriter(
                archivo,
                fieldnames=campos
            )

            escritor.writeheader()

            for registro in registros:
                escritor.writerow(registro)

        archivo_temporal.replace(ruta)

    #agrega un registro sin borrar los anteriores
    @classmethod
    def _agregar_registro(
        cls,
        ruta,
        campos,
        registro
    ):
        cls._preparar_archivo(ruta, campos)

        with open(
            ruta,
            "a",
            newline="",
            encoding="utf-8-sig"
        ) as archivo:
            escritor = csv.DictWriter(
                archivo,
                fieldnames=campos
            )

            escritor.writerow(registro)

    #crea los tres archivos al iniciar la aplicacion
    @classmethod
    def inicializar_archivos(cls):
        cls._preparar_archivo(
            ARCHIVO_INVENTARIO,
            CAMPOS_INVENTARIO
        )
        cls._preparar_archivo(
            ARCHIVO_PEDIDOS,
            CAMPOS_PEDIDOS
        )
        cls._preparar_archivo(
            ARCHIVO_VENTAS,
            CAMPOS_VENTAS
        )

    #lee los medicamentos guardados
    @classmethod
    def leer_inventario(cls):
        return cls._leer_registros(
            ARCHIVO_INVENTARIO,
            CAMPOS_INVENTARIO
        )

    #guarda el estado completo del inventario
    @classmethod
    def guardar_inventario(cls, medicamentos):
        registros = []

        for medicamento in medicamentos:
            registros.append(
                medicamento.a_diccionario()
            )

        cls._guardar_registros(
            ARCHIVO_INVENTARIO,
            CAMPOS_INVENTARIO,
            registros
        )

    #lee los pedidos guardados
    @classmethod
    def leer_pedidos(cls):
        return cls._leer_registros(
            ARCHIVO_PEDIDOS,
            CAMPOS_PEDIDOS
        )

    #guarda el estado actual de los pedidos
    @classmethod
    def guardar_pedidos(cls, pedidos):
        registros = []

        for pedido in pedidos:
            registros.append(
                pedido.a_diccionario()
            )

        cls._guardar_registros(
            ARCHIVO_PEDIDOS,
            CAMPOS_PEDIDOS,
            registros
        )

    #lee las ventas realizadas
    @classmethod
    def leer_ventas(cls):
        return cls._leer_registros(
            ARCHIVO_VENTAS,
            CAMPOS_VENTAS
        )

    #guarda nuevamente el historial de ventas
    @classmethod
    def guardar_ventas(cls, ventas):
        registros = []

        for venta in ventas:
            registros.append(
                venta.a_diccionario()
            )

        cls._guardar_registros(
            ARCHIVO_VENTAS,
            CAMPOS_VENTAS,
            registros
        )

    #agrega una venta nueva al historial
    @classmethod
    def agregar_venta(cls, venta):
        cls._agregar_registro(
            ARCHIVO_VENTAS,
            CAMPOS_VENTAS,
            venta.a_diccionario()
        )