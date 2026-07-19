#biblioteca para medir el tiempo de los ordenamientos
from time import perf_counter


#obtiene el dato que se utilizara para ordenar
def _obtener_valor(elemento, atributo):
    if not hasattr(elemento, atributo):
        raise ValueError(
            f"El atributo '{atributo}' no existe."
        )

    valor = getattr(elemento, atributo)

    if isinstance(valor, str):
        return valor.lower()

    return valor


#ordena los datos comparando elementos cercanos
def ordenamiento_burbuja(
    datos,
    atributo="codigo",
    ascendente=True
):
    lista = list(datos)
    comparaciones = 0
    intercambios = 0

    inicio = perf_counter()
    cantidad = len(lista)

    for recorrido in range(cantidad - 1):
        hubo_cambio = False

        for posicion in range(cantidad - recorrido - 1):
            valor_actual = _obtener_valor(
                lista[posicion],
                atributo
            )
            valor_siguiente = _obtener_valor(
                lista[posicion + 1],
                atributo
            )

            comparaciones += 1

            if ascendente:
                debe_cambiar = valor_actual > valor_siguiente
            else:
                debe_cambiar = valor_actual < valor_siguiente

            if debe_cambiar:
                temporal = lista[posicion]
                lista[posicion] = lista[posicion + 1]
                lista[posicion + 1] = temporal

                intercambios += 1
                hubo_cambio = True

        #termina antes cuando la lista ya se encuentra ordenada
        if not hubo_cambio:
            break

    fin = perf_counter()
    tiempo_ms = (fin - inicio) * 1000

    return {
        "algoritmo": "BubbleSort",
        "lista": lista,
        "tiempo_ms": tiempo_ms,
        "comparaciones": comparaciones,
        "intercambios": intercambios
    }


#ordena los datos separandolos alrededor de un pivote
def ordenamiento_quick_sort(
    datos,
    atributo="codigo",
    ascendente=True
):
    lista = list(datos)
    comparaciones = 0
    intercambios = 0

    #intercambia dos posiciones y registra el movimiento realizado
    def intercambiar(posicion_a, posicion_b):
        nonlocal intercambios

        if posicion_a == posicion_b:
            return

        temporal = lista[posicion_a]
        lista[posicion_a] = lista[posicion_b]
        lista[posicion_b] = temporal
        intercambios += 1

    #separa valores menores, iguales y mayores que el pivote
    def separar(izquierda, derecha):
        nonlocal comparaciones

        pivote = _obtener_valor(
            lista[(izquierda + derecha) // 2],
            atributo
        )

        posicion_menor = izquierda
        posicion_actual = izquierda
        posicion_mayor = derecha

        while posicion_actual <= posicion_mayor:
            valor = _obtener_valor(
                lista[posicion_actual],
                atributo
            )

            comparaciones += 1

            if ascendente:
                corresponde_antes = valor < pivote
            else:
                corresponde_antes = valor > pivote

            if corresponde_antes:
                intercambiar(
                    posicion_menor,
                    posicion_actual
                )
                posicion_menor += 1
                posicion_actual += 1
                continue

            comparaciones += 1

            if ascendente:
                corresponde_despues = valor > pivote
            else:
                corresponde_despues = valor < pivote

            if corresponde_despues:
                intercambiar(
                    posicion_actual,
                    posicion_mayor
                )
                posicion_mayor -= 1
            else:
                posicion_actual += 1

        return posicion_menor, posicion_mayor

    #usa una pila para evitar superar el limite de recursion de Python
    def ordenar():
        if len(lista) < 2:
            return

        pendientes = [(0, len(lista) - 1)]

        while pendientes:
            izquierda, derecha = pendientes.pop()

            while izquierda < derecha:
                inicio_iguales, fin_iguales = separar(
                    izquierda,
                    derecha
                )

                izquierda_a = izquierda
                derecha_a = inicio_iguales - 1
                izquierda_b = fin_iguales + 1
                derecha_b = derecha

                cantidad_a = derecha_a - izquierda_a + 1
                cantidad_b = derecha_b - izquierda_b + 1

                #continua con el segmento pequeno y guarda el grande
                #para mantener tambien reducido el tamano de la pila
                if cantidad_a < cantidad_b:
                    if cantidad_b > 1:
                        pendientes.append((izquierda_b, derecha_b))

                    izquierda = izquierda_a
                    derecha = derecha_a
                else:
                    if cantidad_a > 1:
                        pendientes.append((izquierda_a, derecha_a))

                    izquierda = izquierda_b
                    derecha = derecha_b

    inicio = perf_counter()
    ordenar()
    fin = perf_counter()

    tiempo_ms = (fin - inicio) * 1000

    return {
        "algoritmo": "QuickSort",
        "lista": lista,
        "tiempo_ms": tiempo_ms,
        "comparaciones": comparaciones,
        "intercambios": intercambios
    }


#ejecuta los dos metodos con los mismos datos
def comparar_ordenamientos(
    datos,
    atributo="codigo",
    ascendente=True
):
    resultado_burbuja = ordenamiento_burbuja(
        datos,
        atributo,
        ascendente
    )

    resultado_quick = ordenamiento_quick_sort(
        datos,
        atributo,
        ascendente
    )

    return {
        "burbuja": resultado_burbuja,
        "quick_sort": resultado_quick
    }