import pandas as pd

import numpy as np

from matplotlib import pyplot as plt

data = pd.read_csv("baseDatosFINAL(ANALISISCONTAMINACION)EST (ApartirFebrero).csv")

estaciones_gases = data.keys()[39:].tolist()

def estaciones_activas(gas):
    estaciones = []
    for estacion in estaciones_gases:
        if(gas in "_"+estacion.split("_")[1] and len(gas) == len("_"+estacion.split("_")[1])):
            estaciones.append(estacion)
    return estaciones

def promedios(estaciones):
    df = {}
    for estacion in estaciones:
        df[estacion] = data[estacion].tolist()
    df = pd.DataFrame(df)
    df = df.replace(0, np.NaN)
    df["Promedio"] = df.mean(axis = 1)
    return df["Promedio"].tolist()

# Todas las estaciones que están asociadas a la medición de un gas
estaciones_por_gas = {}
gases = ["_CO", "_NO2", "_NOX", "_NO", "_PM10", "_PM25", "_SO2", "_O3"]

for gas in gases:
    estaciones_por_gas[gas] = estaciones_activas(gas)

# Variables epidemiológicas
var_epi = data.keys()[3:39].tolist()

var_epi = ['Letalidad(123)', 'Letalidad(3)', 'Mortalidad(123)', 'Mortalidad(3)', 'P_Hospitalizados', 'Indice_positividad']

'''
Función para extraer únicamente las estaciones particulares deseadas
@param es un arreglo con la clave de las estaciones deseadas para realizar el análisis
@param gas que se pretende estudiar
@param conjunto de todas las estaciones del cual se hará la segmentación
'''
def extraer_estaciones(estaciones_deseadas, gas,  conjunto_estaciones):
    estaciones = []
    gas = "_"+gas
    for estacion in conjunto_estaciones[gas]:
        est = estacion.split("_")[0]
        if est in estaciones_deseadas:
            estaciones.append(estacion)
    return estaciones

# Obtiene los promedios para las estaciones de interés
'''
Ahora solo tengo que jugar con las combinaciones de las estaciones, obtener el promedio y comparar
con todas las variables epidemiológicas
'''

# Función para generar el conjunto potencia
def potencia(conjunto):
    return potencia_recursiva([], conjunto)

# Función recursiva para obtener el conjunto potencia
def potencia_recursiva(actual, conjunto):
    if(conjunto):
        return potencia_recursiva(actual, conjunto[1:]) + potencia_recursiva(actual + [conjunto[0]], conjunto[1:])
    return [actual]

# Función que genera los promedios con base en la combinación de estaciones
def genera_promedios_combinaciones(conjunto_potencia):
    promedios_l = {}
    for conjunto in conjunto_potencia:
        p = promedios(conjunto)
        promedios_l[str(conjunto)] = p
    return promedios_l


'''
# Manera de extraer ciertas estaciones de interés
estaciones_interes =  estaciones_por_gas["_PM10"] #extraer_estaciones(estaciones_por_gas["_PM10"], "PM10", estaciones_por_gas)
#estaciones_interes =  extraer_estaciones(["BJU"], "PM10", estaciones_por_gas)

#Estos son los promedios tomando en cuenta todas las combinaciones posibles dadaas ciertas estaciones
pot = potencia(estaciones_interes)

# Vamos a guardar en un documento la lista con el conjunto potencia
arch = ""

for conjunto in pot:
    for elemento in conjunto:
        arch += elemento + ","
    arch += "\n"

resultado = open("pm10_potencia", "w")
resultado.write(arch)
resultado.close()

#lista_promedios_combinaciones = genera_promedios_combinaciones(pot)
'''

'''
Ahora tenemos que cruzar las variables de comorbilidades con cada promedio
Realizando una prueba estadística. La idea es quedarnos con las combinaciones de estaciones que nos entreguen
mayor significancia estadística.
'''


def tendencia(X, Y):
    if(len(X) != len(Y)):
        return
    arr = []
    for i in range(len(X)-1):
        # Ambos crecieron
        if( (X[i+1] - X[i]) > 0 and (Y[i+1] - Y[i]) > 0 ):
            arr.append(1)
        elif( (X[i+1] - X[i]) < 0 and (Y[i+1] - Y[i]) < 0  ):
            arr.append(1)
        elif( (X[i+1] - X[i]) == 0 and (Y[i+1] - Y[i]) == 0   ):
            arr.append(1)
        else:
            arr.append(0)
    return arr

def tendencia_I_D_M(X):
    arr = []
    for i in range(len(X) -1):
        if(X[i+1] > X[i]):
            arr.append("I")
        elif(X[i+1] < X[i]):
            arr.append("D")
        else:
            arr.append("M")
    return arr

# Función para ver la cadena con valores consecutivos más larga
def cadena_ma_larga(arreglo):
    max_len_intervalo = 0
    max_cont = 0
    for i in range(len(arreglo)):
        if(max_cont > max_len_intervalo):
            max_len_intervalo = max_cont
        if(arreglo[i] == 1):
            max_cont += 1
        elif(arreglo[i] == 0):
            max_cont = 0
    return max_len_intervalo


#plt.plot([i for i in range(len(data["Infectados(3)"])-1)], y)


# Función para imprimir de una manera legible la lista con los indicadores de I, D, M
def imprimir_lista_I_D_M(lista):
    i = 0
    for elemento in lista:
        if(i % 25 == 0):
            print("\n", end="")
        print(elemento, end="")
        i += 1

