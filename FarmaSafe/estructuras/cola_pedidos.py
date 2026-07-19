#conecta la cola con el modelo de pedido
from modelos.pedido import Pedido


#guarda un pedido y la referencia al siguiente nodo
class NodoCola:
    def __init__(self, pedido):
        self.pedido = pedido
        self.siguiente = None


#organiza los pedidos siguiendo el orden fifo
class ColaPedidos:
    def __init__(self):
        self.frente = None
        self.final = None
        self.cantidad = 0

    #revisa si la cola no tiene pedidos
    def esta_vacia(self):
        return self.frente is None

    #agrega un pedido al final de la cola
    def encolar(self, pedido):
        if not isinstance(pedido, Pedido):
            raise TypeError(
                "La cola solamente puede guardar objetos Pedido."
            )

        nuevo_nodo = NodoCola(pedido)

        if self.esta_vacia():
            self.frente = nuevo_nodo
            self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo

        self.cantidad += 1

    #retira el primer pedido que ingreso en la cola
    def desencolar(self):
        if self.esta_vacia():
            return None

        pedido_retirado = self.frente.pedido
        self.frente = self.frente.siguiente
        self.cantidad -= 1

        if self.frente is None:
            self.final = None

        return pedido_retirado

    #muestra el pedido que sera atendido primero
    def ver_frente(self):
        if self.esta_vacia():
            return None

        return self.frente.pedido

    #busca un pedido recorriendo los nodos de la cola
    def buscar(self, codigo_pedido):
        codigo_pedido = int(codigo_pedido)
        actual = self.frente

        while actual is not None:
            if actual.pedido.codigo_pedido == codigo_pedido:
                return actual.pedido

            actual = actual.siguiente

        return None

    #recorre la cola para mostrarla en la interfaz
    def obtener_pedidos(self):
        pedidos = []
        actual = self.frente

        while actual is not None:
            pedidos.append(actual.pedido)
            actual = actual.siguiente

        return pedidos

    #devuelve la cantidad actual de pedidos
    def obtener_cantidad(self):
        return self.cantidad

    #muestra el recorrido desde el frente hasta el final
    def __str__(self):
        if self.esta_vacia():
            return "Cola vacía"

        pedidos = []
        actual = self.frente

        while actual is not None:
            pedidos.append(
                f"Pedido {actual.pedido.codigo_pedido}"
            )
            actual = actual.siguiente

        return " -> ".join(pedidos)