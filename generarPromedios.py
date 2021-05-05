# Biblioteca para leer los datos
import pandas as pd

# Método para escribir un dataFrame en un nuevo archivo csv
# @param nombre del archivo
# @param data frame que se guardará
def genera_csv(nombre, dataFrame):
    dataFrame.to_csv(nombre, header = True, index = False)

# Nombres de todas las base de datos que contamos
bases_de_datos2021 = ["2021CO.csv", "2021O3.csv", "2021SO2.csv"]
bases_de_datos2020 = ["./BasesDatos2020/2020CO.csv", "./BasesDatos2020/2020O3.csv", "./BasesDatos2020/2020SO2.csv"]

# Método para obtener el promedio de datos de una lista
def averg(lista):
    prom = 0
    contador = 0
    for elem in lista:
        if(elem <= 1 and elem >= 0):
            prom += elem
            contador += 1
    if(contador > 0):
        return prom/contador
    else:
        return 100

# Diccionario con las claves de la ciudad de México
claves_ciudad_mexico = [
    "AJU", "AJM", "BJU", "CAM", "CCA", "TEC", "COR",
    "CUA", "DIC", "EAJ", "EDL", "GAM", "HGM", "IZT",
    "LAA", "IBM", "LOM", "MER", "MGH", "MPA", "MCM",
    "PED", "SNT", "SFE", "SAC", "TAH", "UIZ", "UAX"
]

nombre = bases_de_datos2020[2]
'''
data = pd.read_csv(nombre)

# Nos quedaremos también con las fechas para poderlas colocar en el data set
fechas = data["FECHA"].unique()

data_set_final = {"FECHA":[], "PROMEDIO":[]}
variables_db = data.keys()

for fecha in fechas:
    contador = 0
    promedio = 0
    # Vamos a obtener los promedios de todos los centros de monitoreo atmosférico de la ciudad de méxico para la iésima fecha
    for clave in claves_ciudad_mexico:

        if(clave in variables_db):
            a = averg(data[ (data["FECHA"]==fecha)][(clave)])
            if(a < 100):
                promedio += a
                contador += 1

    if(contador != 0):
        promedio_fecha = promedio/contador
        data_set_final["FECHA"].append(fecha)
        data_set_final["PROMEDIO"].append(promedio_fecha)

dataFrame = pd.DataFrame(data_set_final)
# Generamos el archivo csv para guardarlo
genera_csv(nombre.split(".")[0]+"_promedios.csv", dataFrame)
'''

# Vamos a agrupar los datos generados en una sola base de datos
data_co = pd.read_csv("promedios2020CO.csv")
data_o3 = pd.read_csv("promedios2020O3.csv")
data_so2= pd.read_csv("promedios2020SO2.csv")

fechas = data_co["FECHA"].unique()

data_frame_final = {"FECHA":[], "promedioCO":[], "promedioO3":[], "promedioSO2":[]}
i = 0
for fecha in fechas:
    data_frame_final["FECHA"].append(fecha)
    try:
        data_frame_final["promedioCO"].append(data_co[data_co["FECHA"] == fecha]["PROMEDIO"].tolist()[0])
    except:
        data_frame_final["promedioCO"].append(None)
    try:
        data_frame_final["promedioO3"].append(data_o3[data_o3["FECHA"] == fecha]["PROMEDIO"].tolist()[0])
    except:
        data_frame_final["promedioO3"].append(None)
    try:
        data_frame_final["promedioSO2"].append(data_so2[data_so2["FECHA"] == fecha]["PROMEDIO"].tolist()[0])
    except:
        data_frame_final["promedioSO2"].append(None)
    i+= 1

dataFrame = pd.DataFrame(data_frame_final)

print(dataFrame.head())
genera_csv("promedios2020Final.csv", dataFrame)


#densidadPoblacional acumuladoDeEnfermos NúmeroDeEnfermosActual NúmeroDefunciones NúmeroNuevosCasos promedioCO promedioSo2 promedioO3 tIncidenciaCovid19

#Hacer modelos de regresión lineal.

# Tiempo promedio que la gente pasa en el súper, mercados, algún lugar donde se acumulen personas, al cine, a restaurantes.

'''
Toerema de Guass-Markov El estimador por mínimos cuadrados es el mejor estimador de un modelo
en donde tenemos : Y = bX + epsilon(error)
1) Errores ~ N(o, sigma cuadrada) => E[ei] = 0
2) Var[ei] = sigma cuadrada
3) Cov(ei, ej) = 0 para toda i != j

Turbin Watson prueba la correlación en los errores

mínimos cuadrados


'''
