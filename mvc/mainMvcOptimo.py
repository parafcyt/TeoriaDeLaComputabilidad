import numpy as np 
import random
import pprint


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
        self.contador_aristas = 0
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
                
                    self.contador_aristas += 1

            else:
                self.grafo.setdefault(element1,[])


#GENERAR TODOS LOS SUBCONJUNTOS POSIBLES: EJ. [0,1,0,1] DESDE EL VACÍO HASTA EL [1,1,1,1]
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

def mvc(grafo,cantNodos):
    #TODOS LOS NODOS QUE CUMPLEN CON RECORRER TODOS LAS ARISTAS
    vertexcover=[]
    analizar=[0]*cantNodos
    while analizar:
        nodosAux=[]
        aristasVisitadas=[]
        #RECORRO TODA LA TUPLA
        for i in range(cantNodos):
            if(analizar[i]==1):
                for nodo in grafo.grafo[i]:
                    if {i,nodo} not in aristasVisitadas:
                        aristasVisitadas.append({i,nodo})
                        if i not in nodosAux:
                            nodosAux.append(i)
                       
        if (grafo.contador_aristas==len(aristasVisitadas)):
            if nodosAux not in vertexcover:
                vertexcover.append(nodosAux)    
        analizar=incremen(analizar)
    return vertexcover             


def minimo(minNodos):
    mcv=[]
    for conjunto in minNodos:
        if len(mcv)==0:
            mcv=conjunto
        elif len(conjunto)<len(mcv):
            mcv=conjunto
    return mcv

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
resultado=mvc(grafo,cantNodos)
print()
print(resultado)

print(minimo(resultado))


