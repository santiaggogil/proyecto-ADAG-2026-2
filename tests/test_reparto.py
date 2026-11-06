"""Pruebas de la Parte 1: reparto voraz con montículo."""
import random
import unittest

from solucion import modelo, reparto


def desde_tabla(tabla):
    """Convierte una tabla de ganancias marginales por nodo en la función ganancia(i, x)."""
    return lambda i, x: tabla[i][x]


class TestRepartoVoraz(unittest.TestCase):

    def test_ejemplo_de_clase(self):
        # Ejemplo de la Fase 1: 3 nodos, B = 4. Óptimo 30 con (2, 2, 0).
        tabla = [[10, 6, 3, 1], [8, 6, 4, 2], [5, 4, 3, 2]]
        x, util, traza = reparto.voraz_monticulo(desde_tabla(tabla), [4, 4, 4], 4)
        self.assertEqual(x, [2, 2, 0])
        self.assertAlmostEqual(util, 30)
        self.assertEqual([u["ganancia_marginal"] for u in traza], [10, 8, 6, 6])

    def test_presupuesto_cero(self):
        x, util, traza = reparto.voraz_monticulo(desde_tabla([[5, 4]]), [2], 0)
        self.assertEqual((x, util, traza), ([0], 0.0, []))

    def test_topes_respetados_y_sobrante(self):
        # Suma de topes (3) menor que B (10): se asignan 3 unidades y sobran 7.
        x, util, _ = reparto.voraz_monticulo(desde_tabla([[9, 8, 7], [5, 4, 3]]), [2, 1], 10)
        self.assertEqual(x, [2, 1])
        self.assertEqual(sum(x), 3)

    def test_voraz_igual_a_programacion_dinamica(self):
        # 300 instancias aleatorias cóncavas: el voraz siempre alcanza el óptimo exacto.
        rng = random.Random(1)
        for _ in range(300):
            n = rng.randint(1, 6)
            B = rng.randint(0, 15)
            topes = [rng.randint(0, 8) for _ in range(n)]
            tabla = [sorted((rng.randint(0, 20) for _ in range(9)), reverse=True) for _ in range(n)]
            g = desde_tabla(tabla)
            x, util, _ = reparto.voraz_monticulo(g, topes, B)
            v_dp, _ = reparto.dp_exacto(g, topes, B)
            self.assertAlmostEqual(util, v_dp)
            self.assertLessEqual(sum(x), B)
            self.assertTrue(all(0 <= xi <= t for xi, t in zip(x, topes)))

    def test_con_utilidad_logaritmica_del_modelo(self):
        coef = [8.5, 12.0, 7.6, 10.1, 9.5]
        g = lambda i, x: modelo.ganancia_marginal_nodo(coef[i], x)
        x, util, _ = reparto.voraz_monticulo(g, [18] * 5, 30)
        v_dp, _ = reparto.dp_exacto(g, [18] * 5, 30)
        self.assertAlmostEqual(util, v_dp)
        self.assertAlmostEqual(util, sum(modelo.utilidad_nodo(a, xi) for a, xi in zip(coef, x)))

    def test_no_concava_puede_fallar(self):
        # Contraejemplo: con ganancias 1, 10 (no cóncava) el voraz no es óptimo.
        # Muestra por qué la hipótesis de concavidad es necesaria.
        tabla = [[1, 10], [5, 0]]
        g = desde_tabla(tabla)
        _, util, _ = reparto.voraz_monticulo(g, [2, 2], 2)
        v_dp, _ = reparto.dp_exacto(g, [2, 2], 2)
        self.assertLess(util, v_dp)   # voraz = 6, óptimo = 11


if __name__ == "__main__":
    unittest.main()
