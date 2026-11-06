"""Pruebas de la Parte 2: selección voraz y cota (1 - 1/e)."""
import random
import unittest

from solucion import modelo, seleccion


def f_conjuntos(conjuntos):
    return lambda S: float(len(set().union(*(conjuntos[i] for i in S)))) if S else 0.0


class TestSeleccion(unittest.TestCase):

    def test_ejemplo_de_clase_cobertura(self):
        # Fase 1: N1={1,2,3,4}, N2={1,2,5}, N3={3,4,6}, k=2. Voraz = 5, óptimo = 6.
        conj = [{1, 2, 3, 4}, {1, 2, 5}, {3, 4, 6}]
        S, traza = seleccion.voraz(modelo.CoberturaConjuntos(conj), [0, 1, 2], 2)
        self.assertEqual(S[0], 0)
        self.assertEqual(traza[-1]["utilidad_acumulada"], 5)
        S_opt, f_opt, cuantos = seleccion.fuerza_bruta(f_conjuntos(conj), [0, 1, 2], 2)
        self.assertEqual(sorted(S_opt), [1, 2])
        self.assertEqual(f_opt, 6)
        self.assertEqual(cuantos, 3)
        self.assertGreaterEqual(5 / 6, seleccion.COTA_NWF)

    def test_cota_en_instancias_aleatorias_de_cobertura(self):
        rng = random.Random(2)
        for _ in range(150):
            N, k = rng.randint(3, 9), None
            k = rng.randint(1, N - 1)
            conj = [set(rng.sample(range(12), rng.randint(0, 6))) for _ in range(N)]
            S, traza = seleccion.voraz(modelo.CoberturaConjuntos(conj), list(range(N)), k)
            val = traza[-1]["utilidad_acumulada"]
            _, f_opt, _ = seleccion.fuerza_bruta(f_conjuntos(conj), list(range(N)), k)
            self.assertGreaterEqual(val + 1e-9, seleccion.COTA_NWF * f_opt)

    def test_cota_con_cobertura_probabilistica(self):
        rng = random.Random(3)
        for _ in range(80):
            N = rng.randint(3, 8)
            k = rng.randint(1, N - 1)
            coef = [rng.uniform(1, 10) for _ in range(N)]
            p = [[1.0 if i == j else 0.0 for j in range(N)] for i in range(N)]
            for i in range(N):
                for j in range(i + 1, N):
                    if rng.random() < 0.5:
                        p[i][j] = p[j][i] = rng.uniform(0, 1)
            S, _ = seleccion.voraz(modelo.CoberturaProbabilistica(coef, p), list(range(N)), k)
            evaluar = lambda T: modelo.utilidad_conjunta(T, coef, p)
            _, f_opt, _ = seleccion.fuerza_bruta(evaluar, list(range(N)), k)
            self.assertGreaterEqual(evaluar(S) + 1e-9, seleccion.COTA_NWF * f_opt)

    def test_sin_aristas_voraz_es_optimo(self):
        # Sin grafo, f(S) = Σ_{i∈S} a_i (aditiva): el voraz elige los k mayores y es óptimo.
        coef = [3.0, 9.0, 5.0, 12.0, 7.0, 1.0]
        p = [[1.0 if i == j else 0.0 for j in range(6)] for i in range(6)]
        S, _ = seleccion.voraz(modelo.CoberturaProbabilistica(coef, p), list(range(6)), 3)
        self.assertEqual(S, [3, 1, 4])

    def test_empate_gana_el_primero(self):
        conj = [{1}, {2}, {3}]
        S, _ = seleccion.voraz(modelo.CoberturaConjuntos(conj), [0, 1, 2], 1)
        self.assertEqual(S, [0])

    def test_k_mayor_que_candidatos(self):
        S, _ = seleccion.voraz(modelo.CoberturaConjuntos([{1}, {2}]), [0, 1], 5)
        self.assertEqual(sorted(S), [0, 1])


if __name__ == "__main__":
    unittest.main()
