import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

data_sac = pd.read_csv("SACNOX.csv")
x = data_sac["promedioGasNOX"].tolist()
y = data_sac["Infectados"].tolist()

#data_mer = pd.read_csv("MERNOX.csv")
#x = data_mer["promedioGasNOX"].tolist()
#y = data_mer["Infectados"].tolist()

plt.scatter(x, y)
plt.show()

X = [[dato] for dato in x]

print(len(X))

# Vamos a obtener datos para hacer el test
datos_X_train = X[:-20]
datos_X_test = X[-20:]

print(len(datos_X_train))
print(len(datos_X_test))

# Dividimos los valores que intentaremos predecir en dos clases
datos_y_train = y[:-20]
datos_y_test = y[-20:]

# Creamos el objeto para llevar a cabo el análisis
regr = linear_model.LinearRegression()


regr.fit(datos_X_train, datos_y_train)

# Vamos a hacer predicciones utilizando los datos de prueba
datos_y_pred = regr.predict(datos_X_test)

# Coeficientes del modelo lineal
print('Coefficients: \n', regr.coef_)
# Error cuadrático medio
print('Mean squared error: %.2f'
      % mean_squared_error(datos_y_test, datos_y_pred))
# Coeficiente de determinación
print('Coefficient of determination: %.2f'
      % r2_score(datos_y_test, datos_y_pred))


plt.scatter(datos_X_test, datos_y_test,  color='black')
plt.plot(datos_X_test, datos_y_pred, color='blue', linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()
