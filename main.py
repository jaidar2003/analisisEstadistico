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


def print_formatted(header, content):
    print("\n---", header, "---\n")
    if isinstance(content, str):
        print(content)
    elif isinstance(content, dict):
        for key, value in content.items():
            print(f"{key}: {value}")
    elif isinstance(content, list):
        for item in content:
            if isinstance(item, tuple) or isinstance(item, list):
                print(f"{item[0]}: {item[1]}")
            else:
                print(item)
    print()


def mostrar_resultados(analisis):



    print('-------------------------------------------------------------------------------------------------------------')
    print("Estadísticas por asignatura")

    math_stats = analisis.estadisticas_columna("math_score")
    if math_stats:
        print_formatted("Math Score", math_stats)

    reading_stats = analisis.estadisticas_columna("reading_score")
    if reading_stats:
        print_formatted("Reading Score", reading_stats)

    writing_stats = analisis.estadisticas_columna("writing_score")
    if writing_stats:
        print_formatted("Writing Score", writing_stats)







    print('-------------------------------------------------------------------------------------------------------------')
    print("Estadísticas comparativas según el curso de preparación")

    print("\n")
    print('------ Almunos que se prepararon --------')
    estudiantes_estudiaron = analisis.df[analisis.df["test_preparation_course"] == "completed"]
    resumen_estudiaron = analisis.resumen_estadistico_para_grupo(estudiantes_estudiaron)
    if resumen_estudiaron is not None:
        print_formatted("Estudiantes que estudiaron", resumen_estudiaron.to_dict())

    print("\n")
    print('------ Almunos que no se prepararon --------')
    estudiantes_no_estudiaron = analisis.df[analisis.df["test_preparation_course"] == "none"]
    resumen_no_estudiaron = analisis.resumen_estadistico_para_grupo(estudiantes_no_estudiaron)
    if resumen_no_estudiaron is not None:
        print_formatted("Estudiantes que no estudiaron", resumen_no_estudiaron.to_dict())





    print("\n")
    print('-------------------------------------------------------------------------------------------------------------')
    print("Estadísticas comparativas según el tipo de almuerzo")

    print("\n")
    print('------ Almunos que almorzaron --------')
    estudiantes_comieron = analisis.df[analisis.df["lunch"] == "standard"]
    resumen_comieron = analisis.resumen_estadistico_para_grupo(estudiantes_comieron)
    if resumen_comieron is not None:
        print_formatted("Estudiantes que comieron almuerzo estándar", resumen_comieron.to_dict())

    print("\n")
    print('------Almunos que no almorzaron ------')
    estudiantes_no_comieron = analisis.df[analisis.df["lunch"] == "free/reduced"]
    resumen_no_comieron = analisis.resumen_estadistico_para_grupo(estudiantes_no_comieron)
    if resumen_no_comieron is not None:
        print_formatted("Estudiantes que no comieron almuerzo estándar", resumen_no_comieron.to_dict())








    print("\n")
    print('-------------------------------------------------------------------------------------------------------------')
    print("Prueba de normalidad para los scores de math, writing y reading")
    print("\n")

    normalidad_math = analisis.prueba_normalidad("math_score")
    if normalidad_math:
        print_formatted("Prueba de normalidad para math_score", dict(normalidad_math))

    print("\n")
    normalidad_writing = analisis.prueba_normalidad("writing_score")
    if normalidad_writing:
        print_formatted("Prueba de normalidad para writing_score", dict(normalidad_writing))
    print("\n")
    normalidad_reading = analisis.prueba_normalidad("reading_score")
    if normalidad_reading:
        print_formatted("Prueba de normalidad para reading_score", dict(normalidad_reading))






    print("\n")
    print('-------------------------------------------------------------------------------------------------------------')
    print("Prueba de hipótesis para la media")
    print("\n")

    hipotesis_writing = analisis.prueba_hipotesis_media("writing_score", 70)
    if hipotesis_writing:
        print_formatted("Prueba de hipótesis para la media de writing_score", dict(hipotesis_writing))

    print('\n')
    hipotesis_math = analisis.prueba_hipotesis_media("math_score", 70)
    if hipotesis_math:
        print_formatted("Prueba de hipotesis para la media de math_score", dict(hipotesis_math))
    print('\n')
    hipotesis_reading = analisis.prueba_hipotesis_media("reading_score", 70)
    if hipotesis_reading:
        print_formatted("Prueba de hipotesis para le media de reading_score", dict(hipotesis_reading))




    print("\n")
    print('-------------------------------------------------------------------------------------------------------------')
    print("Prueba de bondad de ajuste para la normalidad")
    print("\n")

    bondad_ajuste_reading = analisis.prueba_bondad_ajuste_normal("reading_score")
    if bondad_ajuste_reading:
        print_formatted("Prueba de bondad de ajuste para la normalidad en reading_score", dict(bondad_ajuste_reading))
    print("\n")
    bondad_ajuste_writing = analisis.prueba_bondad_ajuste_normal("writing_score")
    if bondad_ajuste_writing:
        print_formatted("Pruebda de bonad de ajuste para la normalidad en writing_score", dict(bondad_ajuste_writing))

    print("\n")
    bondad_ajuste_math = analisis.prueba_bondad_ajuste_normal("math_score")
    if bondad_ajuste_math:
        print_formatted("Prueba de bondad de ajuste para la normalidad en math_score", dict(bondad_ajuste_math))


    print("\n")
    print('-------------------------------------------------------------------------------------------------------------')
    print("Análisis de regresión y correlación entre math_score y reading_score")
    print("\n")

    analisis.analisis_regresion_y_correlacion()

if __name__ == "__main__":
     main()


#hola




