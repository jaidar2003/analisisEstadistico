import os
from dotenv import load_dotenv
import pandas as pd


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


if __name__ == "__main__":
    # Cargar variables de entorno desde el archivo .env
    load_dotenv()

    # Obtener la ruta del archivo Excel desde las variables de entorno
    archivo_excel = os.getenv("RUTA_ARCHIVO_EXCEL")

    # Verificar si la ruta del archivo Excel está configurada
    if archivo_excel is None:
        print("La ruta del archivo Excel no está configurada en el archivo .env.")
    else:
        # Crear una instancia de AnalisisEstadistico y realizar el análisis
        analisis = AnalisisEstadistico(archivo_excel)
        analisis.cargar_datos()
        analisis.mostrar_datos()
        print("\nResumen estadístico:")
        analisis.resumen_estadistico()
        print("\nEstadísticas de la columna 'columna1':")
        analisis.estadisticas_columna("columna1")
