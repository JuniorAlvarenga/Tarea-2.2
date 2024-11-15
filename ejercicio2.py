# -*- coding: utf-8 -*-
"""Ejercicio2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aLQSAAwRGkOnZ8p2EkZ_uoPOFstBfIvT
"""

#Mismos Datos pero ahora usando DecisionTreeRegressor
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Cargar los datos
df = pd.read_csv('./housing.csv')
df = df.dropna()  # Eliminar registros con valores nulos

# Crear algunas características adicionales
df['rooms_per_person'] = df['total_rooms'] / df['population']  # Proporción de habitaciones por población
df['bedrooms_per_room'] = df['total_bedrooms'] / df['total_rooms']  # Proporción de dormitorios por habitación
df['population_density'] = df['population'] / (df['latitude'] * df['longitude'])  # Densidad de población
df['value_per_room'] = df['median_house_value'] / df['total_rooms']  # Valor por habitación
df['value_per_bedroom'] = df['median_house_value'] / df['total_bedrooms']  # Valor por dormitorio
df['rooms_times_population'] = df['total_rooms'] * df['population']  # Interacción de habitaciones y población


# Convertir variable categórica en dummies
df = pd.concat([df, pd.get_dummies(df['ocean_proximity'], dtype=int)], axis=1)
df.drop('ocean_proximity', axis=1, inplace=True)
#df.drop('total_bedrooms', axis=1, inplace=True)
df.drop('households', axis=1, inplace=True)# Tiene una colinealidad con total_bedrooms de un 0.98, esto empeora las predicciones


# Seleccionar solo las características con alta correlación
df.corr()['median_house_value'].sort_values(ascending=False)

# Método IQR para detectar outliers
Q1 = df.quantile(0.15)
Q3 = df.quantile(0.85)
IQR = Q3 - Q1

# Filtrar los outliers: eliminar los registros fuera del rango [Q1 - 1.5*IQR, Q3 + 1.5*IQR] CON 2.0 SE OBTUVO MEJORES RESULTADOS!!
df_no_outliers = df[~((df < (Q1 - 2.0 * IQR)) | (df > (Q3 + 2.0 * IQR))).any(axis=1)]

# Separar características y etiqueta
X = df_no_outliers.drop('median_house_value', axis=1)
y = df_no_outliers['median_house_value']


# Dividir el conjunto de datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Crear y entrenar el modelo de Árbol de Decisión
model = DecisionTreeRegressor(random_state=42)
model.fit(X_train, y_train)

# Evaluar el modelo
y_pred = model.predict(X_test)

# Calcular el RMSE
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# Calcular el score
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

# Mostrar resultados
print(f"RMSE: {rmse}")
print(f"Score en entrenamiento: {train_score}")
print(f"Score en prueba: {test_score}")

modelo = DecisionTreeRegressor(max_depth=5, min_samples_split=10, min_samples_leaf=5)  # Limitar la profundidad y las muestras mínimas
modelo.fit(X_train, y_train)

# Realizar la predicción
y_pred = modelo.predict(X_test)

# Graficar el árbol de decisión
plt.figure(figsize=(12,8))
plot_tree(modelo, filled=True, feature_names=X_train.columns, max_depth=3, fontsize=10)  # Limitar la profundidad de la visualización
plt.show()