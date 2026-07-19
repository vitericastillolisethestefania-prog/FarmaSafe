#biblioteca para crear rutas que funcionen desde cualquier carpeta
from pathlib import Path


#obtiene la ubicacion principal del proyecto
CARPETA_PROYECTO = Path(__file__).resolve().parent

CARPETA_DATOS = CARPETA_PROYECTO / "datos"
CARPETA_IMAGENES = CARPETA_PROYECTO / "imagenes"
CARPETA_MEDICAMENTOS = CARPETA_IMAGENES / "medicamentos"
CARPETA_IMAGENES_INTERFAZ = CARPETA_IMAGENES / "interfaz"


#guarda las rutas de los archivos utilizados por el sistema
ARCHIVO_INVENTARIO = CARPETA_DATOS / "inventario.csv"
ARCHIVO_PEDIDOS = CARPETA_DATOS / "pedidos.csv"
ARCHIVO_VENTAS = CARPETA_DATOS / "ventas.csv"

IMAGEN_PREDETERMINADA = (
    CARPETA_MEDICAMENTOS / "default.png"
)


#crea las carpetas cuando todavia no existen
CARPETA_DATOS.mkdir(
    parents=True,
    exist_ok=True
)

CARPETA_MEDICAMENTOS.mkdir(
    parents=True,
    exist_ok=True
)

CARPETA_IMAGENES_INTERFAZ.mkdir(
    parents=True,
    exist_ok=True
)


#valores utilizados por las funciones principales
CANTIDAD_CARGA_MASIVA = 1000
DIAS_ALERTA_VENCIMIENTO = 30


#datos generales de la aplicacion
NOMBRE_APLICACION = "FarmaSafe"
TAMANO_VENTANA = "1280x760"


#colores utilizados en las pantallas
COLOR_FONDO = "#07111f"
COLOR_MENU = "#0b172a"
COLOR_PANEL = "#111f33"
COLOR_PRIMARIO = "#20c997"
COLOR_SECUNDARIO = "#4f8cff"
COLOR_ADVERTENCIA = "#f6c453"
COLOR_PELIGRO = "#f05252"
COLOR_TEXTO = "#f8fafc"
COLOR_TEXTO_SUAVE = "#94a3b8"