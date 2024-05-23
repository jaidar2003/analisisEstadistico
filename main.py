import os
from dotenv import load_dotenv
from pad.analisis_estadistico import AnalisisEstadistico

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

    print("\n--- Resumen Estadístico ---")
    print("")

    print("Resumen estadístico general:")
    analisis.resumen_estadistico()
    print("")

    print("Estadísticas por asignatura:")
    print("")

    print("   - Math Score:")
    analisis.estadisticas_columna("math_score")
    print("")

    print("   - Reading Score:")
    analisis.estadisticas_columna("reading_score")
    print("")

    print("   - Writing Score:")
    analisis.estadisticas_columna("writing_score")
    print("")

    print("Estadísticas comparativas según el curso de preparación:")
    print("")

    estudiantes_estudiaron = analisis.df[analisis.df["test_preparation_course"] == "completed"]
    print("   - Estudiantes que estudiaron:")
    analisis.resumen_estadistico_para_grupo(estudiantes_estudiaron)
    print("")

    estudiantes_no_estudiaron = analisis.df[analisis.df["test_preparation_course"] == "none"]
    print("   - Estudiantes que no estudiaron:")
    analisis.resumen_estadistico_para_grupo(estudiantes_no_estudiaron)
    print("")

    print("Estadísticas comparativas según el tipo de almuerzo:")
    print("")

    estudiantes_comieron = analisis.df[analisis.df["lunch"] == "standard"]
    print("   - Estudiantes que comieron almuerzo estándar:")
    analisis.resumen_estadistico_para_grupo(estudiantes_comieron)
    print("")

    estudiantes_no_comieron = analisis.df[analisis.df["lunch"] == "free/reduced"]
    print("   - Estudiantes que no comieron almuerzo estándar:")
    analisis.resumen_estadistico_para_grupo(estudiantes_no_comieron)
    print("")


if __name__ == "__main__":
    main()
