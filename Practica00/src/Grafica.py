#Computación Distribuida: Práctica 0
#Integrantes: Ocampo Villegas Roberto 316293336
#             David Alvarado Torres 316167613

#Clase Gráfica, la cual contendra nuestra implementación de una Gráfica, los detalles
#de la implementación se encuentran en el readme.

class Grafica():
    numVertices = 0
    listaVertices = []

#Constructor de nuestra gráfica, le pasaremos el numero de vértices que tendrá
#la gráfica.
    def __init__(self, n):
        self.numVertices = n
        i = 0
        while i < n:
            self.listaVertices.append([])
            i += 1

#Agrega una arista nueva a la gráfica, recibe los dos vértices que se uniran.
    def agregaArista(self, v1, v2):
        self.listaVertices[v1].append(v2)
        self.listaVertices[v2].append(v1)

#Nuestra implmentacion de BFS, recibe a la gráfica y el número del vértice del
#cual se va a empezar a recorrer la gráfica.
def bfs(g, n):
    visitados = []
    listaFinal = []
    cola = []
    for ver in g.listaVertices:
        visitados.append(0)
    visitados[n] = 1
    cola.append(n)
    while len(cola) != 0:
        d = cola.pop(0)
        listaFinal.append(d)

        for elemento in g.listaVertices[d]:
            if visitados[elemento] == 0:
                visitados[elemento] = 1
                cola.append(elemento)
    print('La lista de vertices recorridos es: ')
    print(listaFinal)


#Pequeño ejemplo el cual cuenta con 8 vértices.
g = Grafica(8)
g.agregaArista(0, 1);
g.agregaArista(0, 2);
g.agregaArista(1, 3);
g.agregaArista(1, 4);
g.agregaArista(2, 5);
g.agregaArista(2, 6);
g.agregaArista(6, 7);
bfs(g, 0)
