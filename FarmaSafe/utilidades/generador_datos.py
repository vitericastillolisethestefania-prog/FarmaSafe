#bibliotecas para crear datos y fechas aleatorias
import random
from datetime import date, timedelta

#conecta el generador con el modelo de medicamento
from modelos.medicamento import Medicamento


#medicamentos utilizados para formar los registros aleatorios
MEDICAMENTOS_BASE = [
    ("Paracetamol 500mg", "Analgésico"),
    ("Ibuprofeno 400mg", "Analgésico"),
    ("Amoxicilina 500mg", "Antibiótico"),
    ("Loratadina 10mg", "Antihistamínico"),
    ("Omeprazol 20mg", "Gastrointestinal"),
    ("Diclofenaco 50mg", "Antiinflamatorio"),
    ("Azitromicina 500mg", "Antibiótico"),
    ("Losartán 50mg", "Antihipertensivo"),
    ("Metformina 850mg", "Antidiabético"),
    ("Cetirizina 10mg", "Antihistamínico"),
    ("Naproxeno 500mg", "Antiinflamatorio"),
    ("Enalapril 20mg", "Antihipertensivo"),
    ("Fluconazol 150mg", "Antifúngico"),
    ("Sertralina 50mg", "Antidepresivo"),
    ("Pantoprazol 40mg", "Gastrointestinal"),
    ("Ciprofloxacino 500mg", "Antibiótico"),
    ("Prednisona 20mg", "Corticoide"),
    ("Loperamida 2mg", "Antidiarreico"),
    ("Amlodipino 5mg", "Antihipertensivo"),
    ("Salbutamol Inhalador", "Respiratorio")
]


#lineas ficticias usadas solamente para diferenciar los datos de prueba
LINEAS_SIMULADAS = [
    "Aster",
    "Nova",
    "Vital",
    "Andina",
    "Nexa",
    "Prisma",
    "Aurora",
    "Cumbre",
    "Horizonte",
    "Central",
    "Verde",
    "Celeste",
    "Integral",
    "Forte",
    "Activa",
    "Esencial",
    "Balance",
    "Selecta",
    "Avanza",
    "Sol",
    "Luna",
    "Zenit",
    "Alba",
    "Norte",
    "Sur"
]


#forma un catalogo de 5000 nombres sinteticos diferentes
def _crear_catalogo_nombres():
    catalogo = []

    for nombre_base, categoria in MEDICAMENTOS_BASE:
        for linea in LINEAS_SIMULADAS:
            for serie in range(1, 11):
                nombre = (
                    f"{nombre_base} {linea} "
                    f"S{serie:02d}"
                )
                catalogo.append((nombre, categoria))

    return catalogo


#crea fechas vencidas, cercanas y vigentes para las alertas
def _generar_fecha_vencimiento(generador):
    dias = generador.randint(-180, 730)
    fecha_vencimiento = date.today() + timedelta(days=dias)

    return fecha_vencimiento.strftime(
        Medicamento.FORMATO_FECHA
    )


#cambia el orden de los registros antes de entregarlos
def _mezclar_registros(registros, generador):
    for posicion in range(len(registros) - 1, 0, -1):
        posicion_aleatoria = generador.randint(
            0,
            posicion
        )

        temporal = registros[posicion]
        registros[posicion] = registros[posicion_aleatoria]
        registros[posicion_aleatoria] = temporal


#crea la cantidad solicitada de medicamentos
def generar_medicamentos(
    cantidad=1000,
    codigo_inicial=1,
    semilla=None,
    nombres_existentes=None
):
    cantidad = int(cantidad)
    codigo_inicial = int(codigo_inicial)

    if cantidad <= 0:
        raise ValueError(
            "La cantidad debe ser mayor que cero."
        )

    if codigo_inicial <= 0:
        raise ValueError(
            "El código inicial debe ser mayor que cero."
        )

    generador = random.Random(semilla)
    medicamentos = []

    nombres_existentes = {
        str(nombre).strip().lower()
        for nombre in (nombres_existentes or [])
    }

    catalogo_disponible = [
        (nombre, categoria)
        for nombre, categoria in _crear_catalogo_nombres()
        if nombre.lower() not in nombres_existentes
    ]

    if cantidad > len(catalogo_disponible):
        raise ValueError(
            "No existen suficientes nombres únicos disponibles. "
            f"Puede generar hasta {len(catalogo_disponible)} "
            "registros adicionales."
        )

    _mezclar_registros(
        catalogo_disponible,
        generador
    )

    #combina nombres unicos, cantidades, precios y fechas
    for posicion in range(cantidad):
        nombre, categoria = catalogo_disponible[posicion]

        codigo = codigo_inicial + posicion
        lote = f"{nombre[:3].upper()}-{codigo:05d}"
        stock = generador.randint(0, 300)
        stock_minimo = generador.randint(10, 40)
        precio = round(
            generador.uniform(1.50, 35.00),
            2
        )

        medicamento = Medicamento(
            codigo=codigo,
            nombre=nombre,
            categoria=categoria,
            lote=lote,
            fecha_vencimiento=_generar_fecha_vencimiento(
                generador
            ),
            stock=stock,
            stock_minimo=stock_minimo,
            precio=precio,
            imagen="default.png"
        )

        medicamentos.append(medicamento)

    #deja los codigos desordenados para probar los algoritmos
    _mezclar_registros(
        medicamentos,
        generador
    )

    return medicamentos