# Función que va a "normalizar" la lista de indicadores de I, D, M con base en las siguientes reglas:
'''
Problema: cómo se seleccionan los intervalos para irlos modificando, el cálculo del intervalo (i+1) va a depender de la cadena inicial o de la cadena modificada
en la iteración (i) ?

Centrales

1. X X Y X X = X X X X X
2. X X X Y X X = X X X X X X X
3. X X Y X X X = X X X X X X X
Extremos

4. X X X Y X = X X X X X
5. X Y X X X = X X X X X

Problema: Se puede perder información

Ejemplo: (Subdividimos por semanas)

I D D I D I D     |       I D D I D I D    |     I D I D I D D      |      I D D I

I D D D D D D     |       I D D D D D D    |     I D D D D D D      |      I D D D


Propuesta utilizando la moda:

I D D I D I D     |       I D D I D I D    |     I D I D I D D      |      I D D I

                                    D | D | D | I

Propuesta utilizando la moda y la subdivisión en intervalos de 3 letas:

I D D    I D I    D I D    D I D    I D I    D I D    I D D    I D D    I
     |
                            D | I | D | D | I | D | D | D | I

'''
# Método que nos dice la frecuencia
def frecuencia_I_D_M(tercia):
    frec = {"D":0, "M": 0, "I":0}
    for elemento in tercia:
        frec[elemento] += 1
    return max(frec, key=frec.get)


# Implementación de la propuesta utilizando la moda e intervalos de 3 letras
def moda_tres(lista):
    resultado = []
    residuo = len(lista) % 3
    for i in range(0, len(lista)- residuo, 3):
        r = frecuencia_I_D_M([lista[i], lista[i+1], lista[i+2]])
        resultado.append(r)
    return resultado

'''
# Aquí nos está diciendo que la cadena más larga de variables 1 consecuentes es 8 para las variables de Infectados(3) y TIncidencia(3)
imprimir_lista_I_D_M(tendencia_I_D_M(data["Hospitalizados"].tolist()))
imprimir_lista_I_D_M(tendencia_I_D_M(promedios(estaciones_por_gas["_PM10"])))


# Ahora vamos a imprimir las mismas listas pero procesadas
print("\nProcesando listas con método de MODA-3 ... \n")

i_d_m_hospitalizados = moda_tres(tendencia_I_D_M(data["Hospitalizados"].tolist()))
i_d_m_pm10 = moda_tres(tendencia_I_D_M(promedios(estaciones_por_gas["_PM10"])))

imprimir_lista_I_D_M(i_d_m_hospitalizados)
imprimir_lista_I_D_M(i_d_m_pm10)

'''
# Ahora vamos a identificar la subcadena de coincidencia mayor
def subcadena_mayor(lista1, lista2):
    mayor = 0
    subcad_me_larga = 0
    # Índice en donde coindicen
    indice = 0
    for i in range(0, len(lista1)):
        if(subcad_me_larga > mayor):
            mayor = subcad_me_larga
            indice = i
        if(lista1[i] != lista2[i]):
            subcad_me_larga = 0
        else:
            subcad_me_larga += 1

    # En este caso, nos dio 6, eso significa que en un periodo de 3 * 6 días, se siguió una tendencia similar. Buscamos hallar la combinación de dos variables que maximice este valor
    return mayor, indice - mayor

#print(subcadena_mayor(i_d_m_pm10, i_d_m_hospitalizados))
'''

# Algoritmo para obtener el índice de indice_equi_tendencia por caca posible combinación entre todas las estaciones que registran pm10

for variable in var_epi:
    # Estructura de datos que contendrá el indice_equi_tendencia para cada combinación de estaciones junto con alguna variable epidemiológica
    diccionario_indices_equi_tendencias = {"clave":[], "indice_equi_tendencia":[], "indice_posicion":[]}

    # Vamos a leer el archivo con el conjunto potencia
    conjunto_potencia_pm10 = open("pm10_potencia.txt")

    variable_epidemiologica = data[variable].tolist()
    i_d_m_comorbilidad = moda_tres(tendencia_I_D_M(variable_epidemiologica))

    for conjunto in conjunto_potencia_pm10:
        #print("Procesando "+variable+" - "+conjunto, end="")
        # Aquí es donde vamos a analizando cada promedio con cada variable epidemiológica
        # Tenemos que hallar una manera inteligente de quedarnos con aquellas que den buena significancia estadística
        combinacion_estaciones_gas = promedios(conjunto.split(",")[:-1])
        # Aquí es donde viene el análisis propuesto, ya sea geométrico o estadístico
        # También podemos realizar lo siguiente:
        i_d_m_promedio_gas = moda_tres(tendencia_I_D_M(combinacion_estaciones_gas))
        indice_equi_tendencia, indice = subcadena_mayor(i_d_m_comorbilidad, i_d_m_promedio_gas)
        #print(" "+str(indice_equi_tendencia)+" - "+str(indice))
        # Registrar aquellos que tengan un mayor valor para elp  indice_equi_tendencia
        diccionario_indices_equi_tendencias["clave"].append(str(conjunto)+"-"+variable)
        diccionario_indices_equi_tendencias["indice_equi_tendencia"].append(indice_equi_tendencia)
        diccionario_indices_equi_tendencias["indice_posicion"].append(indice)

    print("Generando DataFrame para "+variable+" ... ")
    df = pd.DataFrame(diccionario_indices_equi_tendencias)
    df.to_csv("./PruebasCoeficienteTendencia/"+variable+".csv", header = True, index = False)

'''
