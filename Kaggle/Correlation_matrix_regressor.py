# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 18:41:11 2025

@author: juanmoreno
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def Custom_regressor(dataframe, target):
    """
    Función que realiza lo siguiente:
      1) Ajusta una regresión lineal con las variables independientes para obtener
         los coeficientes (wₓ) y el intercepto.
      2) Calcula la media (xₘ) de cada variable independiente.
      3) Predice, para cada observación, usando la fórmula:
         
         Y_pred = intercept + sum_over_x [ wₓ * x_i + x_i * ((x_i - xₘ) / xₘ) ]
         
         donde:
           - wₓ es el coeficiente obtenido por regresión lineal para la variable x.
           - x_i es el valor de la variable x en la observación i.
           - xₘ es la media de la variable x.
      4) Genera dos scatterplots juntos (lado a lado): uno con los datos reales y
         otro con las predicciones, para facilitar la comparación.
    
    Parámetros:
    -----------
    dataframe : pd.DataFrame
        DataFrame que contiene las variables independientes y la variable dependiente.
    target : str
        Nombre de la variable dependiente.
        
    Retorna:
    --------
    results : dict
        Diccionario con los siguientes elementos:
          - 'coefficients': pd.Series con los coeficientes obtenidos por regresión.
          - 'intercept': Valor del intercepto del modelo.
          - 'means': pd.Series con la media de cada variable independiente.
          - 'predictions': pd.Series con las predicciones calculadas.
          - 'metrics': pd.DataFrame con las métricas de evaluación (RMSE, MAE, R²).
          - 'prediction_df': pd.DataFrame con las columnas 'Actual' y 'Predicted'.
    """
    
    # Verificar que la columna target exista
    if target not in dataframe.columns:
        raise ValueError(f"La columna target '{target}' no se encuentra en el DataFrame.")
    
    # Definir variables independientes: todas las columnas excepto el target
    independents = [col for col in dataframe.columns if col != target]
    if len(independents) == 0:
        raise ValueError("No se encontraron variables independientes en el DataFrame.")
    
    # Separar variables independientes (X) y la dependiente (y)
    X = dataframe[independents]
    y = dataframe[target]
    
    # 1) Ajustar una regresión lineal
    model = LinearRegression()
    model.fit(X, y)
    coefficients = pd.Series(model.coef_, index=independents, name="Coeficiente")
    intercept = model.intercept_
    
    # 2) Calcular la media de cada variable independiente
    means = X.mean()
    
    # 3) Calcular la predicción personalizada para cada observación
    # La aportación de cada variable: wₓ * x_i + x_i * ((x_i - xₘ)/xₘ)
    contributions = pd.DataFrame()
    for col in independents:
        w = coefficients[col]
        x = X[col]
        x_m = means[col]
        # Evitamos división por cero (en caso improbable de que x_m sea 0)
        if x_m == 0:
            raise ValueError(f"La media de la variable {col} es 0, no se puede dividir por 0.")
        contributions[col] = x * (w + np.log(abs((x - x_m) / x_m)))
    
    # La predicción final es la suma de las aportaciones de todas las variables + intercepto
    predictions = contributions.sum(axis=1) + intercept
    
    # 4) Calcular las métricas de evaluación
    rmse = np.sqrt(mean_squared_error(y, predictions))
    mae = mean_absolute_error(y, predictions)
    r2 = r2_score(y, predictions)
    
    metrics_df = pd.DataFrame({
        "Métrica": ["RMSE", "MAE", "R²"],
        "Valor": [rmse, mae, r2]
    })
    
    # Crear un DataFrame con los valores reales y predichos
    prediction_df = pd.DataFrame({
        "Actual": y,
        "Predicted": predictions
    }, index=dataframe.index)
    
    # 5) Generar dos scatterplots lado a lado para comparar los datos reales y las predicciones
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))
    
    # Scatterplot de los datos reales (por ejemplo, vs. índice)
    axs[0].scatter(dataframe.index, y, color='blue', alpha=0.7)
    axs[0].set_title("Datos Reales")
    axs[0].set_xlabel("Índice")
    axs[0].set_ylabel(target)
    axs[0].grid(True)
    
    # Scatterplot de las predicciones (por ejemplo, vs. índice)
    axs[1].scatter(dataframe.index, predictions, color='green', alpha=0.7)
    axs[1].set_title("Predicciones")
    axs[1].set_xlabel("Índice")
    axs[1].set_ylabel("Predicted " + target)
    axs[1].grid(True)
    
    plt.tight_layout()
    plt.show()
    
    results = {
        "coefficients": coefficients,
        "intercept": intercept,
        "means": means,
        "predictions": predictions,
        "metrics": metrics_df,
        "prediction_df": prediction_df
    }
    
    return results

# Ejemplo de uso:
if __name__ == "__main__":
    np.random.seed(42)
    n = 100
    # Generamos un DataFrame de ejemplo
    df_example = pd.DataFrame({
        'X1': np.random.normal(10, 2, n),
        'X2': np.random.normal(20, 5, n),
        'X3': np.random.normal(30, 3, n)
    })
    # Se crea la variable dependiente con cierta relación lineal y algo de ruido
    df_example['Y'] = 0.3 * df_example['X1'] + 0.5 * df_example['X2'] + 0.2 * df_example['X3'] + np.random.normal(0, 1, n)
    
    results = Custom_regressor(df_example, target='Y')
    
    print("\nCoeficientes obtenidos:")
    print(results["coefficients"])
    
    print("\nIntercepto:")
    print(results["intercept"])
    
    print("\nMétricas de evaluación:")
    print(results["metrics"])
    
    print("\nDataFrame de predicciones (primeras 5 filas):")
    print(results["prediction_df"].head())
