#bibliotecas para copiar imagenes y trabajar con rutas
import shutil
from pathlib import Path

#conecta el gestor con el modelo y el arbol
from modelos.medicamento import Medicamento
from estructuras.arbol_avl import ArbolAVL
from servicios.gestor_datos import GestorDatos
from utilidades.validaciones import validar_datos_medicamento
from utilidades.generador_datos import generar_medicamentos
from config import CARPETA_MEDICAMENTOS


#conecta el inventario, el archivo csv y el arbol avl
class GestorInventario:
    def __init__(self):
        self.arbol = ArbolAVL()
        self.errores_carga = []

        GestorDatos.inicializar_archivos()
        self.cargar_desde_archivo()

    #carga los medicamentos guardados al iniciar el sistema
    def cargar_desde_archivo(self):
        self.arbol = ArbolAVL()
        self.errores_carga = []

        registros = GestorDatos.leer_inventario()

        for numero_fila, registro in enumerate(
            registros,
            start=2
        ):
            try:
                medicamento = Medicamento.desde_diccionario(
                    registro
                )

                insertado = self.arbol.insertar(
                    medicamento
                )

                if not insertado:
                    self.errores_carga.append(
                        f"Fila {numero_fila}: código repetido."
                    )
            except (
                ValueError,
                TypeError,
                KeyError
            ) as error:
                self.errores_carga.append(
                    f"Fila {numero_fila}: {error}"
                )

    #guarda el recorrido ordenado del arbol en el archivo
    def guardar_inventario(self):
        GestorDatos.guardar_inventario(
            self.obtener_todos()
        )

    #devuelve los medicamentos ordenados por codigo
    def obtener_todos(self):
        return self.arbol.recorrido_inorden()

    #busca un medicamento utilizando el arbol avl
    def buscar_por_codigo(self, codigo):
        return self.arbol.buscar(codigo)

    #busca coincidencias dentro de los nombres
    def buscar_por_nombre(self, texto):
        texto = str(texto).strip().lower()
        encontrados = []

        for medicamento in self.obtener_todos():
            if texto in medicamento.nombre.lower():
                encontrados.append(medicamento)

        return encontrados

    #obtiene el siguiente codigo disponible
    def obtener_siguiente_codigo(self):
        siguiente_codigo = 1

        for medicamento in self.obtener_todos():
            if medicamento.codigo >= siguiente_codigo:
                siguiente_codigo = medicamento.codigo + 1

        return siguiente_codigo

    #copia la imagen seleccionada dentro del proyecto
    def _copiar_imagen(self, ruta_origen, codigo):
        if not ruta_origen:
            return "default.png"

        origen = Path(ruta_origen)
        extension = origen.suffix.lower()
        nombre_destino = f"medicamento_{codigo}{extension}"
        destino = CARPETA_MEDICAMENTOS / nombre_destino

        if origen.resolve() != destino.resolve():
            shutil.copy2(origen, destino)

        return nombre_destino

    #crea un medicamento con los datos del formulario
    def crear_medicamento(self, datos):
        datos_validos = validar_datos_medicamento(
            datos
        )

        if self.buscar_por_codigo(
            datos_validos["codigo"]
        ) is not None:
            raise ValueError(
                "Ya existe un medicamento con ese código."
            )

        ruta_imagen = datos_validos.pop("imagen")

        imagen = self._copiar_imagen(
            ruta_imagen,
            datos_validos["codigo"]
        )

        datos_validos["imagen"] = imagen
        medicamento = Medicamento(**datos_validos)

        insertado = self.arbol.insertar(
            medicamento
        )

        if not insertado:
            raise ValueError(
                "No se pudo insertar el medicamento."
            )

        self.guardar_inventario()
        return medicamento

    #actualiza los datos sin cambiar el codigo principal
    def actualizar_medicamento(self, codigo, datos):
        medicamento_actual = self.buscar_por_codigo(
            codigo
        )

        if medicamento_actual is None:
            raise ValueError(
                "El medicamento no existe."
            )

        datos_validos = validar_datos_medicamento(
            datos
        )

        if datos_validos["codigo"] != int(codigo):
            raise ValueError(
                "El código del medicamento no se puede cambiar."
            )

        ruta_imagen = datos_validos.pop("imagen")

        if ruta_imagen:
            imagen = self._copiar_imagen(
                ruta_imagen,
                codigo
            )
        else:
            imagen = medicamento_actual.imagen

        datos_validos["imagen"] = imagen
        medicamento_nuevo = Medicamento(
            **datos_validos
        )

        self.arbol.eliminar(codigo)
        self.arbol.insertar(medicamento_nuevo)

        self.guardar_inventario()
        return medicamento_nuevo

    #elimina el medicamento del arbol y del archivo
    def eliminar_medicamento(self, codigo):
        eliminado = self.arbol.eliminar(codigo)

        if eliminado:
            self.guardar_inventario()

        return eliminado

    #agrega unidades al medicamento seleccionado
    def agregar_stock(self, codigo, cantidad):
        medicamento = self.buscar_por_codigo(
            codigo
        )

        if medicamento is None:
            raise ValueError(
                "El medicamento no existe."
            )

        medicamento.aumentar_stock(cantidad)
        self.guardar_inventario()

        return medicamento

    #retira unidades sin permitir valores mayores al stock
    def retirar_stock(self, codigo, cantidad):
        medicamento = self.buscar_por_codigo(
            codigo
        )

        if medicamento is None:
            raise ValueError(
                "El medicamento no existe."
            )

        medicamento.disminuir_stock(cantidad)
        self.guardar_inventario()

        return medicamento

    #agrega registros aleatorios con codigos nuevos
    def generar_carga_masiva(
        self,
        cantidad=1000,
        semilla=None
    ):
        codigo_inicial = self.obtener_siguiente_codigo()
        nombres_existentes = {
            medicamento.nombre
            for medicamento in self.obtener_todos()
        }

        nuevos_medicamentos = generar_medicamentos(
            cantidad=cantidad,
            codigo_inicial=codigo_inicial,
            semilla=semilla,
            nombres_existentes=nombres_existentes
        )

        for medicamento in nuevos_medicamentos:
            self.arbol.insertar(medicamento)

        self.guardar_inventario()
        return nuevos_medicamentos

    #separa los medicamentos que necesitan atencion
    def obtener_alertas(self):
        alertas = {
            "vencidos": [],
            "proximos": [],
            "stock_bajo": [],
            "sin_stock": []
        }

        for medicamento in self.obtener_todos():
            if medicamento.esta_vencido():
                alertas["vencidos"].append(
                    medicamento
                )

            if medicamento.proximo_a_vencer():
                alertas["proximos"].append(
                    medicamento
                )

            if medicamento.tiene_stock_bajo():
                alertas["stock_bajo"].append(
                    medicamento
                )

            if medicamento.stock == 0:
                alertas["sin_stock"].append(
                    medicamento
                )

        return alertas

    #prepara los valores que se mostraran en el panel principal
    def obtener_resumen(self):
        alertas = self.obtener_alertas()

        return {
            "total": self.arbol.obtener_cantidad(),
            "vencidos": len(alertas["vencidos"]),
            "proximos": len(alertas["proximos"]),
            "stock_bajo": len(alertas["stock_bajo"]),
            "sin_stock": len(alertas["sin_stock"]),
            "altura_arbol": self.arbol.obtener_altura()
        }