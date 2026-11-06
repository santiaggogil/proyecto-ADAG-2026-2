"""Pruebas de las propiedades exigidas a las funciones de utilidad del modelo."""
import random
import unittest

from solucion import modelo


class TestUtilidadNodo(unittest.TestCase):

    def test_creciente_y_concava(self):
        for a in (0.5, 7.6, 12.4):
            g = [modelo.ganancia_marginal_nodo(a, x) for x in range(100)]
            self.assertTrue(all(v > 0 for v in g))                       # creciente
            self.assertTrue(all(g[i + 1] <= g[i] for i in range(99)))     # cóncava
            for x in range(20):   # Δ(x) coincide con u(x+1) - u(x)
                self.assertAlmostEqual(g[x], modelo.utilidad_nodo(a, x + 1) - modelo.utilidad_nodo(a, x))

    def test_u_de_cero_es_cero(self):
        self.assertEqual(modelo.utilidad_nodo(10.0, 0), 0.0)


class TestUtilidadConjunta(unittest.TestCase):

    def setUp(self):
        rng = random.Random(4)
        self.N = 8
        self.coef = [rng.uniform(1, 12) for _ in range(self.N)]
        self.p = [[1.0 if i == j else 0.0 for j in range(self.N)] for i in range(self.N)]
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if rng.random() < 0.6:
                    self.p[i][j] = self.p[j][i] = rng.uniform(0, 1)
        self.rng = rng

    def f(self, S):
        return modelo.utilidad_conjunta(S, self.coef, self.p)

    def test_vacio_es_cero(self):
        self.assertEqual(self.f([]), 0.0)

    def test_monotona_y_submodular(self):
        for _ in range(500):
            C = [i for i in range(self.N) if self.rng.random() < 0.5]
            A = [i for i in C if self.rng.random() < 0.5]            # A ⊆ C
            fuera = [v for v in range(self.N) if v not in C]
            self.assertLessEqual(self.f(A), self.f(C) + 1e-12)        # monótona
            for v in fuera:                                           # submodular
                gA = self.f(A + [v]) - self.f(A)
                gC = self.f(C + [v]) - self.f(C)
                self.assertGreaterEqual(gA + 1e-12, gC)

    def test_ganancia_incremental_igual_a_diferencia(self):
        estado = modelo.CoberturaProbabilistica(self.coef, self.p)
        S = []
        for v in [3, 0, 6, 1]:
            esperado = self.f(S + [v]) - self.f(S)
            self.assertAlmostEqual(estado.ganancia(v), esperado)
            estado.agregar(v)
            S.append(v)
            self.assertAlmostEqual(estado.valor, self.f(S))

    def test_pesos_cero_uno_es_cobertura(self):
        # Con pesos 0/1 y coeficientes 1, f es Cobertura Máxima de vecindarios cerrados.
        N = 4
        p = [[1.0 if i == j else 0.0 for j in range(N)] for i in range(N)]
        p[0][1] = p[1][0] = 1.0
        p[2][3] = p[3][2] = 1.0
        coef = [1.0] * N
        self.assertEqual(modelo.utilidad_conjunta([0], coef, p), 2.0)       # cubre {0,1}
        self.assertEqual(modelo.utilidad_conjunta([0, 1], coef, p), 2.0)    # solapamiento total
        self.assertEqual(modelo.utilidad_conjunta([0, 2], coef, p), 4.0)


if __name__ == "__main__":
    unittest.main()
