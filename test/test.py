import unittest
from unittest.mock import patch, mock_open
import pandas as pd
from io import StringIO
from pad.analisis_estadistico import AnalisisEstadistico

class TestAnalisisEstadistico(unittest.TestCase):

    def setUp(self):
        # Aquí configuramos un DataFrame de prueba
        self.data = """columna1,columna2
        1,4
        2,5
        3,6
        4,7
        5,8"""
        self.df = pd.read_csv(StringIO(self.data))
        self.archivo_csv = "test.csv"
        self.analisis = AnalisisEstadistico(self.archivo_csv)

    @patch("builtins.open", new_callable=mock_open, read_data="columna1,columna2\n1,4\n2,5\n3,6\n4,7\n5,8")
    @patch("os.path.exists", return_value=True)
    def test_cargar_datos(self, mock_exists, mock_open):
        self.analisis.cargar_datos()
        pd.testing.assert_frame_equal(self.analisis.df, self.df)

    @patch("builtins.open", new_callable=mock_open, read_data="columna1,columna2\n1,4\n2,5\n3,6\n4,7\n5,8")
    @patch("os.path.exists", return_value=True)
    def test_mostrar_datos(self, mock_exists, mock_open):
        self.analisis.cargar_datos()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.analisis.mostrar_datos()
            self.assertIn("columna1", mock_stdout.getvalue())
            self.assertIn("columna2", mock_stdout.getvalue())

    @patch("builtins.open", new_callable=mock_open, read_data="columna1,columna2\n1,4\n2,5\n3,6\n4,7\n5,8")
    @patch("os.path.exists", return_value=True)
    def test_resumen_estadistico(self, mock_exists, mock_open):
        self.analisis.cargar_datos()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.analisis.resumen_estadistico()
            self.assertIn("count", mock_stdout.getvalue())
            self.assertIn("mean", mock_stdout.getvalue())

    @patch("builtins.open", new_callable=mock_open, read_data="columna1,columna2\n1,4\n2,5\n3,6\n4,7\n5,8")
    @patch("os.path.exists", return_value=True)
    def test_estadisticas_columna(self, mock_exists, mock_open):
        self.analisis.cargar_datos()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.analisis.estadisticas_columna("columna1")
            output = mock_stdout.getvalue()
            self.assertIn("Media:", output)
            self.assertIn("Desviación estándar:", output)
            self.assertIn("Mínimo:", output)
            self.assertIn("Máximo:", output)

    @patch("builtins.open", new_callable=mock_open, read_data="columna1,columna2\n1,4\n2,5\n3,6\n4,7\n5,8")
    @patch("os.path.exists", return_value=True)
    def test_prueba_normalidad(self, mock_exists, mock_open):
        self.analisis.cargar_datos()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.analisis.prueba_normalidad("columna1")
            output = mock_stdout.getvalue()
            self.assertIn("Prueba de Shapiro-Wilk para 'columna1':", output)
            self.assertIn("Estadística de prueba:", output)
            self.assertIn("Valor p:", output)

    # def test_prueba_hipotesis_media(self):
    #     # Load data first
    #     self.analisis.cargar_datos()
    #
    #     # Configura datos de prueba con media conocida
    #     data = {"columna1": [1, 2, 3, 4, 5]}
    #     df_prueba = pd.DataFrame(data)
    #     media_conocida = 3.0
    #
    #     # Llama al método y verifica la salida
    #     with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
    #         self.analisis.prueba_hipotesis_media("columna1", media_conocida)
    #         output = mock_stdout.getvalue()
    #         self.assertIn("Prueba de hipótesis para la media de 'columna1'", output)
    #         self.assertIn("Valor de la media poblacional: 3.0", output)
    #
    # def test_prueba_bondad_ajuste_normal(self):
    #     # Load data first
    #     self.analisis.cargar_datos()
    #
    #     # Configura datos de prueba que no siguen una distribución normal
    #     data_no_normal = {"columna1": [1, 2, 3, 4, 5]}
    #     df_no_normal = pd.DataFrame(data_no_normal)
    #
    #     # Llama al método y verifica la salida
    #     with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
    #         self.analisis.prueba_bondad_ajuste_normal("columna1")
    #         output = mock_stdout.getvalue()
    #         self.assertIn("Prueba de bondad de ajuste para la normalidad en 'columna1'", output)
    #         self.assertIn("Se rechaza la hipótesis nula", output)



if __name__ == "__main__":
    unittest.main()
