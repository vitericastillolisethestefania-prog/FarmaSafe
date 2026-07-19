import tkinter as tk
from pathlib import Path

import customtkinter as ctk
from PIL import Image, ImageTk


#ubica las carpetas donde se guardan las imagenes del proyecto
CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_INTERFAZ = CARPETA_PROYECTO / "imagenes" / "interfaz"
CARPETA_MEDICAMENTOS = CARPETA_PROYECTO / "imagenes" / "medicamentos"


#abre una imagen y calcula un tamano que conserve su proporcion
def preparar_imagen(ruta, ancho_maximo, alto_maximo):
    ruta = Path(ruta)

    if not ruta.exists():
        return None

    try:
        imagen = Image.open(ruta).convert("RGBA")
        imagen.thumbnail(
            (ancho_maximo, alto_maximo),
            Image.Resampling.LANCZOS
        )
        return imagen
    except (OSError, ValueError):
        return None


#carga una imagen para las ventanas que todavia usan tkinter
def cargar_imagen(ruta, ancho_maximo, alto_maximo):
    imagen = preparar_imagen(
        ruta,
        ancho_maximo,
        alto_maximo
    )

    if imagen is None:
        return None

    return ImageTk.PhotoImage(imagen)


#carga una imagen con escalado suave para customtkinter
def cargar_imagen_ctk(ruta, ancho_maximo, alto_maximo):
    imagen = preparar_imagen(
        ruta,
        ancho_maximo,
        alto_maximo
    )

    if imagen is None:
        return None

    return ctk.CTkImage(
        light_image=imagen,
        dark_image=imagen,
        size=imagen.size
    )


#busca las imagenes usadas en las ventanas y en el asistente
def cargar_imagen_interfaz(nombre, ancho_maximo, alto_maximo):
    ruta = CARPETA_INTERFAZ / nombre
    return cargar_imagen(
        ruta,
        ancho_maximo,
        alto_maximo
    )


#busca las imagenes de interfaz usadas por customtkinter
def cargar_imagen_interfaz_ctk(nombre, ancho_maximo, alto_maximo):
    ruta = CARPETA_INTERFAZ / nombre
    return cargar_imagen_ctk(
        ruta,
        ancho_maximo,
        alto_maximo
    )


#busca la imagen relacionada con cada medicamento
def cargar_imagen_medicamento(nombre, ancho_maximo, alto_maximo):
    ruta = CARPETA_MEDICAMENTOS / nombre
    return cargar_imagen(
        ruta,
        ancho_maximo,
        alto_maximo
    )


#busca la imagen de cada medicamento para customtkinter
def cargar_imagen_medicamento_ctk(nombre, ancho_maximo, alto_maximo):
    ruta = CARPETA_MEDICAMENTOS / nombre
    return cargar_imagen_ctk(
        ruta,
        ancho_maximo,
        alto_maximo
    )