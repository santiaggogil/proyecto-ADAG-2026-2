"""Pruebas de extremo a extremo con los casos de la carpeta casos/."""
import unittest
from pathlib import Path

from solucion import entrada, rondas

RAIZ = Path(__file__).resolve().parent.parent


class TestIntegracion(unittest.TestCase):

    def test_todos_los_casos_cumplen_restricciones(self):
        for arch in sorted((RAIZ / "casos").glob("*.json")):
            with self.subTest(caso=arch.name):
                inst = entrada.cargar(arch)
                res = rondas.ejecutar(inst, verificar=True, repeticiones=1)
                self.assertTrue(res["todas_las_restricciones_cumplen"])
                self.assertTrue(res["topes_por_nodo_respetados"])
                for r in res["rondas"]:
                    self.assertLessEqual(r["presupuesto_usado"], inst.B)

    def test_sin_aristas_es_optimo(self):
        res = rondas.ejecutar(entrada.cargar(RAIZ / "casos" / "propio_02_sin_aristas_6_nodos.json"),
                              repeticiones=1)
        r = res["rondas"][0]
        self.assertEqual(r["seleccion"], ["N4", "N2", "N5"])
        self.assertAlmostEqual(r["comparacion_con_optimo"]["seleccion"]["razon"], 1.0)

    def test_topes_agotados(self):
        res = rondas.ejecutar(entrada.cargar(RAIZ / "casos" / "propio_03_topes_agotados_5_nodos.json"),
                              repeticiones=1)
        self.assertEqual(res["rondas"][-1]["seleccion"], [])        # nadie tiene presupuesto
        self.assertEqual(res["gasto_total_por_nodo"], {"P1": 4, "P2": 4, "P3": 4, "P4": 2, "P5": 2})

    def test_caso_profesora_gasta_todo(self):
        res = rondas.ejecutar(entrada.cargar(RAIZ / "casos" / "entrada_G2_red_15_nodos.json"),
                              repeticiones=1)
        self.assertEqual([r["presupuesto_usado"] for r in res["rondas"]], [30, 30, 30])


if __name__ == "__main__":
    unittest.main()
