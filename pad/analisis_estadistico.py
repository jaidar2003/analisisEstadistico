import os
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress


class AnalisisEstadistico:
    def __init__(self, archivo_csv):
        self.archivo_csv = archivo_csv
        self.df = None

    def cargar_datos(self):
        if os.path.exists(
                self.archivo_csv):
            try:
                self.df = pd.read_csv(self.archivo_csv)
            except Exception as e:
                print(f"Error al cargar el archivo CSV: {e}")
        else:
            print(
                f"No se encontró el archivo CSV: {self.archivo_csv}")

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
                stats_list = [["Media", self.df[columna].mean()], ["Desviación estándar", self.df[columna].std()],
                              ["Mínimo", self.df[columna].min()], ["Máximo", self.df[columna].max()]]
                return stats_list
            else:
                print("La columna especificada no existe en el DataFrame.")
        else:
            print("Primero carga los datos usando el método cargar_datos().")

    @staticmethod
    def resumen_estadistico_para_grupo(grupo):
        if grupo is not None:
            print(grupo.describe())
        else:
            print("El grupo proporcionado es nulo.")

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

    def prueba_hipotesis_media(self, columna, mu):
        if self.df is not None:
            if columna in self.df.columns:
                datos = self.df[columna]
                _, p_valor = stats.ttest_1samp(datos, mu)
                print(f"Prueba de hipótesis para la media de '{columna}':")
                print("Valor de la media poblacional:", mu)
                print("Estadística de prueba:", _)
                print("Valor p:", p_valor)
                if p_valor > 0.05:
                    print("No se rechaza la hipótesis nula.")
                else:
                    print("Se rechaza la hipótesis nula.")
            else:
                print("La columna especificada no existe en el DataFrame.")
        else:
            print("Primero carga los datos usando el método cargar_datos().")

    def prueba_bondad_ajuste_normal(self, columna):
        if self.df is not None:
            if columna in self.df.columns:
                datos = self.df[columna]
                _, p_valor = stats.normaltest(datos)
                print(f"Prueba de bondad de ajuste para la normalidad en '{columna}':")
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

    def analisis_regresion_y_correlacion(self):
        if self.df is not None:
            if 'math_score' in self.df.columns and 'reading_score' in self.df.columns:
                df = self.df[['math_score', 'reading_score']].dropna()

                df['math_score'] = pd.to_numeric(df['math_score'], errors='coerce')
                df['reading_score'] = pd.to_numeric(df['reading_score'], errors='coerce')
                df = df.dropna(subset=['math_score', 'reading_score'])

                slope, intercept, r_value, p_value, std_err = linregress(df['math_score'], df['reading_score'])

                df['regression_line'] = slope * df['math_score'] + intercept

                sns.set(style="whitegrid")

                plt.figure(figsize=(10, 6))
                sns.scatterplot(x='math_score', y='reading_score', data=df, label='Datos reales')
                plt.plot(df['math_score'], df['regression_line'], color='red', label=f'Regresión lineal: y={slope:.2f}x+{intercept:.2f}')
                plt.xlabel('Puntuación en Matemáticas')
                plt.ylabel('Puntuación en Lectura')
                plt.title('Regresión y Correlación entre Puntuaciones de Matemáticas y Lectura')
                plt.legend()
                plt.show()

                correlation = df.corr().loc['math_score', 'reading_score']
                print(f"Correlación: {correlation}")
                print(f"Coeficiente de determinación (R^2): {r_value**2:.2f}\n")
            else:
                print("Las columnas 'math_score' y 'reading_score' no existen en el DataFrame.")
        else:
            print("Primero carga los datos usando el método cargar_datos().")
