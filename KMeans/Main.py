# Integración de todo el análisis
import pandas as pd

from AlgoritmoKMeans import AlgoritmoKMeans

from Estadistica import Estadistica

data = pd.read_csv("../SegmentacionDelegacionesNO2/iztapalapa_emisiones_covid19.csv")

# Definimos el número de clusters que utilizaremos
clusters = 5

# Definimos las variables de estudio
variables_de_estudio = ["Infectados", "Defunciones", "promedioGas", "Hospitalizados","Letalidad"]

# Definimos el número de iteraciones que queremos que realice el algoritmo
iteraciones = 100

kmeans = AlgoritmoKMeans(clusters, data, variables_de_estudio, iteraciones)

kmeans.start()
'''
# Aquí vamos a hacer un análisis estadístico de los grupos que nos generó el algoritmo
centroides = ["centroide-"+str(i)+".csv" for i in range(1, clusters+1)]

estadistica = Estadistica()

# Vamos primero a imprimir los promedios para cada variable
for centroide in centroides:
    print(centroide)
    data = pd.read_csv(centroide)
    data.pop("Poblacion")
    data.pop("Cluster")
    print("\nDescripción del Cluster ")
    print(data.describe())
    print("\nCovarianzas entre variables del cluster (coeficiente de Pearson )\n")
    print(data.corr(method ='pearson'))
    print("\n=======================================================================================================================================\n\n")
'''
