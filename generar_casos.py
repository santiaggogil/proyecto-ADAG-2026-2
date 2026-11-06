"""
generar_casos.py — Genera instancias sintéticas en el MISMO formato que la entrada
de la profesora, con semilla fija (reproducible).

Uso:
    python generar_casos.py                 # genera los casos aleatorios propios en casos/
    python generar_casos.py --N 40 --k 5 --B 30 --T 3 --densidad 0.3 --semilla 7 --salida casos/x.json
"""
from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

RAIZ = Path(__file__).resolve().parent


def generar(N: int, k: int, B: int, T: int, densidad: float, semilla: int) -> dict:
    rng = random.Random(semilla)
    ids = [f"N{i:02d}" for i in range(1, N + 1)]
    grafo = []
    for a in range(N):
        for b in range(a + 1, N):
            if rng.random() < densidad:
                grafo.append({"u": ids[a], "v": ids[b],
                              "peso_influencia": round(rng.uniform(0.1, 0.9), 2)})
    tope = math.ceil(T * B / k)       # misma relación que en el caso de la profesora (18 = 3·30/5)
    nodos = [{"id": i, "coeficiente_utilidad": round(rng.uniform(7.0, 13.0), 1),
              "presupuesto_total_nodo": tope,
              "costo_participacion": rng.randint(2, 7)} for i in ids]
    return {"parametros": {"numero_nodos": N, "numero_rondas": T,
                           "cupo_participantes_por_ronda_k": k,
                           "presupuesto_ruido_por_ronda_B": B,
                           "presupuesto_costos_participacion_por_ronda": round(4.8 * k)},
            "grafo": grafo, "nodos": nodos}


CASOS_PROPIOS = [
    # (archivo, N, k, B, T, densidad, semilla)
    ("propio_04_aleatorio_30_nodos.json", 30, 4, 30, 3, 0.3, 2026),
    ("propio_05_aleatorio_60_nodos.json", 60, 6, 40, 3, 0.2, 2027),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int)
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--B", type=int, default=30)
    ap.add_argument("--T", type=int, default=3)
    ap.add_argument("--densidad", type=float, default=0.3)
    ap.add_argument("--semilla", type=int, default=2026)
    ap.add_argument("--salida")
    a = ap.parse_args()
    if a.N is None:
        for nombre, N, k, B, T, d, s in CASOS_PROPIOS:
            ruta = RAIZ / "casos" / nombre
            ruta.write_text(json.dumps(generar(N, k, B, T, d, s), indent=2), encoding="utf-8")
            print("generado", ruta)
    else:
        ruta = Path(a.salida or f"casos/aleatorio_{a.N}_nodos_s{a.semilla}.json")
        ruta.write_text(json.dumps(generar(a.N, a.k, a.B, a.T, a.densidad, a.semilla), indent=2),
                        encoding="utf-8")
        print("generado", ruta)


if __name__ == "__main__":
    main()
