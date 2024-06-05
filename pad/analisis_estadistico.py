import os
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from scipy.stats import linregress
from tabulate import tabulate
from scipy.stats import chi2_contingency
from collections import Counter
from statsmodels.formula.api import ols

class AnalisisEstadistico:
    def __init__(self, archivo_csv):
        self.archivo_csv = archivo_csv
        self.df = None
        self.carpeta_graficos = "graficos"
        self.crear_carpeta_graficos()

    def crear_carpeta_graficos(self):
        if not os.path.exists(self.carpeta_graficos):
            os.makedirs(self.carpeta_graficos)

    def cargar_datos(self):
        if os.path.exists(self.archivo_csv):
            try:
                self.df = pd.read_csv(self.archivo_csv)
            except Exception as e:
                print(f"Error al cargar el archivo CSV: {e}")
        else:
            print(f"No se encontró el archivo CSV: {self.archivo_csv}")

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


    ######################################  ESTIMACION PARAMETROS #########################################

    def estimacion_parametros(self):
        if self.df is not None:
            print("Estimación de parámetros:")
            print("\n")
            print("Estimación de la media")
            print("Media de 'math_score':", self.df['math_score'].mean())
            print("Media de 'reading_score':", self.df['reading_score'].mean())
            print("Media de 'writing_score':", self.df['writing_score'].mean())
            
            print("\n")
            print("Estimación de la varianza")
            print("Varianza de 'math_score':", self.df['math_score'].var())
            print("Varianza de 'reading_score':", self.df['reading_score'].var())
            print("Varianza de 'writing_score':", self.df['writing_score'].var())

            print("\n")
            print("Estimación de proporciones")
            gender_counts = Counter(self.df['gender'])
            total = len(self.df['gender'])
            print("Proporción de género 'female':", gender_counts['female'] / total)
            print("Proporción de género 'male':", gender_counts['male'] / total)

            print("\n")
            # Por ejemplo, comparación de medias
            math_male = self.df[self.df['gender'] == 'male']['math_score']
            math_female = self.df[self.df['gender'] == 'female']['math_score']
            t_stat, p_value = stats.ttest_ind(math_male, math_female)
            print("Comparación de medias de 'math_score' entre géneros:")
            print("Estadística de prueba (t):", t_stat)
            print("Valor p:", p_value)
            if p_value > 0.05:
                print("No hay diferencia significativa en las medias entre géneros.")
            else:
                print("Hay una diferencia significativa en las medias entre géneros.")
        else:
            print("Primero carga los datos usando el método cargar_datos().")







    ######################################  PRUEBA DE HIPOTESIS #########################################


    # hipotesis media
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


    # hipotesis varianza
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


    # hipotesis proporcion
    # def prueba_hipotesis_proporcion(self, columna, proporcion_hipotetica):
    #     if self.df is not None:
    #         if columna in self.df.columns:
    #             datos = self.df[columna]
    #             conteo_exitos = datos.sum()
    #             n = len(datos)
    #             stat, p_valor = stats.binom_test(conteo_exitos, n, proporcion_hipotetica)
    #             print(f"Prueba de hipótesis sobre la proporción para '{columna}':")
    #             print("Estadística de prueba:", stat)
    #             print("Valor p:", p_valor)
    #         else:
    #             print("La columna especificada no existe en el DataFrame.")
    #     else:
    #         print("Primero carga los datos usando el método cargar_datos().")



    # prueba hipotesis
    def prueba_hipotesis_media_alumnos_almuerzo(self):
        if self.df is not None:
            math_score_standard = self.df[self.df["lunch"] == "standard"]["math_score"]
            math_score_free_reduced = self.df[self.df["lunch"] != "standard"]["math_score"]
            _, p_value = stats.ttest_ind(math_score_standard, math_score_free_reduced)
            alpha = 0.05
            print("Prueba de hipótesis para las calificaciones de matemáticas según el tipo de almuerzo:")
            print("H0: Los estudiantes que almorzaron SI tienen mejores calificaciones.")
            print("H1: Los estudiantes que almorzaron NO tienen mejores calificaciones que los que no almorzaron o tuvieron almuerzo reducido.")
            print("Nivel de significancia (alpha) =", alpha)
            print("Valor p (p-value) =", p_value)
            if p_value < alpha:
                print("Se rechaza la hipótesis nula. Hay evidencia suficiente para afirmar que los estudiantes que almorzaron NO tienen mejores calificaciones.")
            else:
                print("No se rechaza la hipótesis nula. No hay suficiente evidencia para afirmar que los estudiantes que almorzaron NO tienen mejores calificaciones.")
        else:
            print("Primero carga los datos usando el método cargar_datos().")


    # prueba hipotesis
    def prueba_hipotesis_genero_educacion_padres(self):
        if self.df is not None:
            male_bachelor = self.df[(self.df["gender"] == "male") & (self.df["parental_level_of_education"] == "bachelor's degree")]["math_score"]
            female_bachelor = self.df[(self.df["gender"] == "female") & (self.df["parental_level_of_education"] == "bachelor's degree")]["math_score"]
            _, p_value = stats.ttest_ind(male_bachelor, female_bachelor)
            alpha = 0.05
            print("Prueba de hipótesis para las puntuaciones de matemáticas según el género y el nivel educativo de los padres:")
            print("H0: No hay diferencia significativa en las puntuaciones de matemáticas entre hombres y mujeres cuyos padres tienen un título universitario de licenciatura.")
            print("H1: Hay una diferencia significativa en las puntuaciones de matemáticas entre hombres y mujeres cuyos padres tienen un título universitario de licenciatura.")
            print("Nivel de significancia (alpha) =", alpha)
            print("Valor p (p-value) =", p_value)
            if p_value < alpha:
                print("Se rechaza la hipótesis nula. Hay evidencia suficiente para afirmar que hay una diferencia significativa en las puntuaciones de matemáticas entre hombres y mujeres cuyos padres tienen un título universitario de licenciatura.")
            else:
                print("No se rechaza la hipótesis nula. No hay suficiente evidencia para afirmar que hay una diferencia significativa en las puntuaciones de matemáticas entre hombres y mujeres cuyos padres tienen un título universitario de licenciatura.")
        else:
            print("Primero carga los datos usando el método cargar_datos().")


    #tabla contingencia de edu padres
    def tabla_contingencia(self, columna1, columna2):
        if self.df is not None:
            if columna1 in self.df.columns and columna2 in self.df.columns:
                tabla_contingencia = pd.crosstab(self.df[columna1], self.df[columna2])
                marginales = tabla_contingencia.sum(axis=1)
                total = tabla_contingencia.values.sum()
                frecuencias_condicionales = tabla_contingencia.div(marginales, axis=0)

                print("Tabla de Contingencia:")
                print(tabulate(tabla_contingencia, headers='keys', tablefmt='fancy_grid'))

                print("\nMarginales:")
                print(tabulate(pd.DataFrame(marginales), headers=['Marginales'], tablefmt='fancy_grid'))

                print("\nFrecuencias Condicionales:")
                print(tabulate(frecuencias_condicionales, headers='keys', tablefmt='fancy_grid'))
            else:
                print("Al menos una de las columnas especificadas no existe en el DataFrame.")
        else:
            print("Primero carga los datos usando el método cargar_datos().")


    # prueba independencia (tabla contingencia de edu padre)
    def prueba_independencia(tabla_contingencia):
 
        #Realiza una prueba de independencia utilizando el test de chi-cuadrado.

        #Parámetros:
        #tabla_contingencia (array_like): Una tabla de contingencia representada como una matriz numpy.

        #Retorna:
        #tuple: Un tuple que contiene el estadístico de chi-cuadrado, el valor p, los grados de libertad y los valores esperados.
    
        # Aplica la prueba de chi-cuadrado
        chi2, p, dof, expected = chi2_contingency(tabla_contingencia)
        return chi2, p, dof, expected

    



    # Prueba Bondad
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


                plt.figure(figsize=(10, 6))
                stats.probplot(datos, dist="norm", plot=plt)
                plt.title(f'Q-Q plot de {columna}')
                plt.savefig(os.path.join(self.carpeta_graficos, f'qqplot_{columna}.png'))
                plt.close()
            else:
                print("La columna especificada no existe en el DataFrame.")
        else:
            print("Primero carga los datos usando el método cargar_datos().")


    # ...............................................
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


    # ...............................................
    def prueba_bondad_ajuste(self, columna, distribucion_esperada):
        if self.df is not None:
            if columna in self.df.columns:
                datos = self.df[columna].value_counts()
                valores_observados = datos.values
                stat, p_valor = stats.chisquare(valores_observados, f_exp=distribucion_esperada)
                print(f"Prueba de bondad de ajuste para '{columna}':")
                print("Estadística de prueba Chi-cuadrado:", stat)
                print("Valor p:", p_valor)


    

    # Prueba independencia 

    def prueba_independencia(self):
        pass
        



    # analisis de varianza 
    def analisis_anova(self):
        if self.df is not None:
            # Fórmulas para el ANOVA
            formulas = {
                "math_score": "math_score ~ C(gender) + C(parental_level_of_education) + C(lunch) + C(test_preparation_course)",
                "reading_score": "reading_score ~ C(gender) + C(parental_level_of_education) + C(lunch) + C(test_preparation_course)",
                "writing_score": "writing_score ~ C(gender) + C(parental_level_of_education) + C(lunch) + C(test_preparation_course)"
            }

            # Resultados del ANOVA
            anova_results = {}
            for score, formula in formulas.items():
                model = ols(formula, data=self.df).fit()
                anova_table = sm.stats.anova_lm(model, typ=2)
                anova_results[score] = anova_table

            # Mostrar los resultados
            for score, table in anova_results.items():
                print(f"\nANOVA para {score}:\n")
                print(table)
        else:
            print("Primero carga los datos usando el método cargar_datos().")


    # def anova(self, columna_dependiente, columna_independiente): # Análisis de la varianza
    #     if self.df is not None:
    #         if columna_dependiente in self.df.columns and columna_independiente in self.df.columns:
    #             modelo = stats.f_oneway(*[grupo[columna_dependiente].values for nombre_grupo, grupo in self.df.groupby(columna_independiente)])
    #             print(f"Análisis de varianza (ANOVA) para '{columna_dependiente}' por '{columna_independiente}':")
    #             print("Estadística F:", modelo.statistic)
    #             print("Valor p:", modelo.pvalue)
    #         else:
    #             print("Al menos una de las columnas especificadas no existe en el DataFrame.")
    #     else:
    #         print("Primero carga los datos usando el método cargar_datos().")


    





    # graficos

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
                plt.plot(df['math_score'], df['regression_line'], color='red',
                         label=f'Regresión lineal: y={slope:.2f}x+{intercept:.2f}')
                plt.xlabel('Puntuación en Matemáticas')
                plt.ylabel('Puntuación en Lectura')
                plt.title('Regresión y Correlación entre Puntuaciones de Matemáticas y Lectura')
                plt.legend()
                plt.savefig(os.path.join(self.carpeta_graficos, 'regresion_correlacion.png'))
                plt.close()

                correlation = df.corr().loc['math_score', 'reading_score']
                print(f"Correlación: {correlation}")
                print(f"Coeficiente de determinación (R^2): {r_value ** 2:.2f}\n")
            else:
                print("Las columnas 'math_score' y 'reading_score' no existen en el DataFrame.")
        else:
            print("Primero carga los datos usando el método cargar_datos().")



    def generar_histograma(self, columna):
        if self.df is not None:
            if columna in self.df.columns:
                plt.figure(figsize=(10, 6))
                sns.histplot(self.df[columna], kde=True)
                plt.title(f'Histograma de {columna}')
                plt.xlabel(columna)
                plt.ylabel('Frecuencia')
                plt.savefig(os.path.join(self.carpeta_graficos, f'histograma_{columna}.png'))
                plt.close()
            else:
                print("La columna especificada no existe en el DataFrame.")
        else:
            print("Primero carga los datos usando el método cargar_datos().")

    def generar_boxplot(self, columna):
        if self.df is not None:
            if columna in self.df.columns:
                plt.figure(figsize=(10, 6))
                sns.boxplot(x=self.df[columna])
                plt.title(f'Gráfico de Caja y Bigotes de {columna}')
                plt.xlabel(columna)
                plt.savefig(os.path.join(self.carpeta_graficos, f'boxplot_{columna}.png'))
                plt.close()
            else:
                print("La columna especificada no existe en el DataFrame.")
        else:
            print("Primero carga los datos usando el método cargar_datos().")


    


    
    


    




if __name__ == "__main__":
    analisis = AnalisisEstadistico("path_to_your_csv.csv")
    analisis.cargar_datos()
    analisis.mostrar_datos()
    analisis.resumen_estadistico()
    analisis.prueba_normalidad("math_score")
    analisis.generar_histograma("math_score")
    analisis.generar_boxplot("math_score")
    analisis.analisis_regresion_y_correlacion()