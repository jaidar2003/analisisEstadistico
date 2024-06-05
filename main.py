import os
from dotenv import load_dotenv
import numpy as np
from pad.analisis_estadistico import AnalisisEstadistico
import matplotlib.pyplot as plt  # Importación necesaria para mostrar gráficos
from scipy.stats import chi2_contingency



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
    print('\033[1;33m' + "ESTADÍSTICAS POR ASIGNATURA")
    print('\033[0m')

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
    print('\033[1;33m' + "Estadísticas comparativas según el curso de preparación".upper())
    print('\033[0m')

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
    print('\033[1;33m' + "Estadísticas comparativas según el tipo de almuerzo".upper())
    print('\033[0m')
    

    print("\n")
    print('------ Almunos que almorzaron --------')
    estudiantes_comieron = analisis.df[analisis.df["lunch"] == "standard"]
    resumen_comieron = analisis.resumen_estadistico_para_grupo(estudiantes_comieron)
    if resumen_comieron is not None:
        print_formatted("Estudiantes que comieron almuerzo estándar", resumen_comieron.to_dict())

    print("\n")
    print('------ Almunos que no almorzaron ------')
    estudiantes_no_comieron = analisis.df[analisis.df["lunch"] == "free/reduced"]
    resumen_no_comieron = analisis.resumen_estadistico_para_grupo(estudiantes_no_comieron)
    if resumen_no_comieron is not None:
        print_formatted("Estudiantes que no comieron almuerzo estándar", resumen_no_comieron.to_dict())



    # -------------------------------------------------ESTIMACION DE PARAMETROS--------------------------------------------------
    print("\n")
    print('-------------------------------------------------------------------------------------------------------------')
    print('\033[1;33m' + "estimacion_parametro".upper())
    print('\033[0m')
    print("\n")

    analisis.estimacion_parametros()



    # -------------------------------------------------PRUEBA DE HIPOTESIS--------------------------------------------------
    
    # Prueba de hipótesis para la media

    print("\n")
    print('-------------------------------------------------------------------------------------------------------------')
    print('\033[1;33m' + "Prueba de hipótesis para la media".upper())
    print('\033[0m')
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



    #Prueba de hipótesis para la varianza

    print("\n")
    print('-------------------------------------------------------------------------------------------------------------')
    print('\033[1;33m' + "Prueba de hipótesis para la varianza".upper())
    print('\033[0m')
    print("\n")

    prueba_varianza_math = analisis.prueba_hipotesis_varianza("math_score", 100)
    if prueba_varianza_math:
        print_formatted("Prueba de hipótesis para la varianza de math_score", dict(prueba_varianza_math))

    print('\n')
    prueba_varianza_reading = analisis.prueba_hipotesis_varianza("reading_score", 100)
    if prueba_varianza_reading:
        print_formatted("Prueba de hipótesis para la varianza de reading_score", dict(prueba_varianza_reading))
    print('\n')
    prueba_varianza_writing = analisis.prueba_hipotesis_varianza("writing_score", 100)
    if prueba_varianza_writing:
        print_formatted("Prueba de hipótesis para la varianza de writing_score", dict(prueba_varianza_writing))



    #Prueba de hipótesis para la proporcion 

   







    # Prueba de bondad de ajuste para la normalidad

    print("\n")
    print('-------------------------------------------------------------------------------------------------------------')
    print('\033[1;33m' + "Prueba de bondad de ajuste para la normalidad".upper())
    print('\033[0m')
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



    
    
    # prueba_hipotesis_media_alumnos_almuerzo
    print("\n")
    print('-------------------------------------------------------------------------------------------------------------')
    print('\033[1;33m' + "prueba hipotesis media alumnos almuerzo".upper())
    print('\033[0m')
    print("\n")

    analisis.prueba_hipotesis_media_alumnos_almuerzo()




    # prueba_hipotesis_genero_educacion_padres
    print("\n")
    print('-------------------------------------------------------------------------------------------------------------')
    print('\033[1;33m' + "prueba_hipotesis_genero_educacion_padres".upper())
    print('\033[0m')
    print("\n")
    analisis.prueba_hipotesis_genero_educacion_padres()

   


    # tabla de contingencia
    print("\n")
    print('-------------------------------------------------------------------------------------------------------------')
    print('\033[1;33m' + "TABLA DE CONTINGENCIA PARA GÉNERO Y NIVEL EDUCATIVO DE LOS PADRES")
    print('\033[0m')
    print("\n")
    analisis.tabla_contingencia("gender", "parental_level_of_education")  # Llamada a la función tabla_contingencia



    # prueba de independencia(tabla contingencia)
    print("\n")
    print('-------------------------------------------------------------------------------------------------------------')
    print('\033[1;33m' + "Prueba de Independencia".upper())
    print('\033[0m')
    print("\n")
    observed = np.array([[116, 63, 94, 36, 118, 91],
                     [106, 55, 102, 23, 108, 88]])
    chi2, p, dof, expected = chi2_contingency(observed)
    print("Estadístico de chi-cuadrado:", chi2)
    print("Valor p:", p)
    print("Grados de libertad:", dof) # por ser tabla de 2x6, hay 5 grados de libertad
    print("Valores esperados:")
    #Valores esperados: Son los valores esperados bajo la hipótesis nula de independencia entre las variables.
    #Estos valores se calculan a partir de la tabla de contingencia observada y se utilizan para comparar con los valores observados. 
    print(expected)
    print("\n")
    print("Interpretacion: El valor p es muy alto, no hay suficiente evidencia para rechazar la hipótesis nula de independencia entre género y nivel educativo (nivel sig = 0.05)")





    # Prueba de Bondad
    print("\n")
    print('-------------------------------------------------------------------------------------------------------------')
    print('\033[1;33m' + "Prueba de normalidad para los scores de math, writing y reading (Prueba de Bondad)".upper())
    print('\033[0m')
    print("\n")
    print("H0 (Hipótesis Nula): Las puntuaciones de matemáticas, lectura y escritura siguen una distribución normal.")
    print("H1 (Hipótesis Alternativa): Las puntuaciones de matemáticas, lectura y escritura no siguen una distribución normal.")
    print("Si el valor p es menor que 0.05, rechazamos la hipótesis nula y concluimos que los datos no siguen una distribución normal")
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



    #analisis de variacion
    print("\n")
    print('-------------------------------------------------------------------------------------------------------------')
    print('\033[1;33m' + "Analisis de Variacion".upper())
    print('\033[0m')
    print("\n")
    print("Primero analizamos cómo las variables categóricas afectan los puntajes de matemáticas, lectura y escritura. Las variables categóricas a considerar son gender, parental_level_of_education, lunch y test_preparation_course.")
    print("\n")
    print("Para math_score:")
    print("H0: No hay diferencia significativa en los puntajes de matemáticas entre los grupos definidos por género, nivel educativo de los padres, almuerzo y curso de preparación para el examen.")
    print("H1: Hay al menos una diferencia significativa en los puntajes de matemáticas entre los grupos definidos por género, nivel educativo de los padres, almuerzo y curso de preparación para el examen.")

    print("\nPara reading_score:")
    print("H0: No hay diferencia significativa en los puntajes de lectura entre los grupos definidos por género, nivel educativo de los padres, almuerzo y curso de preparación para el examen.")
    print("H1: Hay al menos una diferencia significativa en los puntajes de lectura entre los grupos definidos por género, nivel educativo de los padres, almuerzo y curso de preparación para el examen.")

    print("\nPara writing_score:")
    print("H0: No hay diferencia significativa en los puntajes de escritura entre los grupos definidos por género, nivel educativo de los padres, almuerzo y curso de preparación para el examen.")
    print("H1: Hay al menos una diferencia significativa en los puntajes de escritura entre los grupos definidos por género, nivel educativo de los padres, almuerzo y curso de preparación para el examen.")

    analisis.analisis_anova()
    print("Intepretacion:")
    





    # graficos
    print("\n")
    print('-------------------------------------------------------------------------------------------------------------')
    print('\033[1;33m' + "Analisis exploratorios: (GRAFICOS)".upper())
    print('\033[0m')

    while True:
        print("\nPresiona una tecla para ver los graficos: ")
        print("a) Mostrar el análisis de regresión y correlación")
        print("b) Mostrar histograma de math_score")
        print("c) Mostrar histograma de reading_score")
        print("d) Mostrar histograma de writing_score")
        print("e) Mostrar boxplot de math_score")
        print("f) Mostrar boxplot de reading_score")
        print("g) Mostrar boxplot de writing_score")
        print("t) Mostar todos los graficos")
        print("q) Salir del programa")
        key_pressed = input().lower()

        if key_pressed == 'a':
            print_formatted("Análisis de regresión y correlación entre math_score y reading_score", "")
            analisis.analisis_regresion_y_correlacion()
            plt.show()

        elif key_pressed == 'b':
            print("Histograma de math_score")
            analisis.generar_histograma("math_score")
            plt.show()

        elif key_pressed == 'c':
            print("Histograma de reading_score")
            analisis.generar_histograma("reading_score")
            plt.show()

        elif key_pressed == 'd':
            print("Histograma de writing_score")
            analisis.generar_histograma("writing_score")
            plt.show()

        elif key_pressed == 'e':
            print("Boxplot de math_score")
            analisis.generar_boxplot("math_score")
            plt.show()

        elif key_pressed == 'f':
            print("Boxplot de reading_score")
            analisis.generar_boxplot("reading_score")
            plt.show()

        elif key_pressed == 'g':
            print("Boxplot de writing_score")
            analisis.generar_boxplot("writing_score")
            plt.show()

        elif key_pressed == 't':
            print("Todos los graficos estadisticos")
            analisis.analisis_regresion_y_correlacion()
            analisis.generar_histograma("math_score")
            analisis.generar_histograma("reading_score")
            analisis.generar_histograma("writing_score")
            analisis.generar_boxplot("math_score")
            analisis.generar_boxplot("reading_score")
            analisis.generar_boxplot("writing_score")


        elif key_pressed == 'q':
            print("Muchas gracias")
            break

        else:
            print("Opción no válida. Por favor, selecciona una opcion correcta")

if __name__ == "__main__":
    main()