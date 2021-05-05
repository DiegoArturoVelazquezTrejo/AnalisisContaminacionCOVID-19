# Implementación del algoritmo KMeans
'''
Variables de clase:

    Cantidad de Centroides que queremos.
    Lista de datos original (no se va a modificar).
    Diccionario con los centroides (el de listas).
    Diccionario con las coordenadas de cada centroide.


Seleccionar los centroides de manera aleatoria (entre los datos).
Función que calcule las distancias ecucledianas.

{C1: [], C2: [], C3:[]}

 # En esta estructura de datos, vamos a tener que estar actualizando las coordenadas
{C1: coordenadasC1, C2: coordenadasC2, ... , Cn: coordenadasCn}

Observación:

            Cada centroide tiene sus propias coordenadas.

            C1       C2       C3

            a1       b1        c1
            a2       b2        c2
            a3       b3        c3
            a4       b4        c4
            a5       b5        c5


Función que asigne los datos a sus respectivos centroides.

Función que nos regrese el centroide con menor distancia.

Función de predicción (le pasamos un nuevo dato y al final de la ejecución, nos dice a qué categoría pertenece).

Función que guarde las coordenadas de los centroides finales (Para poder ir comparando). Las guardará en un .txt


Observación:

    Generar J iteraciones del algoritmo para obtener J clasificaciones de centroides distintos.

    Diseñar otra clase que estudie las relaciones de los datos en cada clase.
'''
# Biblioteca para leer datos
import pandas as pd
# Biblioteca para trabajar con operaciones matemáticas
import math

