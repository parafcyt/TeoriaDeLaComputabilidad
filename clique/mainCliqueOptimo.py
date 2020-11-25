import numpy as np 
import random
import pprint
import time


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
    def esVecino(self,clique:list,nodo:int ):
        for elemento in clique:
            #ME FIJO EN EL DICCIONARIO DEL NODO SI LOS ELEMENTOS DEL CLIQUE ESTÁN EN EL
            #CON QUE 1 ELEMENTO NO ESTÉ, YA EL NODO NO ES VECINO DEL CLIQUE
            if elemento not in self.grafo[nodo]:
                return False
        return True

        
#GENERAR TODOS LOS SUBCONJUNTOS POSIBLES: EJ. [0,1,0,1] DESDE EL VACÍO HASTA EL [1,1,1,1]
def incrementar(fila):
    cadena=''
    for num in fila:
        cadena+=str(num)
        
    totalunos=cadena.count('1')
    
    if  totalunos== len(cadena):
        return None

    lineaSuma=bin(int(cadena,2)+int('1',2))[2:]
    
    lineaSuma.zfill(len(cadena))
    
    lineaNueva=lineaSuma.zfill(len(cadena))
    
    filaNueva=[]
    for i in range(0,len(lineaNueva)):
        
        filaNueva.append(int(lineaNueva[i]))
        
    return filaNueva


def incremen(fila):
    cadena=''
    for num in fila:
        cadena+=str(num)
        
    totalunos=cadena.count('1')
    
    if  totalunos== len(cadena):
        return None

    j = len(fila)-1
    while fila[j]==1:
        fila[j] = 0
        j -= 1
    fila[j]=1

    
    return fila


def cliqueMaximo(grafo,cantNodos):
    inicio=time.clock()
    maxClique=[]
    #VECTOR DE CEROS
    analizar=[0]*cantNodos
    while analizar:
        clique=[]
        for i in range(cantNodos):
            if(analizar[i]==1):
                if(len(clique)==0):
                    clique.append(i)
                elif (grafo.esVecino(clique,i)):
                    clique.append(i)
        if(len(clique)>len(maxClique)):
            maxClique=clique
        analizar=incremen(analizar)
    final=time.clock()-inicio
    return maxClique, final


cantNodos=5
probabilidad=0.3

m=matrizIncidencia(cantNodos,probabilidad)
print(m)
print()

l=listaConexiones(m)
print(l)
print()

grafo=TDAGrafo(l)

pretty_print = pprint.PrettyPrinter()
pretty_print.pprint(grafo.grafo)

resultado=cliqueMaximo(grafo,cantNodos)


print()
print(resultado)