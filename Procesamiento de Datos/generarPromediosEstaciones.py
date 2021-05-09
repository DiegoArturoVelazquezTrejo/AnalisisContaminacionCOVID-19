'''
Programa que obtiene los promedios por día de emisiones de algún gas para estaciones de monitoreo.
Es independiente a la información de COVID-19.
'''
import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_csv("./PM25(2020-2021).csv")

fechas = data["FECHA"].unique()
#estaciones = data.keys()[2:]
estaciones = ["CAM", "CCA", "MER", "PED", "SAC", "SFE", "TAH", "UAX", "UIZ"]

data_frame = {"Fecha":[]}

for estacion in estaciones:
    data_frame[estacion] = []

iteracion = 0
for estacion in estaciones:

    for fecha in fechas:

        datos = [dato for dato in data[(data["FECHA"]==fecha)][estacion].tolist() if dato != -99]
        suma_datos = sum(datos)
        if(len(datos) != 0):
            promedio = suma_datos/len(datos)
        else:
            promedio = 0

        # Vamos a reconstruir la fecha
        componentes_fecha = fecha.split("/")
        if(len(componentes_fecha[0]) == 1):
            componentes_fecha[0] = "0"+componentes_fecha[0]
        if(len(componentes_fecha[1]) == 1):
            componentes_fecha[1] = "0"+componentes_fecha[1]
        fecha_modificada = componentes_fecha[2]+"-"+componentes_fecha[0]+"-"+componentes_fecha[1]

        data_frame[estacion].append(promedio)
        if(iteracion < 1):
            data_frame["Fecha"].append(fecha)
    iteracion += 1

df = pd.DataFrame(data_frame)

df.to_csv("promediosGasesPM25EstacionesMonitoreo.csv", header = True, index = False)

print(df)

# ESTACIONES PROMINENTES: {'CCA', 'CAM', 'SFE', 'TAH', 'UIZ', 'UAX', 'TLA'}
