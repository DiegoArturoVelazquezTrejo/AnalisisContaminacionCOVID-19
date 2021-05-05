# Integración de todo el análisis
import pandas as pd

from AlgoritmoKMeans import AlgoritmoKMeans

from Estadistica import Estadistica

data = pd.read_csv("CiudadMexicoDatosFinales.csv")

# Definimos el número de clusters que utilizaremos
clusters = 4

# Definimos las variables de estudio
variables_de_estudio = ["Infectados", "promedioO3Esc", "promedioSO2Esc", "promedioCOEsc"]

# Definimos el número de iteraciones que queremos que realice el algoritmo
iteraciones = 1000

kmeans = AlgoritmoKMeans(clusters, data, variables_de_estudio, iteraciones)

#kmeans.start()

# Aquí vamos a hacer un análisis estadístico de los grupos que nos generó el algoritmo
centroides = ["centroide-"+str(i)+".csv" for i in range(1, clusters+1)]

# Ahora vamos a realizar un estudio individual de las variables, definimos aquellas de las que queremos hacer estudio
relacion_interes = [("Infectados", "promedioO3Esc"), ("Infectados", "promedioCOEsc"), ("Infectados", "promedioSO2Esc")]
