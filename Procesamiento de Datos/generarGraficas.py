from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates

import numpy as np
import pandas as pd

plt.style.use('seaborn')

data = pd.read_csv("baseDatosFINAL(ANALISISCONTAMINACION)EST (ApartirFebrero).csv")

# Le pasamos la variable epidemiológica a graficar y el promedio del gas (nosotros tenemos que generarlo por todas las posibles combinaciones)
# Genera una única gráfica
def generaGrafica(variable_epi, y2):

    fechas = [datetime(int(fecha.split("-")[0]), int(fecha.split("-")[1]), int(fecha.split("-")[2])) for fecha in data["Fecha"].tolist()]

    y1 = data[variable_epi].tolist()

    x = fechas

    fig = plt.figure()

    ax1 = fig.add_subplot(111)

    ax1.plot(x, y1)

    ax1.set_ylabel(variable_epi)

    ax1.set_title(variable_epi+" y emisiones de PM10 :")

    ax2 = ax1.twinx()

    ax2.plot(x, y2, 'r')

    ax2.set_ylabel('Emisiones de PM10')

    ax2.set_xlabel('Fechas')

    plt.gcf().autofmt_xdate()

    date_format = mpl_dates.DateFormatter('%b, %d %Y')

    plt.gca().xaxis.set_major_formatter(date_format)

    fig.legend(labels = (variable_epi, 'Emisiones PM10'), loc='lower center')

    fig.set_size_inches(18.5, 10.5)

    #plt.savefig("./graficas_pm10/"+variable_epi+".jpg", pad_inches=0.1)

    #plt.clf()

    plt.show()

# Función para obtener los promedios con base en las estaciones
def promedios(estaciones):
    df = {}

    for estacion in estaciones:

        df[estacion] = data[estacion].tolist()

    df = pd.DataFrame(df)

    df = df.replace(0, np.NaN)

    df["Promedio"] = df.mean(axis = 1)

    return df["Promedio"].tolist()

estaciones_gases = data.keys()[39:].tolist()

# Función para obtener las estaciones que registran un gas en particular
def estaciones_activas(gas):
    estaciones = []

    for estacion in estaciones_gases:

        if(gas in "_"+estacion.split("_")[1] and len(gas) == len("_"+estacion.split("_")[1])):

            estaciones.append(estacion)

    return estaciones

# variable_epi es la variable epidemiológica de interés y estaciones es un arreglo con estaciones (no mayor a 6 de tamaño)
# Genera un plot con subplots de varias combinaciones
def multi_graficos(variable_epi, estaciones):

    promedio_gas = promedios(estaciones_de_combinacion)

    fig = plt.figure(figsize=(15, 15))

    fig.tight_layout()

    colores = ["yellow", "black", "green", "orange", "magenta", "blue", "black", "white"]



    x = [datetime(int(fecha.split("-")[0]), int(fecha.split("-")[1]), int(fecha.split("-")[2])) for fecha in data["Fecha"].tolist()]
    y = data[variable_epi].tolist()

    # si es 7, se grafican seis, si es 6 se grafican 5, si es 4 se grafican tres
    for i in range(1, len(estaciones)+1):

        es = estaciones[i-1].split(",")[:-1]
        prom_estaciones = promedios(es)

        y1 = prom_estaciones

        ax = plt.subplot(2, 3, i)
        ax2 = ax.twinx()
        ax2.plot(x, y, 'r')
        ax.plot(x, y1, color=colores[i])

        ax.set_ylabel(variable_epi)
        ax.set_title(variable_epi+" y emisiones de PM10 :")
        ax2.set_ylabel('Emisiones de PM10')

        plt.gcf().autofmt_xdate()
        date_format = mpl_dates.DateFormatter('%b, %d %Y')
        plt.gca().xaxis.set_major_formatter(date_format)

        ax2.set_xlabel('Fechas')
        ax.set_title('Gráfica de combinación '+str(i))

    plt.tight_layout(pad=3.0)

    plt.show()

# Estaciones resultado del programa de analisisPrueba.py

veinte = ['ACO_PM10,AJM_PM10,CUA_PM10,HGM_PM10,SAG_PM10,VIF_PM10,\n-Mortalidad(3)',
'AJM_PM10,CUA_PM10,HGM_PM10,SAG_PM10,VIF_PM10,\n-Mortalidad(3)',
 'ACO_PM10,AJM_PM10,CUA_PM10,GAM_PM10,HGM_PM10,SAG_PM10,VIF_PM10,\n-Mortalidad(3)',
 'ACO_PM10,AJM_PM10,CUA_PM10,GAM_PM10,SAG_PM10,VIF_PM10,\n-Mortalidad(3)',
 'ACO_PM10,AJM_PM10,CUA_PM10,SAG_PM10,VIF_PM10,\n-Mortalidad(3)',
 'AJM_PM10,CUA_PM10,GAM_PM10,HGM_PM10,SAG_PM10,VIF_PM10,\n-Mortalidad(3)',
 'AJM_PM10,CUA_PM10,SAG_PM10,VIF_PM10,\n-Mortalidad(3)',
 'AJM_PM10,CUA_PM10,GAM_PM10,SAG_PM10,VIF_PM10,\n-Mortalidad(3)']

diecinueve = ['AJM_PM10,BJU_PM10,CUA_PM10,GAM_PM10,SAG_PM10,VIF_PM10,\n-Mortalidad(3)',
'AJM_PM10,BJU_PM10,CUA_PM10,GAM_PM10,HGM_PM10,SAG_PM10,VIF_PM10,\n-Mortalidad(3)',
'AJM_PM10,BJU_PM10,CUA_PM10,HGM_PM10,SAG_PM10,VIF_PM10,\n-Mortalidad(3)',
'AJM_PM10,BJU_PM10,CUA_PM10,SAG_PM10,VIF_PM10,\n-Mortalidad(3)',
'ACO_PM10,AJM_PM10,ATI_PM10,BJU_PM10,CAM_PM10,CUA_PM10,CUT_PM10,FAC_PM10,GAM_PM10,HGM_PM10,INN_PM10,IZT_PM10,MER_PM10,PED_PM10,SAG_PM10,SFE_PM10,TAH_PM10,TLA_PM10,UIZ_PM10,VIF_PM10,\n-Mortalidad(3)',
'AJM_PM10,ATI_PM10,CAM_PM10,CUA_PM10,FAC_PM10,GAM_PM10,INN_PM10,MER_PM10,PED_PM10,TAH_PM10,TLA_PM10,VIF_PM10,\n-Mortalidad(3)']

estaciones_de_combinacion = diecinueve[0].split(",")[:-1]

variable_epi = "Mortalidad(3)"

#multi_graficos(variable_epi, veinte[:6])
multi_graficos(variable_epi, diecinueve)


#   Lo que queda por hacer:

#   1. Generar un programa que abra todos los .csv del índice de equi tendencia
#   y guarde únicamente aquellos con mayor índice
#   2. Conectar el programa del punto 1 con este script para visualizar resultados


'''
    Algoritmo para graficar de manera independiente

    for estacion in estaciones:

        est = estacion.split(",")[:-1]

        emisiones_pm10_promedio = promedios(est)

        for variable_epi in variables_epi:

            generaGrafica(variable_epi, emisiones_pm10_promedio)
'''
