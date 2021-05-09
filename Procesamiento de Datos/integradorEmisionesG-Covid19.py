'''
Programa que va a integrar la información de las emisiones de gases registradas en una alcaldía de la ciudad de méxico
con los datos de covid-19 registrados para esa alcaldía: infectados, acumulado, tasa de incidencia, curados, etc.
'''
import pandas as pd

# Datos de los centros de monitoreo que contamos
centros_monitoreo = pd.read_csv("alcaldias_cdmx.csv")
# Datos de las emisiones de un cierto tipo de gas para los centros de monitoreo que contamos. Estos datos son generados por el programa generarPromediosEstaciones.py
emisiones = pd.read_csv("promediosGasesCOEstacionesMonitoreo.csv")
# Datos procesados que indican la situación pandémica del covid-19 en la ciudad de méxico
datos_covid = pd.read_csv("datosCOVID-19CiudadMexico.csv")

# Nos quedamos con las claves de las alcaldías (no repetidas)
claves_alcaldias = centros_monitoreo["MUNICIPIO_RES"].unique().tolist()

# Nos quedamos con los nombres de las alcaldías (no repetidos)
nombres_alcaldias = {}
for clave in claves_alcaldias:
    if(not (clave in nombres_alcaldias)):
        nombres_alcaldias[clave] = centros_monitoreo[centros_monitoreo["MUNICIPIO_RES"]==clave]["Delegacion"].tolist()[0]

fechas = emisiones["Fecha"].unique().tolist()

# Vamos a generar un .csv por cada alcaldía
for clave in claves_alcaldias:
    data_frame = {"Fecha":fechas, "promedioGas":[], "Infectados":[], "Defunciones":[], "Hospitalizados":[], "Acumulado":[], "TIncidencia":[], "Mortalidad":[], "Letalidad":[],"Poblacion":[], "DensidadP":[]}

    # Obtenemos las estaciones que están agrupadas en la misma acaldía
    estaciones = centros_monitoreo[centros_monitoreo["MUNICIPIO_RES"]==clave]["Estacion"].tolist()
    densidad_pob = centros_monitoreo[centros_monitoreo["MUNICIPIO_RES"]==clave]["Densidad_pob"].tolist()[0]
    poblacion = centros_monitoreo[centros_monitoreo["MUNICIPIO_RES"]==clave]["Poblacion"].tolist()[0]
    print("La delegación "+nombres_alcaldias[clave]+" tiene como centros a: ", end=" ")
    print(estaciones)

    for fecha in fechas:

        # Vamos a reconstruir la fecha
        componentes_fecha = fecha.split("/")
        if(len(componentes_fecha[0]) == 1):
            componentes_fecha[0] = "0"+componentes_fecha[0]
        if(len(componentes_fecha[1]) == 1):
            componentes_fecha[1] = "0"+componentes_fecha[1]
        fecha_modificada = componentes_fecha[2]+"-"+componentes_fecha[0]+"-"+componentes_fecha[1]


        # 1. Obtener los promedios de las estaciones que son relativas a una misma alcaldía, por día.
        promedio_iesimo_dia_sin_cero = 0
        promedio_iesimo_dia_con_cero = 0
        denominador = 0
        for estacion in estaciones:

            # Caso en donde no consideramos al cero como medida
            dato = emisiones[emisiones["Fecha"]==fecha][estacion].tolist()[0]
            if(dato != 0):
                denominador += 1
                promedio_iesimo_dia_sin_cero += dato

            # Caso en donde consideramos al 0 como medida
            promedio_iesimo_dia_con_cero += dato

        # Caso en donde no consideramos al cero como medida
        if(denominador != 0):
            promedio_iesimo_dia_sin_cero *= (1/denominador)
        else:
            promedio_iesimo_dia_sin_cero = 0
        # Caso en donde consideramos al 0 como medida
        promedio_iesimo_dia_con_cero *= (1/len(estaciones))

        # 2. Obtenemos los datos de infectados para ese día para esa alcaldía
        infectados = datos_covid[(datos_covid["MUNICIPIO_RES"] == clave) & (datos_covid["Fecha"] == fecha_modificada)]["Infectados"].tolist()[0]
        # 3. Obtenemos los datos de defunciones para ese día para esa alcaldía
        defunciones = datos_covid[(datos_covid["MUNICIPIO_RES"] == clave) & (datos_covid["Fecha"] == fecha_modificada)]["Defunciones"].tolist()[0]
        # 4. Obtenemos la tasa de incidencia para ese día para esa alcaldía
        tincidencia = datos_covid[(datos_covid["MUNICIPIO_RES"] == clave) & (datos_covid["Fecha"] == fecha_modificada)]["TIncidencia"].tolist()[0]
        # 5. Obtenemos el acumulado de personas enfermas en tiempo real
        acumulado = datos_covid[(datos_covid["MUNICIPIO_RES"] == clave) & (datos_covid["Fecha"] == fecha_modificada)]["Acumulado"].tolist()[0]
        # 6. Obtenemos la cantidad de Hospitalizados
        hospitalizados = datos_covid[(datos_covid["MUNICIPIO_RES"] == clave) & (datos_covid["Fecha"] == fecha_modificada)]["Hospitalizados"].tolist()[0]

        data_frame["Infectados"].append(infectados)
        data_frame["Defunciones"].append(defunciones)
        data_frame["Acumulado"].append(acumulado)

        #data_frame["promedioGas"].append(promedio_iesimo_dia_sin_cero)
        data_frame["promedioGas"].append(promedio_iesimo_dia_con_cero)

        data_frame["TIncidencia"].append(tincidencia)
        data_frame["Poblacion"].append(poblacion)
        data_frame["DensidadP"].append(densidad_pob)
        data_frame["Hospitalizados"].append(hospitalizados)

        # Vamos a realizar cálculos de las tasas de letalidad y de mortalidad
        mortalidad = defunciones/poblacion
        if(acumulado != 0):
            letalidad  = defunciones/acumulado
        else:
            letalidad = 0
        data_frame["Mortalidad"].append(mortalidad * 100000)
        data_frame["Letalidad"].append(letalidad * 10000)




    data_frame = pd.DataFrame(data_frame)
    data_frame.to_csv(nombres_alcaldias[clave]+"_emisiones_covid19.csv",header=True, index=False)
