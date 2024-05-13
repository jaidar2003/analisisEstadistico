import os
from dotenv import load_dotenv
from analisis_estadistico import AnalisisEstadistico

def main():
    # Cargar variables de entorno desde el archivo .env
    load_dotenv()

    # Obtener la ruta del archivo Excel desde las variables de entorno
    archivo_excel = os.getenv("DATABASE_PATH")

    # Verificar si la ruta del archivo Excel está configurada
    if archivo_excel is None:
        print("La ruta del archivo Excel no está configurada en el archivo .env.")
    else:
        # Realizar el análisis estadístico
        realizar_analisis(archivo_excel)

def realizar_analisis(archivo_excel):
    # Crear una instancia de AnalisisEstadistico y realizar el análisis
    analisis = AnalisisEstadistico(archivo_excel)
    analisis.cargar_datos()
    mostrar_resultados(analisis)

def mostrar_resultados(analisis):
    # Mostrar los datos
    print("\nDatos:")
    analisis.mostrar_datos()

    # Mostrar el resumen estadístico
    print("\nResumen estadístico:")
    analisis.resumen_estadistico()

    # Mostrar las estadísticas de la columna 'columna1'
    print("\nEstadísticas de la columna 'columna1':")
    analisis.estadisticas_columna("columna1")

if __name__ == "__main__":
    main()
