import simpy
#import Canales.CanalBroadcastArbol
from Canales.CanalBroadcastArbol import *
from Nodo import *

class NodoBroadcastArbol(Nodo):
    '''Implementa la interfaz de Nodo '''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        '''Inicializamos el nodo.'''
        self.id_nodo = id_nodo
        self.data = ""
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida

    def broadcastArbol(self, envi):
        '''Función de broadcast para nodos. Resuelto por el algoritmo de broadcast.'''
        if self.id_nodo == 0: # Solo el nodo raiz (representado con id = 0) envia el primer msj
            # Esperamos la siguiente transmisión
            yield envi.timeout(1)
            self.data = "hola"
            self.canal_salida.envia([self.id_nodo, self.data], self.vecinos)
        else:
            while True:
                mensaje = yield self.canal_entrada.get()
                self.data = mensaje[1]
                print('%d recibió el mensaje %s de %d en la ronda %d' %(self.id_nodo, mensaje[1], mensaje[0], envi.now))
                yield envi.timeout(1)
                self.canal_salida.envia([self.id_nodo, self.data], self.vecinos)
                break


    def get_id(self):
        return self.id_nodo


if __name__ == "__main__":
    # Inicializamos ambiente y canal
    envi = simpy.Environment()
    bc_pipe = CanalBroadcastArbol(envi)

    # Creamos los nodos
    grafica = []
    # adyacencias = [[1, 2], [0, 2, 7], [0, 1, 3, 7], [2, 4, 6], [2, 3, 5], [4], [3, 7], [1, 2, 6]]
    adyacencias = [[1, 2], [3, 4], [5, 6], [7], [], [], [], []]
    for i in range(0, len(adyacencias)):
        grafica.append(NodoBroadcastArbol(i, adyacencias[i], bc_pipe.crea_canal_de_entrada(), bc_pipe))

    # Y le decimos al ambiente que lo procese
    for i in range(0, len(adyacencias)):
        envi.process(grafica[i].broadcastArbol(envi))
    envi.run(until=15)
