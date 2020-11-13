import simpy
from Canales import CanalBroadcast
from Nodo import *

class NodoGenerador(Nodo):
    
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        '''Inicializamos el nodo.'''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        # Atributos extra para poder crear el árbol generador
        self.expected_msg = 0
        self.hijos = []
        self.padre = None
        
    def genera_arbol(self, envi):
        if self.id_nodo == 0:
            yield envi.timeout(1)
            self.padre = 0
            self.expected_msg = len(self.vecinos)
            self.canal_salida.envia(["GO", self.id_nodo], self.vecinos)
        
        while True:
            mensaje = yield self.canal_entrada.get()
            if mensaje[0] == "GO":
                #print('%d recibió GO de %d en el %d' %(self.id_nodo, mensaje[1], envi.now))
                if self.padre == None:
                    self.padre = mensaje[1]
                    self.expected_msg = len(self.vecinos) - 1
                    print("El padre de %d es %d" % (self.id_nodo, self.padre))
                    if self.expected_msg == 0:
                        print("Los hijos de {} son: {}".format(self.id_nodo, self.hijos))
                        yield envi.timeout(1)
                        self.canal_salida.envia(["BACK", self.id_nodo], [self.padre])
                    else:
                        yield envi.timeout(1)
                        self.canal_salida.envia(["GO", self.id_nodo], [v for v in self.vecinos if v != self.padre])
                else:
                    if self.id_nodo != 0:
                        yield envi.timeout(1)
                        self.canal_salida.envia(["BACK", -1], [mensaje[1]])

            elif mensaje[0] == "BACK":
                # if mensaje[1] != -1:
                #     print('%d recibió BACK de %d en el %d' %(self.id_nodo, mensaje[1], envi.now))
                self.expected_msg -= 1
                if mensaje[1] != -1:
                    self.hijos.append(mensaje[1])
                if self.expected_msg == 0:
                    print("Los hijos de {} son: {}".format(self.id_nodo, self.hijos))
                    if self.padre != self.id_nodo:
                        yield envi.timeout(1)
                        self.canal_salida.envia(["BACK", self.id_nodo], [self.padre])
                    else:
                        print("El algoritmo completó su ejecución pues la raíz recibió BACK de todos sus vecinos")
                        break

"""
if __name__ == "__main__":
    # Inicializamos ambiente y canal
    envi = simpy.Environment()
    bc_pipe = CanalBroadcast.CanalBroadcast(envi)

    # Creamos los nodos
    grafica = []
    adyacencias = [[1, 2], [0, 3], [0, 3, 5], [1, 2, 4], [3, 5], [2, 4]]
    for i in range(0, len(adyacencias)):
        grafica.append(NodoGenerador(i, adyacencias[i], bc_pipe.crea_canal_de_entrada(), bc_pipe))

    # Y le decimos al ambiente que lo procese
    for i in range(0, len(adyacencias)):
        envi.process(grafica[i].genera_arbol(envi))
    envi.run()
"""