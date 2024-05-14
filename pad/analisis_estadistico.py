import os
import pandas as pd
import scipy.stats as stats

class AnalisisEstadistico:
    def __init__(self, archivo_csv):
        self.archivo_csv = archivo_csv
        self.df = None

    def cargar_datos(self):
        if os.path.exists(
                self.archivo_csv):  # Reemplaza self.archivo_excel con tu variable que contiene la ruta del archivo CSV
            try:
                self.df = pd.read_csv(self.archivo_csv)  # Usa pd.read_csv para leer el archivo CSV
            except Exception as e:
                print(f"Error al cargar el archivo CSV: {e}")
        else:
            print(
                f"No se encontró el archivo CSV: {self.archivo_csv}")  # Ajusta el mensaje para indicar que es un archivo CSV

    def mostrar_datos(self):
        if self.df is not None:
            print(self.df.head())
        else:
            print("Primero carga los datos usando el método cargar_datos().")

    def resumen_estadistico(self):
        if self.df is not None:
            print(self.df.describe())
        else:
            print("Primero carga los datos usando el método cargar_datos().")

    def estadisticas_columna(self, columna):
        if self.df is not None:
            if columna in self.df.columns:
                print("Media:", self.df[columna].mean())
                print("Desviación estándar:", self.df[columna].std())
                print("Mínimo:", self.df[columna].min())
                print("Máximo:", self.df[columna].max())
            else:
                print("La columna especificada no existe en el DataFrame.")
        else:
            print("Primero carga los datos usando el método cargar_datos().")

    def prueba_normalidad(self, columna):
        if self.df is not None:
            if columna in self.df.columns:
                datos = self.df[columna]
                _, p_valor = stats.shapiro(datos)
                print(f"Prueba de Shapiro-Wilk para '{columna}':")
                print("Estadística de prueba:", _)
                print("Valor p:", p_valor)
                if p_valor > 0.05:
                    print("No se rechaza la hipótesis nula (los datos parecen seguir una distribución normal).")
                else:
                    print("Se rechaza la hipótesis nula (los datos no siguen una distribución normal).")
            else:
                print("La columna especificada no existe en el DataFrame.")
        else:
            print("Primero carga los datos usando el método cargar_datos().")

    def correlacion_pearson(self, columna1, columna2):
        if self.df is not None:
            if columna1 in self.df.columns and columna2 in self.df.columns:
                correlacion = self.df[columna1].corr(self.df[columna2])
                print(f"Coeficiente de correlación de Pearson entre '{columna1}' y '{columna2}':", correlacion)
            else:
                print("Al menos una de las columnas especificadas no existe en el DataFrame.")
        else:
            print("Primero carga los datos usando el método cargar_datos().")
    
    def correlacion_spearman(self, columna1, columna2):
        if self.df is not None:
            if columna1 in self.df.columns and columna2 in self.df.columns:
                correlacion = self.df[columna1].corr(self.df[columna2], method="spearman")
                print(f"Coeficiente de correlación de Spearman entre '{columna1}' y '{columna2}':", correlacion)
            else:
                print("Al menos una de las columnas especificadas no existe en el DataFrame.")
        else:
            print("Primero carga los datos usando el método cargar_datos().")




# Path: pad/main.py
# Compare this snippet from pad/analisis_estadistico.py:
# import os


