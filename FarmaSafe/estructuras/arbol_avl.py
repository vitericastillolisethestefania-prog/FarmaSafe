#conecta el arbol con el modelo de medicamento
from modelos.medicamento import Medicamento


#guarda el medicamento y sus conexiones dentro del arbol
class NodoAVL:
    def __init__(self, medicamento):
        self.medicamento = medicamento
        self.izquierdo = None
        self.derecho = None
        self.altura = 1


#mantiene los medicamentos ordenados y balanceados por codigo
class ArbolAVL:
    def __init__(self):
        self.raiz = None
        self.cantidad = 0

    #revisa si el arbol no tiene medicamentos
    def esta_vacio(self):
        return self.raiz is None

    #devuelve la altura de un nodo
    def obtener_altura_nodo(self, nodo):
        if nodo is None:
            return 0

        return nodo.altura

    #calcula la diferencia entre los dos lados del nodo
    def obtener_balance(self, nodo):
        if nodo is None:
            return 0

        return (
            self.obtener_altura_nodo(nodo.izquierdo)
            - self.obtener_altura_nodo(nodo.derecho)
        )

    #actualiza la altura despues de cada cambio
    def _actualizar_altura(self, nodo):
        altura_izquierda = self.obtener_altura_nodo(
            nodo.izquierdo
        )
        altura_derecha = self.obtener_altura_nodo(
            nodo.derecho
        )

        nodo.altura = 1 + max(
            altura_izquierda,
            altura_derecha
        )

    #gira los nodos hacia la derecha para recuperar el equilibrio
    def _rotacion_derecha(self, nodo_desbalanceado):
        nueva_raiz = nodo_desbalanceado.izquierdo
        nodo_temporal = nueva_raiz.derecho

        nueva_raiz.derecho = nodo_desbalanceado
        nodo_desbalanceado.izquierdo = nodo_temporal

        self._actualizar_altura(nodo_desbalanceado)
        self._actualizar_altura(nueva_raiz)

        return nueva_raiz

    #gira los nodos hacia la izquierda para recuperar el equilibrio
    def _rotacion_izquierda(self, nodo_desbalanceado):
        nueva_raiz = nodo_desbalanceado.derecho
        nodo_temporal = nueva_raiz.izquierdo

        nueva_raiz.izquierdo = nodo_desbalanceado
        nodo_desbalanceado.derecho = nodo_temporal

        self._actualizar_altura(nodo_desbalanceado)
        self._actualizar_altura(nueva_raiz)

        return nueva_raiz

    #agrega un medicamento y aumenta la cantidad del arbol
    def insertar(self, medicamento):
        if not isinstance(medicamento, Medicamento):
            raise TypeError(
                "El árbol solamente puede guardar objetos Medicamento."
            )

        self.raiz, insertado = self._insertar(
            self.raiz,
            medicamento
        )

        if insertado:
            self.cantidad += 1

        return insertado

    #coloca el medicamento segun su codigo y revisa el balance
    def _insertar(self, nodo, medicamento):
        if nodo is None:
            return NodoAVL(medicamento), True

        if medicamento.codigo < nodo.medicamento.codigo:
            nodo.izquierdo, insertado = self._insertar(
                nodo.izquierdo,
                medicamento
            )
        elif medicamento.codigo > nodo.medicamento.codigo:
            nodo.derecho, insertado = self._insertar(
                nodo.derecho,
                medicamento
            )
        else:
            return nodo, False

        if not insertado:
            return nodo, False

        self._actualizar_altura(nodo)
        balance = self.obtener_balance(nodo)

        #corrige el caso izquierdo izquierdo
        if (
            balance > 1
            and medicamento.codigo
            < nodo.izquierdo.medicamento.codigo
        ):
            return self._rotacion_derecha(nodo), True

        #corrige el caso derecho derecho
        if (
            balance < -1
            and medicamento.codigo
            > nodo.derecho.medicamento.codigo
        ):
            return self._rotacion_izquierda(nodo), True

        #corrige el caso izquierdo derecho
        if (
            balance > 1
            and medicamento.codigo
            > nodo.izquierdo.medicamento.codigo
        ):
            nodo.izquierdo = self._rotacion_izquierda(
                nodo.izquierdo
            )
            return self._rotacion_derecha(nodo), True

        #corrige el caso derecho izquierdo
        if (
            balance < -1
            and medicamento.codigo
            < nodo.derecho.medicamento.codigo
        ):
            nodo.derecho = self._rotacion_derecha(
                nodo.derecho
            )
            return self._rotacion_izquierda(nodo), True

        return nodo, True

    #busca un medicamento siguiendo el orden de los codigos
    def buscar(self, codigo):
        codigo = int(codigo)
        actual = self.raiz

        while actual is not None:
            if codigo == actual.medicamento.codigo:
                return actual.medicamento

            if codigo < actual.medicamento.codigo:
                actual = actual.izquierdo
            else:
                actual = actual.derecho

        return None

    #elimina un medicamento y reduce la cantidad del arbol
    def eliminar(self, codigo):
        codigo = int(codigo)

        self.raiz, eliminado = self._eliminar(
            self.raiz,
            codigo
        )

        if eliminado:
            self.cantidad -= 1

        return eliminado

    #retira el nodo y vuelve a revisar el equilibrio
    def _eliminar(self, nodo, codigo):
        if nodo is None:
            return None, False

        if codigo < nodo.medicamento.codigo:
            nodo.izquierdo, eliminado = self._eliminar(
                nodo.izquierdo,
                codigo
            )
        elif codigo > nodo.medicamento.codigo:
            nodo.derecho, eliminado = self._eliminar(
                nodo.derecho,
                codigo
            )
        else:
            eliminado = True

            if nodo.izquierdo is None:
                return nodo.derecho, True

            if nodo.derecho is None:
                return nodo.izquierdo, True

            sucesor = self._obtener_menor(nodo.derecho)
            nodo.medicamento = sucesor.medicamento

            nodo.derecho, _ = self._eliminar(
                nodo.derecho,
                sucesor.medicamento.codigo
            )

        if not eliminado:
            return nodo, False

        self._actualizar_altura(nodo)
        balance = self.obtener_balance(nodo)

        #corrige el lado izquierdo despues de eliminar
        if balance > 1:
            if self.obtener_balance(nodo.izquierdo) >= 0:
                return self._rotacion_derecha(nodo), True

            nodo.izquierdo = self._rotacion_izquierda(
                nodo.izquierdo
            )
            return self._rotacion_derecha(nodo), True

        #corrige el lado derecho despues de eliminar
        if balance < -1:
            if self.obtener_balance(nodo.derecho) <= 0:
                return self._rotacion_izquierda(nodo), True

            nodo.derecho = self._rotacion_derecha(
                nodo.derecho
            )
            return self._rotacion_izquierda(nodo), True

        return nodo, True

    #encuentra el codigo menor de un subarbol
    def _obtener_menor(self, nodo):
        actual = nodo

        while actual.izquierdo is not None:
            actual = actual.izquierdo

        return actual

    #recorre los medicamentos de menor a mayor codigo
    def recorrido_inorden(self):
        medicamentos = []
        self._inorden(self.raiz, medicamentos)
        return medicamentos

    def _inorden(self, nodo, medicamentos):
        if nodo is not None:
            self._inorden(nodo.izquierdo, medicamentos)
            medicamentos.append(nodo.medicamento)
            self._inorden(nodo.derecho, medicamentos)

    #recorre primero la raiz y despues sus dos lados
    def recorrido_preorden(self):
        medicamentos = []
        self._preorden(self.raiz, medicamentos)
        return medicamentos

    def _preorden(self, nodo, medicamentos):
        if nodo is not None:
            medicamentos.append(nodo.medicamento)
            self._preorden(nodo.izquierdo, medicamentos)
            self._preorden(nodo.derecho, medicamentos)

    #recorre primero los lados y deja la raiz para el final
    def recorrido_postorden(self):
        medicamentos = []
        self._postorden(self.raiz, medicamentos)
        return medicamentos

    def _postorden(self, nodo, medicamentos):
        if nodo is not None:
            self._postorden(nodo.izquierdo, medicamentos)
            self._postorden(nodo.derecho, medicamentos)
            medicamentos.append(nodo.medicamento)

    #agrupa los medicamentos por nivel para mostrarlos en la interfaz
    def obtener_niveles(self):
        niveles = []
        self._guardar_por_nivel(
            self.raiz,
            0,
            niveles
        )
        return niveles

    def _guardar_por_nivel(self, nodo, nivel, niveles):
        if nodo is None:
            return

        if len(niveles) == nivel:
            niveles.append([])

        niveles[nivel].append(nodo.medicamento)

        self._guardar_por_nivel(
            nodo.izquierdo,
            nivel + 1,
            niveles
        )
        self._guardar_por_nivel(
            nodo.derecho,
            nivel + 1,
            niveles
        )

    #devuelve la altura actual del arbol
    def obtener_altura(self):
        return self.obtener_altura_nodo(self.raiz)

    #devuelve la cantidad de medicamentos guardados
    def obtener_cantidad(self):
        return self.cantidad

    #muestra los codigos en orden ascendente
    def __str__(self):
        if self.esta_vacio():
            return "Árbol vacío"

        codigos = []

        for medicamento in self.recorrido_inorden():
            codigos.append(str(medicamento.codigo))

        return " -> ".join(codigos)