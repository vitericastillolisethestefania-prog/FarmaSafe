<p align="center">
  <img src="./FarmaSafe/imagenes/interfaz/logo_horizontal.png" alt="Logotipo de FarmaSafe" width="720">
</p>

<h1 align="center">FarmaSafe</h1>

<p align="center">
  <strong>Sistema preventivo de inventario, dispensación y control de ventas farmacéuticas</strong>
</p>

<p align="center">
  Control que previene, seguridad que protege.
</p>

---

## Descripción

FarmaSafe es una aplicación de escritorio desarrollada en Python para administrar el inventario, los pedidos y las ventas de una farmacia.

El sistema permite registrar medicamentos, controlar sus existencias, identificar productos vencidos o próximos a vencer, prevenir ventas sin stock, atender pedidos en orden de llegada y conservar un historial de las operaciones realizadas.

El proyecto integra estructuras de datos lineales y no lineales dentro de una interfaz gráfica construida con Tkinter y CustomTkinter.

## Problema identificado

Las farmacias pueden sufrir pérdidas y errores en el despacho cuando no controlan correctamente las fechas de vencimiento, las existencias disponibles, el orden de las solicitudes y el registro de las ventas.

FarmaSafe fue creado para organizar el inventario, detectar medicamentos vencidos o próximos a caducar, prevenir ventas sin stock, gestionar el flujo de pedidos y conservar un historial de las transacciones realizadas.

## Objetivo

Desarrollar una aplicación gráfica que permita administrar medicamentos, pedidos y ventas, aplicando estructuras de datos y algoritmos estudiados durante la asignatura Estructura de Datos.

## Funciones principales

- Registro, edición y eliminación de medicamentos.
- Búsqueda y filtrado del inventario.
- Identificación de medicamentos vencidos.
- Alertas de próximos vencimientos.
- Control de stock mínimo y productos agotados.
- Registro de ventas y actualización de existencias.
- Atención de pedidos en orden FIFO.
- Historial de pedidos atendidos, pendientes y rechazados.
- Registro de pedidos atendidos como ventas.
- Almacenamiento permanente mediante archivos CSV.
- Generación masiva de medicamentos ficticios.
- Comparación entre BubbleSort y QuickSort.
- Comparación entre búsqueda lineal y búsqueda binaria.
- Consultas locales mediante el asistente FARMI.

## Estructuras de datos utilizadas

### Árbol AVL

El inventario se organiza mediante un árbol AVL que utiliza el código del medicamento como clave.

Esta estructura permite:

- Insertar medicamentos.
- Buscar medicamentos por código.
- Eliminar registros.
- Obtener los medicamentos en orden ascendente.
- Mantener el árbol equilibrado durante las operaciones.

### Cola enlazada FIFO

Los pedidos se organizan mediante una cola enlazada que sigue el principio FIFO:

> First In, First Out: el primero en entrar es el primero en salir.

Cada pedido nuevo se agrega al final de la cola y la atención se realiza desde el frente.

## Algoritmos incorporados

### Ordenamiento

- BubbleSort.
- QuickSort.

La aplicación compara:

- Tiempo de ejecución.
- Número de comparaciones.
- Número de intercambios.
- Corrección de los resultados.

### Búsqueda

- Búsqueda lineal.
- Búsqueda binaria.

La búsqueda binaria se ejecuta sobre una copia ordenada previamente mediante QuickSort. El tiempo de preparación se presenta de forma separada.

## Asistente FARMI

FARMI es un asistente local basado en reglas que permite consultar información del sistema mediante mensajes sencillos.

Puede consultar:

- Resumen general.
- Medicamentos con stock bajo.
- Productos agotados.
- Medicamentos vencidos.
- Próximos vencimientos.
- Información por nombre o código.
- Pedidos pendientes.
- Resumen de ventas.
- Medicamentos por categoría.

FARMI no necesita conexión a internet, no utiliza servicios externos y no modifica directamente los archivos del sistema.