class AlgoritmoKMeans:

    '''
    Definimos el constructor de la clase
    @param numeroCentroides -> Indica el número de centroides del algoritmo.
    @param datos -> Data Frame que contiene los datos a clasificar.
    @param variables -> Lista con las variables que nos interesa estudiar (reduce o aumenta dimensionalidad de los datos).
    @param Número de iteraciones
    '''
    def __init__(self, numeroCentroides, datos, variables, iteraciones):
        # Variables de clase
        self.datos = datos
        self.numeroCentroides = numeroCentroides
        self.iteraciones = iteraciones
        # Estructuras de datos auxiliares
        self.lista_centroides = {} # Esta variable es la que contiene la lista de identificadores para centroide
        self.centroides = {}
        # Necesitamos inicializar las estructuras de datos que utilizaremos
        for i in range(numeroCentroides):
            nombre = "centroide-"+str(i+1)
            self.lista_centroides[nombre] = []
        # self.lista_centroides = {"centroide-1":['2020-09-10', '2020-09-11', '2020-09-12', '2020-09-13', ...], "centoride-2":[], ..., "centroide-n":[]}

        # Vamos a seleccionar los centroides de manera aleatoria entre los datos
        muestra_aleatoria = self.datos.sample(self.numeroCentroides)
        # Vamos a obtener las fechas para de esta manera acceder a los datos individuales de la muestra
        fechas = muestra_aleatoria["Fecha"].tolist()
        i = 0

        for centroide in self.lista_centroides:
            coordenadas = []
            # Vamos a meter en un vector las variables que nos interesa
            for variable in variables:
                coordenadas.append( self.datos[self.datos["Fecha"] == fechas[i]][variable].tolist()[0] )
            i += 1
            self.centroides[centroide] = coordenadas

        # Aquí tenemos que traducir todo el dataFrame a vectores de la forma (a1, a2, ..., an):  {'2020-09-10': (a1, a2, ..., an), '2020-09-10':(a1, a2, ..., an)}

        # Ciudad de México	2020-12-21	5518	5141	144	58924	8918653	0.006606827286587	0.38531746031746	0.75	1
        # => (5518,	5141,	144	58924,	8918653,	0.006606827286587)

        self.diccionario_data = {}     # Contendrá los datos procesados a vectores numéricos que podemos manipular
        fechas = self.datos["Fecha"].unique()
        for fecha in fechas:
            coordenadas = []
            # Vamos a meter en un vector las variables que nos interesa
            for variable in variables:
                coordenadas.append( self.datos[self.datos["Fecha"] == fecha][variable].tolist()[0] )
            self.diccionario_data[fecha] = coordenadas

    '''
    Método para calcular la distancia euclediana de un vector en R^n
    @param Vector 1 de tamaño n (n es el número de variables que manejamos)
    @param Vector 2 de tamaño n
    @return constante c que es la distancia entre esos dos vectores
    '''
    def distancia_euclediana(self, vector1, vector2):
        distancia = 0
        for i in range(len(vector1)):
            distancia += math.pow(vector1[i] - vector2[i], 2)

        return math.sqrt(distancia)

    '''
    Método que determina el centroide más cercano al iésimo dato
    @param vector de datos
    @return centoride k más cercano
    '''
    def define_centroide_cercano(self, vector):
        dist_min = float('inf')
        centroide_min = ""
        for centroide in self.centroides:
            d = self.distancia_euclediana(vector, self.centroides[centroide])
            #print(d)
            if(d < dist_min):
                dist_min = d
                centroide_min = centroide
        return centroide_min

    '''
    Método para redefinir el nuevo centroide donde la lista que se pasaría como parámetro de entrada es de la forma: ['2020-09-10', '2020-09-11', '2020-09-12', '2020-09-13', ...]
    @param Lista con los identificadores de los vectores que le corresponden a ese vector
    @return vector (lista) que contiene las nuevas coordenadas del centroide

    Recibimos esto                    self.diccionario_data
    [                           [
        2020-09-10       ->       (a1, b1, c1)
        2020-09-10       ->       (a2, b2, c2)
        2020-09-10       ->       (a3, b3, c3)
        2020-09-10       ->       (a4, b4, c4)
        2020-09-10       ->       (a5, b5, c5)
    ]                           ]
    Coordenadas del C1 = (a1+a2+a3+a4+a5/5, b1+b2+b3+b4+b5/5, c1+c2+c3+c4c5/5)
    '''
    def redefine_centroide(self, lista_vectores):
        dim_vector = len(self.centroides['centroide-1'])
        vector_sumas = []
        for i in range(0, dim_vector):
            iesima_suma = 0
            # Obtener la iésima entrada para cada vector en los datos
            for identificador in lista_vectores:
                iesima_suma += self.diccionario_data[identificador][i]
            vector_sumas.append(iesima_suma/len(lista_vectores))
        return vector_sumas

    '''
    Método que nos ayuda a ver las condiciones finales de los centroides
    '''
    def verificar_condiciones(self):
        for centroide in self.lista_centroides:
            print("Longitud del "+centroide+"    : " + str(len(self.lista_centroides[centroide])), end = " ")
            print("Coordenadas para el "+centroide+"    son: "+str(self.centroides[centroide]))
    '''
    Método que ejecuta el algoritmo kmeans
    '''
    def start(self):

        for i in range(self.iteraciones):
            # Cada dato es un identificador, una fecha, '2020-03-01'
            for dato in self.diccionario_data:

                centroide = self.define_centroide_cercano(self.diccionario_data[dato])
                #print(centroide)
                self.lista_centroides[centroide].append(dato)

            # Reasignar los nuevos centroides
            for centroide in self.lista_centroides:
                coords = self.redefine_centroide(self.lista_centroides[centroide])
                self.centroides[centroide] = coords

            if(i < self.iteraciones -1):
                # Tenemos que reiniciar las listas que tienen los centroides (para las iteraciones n -1)
                for centroide in self.lista_centroides:
                    self.lista_centroides[centroide] = []

        self.verificar_condiciones()
        self.guarda_informacion()

    '''
    Método que guarde absolutamente todo en archivos csv
    '''
    def guarda_informacion(self):
        numero_cluster = 1
        for centroide in self.lista_centroides:
            datosF = []
            for dato in self.lista_centroides[centroide]:
                datosF.append(self.datos[self.datos["Fecha"]==dato].values.tolist()[0])
            dataFrame = pd.DataFrame(datosF, columns=self.datos.keys())

            # Vamos a agregar el número del cluster al que perteneden los datos
            cluster = [numero_cluster for i in range(len(datosF))]
            dataFrame["Cluster"] = cluster
            # Ahora guardamos el dataframe
            dataFrame.to_csv(centroide+".csv", header = True, index = False)
            numero_cluster += 1

    '''
    Método que va a predecir la categoría de un dato
    @param vector de datos
    @return categoría a la que pertenece
    '''
    def predice(self, dato):
        return self.define_centroide_cercano(dato)

    '''
    Método que graficará datos en dos dimensiones (ejemplo)
    únicamentr graficará datos que tienen dos dimensiones
    '''
    def grafica(self):
        # Vamos a ir graficando los datos que cada centroide tiene
        colores = ['red', 'blue', 'yellow', 'green', 'black', 'pink', 'brown', 'orange']
        i = 0
        # Vamos a ir obteniendo los vectores para cada centroide
        for centroide in self.lista_centroides:
            lista = self.lista_centroides[centroide]
            vector_xs = []
            vector_ys = []
            for id in lista:
                coordenadas = self.diccionario_data[id] # Obtenemos el vector del dato correspondiente al identificador
                vector_xs.append(coordenadas[0])
                vector_ys.append(coordenadas[1])
            plt.scatter(vector_xs, vector_ys, c = colores[i])
            i += 1
        plt.title("Categorías generadas por KMeans")
        plt.show()

    '''
    Método para calcular varianzas
    '''
    def varianza(self):

        for centroide in self.lista_centroides:
            # Obtenemos los vectores del centroide
            vectores = self.lista_centroides[centroide]
            # vectores = ["2020-01-09", "2020-03-01", ..., ]
            lista_vectores = [self.diccionario_data[vector] for vector in vectores]

            # Aquí ya tu lista de vectores contiene todos los vectores para el késimo centroide




# Prueba
import random
from matplotlib import pyplot as plt

datosX = [random.random()*100 for i in range(1000)]
datosY = [random.random()*100 for i in range(1000)]
fechas = [i for i in range(len(datosX))] # Funciona como un vil identificador para cada dato

datos = {"Fecha":fechas, "X":datosX, "Y":datosY}

#df = pd.DataFrame(datos)

#kmeans = AlgoritmoKMeans(6, df, ["X", "Y"], 30)

#kmeans.start()
#kmeans.grafica()
