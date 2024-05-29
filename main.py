import os
from dotenv import load_dotenv
from pad.analisis_estadistico import AnalisisEstadistico
from pad.resultados import *

def main():
    load_dotenv()

    archivo_excel = os.getenv("DATABASE_PATH")
    carpeta_datos = os.getenv("CARPETA_DATOS")

    ruta_archivo = os.path.join(carpeta_datos, "resultados.txt")

    if archivo_excel is None:
        print("La ruta del archivo Excel no está configurada en el archivo .env.")
    else:
        analisis = realizar_analisis(archivo_excel)
        analisis_exploratorio_graficos(analisis)


def realizar_analisis(archivo_excel):
    analisis = AnalisisEstadistico(archivo_excel)
    analisis.cargar_datos()
    mostrar_resultados(analisis)
    return analisis



if __name__ == "__main__":
    main()
