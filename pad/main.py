import os
from dotenv import load_dotenv
from analisis_estadistico import AnalisisEstadistico

def main():
    load_dotenv()

    archivo_excel = os.getenv("DATABASE_PATH")

    if archivo_excel is None:
        print("La ruta del archivo Excel no está configurada en el archivo .env.")
    else:
        realizar_analisis(archivo_excel)

def realizar_analisis(archivo_excel):
    analisis = AnalisisEstadistico(archivo_excel)
    analisis.cargar_datos()
    mostrar_resultados(analisis)

def mostrar_resultados(analisis):
    print("\nDatos:")
    analisis.mostrar_datos()

    print("\nResumen estadístico:")
    analisis.resumen_estadistico()

    print("\nEstadísticas de la columna 'columna1':")
    analisis.estadisticas_columna("columna1")

if __name__ == "__main__":
    main()
