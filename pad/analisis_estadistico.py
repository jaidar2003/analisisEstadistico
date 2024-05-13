import pandas as pd
import scipy.stats as stats

class AnalisisEstadistico:
    def __init__(self, archivo_excel):
        self.archivo_excel = archivo_excel
        self.df = None

    def cargar_datos(self):
        try:
            self.df = pd.read_excel(self.archivo_excel)
        except FileNotFoundError:
            print(f"No se encontró el archivo: {self.archivo_excel}")

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


