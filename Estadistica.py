# Implementación de algoritmos para estudiar medidas estadísticas en datos.
import math
'''
En esta clase vamos a implementar funciones de estadística básica, es decir:

    a) Promedio
    b) Moda
    c) Varianza


La idea es que cuando tengamos ya los datos clasificados:


    Cada centroide tiene sus propias coordenadas.

            C1       C2       C3

            a1       b1        c1
            a2       b2        c2
            a3       b3        c3
            a4       b4        c4
            a5       b5        c5

Queremos calcular el promedio de emisiones un gas U en los datos del centroide 1, de igual manera, queremos hacer
lo mismo para los datos del centroide 2 y del 3, y comparar esos promedios.

U obtener la moda en los datos para cada centroide y por ejemplo, concluir, los datos en el centroide 1
la moda o el intervalo para X variable es [a, b]. Todo esto es con el fin de hallar relaciones y patrones dentro de la
clasificación de datos que hicimos.


Una observación podría ser:
    Los datos en el cluster 1 se caracterizan por ser aquellos con mayor número de personas infectadas y además tener un promedio
    de emisiones de CO2 mayor a 0.8 (aquí podríamos generar la conclusión inmediata de una relación entre infectados y aumento de
    emisiones de CO2).

'''
class Estadistica:
    '''
    Método que calcula el promedio de una lista de datos
    @param lista de datos
    @return promedio de la suma de datos
    '''
    def promedio(self, valores):

        if(len(valores) == 0 ):
            return 0
        suma = 0
        for valor in valores:
            suma += valor
        return valor/len(valores)

    '''
    Método que regresa la moda redondeada a un número entero
    @param lista de valores
    @return Moda de un conjunto de datos
    '''
    def moda(self, valores):
        diccionario = {}
        for valor in valores:
            # Vamos a quedarnos con el entero mayor del número
            valor = math.ceil(valor)

            if(valor in diccionario):
                diccionario[valor] += 1
            else:
                diccionario[valor] = 1
        return max(diccionario, key=diccionario.get), max(diccionario.values())
    '''
    Método para implementar el cálculo de la varianza en un conjunto de datos
    @param conjunto de datos
    @return varianza del conjunto de datos
    '''
    def varianza(self, valores):

        if(len(valores) == 0):
            return 0
        promedio = self.promedio(valores)
        suma = 0
        for valor in valores:
            suma += math.pow((valor - promedio), 2)
        return suma/len(valores)
    '''
    Método para calcular la covarianza entre dos conjuntos de datos
    @param lista de datos X
    @param lista de datos Y
    @return covarianza entre datos X y datos Y
    '''
    def covarianza(self, valoresX, valoresY):

        if(len(valoresX) == 0 or len(valoresY) == 0 or len(valoresX) != len(valoresY)):
            return 0

        promedioX = self.promedio(valoresX)
        promedioY = self.promedio(valoresY)
        suma = 0
        for i in range(len(valoresX)):
            suma += (valoresX[i] - promedioX)*(valoresY[i] - promedioY)
        return suma/len(valoresX)
