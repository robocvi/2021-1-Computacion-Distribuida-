import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoBFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo BFS. '''
        ''' Aquí va tu implementacion '''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.padre = None if id_nodo != 0 else id_nodo
        self.hijos = list()
        self.distancia = float('inf') if id_nodo != 0 else 0

    def bfs(self, env):
        ''' Algoritmo BFS. '''
        if self.id_nodo == 0:
            yield env.timeout(TICK)
            self.canal_salida.envia([self.id_nodo, self.distancia], self.vecinos)

        while True:
            mensaje = yield self.canal_entrada.get()
            id_remitente = mensaje[0]
            d_recibida = mensaje[1]

            if(d_recibida+1 < self.distancia):
                self.distancia = d_recibida+1
                self.padre = id_remitente
                yield env.timeout(TICK)
                self.canal_salida.envia([self.id_nodo, self.distancia], self.vecinos)

