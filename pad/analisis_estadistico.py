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

    def prueba_hipotesis_media(self, columna, media_hipotetica):
        if self.df is not None:
            if columna in self.df.columns:
                stat, p_valor = stats.ttest_1samp(self.df[columna], media_hipotetica)
                print(f"Prueba de hipótesis sobre la media para '{columna}':")
                print("Estadística de prueba:", stat)
                print("Valor p:", p_valor)
            else:
                print("La columna especificada no existe en el DataFrame.")
        else:
            print("Primero carga los datos usando el método cargar_datos().")

    def prueba_hipotesis_varianza(self, columna, varianza_hipotetica):
        if self.df is not None:
            if columna in self.df.columns:
                datos = self.df[columna]
                n = len(datos)
                chi2_stat = (n - 1) * datos.var() / varianza_hipotetica
                p_valor = stats.chi2.sf(chi2_stat, n - 1)
                print(f"Prueba de hipótesis sobre la varianza para '{columna}':")
                print("Estadística de prueba Chi-cuadrado:", chi2_stat)
                print("Valor p:", p_valor)
            else:
                print("La columna especificada no existe en el DataFrame.")
        else:
            print("Primero carga los datos usando el método cargar_datos().")

    def prueba_hipotesis_proporcion(self, columna, proporcion_hipotetica):
        if self.df is not None:
            if columna in self.df.columns:
                datos = self.df[columna]
                conteo_exitos = datos.sum()
                n = len(datos)
                stat, p_valor = stats.binom_test(conteo_exitos, n, proporcion_hipotetica)
                print(f"Prueba de hipótesis sobre la proporción para '{columna}':")
                print("Estadística de prueba:", stat)
                print("Valor p:", p_valor)
            else:
                print("La columna especificada no existe en el DataFrame.")
        else:
            print("Primero carga los datos usando el método cargar_datos().")

    def prueba_bondad_ajuste(self, columna, distribucion_esperada):
        if self.df is not None:
            if columna in self.df.columns:
                datos = self.df[columna].value_counts()
                valores_observados = datos.values
                stat, p_valor = stats.chisquare(valores_observados, f_exp=distribucion_esperada)
                print(f"Prueba de bondad de ajuste para '{columna}':")
                print("Estadística de prueba Chi-cuadrado:", stat)
                print("Valor p:", p_valor)
            else:
                print("La columna especificada no existe en el DataFrame.")
        else:
            print("Primero carga los datos usando el método cargar_datos().")

    def prueba_independencia(self, columna1, columna2):
        if self.df is not None:
            if columna1 in self.df.columns and columna2 in self.df.columns:
                tabla_contingencia = pd.crosstab(self.df[columna1], self.df[columna2])
                stat, p_valor, _, _ = stats.chi2_contingency(tabla_contingencia)
                print(f"Prueba de independencia para '{columna1}' y '{columna2}':")
                print("Estadística de prueba Chi-cuadrado:", stat)
                print("Valor p:", p_valor)
            else:
                print("Al menos una de las columnas especificadas no existe en el DataFrame.")
        else:
            print("Primero carga los datos usando el método cargar_datos().")

    def anova(self, columna_dependiente, columna_independiente):
        if self.df is not None:
            if columna_dependiente in self.df.columns and columna_independiente in self.df.columns:
                modelo = stats.f_oneway(*[grupo[columna_dependiente].values for nombre_grupo, grupo in self.df.groupby(columna_independiente)])
                print(f"Análisis de varianza (ANOVA) para '{columna_dependiente}' por '{columna_independiente}':")
                print("Estadística F:", modelo.statistic)
                print("Valor p:", modelo.pvalue)
            else:
                print("Al menos una de las columnas especificadas no existe en el DataFrame.")
        else:
            print("Primero carga los datos usando el método cargar_datos().")


####

    


# land of hope and glory
    
