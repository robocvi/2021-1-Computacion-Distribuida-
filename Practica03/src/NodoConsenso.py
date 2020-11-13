import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoConsenso(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Consenso.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo de consenso. '''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        # Atributos extra
        self.V = [None] * (len(vecinos) + 1) # Llenamos la lista de Nones
        self.V[id_nodo] = id_nodo
        self.New = set([id_nodo])
        self.rec_from = [None] * (len(vecinos) + 1)
        self.fallare = False      # Colocaremos esta en True si el nodo fallará
        self.lider = None         # La elección del lider.

    def consenso(self, env, f):
        '''El algoritmo de consenso.'''
        # Aquí va su implementación
        rondaFinal = f+1
        fallo = 0
        while True:
            #Hacemos que un proceso falle por cada ronda, estos fallaran antes mandar mensaje
            fallo = env.now if env.now < f else -1
            if(self.id_nodo == fallo):
                self.fallare = True
                return
            #Mandamos mensajes a los procesos vecinos
            if(len(self.New) != 0):
                yield env.timeout(TICK)
                a = [self.id_nodo, self.New]
                self.canal_salida.envia(a, self.vecinos)

            else:
                yield env.timeout(TICK)
                self.canal_salida.envia([self.id_nodo, set([])], self.vecinos)

            expected_msg = len(self.vecinos) - env.now
            if(env.now == rondaFinal):
                expected_msg = len(self.vecinos) - (env.now-1)
            while (expected_msg > 0):
                mensaje = yield self.canal_entrada.get()
                id_remitente = mensaje[0]
                self.rec_from[id_remitente] = mensaje
                mensaje = None
                expected_msg = expected_msg-1
            self.New = set([])
            i = 0
            while i < len(self.rec_from):
                if(i != self.id_nodo and self.rec_from[i] != None):
                    x = self.rec_from[i]
                    for y in x[1]:
                        if(self.V[y] is None):
                            self.V[y] = y
                            self.New.add(y)
                i = i+1

            if(env.now == rondaFinal):
                break

        self.lider = self.primerNoNone(self.V)
        print('El proceso %d propone a: %d' %(self.id_nodo, self.lider))

    #Funcion auxiliar que nos permite tomar el primer elemento diferente de None
    def primerNoNone(self, l):
        i = 0
        while i < len(l):
            if(l[i] is None):
                i = i+1
            else: return l[i]
