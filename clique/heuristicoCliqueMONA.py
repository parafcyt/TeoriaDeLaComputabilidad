import numpy as np 
import random
import pprint
import operator
import copy
import time
from itertools import combinations


class TDAPila:
    def __init__(self):
        self.items = []

    def estaVacia(self):
        return self.items == []

    def apilar(self, item):
        self.items.append(item)

    def desapilar(self):
        """ Devuelve el elemento tope y lo elimina de la pila.
        Si la pila está vacía levanta una excepción. """
        try:
            return self.items.pop()
        except IndexError:
            raise ValueError("La pila está vacía")

    def inspeccionar(self):
        return self.items[len(self.items)-1]

    def tamano(self):
        return len(self.items)




class TDAGrafo:
    def __init__(self,listaConexiones):
        self.grafo=dict()
        self.listaADiccionario(listaConexiones)
        self.cardinalesDicc=dict()
        #self.cardinalidades()


    #DE LISTA DE CONEXIONES A DICCIONARIO
    def listaADiccionario(self,listaConexiones):
    
        for element1,element2 in listaConexiones:
            if element2 !=None:

                self.grafo.setdefault(element1,[]) #ESTRUCTURA
                if element2 not in self.grafo[element1]: #NO DUPLICADOS
                    self.grafo[element1].append(element2)

                self.grafo.setdefault(element2,[]) #ESTRUCTURA
                if element1 not in self.grafo[element2]: #NO DUPLICADOS
                    self.grafo[element2].append(element1)

            else:
                self.grafo.setdefault(element1,[])


    #SEGÚN UN CLIQUE, DECIR SI UN NODO ES VECINO A TODOS SUS ELEMENTOS
    def esVecino(self,clique:list,nodo:int):
        for elemento in clique:
            #ME FIJO EN EL DICCIONARIO DEL NODO SI LOS ELEMENTOS DEL CLIQUE ESTÁN EN EL
            #CON QUE 1 ELEMENTO NO ESTÉ, YA EL NODO NO ES VECINO DEL CLIQUE
            if elemento not in self.grafo[nodo]:
                return False
        return True


    #HACE TODAS LAS COMBINACIONES DE LOS VERTICES DE UNA CARDINALIDAD Y DICE SI SON CLIQUE(Y LO DEVUELVE)
    def combinacionEsClique(self,vertices, cardiClique):
        combinaciones=list(combinations(vertices, cardiClique))
        print('COMBINACIONES:{}, {}'.format(combinaciones,cardiClique)) 
        for combinacion in combinaciones:
            if self.esClique(combinacion):
                return combinacion
        return False
        

    #DADA UNA COMBINACION SE FIJA SI ENTRE ELLOS SON VECINOS
    def esClique(self,combinacion):
        for nodo in combinacion:
            for elemento in combinacion:
                if nodo != elemento:
                    if nodo not in self.grafo[elemento]:
                        return False
        return True

#CARGAR MATRIZ INCIDENCIA RANDOM, CONTROLO EL % DE CONEXIONES(1)
def matrizIncidencia(cantNodos:int, probabilidad:float):
    matriz=np.zeros((cantNodos,cantNodos),int)
    for fila in range(cantNodos):
        for columna in range(cantNodos):
            if fila==columna:
                matriz[fila][columna]=0
            elif random.random()<probabilidad:
                #CONTROLO CANT DE 1
                matriz[fila][columna]=1
    return matriz


#DE MATRIZ DE INCIDENCIA HAGO LISTA DE CONEXIONES
def listaConexiones(matriz:np.ndarray):
    lista=[]
    cantNodos=matriz.shape[0]
    for fila in range(cantNodos):
        columna=-1
        conexion=False
        for elemento in matriz[fila]:
            #ME EMPIEZO A MOVER X LAS COLUMNAS
            columna+=1
            if elemento==1:
                lista.append((fila,columna))
                conexion=True
        if conexion==False:
            #NODO SIN ARISTAS
            lista.append((fila,None))
    return lista



        
#DICCIONARIO DE CARDINALIDADES X NODO
def nodoYcardinalDic(grafo):
    cardinalidades=dict()
    for nodo,conectados in grafo.items():
        cardinalidades[nodo]=len(conectados) #NO TIENE ORDEN
        #print(cardinalidades[nodo])
    
    return cardinalidades


#DADO UN NODO LO ELIMINA DEL DICCIONARIO DE CARDINALIDADES X NODO
def eliminarNodo(grafoAux,nodo):
    conexionesNodo=grafoAux[nodo]
    for conexion in conexionesNodo:
        grafoAux[conexion].remove(nodo)
    grafoAux.pop(nodo)
    return grafoAux


#DEVUELVE PILA CON CARDINALIDADES
def pilaCardinales(grafoAux):
    pilaFinal=TDAPila()
    listaOrdenada=sorted(nodoYcardinalDic(grafoAux).items(), key=lambda x: x[1])

    while len(listaOrdenada)>0:
        pilaFinal.apilar(listaOrdenada[0][0])
        grafoAux=eliminarNodo(grafoAux,listaOrdenada[0][0])
        
        listaOrdenada=sorted(nodoYcardinalDic(grafoAux).items(), key=lambda x: x[1])
    return pilaFinal

#COPIO EL GRAFO Y DEVUELVO COPIA
def copiarGrafo(grafo):
    grafoAux=copy.deepcopy(grafo)
    return grafoAux


#ALGORITMO CLIQUEMAX MONA
def maxCliqueMona(grafo):
    inicio=time.clock()
    pila=pilaCardinales(copiarGrafo(grafo.grafo))
    
    clique=[]
    
    while not pila.estaVacia():
        nodoTratar=pila.desapilar()
        if len(clique)==0:
            clique.append(nodoTratar)
        elif grafo.esVecino(clique,nodoTratar):
            clique.append(nodoTratar)
        else:
            final=time.clock()-inicio
            return clique,final
    
    final=time.clock()-inicio
    return clique,final



