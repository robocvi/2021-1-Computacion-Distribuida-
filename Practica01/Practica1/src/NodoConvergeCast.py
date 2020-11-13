import simpy
from Canales.CanalConvergeCast import *
from Nodo import *

class NodoConvergeCast(Nodo):
    '''Implementa la interfaz de Nodo para el algoritmo de Coverge Cast.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida, padre):
        '''Inicializamos el nodo.'''
        self.id_nodo = id_nodo
        self.valores = "valor %d" %(id_nodo)
        self.padre = padre
        self.vecinos = vecinos
        self.expected_msg = len(vecinos)
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.lista = []

    def convergeCast(self, envi):
        if (len(self.vecinos) == 0): # Solo las hojas realizan este paso
            # Esperamos la siguiente transmisión
            yield envi.timeout(1)
            self.canal_salida.envia([[self.id_nodo, self.valores]], [self.padre])
        else:
            while True:
                 # Esperamos a que nos llegue el mensaje
                 while (self.expected_msg > 0):
                    mensaje = yield self.canal_entrada.get()
                    print('%d recibío mensaje en la ronda %d' %(self.id_nodo, envi.now))
                    self.lista = self.lista + mensaje
                    self.expected_msg = self.expected_msg-1
                 print('%d recibío todos los mensaje en la ronda %d' %(self.id_nodo, envi.now))
                 print(self.lista)
                 yield envi.timeout(1)

                 if(self.id_nodo != 0):
                     self.lista.append([self.id_nodo, self.valores])
                     self.canal_salida.envia(self.lista, [self.padre])
                 else:
                     print("Ejecucion terminada")
                 break



    def get_id(self):
        return self.id_nodo


if __name__ == "__main__":
    # Inicializamos ambiente y canal
    envi = simpy.Environment()
    bc_pipe = CanalConvergeCast(envi)

    # Creamos los nodos
    grafica = []
    # adyacencias = [[1, 2], [0, 2, 7], [0, 1, 3, 7], [2, 4, 6], [2, 3, 5], [4], [3, 7], [1, 2, 6]]
    adyacencias = [[1, 2], [3, 4], [5, 6], [], [], [], []]
    for i in range(0, len(adyacencias)):
        grafica.append(NodoConvergeCast(i, adyacencias[i], bc_pipe.crea_canal_de_entrada(), bc_pipe, None))
    grafica[0].padre = None
    grafica[1].padre = 0
    grafica[2].padre = 0
    grafica[3].padre = 1
    grafica[4].padre = 1
    grafica[5].padre = 2
    grafica[6].padre = 2

    # Y le decimos al ambiente que lo procese
    for i in range(0, len(adyacencias)):
        envi.process(grafica[i].convergeCast(envi))
    envi.run(until=15)
