import os
from dotenv import load_dotenv
from pad.analisis_estadistico import AnalisisEstadistico

def print_formatted(header, content):
    print("\n---", header, "---\n")
    print(content)
    print()

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
    print_formatted("Resumen Estadístico", "")
    print_formatted("Resumen Estadístico", analisis.resumen_estadistico())
    print_formatted("Estadísticas por asignatura", "")
    print_formatted("Math Score", analisis.estadisticas_columna("math_score"))
    print_formatted("Reading Score", analisis.estadisticas_columna("reading_score"))
    print_formatted("Writing Score", analisis.estadisticas_columna("writing_score"))
    print_formatted("Estadísticas comparativas según el curso de preparación", "")
    estudiantes_estudiaron = analisis.df[analisis.df["test_preparation_course"] == "completed"]
    print_formatted("Estudiantes que estudiaron", analisis.resumen_estadistico_para_grupo(estudiantes_estudiaron))
    estudiantes_no_estudiaron = analisis.df[analisis.df["test_preparation_course"] == "none"]
    print_formatted("Estudiantes que no estudiaron", analisis.resumen_estadistico_para_grupo(estudiantes_no_estudiaron))
    print_formatted("Estadísticas comparativas según el tipo de almuerzo", "")
    estudiantes_comieron = analisis.df[analisis.df["lunch"] == "standard"]
    print_formatted("Estudiantes que comieron almuerzo estándar", analisis.resumen_estadistico_para_grupo(estudiantes_comieron))
    estudiantes_no_comieron = analisis.df[analisis.df["lunch"] == "free/reduced"]
    print_formatted("Estudiantes que no comieron almuerzo estándar", analisis.resumen_estadistico_para_grupo(estudiantes_no_comieron))
    print_formatted("Prueba de normalidad para math_score", analisis.prueba_normalidad("math_score"))
    print_formatted("Prueba de hipótesis para la media de writing_score", analisis.prueba_hipotesis_media("writing_score", 70))
    print_formatted("Prueba de bondad de ajuste para la normalidad en reading_score", analisis.prueba_bondad_ajuste_normal("reading_score"))

if __name__ == "__main__":
    main()
