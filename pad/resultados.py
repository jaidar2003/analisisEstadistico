
def format_content(header, content):
    output = "\n--- " + header + " ---\n"
    if isinstance(content, str):
        output += content
    elif isinstance(content, dict):
        for key, value in content.items():
            output += f"{key}: {value}\n"
    elif isinstance(content, list):
        for item in content:
            if isinstance(item, tuple) or isinstance(item, list):
                output += f"{item[0]}: {item[1]}\n"
            else:
                output += str(item) + "\n"
    return output + "\n"

def mostrar_resultados(analisis):
    ruta_archivo = "datos_recogidos/resultados.txt"

    with open(ruta_archivo, "w") as archivo:
        archivo.write('-------------------------------------------------------------------------------------------------------------\n')
        archivo.write("Estadísticas por asignatura\n\n")

        math_stats = analisis.estadisticas_columna("math_score")
        if math_stats:
            archivo.write(format_content("Math Score", math_stats) + "\n")

        reading_stats = analisis.estadisticas_columna("reading_score")
        if reading_stats:
            archivo.write(format_content("Reading Score", reading_stats) + "\n")

        writing_stats = analisis.estadisticas_columna("writing_score")
        if writing_stats:
            archivo.write(format_content("Writing Score", writing_stats) + "\n")

        archivo.write('-------------------------------------------------------------------------------------------------------------\n')
        archivo.write("Estadísticas comparativas según el curso de preparación\n\n")

        archivo.write('\n------ Almunos que se prepararon --------\n')
        estudiantes_estudiaron = analisis.df[analisis.df["test_preparation_course"] == "completed"]
        resumen_estudiaron = analisis.resumen_estadistico_para_grupo(estudiantes_estudiaron)
        if resumen_estudiaron is not None:
            archivo.write(format_content("Estudiantes que estudiaron", resumen_estudiaron.to_dict()) + "\n")

        archivo.write('\n------ Almunos que no se prepararon --------\n')
        estudiantes_no_estudiaron = analisis.df[analisis.df["test_preparation_course"] == "none"]
        resumen_no_estudiaron = analisis.resumen_estadistico_para_grupo(estudiantes_no_estudiaron)
        if resumen_no_estudiaron is not None:
            archivo.write(format_content("Estudiantes que no estudiaron", resumen_no_estudiaron.to_dict()) + "\n")

        archivo.write('\n-------------------------------------------------------------------------------------------------------------\n')
        archivo.write("Estadísticas comparativas según el tipo de almuerzo\n\n")

        archivo.write('\n------ Almunos que almorzaron --------\n')
        estudiantes_comieron = analisis.df[analisis.df["lunch"] == "standard"]
        resumen_comieron = analisis.resumen_estadistico_para_grupo(estudiantes_comieron)
        if resumen_comieron is not None:
            archivo.write(format_content("Estudiantes que comieron almuerzo estándar", resumen_comieron.to_dict()) + "\n")

        archivo.write('\n------ Almunos que no almorzaron ------\n')
        estudiantes_no_comieron = analisis.df[analisis.df["lunch"] == "free/reduced"]
        resumen_no_comieron = analisis.resumen_estadistico_para_grupo(estudiantes_no_comieron)
        if resumen_no_comieron is not None:
            archivo.write(format_content("Estudiantes que no comieron almuerzo estándar", resumen_no_comieron.to_dict()) + "\n")

        archivo.write('\n-------------------------------------------------------------------------------------------------------------\n')
        archivo.write("Prueba de normalidad para los scores de math, writing y reading\n\n")

        normalidad_math = analisis.prueba_normalidad("math_score")
        if normalidad_math:
            archivo.write(format_content("Prueba de normalidad para math_score", dict(normalidad_math)) + "\n")

        normalidad_writing = analisis.prueba_normalidad("writing_score")
        if normalidad_writing:
            archivo.write(format_content("Prueba de normalidad para writing_score", dict(normalidad_writing)) + "\n")

        normalidad_reading = analisis.prueba_normalidad("reading_score")
        if normalidad_reading:
            archivo.write(format_content("Prueba de normalidad para reading_score", dict(normalidad_reading)) + "\n")

        archivo.write('\n-------------------------------------------------------------------------------------------------------------\n')
        archivo.write("Prueba de hipótesis para la media\n\n")

        hipotesis_writing = analisis.prueba_hipotesis_media("writing_score", 70)
        if hipotesis_writing:
            archivo.write(format_content("Prueba de hipótesis para la media de writing_score", dict(hipotesis_writing)) + "\n")

        hipotesis_math = analisis.prueba_hipotesis_media("math_score", 70)
        if hipotesis_math:
            archivo.write(format_content("Prueba de hipotesis para la media de math_score", dict(hipotesis_math)) + "\n")

        hipotesis_reading = analisis.prueba_hipotesis_media("reading_score", 70)
        if hipotesis_reading:
            archivo.write(format_content("Prueba de hipotesis para le media de reading_score", dict(hipotesis_reading)) + "\n")

        archivo.write('\n-------------------------------------------------------------------------------------------------------------\n')
        archivo.write("Prueba de bondad de ajuste para la normalidad\n\n")

        bondad_ajuste_reading = analisis.prueba_bondad_ajuste_normal("reading_score")
        if bondad_ajuste_reading:
            archivo.write(format_content("Prueba de bondad de ajuste para la normalidad en reading_score", dict(bondad_ajuste_reading)) + "\n")

        bondad_ajuste_writing = analisis.prueba_bondad_ajuste_normal("writing_score")
        if bondad_ajuste_writing:
            archivo.write(format_content("Pruebda de bonad de ajuste para la normalidad en writing_score", dict(bondad_ajuste_writing)) + "\n")

        bondad_ajuste_math = analisis.prueba_bondad_ajuste_normal("math_score")
        if bondad_ajuste_math:
            archivo.write(format_content("Prueba de bondad de ajuste para la normalidad en math_score", dict(bondad_ajuste_math)) + "\n")

        archivo.write('\n-------------------------------------------------------------------------------------------------------------\n')
        archivo.write("Generación de Histograma y Boxplot para la puntuación de Lectura\n\n")

        analisis.generar_histograma("reading_score")
        analisis.generar_boxplot("reading_score")

        archivo.write('\n-------------------------------------------------------------------------------------------------------------\n')
        archivo.write("Análisis de Regresión y Correlación entre Puntuaciones de Matemáticas y Lectura\n\n")

        analisis.analisis_regresion_y_correlacion()

    print("Los resultados se han guardado en el archivo:", ruta_archivo)


def analisis_exploratorio_graficos(analisis):
    print("\n")
    print('-------------------------------------------------------------------------------------------------------------')
    print("Analisis exploratorios: (GRAFICOS)")
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
            print("Análisis de regresión y correlación entre math_score y reading_score")
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
            print("Todos los gráficos estadísticos")
            analisis.analisis_regresion_y_correlacion()
            analisis.generar_histograma("math_score")
            analisis.generar_histograma("reading_score")
            analisis.generar_histograma("writing_score")
            analisis.generar_boxplot("math_score")
            analisis.generar_boxplot("reading_score")
            analisis.generar_boxplot("writing_score")
            plt.show()

        elif key_pressed == 'q':
            print("Muchas gracias")
            break

        else:
            print("Opción no válida. Por favor, selecciona una opción correcta")

