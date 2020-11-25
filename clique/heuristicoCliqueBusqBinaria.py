import numpy as np 
import random
import pprint
from itertools import combinations

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


class TDAGrafo:
    def __init__(self,listaConexiones):
        self.grafo=dict()
        self.listaADiccionario(listaConexiones)
        self.cardinalesDicc=dict()
        self.cardinalidades()


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

    #ARMO DICCIONARIO CON CARDINALIDADES DE ARISTAS Y COMO VALOR: LOS NODOS CON ESA CARDINALIDAD
    def cardinalidades(self):
    
        for nodo,conexiones in self.grafo.items(): #ITENS TRAE CLAVE Y VALOR
            self.cardinalesDicc.setdefault(len(conexiones),[]).append(nodo) #ESTRUCTURA
        

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

    #DADO UN VALOR, DEVUELVE UN ARRAY CON TODOS LOS NODOS DE ESA CARDINALIDAD PARA ARRIBA INCLUSIVE
def nodosSuperiores(grafo, valor):
    lista=list(grafo.cardinalesDicc.keys())
    lista.sort()
    print('DICCIONARIO CARDINALES LISTA:{} '.format(lista))
    arrayNodosSup=[]
    arrayCardinalesSup=[]
    for cardi in lista:
        if cardi>=valor:
            arrayCardinalesSup.append(cardi)
    
    print('ARRAY CARDINALES SUP:{} '.format(arrayCardinalesSup))
    
    for card in arrayCardinalesSup:
        for nodo in grafo.cardinalesDicc[card]:
            arrayNodosSup.append(nodo)
    print('Nodos Superiores para cardinalidad {}: {}'.format(valor,arrayNodosSup))
    return arrayNodosSup


def cliqueMaxHeuristic(grafo:TDAGrafo):
    cardiordenado=sorted(grafo.cardinalesDicc)
    gradoMax=cardiordenado[-1] #TRAE EL GRADO MAXIMO DE LOS NODOS DEL GRAFO
    limInf=0
    limSup=gradoMax
    print('Limite Superior:'+str(limSup))
    cliqueMax=None
    mitad=(limInf+limSup)//2

    while limInf<=limSup:
        nodosSuper=nodosSuperiores(grafo,mitad) # DE MITAD PARA ARRIBA INCLUSIVE
        cantNodosSup=len(nodosSuper)
        if cantNodosSup>mitad: #TENGO NODOS PARA ANALIZAR EN LA PARTE DERECHA
            cliqueAux=grafo.combinacionEsClique(nodosSuper, mitad+1) #BUSCO CLIQUE DE GRADO MITAD+1
            if cliqueAux: #SI HAY BUSCO MAS GRANDES

                cliqueMax=cliqueAux
                limInf=mitad+1
            else:
                limSup=mitad-1 #SI NO HAY BUSCO DE LA MITAD INFERIOR
        else: 
            limSup=mitad-1 #
        mitad=(limInf+limSup)//2 #ACTUALIZO LA MITAD SIEMPRE
    return cliqueMax  