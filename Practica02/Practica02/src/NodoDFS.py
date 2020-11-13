import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoDFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo DFS. '''
        # Tu implementación va aquí
        self.id_nodo = id_nodo
        # Hacemos que vecinos sea un conjunto pues ya es mucho más sencillo realizar las operaciones de diferencia
        # con otros conjuntos, o la de verificar su un conjunto es subconjunto de algún otro. 
        self.vecinos = set(vecinos)
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        # Variables necesarias para construir el árbol:
        self.padre = self.id_nodo
        self.hijos = []

    def dfs(self, env):
        ''' Algoritmo DFS. '''
        # Tu implementación va aquí

        # Solo el proceso distinguido ejecuta este bloque:
        if self.id_nodo == 0:
            self.padre = 0
            # Como se especifica para esta práctica, solo podemos enviar un mensaje al elemento más chico de nuestro
            # conjunto de vecinos
            child = min(self.vecinos)
            yield env.timeout(TICK)
            self.canal_salida.envia(["GO", set([self.id_nodo]), self.id_nodo], [child])
            self.hijos.append(child)
        
        while True:
            m = yield self.canal_entrada.get()
            # Tipo de mensaje, i.e. GO ó BACK:
            mensaje = m[0]
            # EL conjunto de nodos que el proceso remitente ha visitado:
            visited = m[1]
            # El remitente del mensaje:
            sender = m[2]
            if mensaje == "GO":
                self.padre = sender
                if self.vecinos.issubset(visited):
                    visited.add(self.id_nodo)
                    yield env.timeout(TICK)
                    self.canal_salida.envia(["BACK", visited, self.id_nodo], [sender])
                    self.hijos.clear()
                else:
                    # Nos regresa el elemento más chico del conjunto vecinos\visited
                    child = min(self.vecinos.difference(visited))
                    visited.add(self.id_nodo)
                    yield env.timeout(TICK)
                    self.canal_salida.envia(["GO", visited, self.id_nodo], [child])
                    self.hijos = [child]
            elif mensaje == "BACK":
                if self.vecinos.issubset(visited):
                    if self.padre == self.id_nodo:
                        break
                    else:
                        yield env.timeout(TICK)
                        self.canal_salida.envia(["BACK", visited, self.id_nodo], [self.padre])
                else:
                    child = min(self.vecinos.difference(visited))
                    visited.add(self.id_nodo)
                    yield env.timeout(TICK)
                    self.canal_salida.envia(["GO", visited, self.id_nodo], [child])
                    self.hijos.append(child)
