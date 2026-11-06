"""Pruebas del módulo de entrada (lectura y validación)."""
import copy
import unittest
from pathlib import Path

from solucion import entrada

RAIZ = Path(__file__).resolve().parent.parent
CASO_PROFESORA = RAIZ / "casos" / "entrada_G2_red_15_nodos.json"

BASE = {
    "parametros": {"numero_nodos": 3, "numero_rondas": 1, "cupo_participantes_por_ronda_k": 1,
                   "presupuesto_ruido_por_ronda_B": 4},
    "grafo": [{"u": "A", "v": "B", "peso_influencia": 0.5}],
    "nodos": [{"id": "A", "coeficiente_utilidad": 1, "presupuesto_total_nodo": 4},
              {"id": "B", "coeficiente_utilidad": 2, "presupuesto_total_nodo": 4},
              {"id": "C", "coeficiente_utilidad": 3, "presupuesto_total_nodo": 4}],
}


class TestEntrada(unittest.TestCase):

    def test_caso_profesora(self):
        inst = entrada.cargar(CASO_PROFESORA)
        self.assertEqual((inst.N, inst.T, inst.k, inst.B), (15, 3, 5, 30))
        self.assertEqual(inst.presupuesto_costos, 24)
        self.assertEqual(inst.num_aristas, 105)
        for i in range(inst.N):
            self.assertEqual(inst.p[i][i], 1.0)
            for j in range(inst.N):
                self.assertEqual(inst.p[i][j], inst.p[j][i])     # simétrica

    def test_minimo_valido(self):
        inst = entrada.desde_diccionario(BASE)
        self.assertEqual(inst.p[0][1], 0.5)
        self.assertEqual(inst.p[0][2], 0.0)
        self.assertEqual(inst.costo, [0, 0, 0])                    # costo opcional
        self.assertIsNone(inst.presupuesto_costos)

    def _error(self, modificar):
        d = copy.deepcopy(BASE)
        modificar(d)
        with self.assertRaises(entrada.ErrorEntrada):
            entrada.desde_diccionario(d)

    def test_errores(self):
        self._error(lambda d: d["parametros"].update(cupo_participantes_por_ronda_k=3))  # k >= N
        self._error(lambda d: d["parametros"].update(numero_nodos=4))                     # N no coincide
        self._error(lambda d: d["grafo"].append({"u": "A", "v": "Z", "peso_influencia": 0.1}))
        self._error(lambda d: d["grafo"].append({"u": "A", "v": "C", "peso_influencia": 1.5}))
        self._error(lambda d: d["grafo"].append({"u": "B", "v": "A", "peso_influencia": 0.7}))  # repetida
        self._error(lambda d: d["nodos"].append({"id": "A", "coeficiente_utilidad": 1}))     # id repetido
        self._error(lambda d: d["parametros"].update(presupuesto_ruido_por_ronda_B=2.5))
        self._error(lambda d: d.pop("nodos"))


if __name__ == "__main__":
    unittest.main()
