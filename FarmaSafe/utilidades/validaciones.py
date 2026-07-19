#bibliotecas para revisar fechas y archivos
from datetime import datetime
from pathlib import Path


#revisa que un campo de texto no se encuentre vacio
def validar_texto(valor, nombre_campo):
    texto = str(valor).strip()

    if not texto:
        raise ValueError(
            f"El campo {nombre_campo} es obligatorio."
        )

    return texto


#convierte un campo a numero entero y revisa su limite
def validar_entero(
    valor,
    nombre_campo,
    minimo=0
):
    if str(valor).strip() == "":
        raise ValueError(
            f"El campo {nombre_campo} es obligatorio."
        )

    try:
        numero = int(valor)
    except ValueError as error:
        raise ValueError(
            f"El campo {nombre_campo} debe ser un número entero."
        ) from error

    if numero < minimo:
        raise ValueError(
            f"El campo {nombre_campo} debe ser mayor o igual a {minimo}."
        )

    return numero


#convierte un campo a decimal y acepta punto o coma
def validar_decimal(
    valor,
    nombre_campo,
    minimo=0.0
):
    texto = str(valor).strip().replace(",", ".")

    if not texto:
        raise ValueError(
            f"El campo {nombre_campo} es obligatorio."
        )

    try:
        numero = float(texto)
    except ValueError as error:
        raise ValueError(
            f"El campo {nombre_campo} debe ser numérico."
        ) from error

    if numero < minimo:
        raise ValueError(
            f"El campo {nombre_campo} debe ser mayor o igual a {minimo}."
        )

    return numero


#revisa que la fecha tenga el formato utilizado por el sistema
def validar_fecha(valor):
    texto = str(valor).strip()

    if not texto:
        raise ValueError(
            "La fecha de vencimiento es obligatoria."
        )

    try:
        fecha = datetime.strptime(
            texto,
            "%Y-%m-%d"
        ).date()
    except ValueError as error:
        raise ValueError(
            "La fecha debe tener el formato AAAA-MM-DD."
        ) from error

    return fecha


#revisa que el archivo seleccionado sea una imagen
def validar_imagen(ruta):
    if not ruta:
        return ""

    archivo = Path(ruta)

    extensiones_validas = (
        ".png",
        ".jpg",
        ".jpeg",
        ".webp"
    )

    if archivo.suffix.lower() not in extensiones_validas:
        raise ValueError(
            "El archivo seleccionado no es una imagen válida."
        )

    if not archivo.exists():
        raise ValueError(
            "La imagen seleccionada no existe."
        )

    return str(archivo)


#revisa todos los campos antes de crear el medicamento
def validar_datos_medicamento(datos):
    return {
        "codigo": validar_entero(
            datos.get("codigo", ""),
            "código",
            1
        ),
        "nombre": validar_texto(
            datos.get("nombre", ""),
            "nombre"
        ),
        "categoria": validar_texto(
            datos.get("categoria", ""),
            "categoría"
        ),
        "lote": validar_texto(
            datos.get("lote", ""),
            "lote"
        ),
        "fecha_vencimiento": validar_fecha(
            datos.get("fecha_vencimiento", "")
        ),
        "stock": validar_entero(
            datos.get("stock", ""),
            "stock",
            0
        ),
        "stock_minimo": validar_entero(
            datos.get("stock_minimo", ""),
            "stock mínimo",
            0
        ),
        "precio": validar_decimal(
            datos.get("precio", ""),
            "precio",
            0.01
        ),
        "imagen": validar_imagen(
            datos.get("imagen", "")
        )
    }


#revisa los campos utilizados para crear un pedido
def validar_datos_pedido(datos):
    return {
        "codigo_pedido": validar_entero(
            datos.get("codigo_pedido", ""),
            "código del pedido",
            1
        ),
        "cliente": validar_texto(
            datos.get("cliente", ""),
            "cliente"
        ),
        "codigo_medicamento": validar_entero(
            datos.get("codigo_medicamento", ""),
            "código del medicamento",
            1
        ),
        "nombre_medicamento": validar_texto(
            datos.get("nombre_medicamento", ""),
            "medicamento"
        ),
        "cantidad": validar_entero(
            datos.get("cantidad", ""),
            "cantidad",
            1
        )
    }