## Persistencia de los datos

FarmaSafe conserva la información mediante tres archivos CSV:

- `inventario.csv`
- `pedidos.csv`
- `ventas.csv`

Al iniciar la aplicación, los gestores recuperan los registros almacenados y reconstruyen:

- El árbol AVL del inventario.
- La cola de pedidos pendientes.
- El historial de pedidos.
- El historial de ventas.

Esto permite conservar los cambios realizados después de cerrar y volver a ejecutar la aplicación, sin necesidad de instalar un servidor de base de datos.

## Tecnologías utilizadas

- Python.
- Tkinter.
- CustomTkinter.
- Pillow.
- Archivos CSV.
- Programación orientada a objetos.

## Estructura del proyecto

```text
FarmaSafe/
│
├── algoritmos/
│   ├── __init__.py
│   ├── busquedas.py
│   └── ordenamientos.py
│
├── datos/
│   ├── inventario.csv
│   ├── pedidos.csv
│   └── ventas.csv
│
├── estructuras/
│   ├── __init__.py
│   ├── arbol_avl.py
│   └── cola_pedidos.py
│
├── imagenes/
│   ├── interfaz/
│   └── medicamentos/
│
├── interfaz/
│   ├── __init__.py
│   ├── panel_principal.py
│   ├── vista_asistente.py
│   ├── vista_inventario.py
│   ├── vista_pedidos.py
│   ├── vista_rendimiento.py
│   └── vista_ventas.py
│
├── modelos/
│   ├── __init__.py
│   ├── medicamento.py
│   ├── pedido.py
│   └── venta.py
│
├── servicios/
│   ├── __init__.py
│   ├── gestor_datos.py
│   ├── gestor_inventario.py
│   ├── gestor_pedidos.py
│   └── gestor_ventas.py
│
├── utilidades/
│   ├── __init__.py
│   ├── generador_datos.py
│   ├── gestor_imagenes.py
│   └── validaciones.py
│
├── config.py
├── main.py
├── README.md
└── requirements.txt
```

## Instalación

### 1. Abrir la carpeta del proyecto

Desde una terminal, ubicarse en la carpeta principal del proyecto:

```powershell
cd FarmaSafe
```

### 2. Crear un entorno virtual

```powershell
python -m venv .venv
```

### 3. Activar el entorno virtual en Windows

```powershell
.venv\Scripts\activate
```

### 4. Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

El archivo `requirements.txt` contiene las bibliotecas externas necesarias para ejecutar la interfaz gráfica y trabajar con las imágenes del sistema.

## Ejecución

Con el entorno virtual activado, ejecutar:

```powershell
python main.py
```

Después de ejecutar el comando, se abrirá el panel principal de FarmaSafe.

## Datos académicos

**Universidad:** Universidad Nacional de Chimborazo  
**Facultad:** Facultad de Ingeniería  
**Carrera:** Ciencia de Datos e Inteligencia Artificial  
**Asignatura:** Estructura de Datos  
**Docente:** Mg. Johanna Moyano Arias  
**Periodo académico:** 2026-1S  
**Fecha de ejecución:** 19 de julio de 2026  

## Autores

- Shaigua Estalin.
- Ramírez Sebastián.
- Valarezo Jamilex.
- Viteri Liseth.

## Propósito académico

FarmaSafe fue desarrollado como proyecto de investigación formativa para aplicar los contenidos estudiados durante las cuatro unidades de la asignatura.

El proyecto demuestra el uso de estructuras lineales y no lineales, algoritmos de búsqueda y ordenamiento, persistencia mediante archivos CSV y construcción de interfaces gráficas.

También permite comprobar cómo las estructuras de datos pueden utilizarse para resolver una necesidad real relacionada con el control de medicamentos, la atención ordenada de pedidos y el registro de ventas.

---

<p align="center">
  <strong>FarmaSafe</strong>
</p>

<p align="center">
  Control que previene, seguridad que protege.
</p>
