import simpy
from Canales import CanalBroadcast
from Nodo import *

class NodoVecinos(Nodo):
    
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        '''Inicializamos el nodo.'''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        # Variable para implementar el algoritmo 1:
        self.identifiers = []
        # Esta variable no es necesaria, pues el algoritmo termina bien sin ella
        # pero la ponemos para poder salir del ciclo e imprimir los valores finales de cada nodo
        self.expected_msg = len(vecinos)
        
    def conoceVecinos(self, envi):
        '''Función para conocer los vecinos de los vecinos'''
        yield envi.timeout(1)
        self.canal_salida.envia(self.vecinos, self.vecinos)
            
        while True:
            mensaje = yield self.canal_entrada.get()
            self.identifiers.extend(mensaje)
            self.expected_msg -= 1
            # Gracias a la variable expected_msg sabemos en qué momento detener la ejecución
            if not self.expected_msg:
                # Convertimos la lista identifiers en un conjunto para eliminar elementos repetidos.
                self.identifiers = set(self.identifiers)
                break
        #print("Nodo: %d, identifiers_%d: " % (self.id_nodo, self.id_nodo))
        #print(self.identifiers)


if __name__ == "__main__":
    # Inicializamos ambiente y canal
    envi = simpy.Environment()
    bc_pipe = CanalBroadcast.CanalBroadcast(envi)

    # Creamos los nodos
    grafica = []
    adyacencias = [[1, 2], [0, 2, 7], [0, 1, 3, 4, 7], [2, 4, 6], [2, 3, 5], [4], [3, 7], [1, 2, 6]]
    for i in range(0, len(adyacencias)):
        grafica.append(NodoVecinos(i, adyacencias[i], bc_pipe.crea_canal_de_entrada(), bc_pipe))

    # Y le decimos al ambiente que lo procese
    for i in range(0, len(adyacencias)):
        envi.process(grafica[i].conoceVecinos(envi))
    envi.run(until=50)
