import pandas as pd

from matplotlib import pyplot as plt

data = pd.read_csv("./BasesDatos/21RAMA/NOX(2020-2021).csv")

datos_covid = pd.read_csv("./CiudadMexicoDatosFinales.csv")

gas = "NOX"

fechas = data["FECHA"].unique()

#estaciones = data.keys()[2:]

#estaciones = ["BJU","CAM","CCA","SFE","TAH","TLA","UAX","UIZ"]

estaciones = ["MER", "SAC"]

for estacion in estaciones:
    data_frame = {"Fecha":[], "promedioGas"+gas:[], "Infectados":[], "Defunciones":[]}

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

        if(len(datos_covid[datos_covid["Fecha"]==fecha_modificada]["Infectados"].tolist()) == 0):
            break

        data_frame["promedioGas"+gas].append(promedio*100)
        data_frame["Fecha"].append(fecha)
        data_frame["Infectados"].append( datos_covid[datos_covid["Fecha"]==fecha_modificada]["Infectados"].tolist()[0] )
        data_frame["Defunciones"].append( datos_covid[datos_covid["Fecha"]==fecha_modificada]["Defunciones"].tolist()[0] )

    df = pd.DataFrame(data_frame)
    df.to_csv(estacion+gas+".csv", header = True, index = False)

    plt.plot(data_frame["promedioGas"+gas])
    plt.plot(data_frame["Infectados"])
    plt.plot(data_frame["Defunciones"])
    plt.title(estacion)
    plt.savefig(estacion+".png")
    plt.clf()

print(df)



# ESTACIONES PROMINENTES: {'CCA', 'CAM', 'SFE', 'TAH', 'UIZ', 'UAX', 'TLA'}

# Vamos a escoger una estacion y el número de infectados y vamos a calcular Pearson y una regresión Lineal
