#biblioteca para medir el tiempo de las busquedas
from time import perf_counter


#obtiene el dato que se utilizara durante la busqueda
def _obtener_valor(elemento, atributo):
    if not hasattr(elemento, atributo):
        raise ValueError(
            f"El atributo '{atributo}' no existe."
        )

    valor = getattr(elemento, atributo)

    if isinstance(valor, str):
        return valor.strip().lower()

    return valor


#prepara el valor escrito para poder compararlo
def _normalizar_valor(valor):
    if isinstance(valor, str):
        return valor.strip().lower()

    return valor


#busca revisando los datos uno por uno
def busqueda_lineal(
    datos,
    valor_buscado,
    atributo="codigo"
):
    valor_buscado = _normalizar_valor(valor_buscado)
    comparaciones = 0
    posicion_encontrada = -1
    resultado = None

    inicio = perf_counter()

    for posicion in range(len(datos)):
        valor_actual = _obtener_valor(
            datos[posicion],
            atributo
        )

        comparaciones += 1

        if valor_actual == valor_buscado:
            posicion_encontrada = posicion
            resultado = datos[posicion]
            break

    fin = perf_counter()
    tiempo_ms = (fin - inicio) * 1000

    return {
        "algoritmo": "Búsqueda lineal",
        "resultado": resultado,
        "posicion": posicion_encontrada,
        "tiempo_ms": tiempo_ms,
        "comparaciones": comparaciones
    }


#busca descartando la mitad de los datos en cada paso
def busqueda_binaria(
    datos_ordenados,
    valor_buscado,
    atributo="codigo",
    ascendente=True
):
    valor_buscado = _normalizar_valor(valor_buscado)
    izquierda = 0
    derecha = len(datos_ordenados) - 1
    comparaciones = 0
    posicion_encontrada = -1
    resultado = None

    inicio = perf_counter()

    while izquierda <= derecha:
        centro = (izquierda + derecha) // 2

        valor_central = _obtener_valor(
            datos_ordenados[centro],
            atributo
        )

        comparaciones += 1

        if valor_central == valor_buscado:
            posicion_encontrada = centro
            resultado = datos_ordenados[centro]
            break

        if ascendente:
            if valor_buscado < valor_central:
                derecha = centro - 1
            else:
                izquierda = centro + 1
        else:
            if valor_buscado > valor_central:
                derecha = centro - 1
            else:
                izquierda = centro + 1

    fin = perf_counter()
    tiempo_ms = (fin - inicio) * 1000

    return {
        "algoritmo": "Búsqueda binaria",
        "resultado": resultado,
        "posicion": posicion_encontrada,
        "tiempo_ms": tiempo_ms,
        "comparaciones": comparaciones
    }


#ejecuta las dos busquedas para comparar sus resultados
def comparar_busquedas(
    datos_originales,
    datos_ordenados,
    valor_buscado,
    atributo="codigo"
):
    resultado_lineal = busqueda_lineal(
        datos_originales,
        valor_buscado,
        atributo
    )

    resultado_binario = busqueda_binaria(
        datos_ordenados,
        valor_buscado,
        atributo
    )

    return {
        "lineal": resultado_lineal,
        "binaria": resultado_binario
    }