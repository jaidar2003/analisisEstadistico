import unittest
from unittest.mock import patch, mock_open, MagicMock
import pandas as pd
from io import StringIO
from pad.analisis_estadistico import AnalisisEstadistico
import os
import seaborn as sns
import matplotlib.pyplot as plt

class TestAnalisisEstadistico(unittest.TestCase):

    def setUp(self):
        data = {
            "math_score": [1, 2, 3, 4, 5],
            "reading_score": [10, 20, 30, 40, 50]
        }
        self.df = pd.DataFrame(data)
        self.archivo_csv = "test.csv"
        self.analisis = AnalisisEstadistico(self.archivo_csv)

    @patch("builtins.open", new_callable=mock_open, read_data="math_score,reading_score\n1,10\n2,20\n3,30\n4,40\n5,50")
    @patch("os.path.exists", return_value=True)
    def test_cargar_datos(self, mock_exists, mock_open):
        self.analisis.cargar_datos()
        pd.testing.assert_frame_equal(self.analisis.df, self.df)

    @patch("builtins.open", new_callable=mock_open, read_data="math_score,reading_score\n1,10\n2,20\n3,30\n4,40\n5,50")
    @patch("os.path.exists", return_value=True)
    def test_mostrar_datos(self, mock_exists, mock_open):
        self.analisis.cargar_datos()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.analisis.mostrar_datos()
            self.assertIn("math_score", mock_stdout.getvalue())
            self.assertIn("reading_score", mock_stdout.getvalue())

    @patch("builtins.open", new_callable=mock_open, read_data="math_score,reading_score\n1,10\n2,20\n3,30\n4,40\n5,50")
    @patch("os.path.exists", return_value=True)
    def test_resumen_estadistico(self, mock_exists, mock_open):
        self.analisis.cargar_datos()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.analisis.resumen_estadistico()
            self.assertIn("count", mock_stdout.getvalue())
            self.assertIn("mean", mock_stdout.getvalue())

    @patch("builtins.open", new_callable=mock_open, read_data="math_score,reading_score\n1,10\n2,20\n3,30\n4,40\n5,50")
    @patch("os.path.exists", return_value=True)
    def test_estadisticas_columna(self, mock_exists, mock_open):
        self.analisis.cargar_datos()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            stats_list = self.analisis.estadisticas_columna("math_score")
            output = mock_stdout.getvalue()
            self.assertIn("Media", stats_list[0][0])
            self.assertIn("Desviación estándar", stats_list[1][0])
            self.assertIn("Mínimo", stats_list[2][0])
            self.assertIn("Máximo", stats_list[3][0])

    @patch("builtins.open", new_callable=mock_open, read_data="math_score,reading_score\n1,10\n2,20\n3,30\n4,40\n5,50")
    @patch("os.path.exists", return_value=True)
    def test_prueba_normalidad(self, mock_exists, mock_open):
        self.analisis.cargar_datos()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.analisis.prueba_normalidad("math_score")
            output = mock_stdout.getvalue()
            self.assertIn("Prueba de Shapiro-Wilk para 'math_score':", output)
            self.assertIn("Estadística de prueba:", output)
            self.assertIn("Valor p:", output)

    @patch("os.makedirs")
    @patch("os.path.exists", return_value=False)
    def test_crear_carpeta_graficos(self, mock_exists, mock_makedirs):
        self.analisis.crear_carpeta_graficos()
        mock_makedirs.assert_called_once_with("graficos")

    @patch("builtins.open", new_callable=mock_open, read_data="math_score,reading_score\n1,10\n2,20\n3,30\n4,40\n5,50")
    @patch("os.path.exists", return_value=True)
    def test_generar_histograma(self, mock_exists, mock_open):
        self.analisis.cargar_datos()
        with patch.object(plt, 'savefig'):
            self.analisis.generar_histograma("math_score")
            plt.savefig.assert_called_with(os.path.join(self.analisis.carpeta_graficos, 'histograma_math_score.png'))

    @patch("builtins.open", new_callable=mock_open, read_data="math_score,reading_score\n1,10\n2,20\n3,30\n4,40\n5,50")
    @patch("os.path.exists", return_value=True)
    def test_generar_boxplot(self, mock_exists, mock_open):
        self.analisis.cargar_datos()
        with patch.object(plt, 'savefig'):
            self.analisis.generar_boxplot("math_score")
            plt.savefig.assert_called_with(os.path.join(self.analisis.carpeta_graficos, 'boxplot_math_score.png'))

    @patch("builtins.open", new_callable=mock_open, read_data="math_score,reading_score\n1,10\n2,20\n3,30\n4,40\n5,50")
    @patch("os.path.exists", return_value=True)
    def test_analisis_regresion_y_correlacion(self, mock_exists, mock_open):
        self.analisis.cargar_datos()
        with patch.object(plt, 'savefig'):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.analisis.analisis_regresion_y_correlacion()
                output = mock_stdout.getvalue()
                self.assertIn("Correlación:", output)
                self.assertIn("Coeficiente de determinación (R^2):", output)
                plt.savefig.assert_called_with(os.path.join(self.analisis.carpeta_graficos, 'regresion_correlacion.png'))

    @patch("builtins.open", new_callable=mock_open, read_data="math_score,reading_score\n1,10\n2,20\n3,30\n4,40\n5,50")
    @patch("os.path.exists", return_value=True)
    def test_prueba_bondad_ajuste_normal(self, mock_exists, mock_open):
        self.analisis.cargar_datos()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.analisis.prueba_bondad_ajuste_normal("math_score")
            output = mock_stdout.getvalue()
            self.assertIn("Prueba de bondad de ajuste para la normalidad en 'math_score'", output)
            self.assertIn("Estadística de prueba:", output)
            self.assertIn("Valor p:", output)

    def test_resumen_estadistico_para_grupo(self):
        data = {
            "group": ["A", "A", "B", "B"],
            "value": [1, 2, 3, 4]
        }
        df = pd.DataFrame(data)
        grupo = df.groupby('group').get_group('A')
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            AnalisisEstadistico.resumen_estadistico_para_grupo(grupo)
            output = mock_stdout.getvalue()
            self.assertIn("count", output)
            self.assertIn("mean", output)

if __name__ == "__main__":
    unittest.main()
