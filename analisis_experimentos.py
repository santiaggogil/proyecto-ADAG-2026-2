"""
analisis_experimentos.py — Calcula el ajuste entre los tiempos medidos y la teoría.

Lee los CSV que genera experimentos.py (NO vuelve a medir tiempos) y calcula,
para cada experimento de escalamiento:
  * c   : constante que minimiza Σ (t − c·g)²   (ajuste por el origen)
  * R²  : coeficiente de determinación de ese ajuste
  * pendiente log-log: exponente observado del crecimiento (mínimos cuadrados
    sobre ln(x) frente a ln(t))
Para la Parte I variando N calcula además el ajuste con término constante
t ≈ a + c·g, que corresponde al término c3·B de la Ecuación (10) del informe.

Uso:   python analisis_experimentos.py
Salida: impresión en consola y salidas/experimentos/analisis_ajuste.csv
Solo usa la biblioteca estándar.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

DIR = Path(__file__).resolve().parent / "salidas" / "experimentos"

EXPERIMENTOS = [
    # (archivo, columna que crece, descripción)
    ("parte1_variando_B.csv", "B", "Parte I, variando B"),
    ("parte1_variando_N.csv", "N", "Parte I, variando N"),
    ("parte2_variando_N.csv", "N", "Parte II, variando N"),
    ("parte2_variando_k.csv", "k", "Parte II, variando k"),
]


def leer(nombre):
    with (DIR / nombre).open(encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def r2(medidos, predichos):
    media = sum(medidos) / len(medidos)
    ss_res = sum((t - p) ** 2 for t, p in zip(medidos, predichos))
    ss_tot = sum((t - media) ** 2 for t in medidos)
    return 1 - ss_res / ss_tot


def ajuste_origen(t, g):
    c = sum(a * b for a, b in zip(t, g)) / sum(b * b for b in g)
    return c, r2(t, [c * b for b in g])


def ajuste_con_constante(t, g):
    n = len(t)
    mg, mt = sum(g) / n, sum(t) / n
    c = sum((x - mg) * (y - mt) for x, y in zip(g, t)) / sum((x - mg) ** 2 for x in g)
    a = mt - c * mg
    return a, c, r2(t, [a + c * x for x in g])


def pendiente_loglog(xs, t):
    lx, lt = [math.log(x) for x in xs], [math.log(v) for v in t]
    n = len(lx)
    mx, my = sum(lx) / n, sum(lt) / n
    return sum((a - mx) * (b - my) for a, b in zip(lx, lt)) / sum((a - mx) ** 2 for a in lx)


def main():
    filas = []
    print(f"{'Experimento':<24}{'pendiente log-log':>20}{'R² (origen)':>14}{'R² (con constante)':>22}")
    for archivo, col, desc in EXPERIMENTOS:
        datos = leer(archivo)
        t = [float(d["tiempo_s"]) for d in datos]
        g = [float(d["teorico"]) for d in datos]
        xs = [float(d[col]) for d in datos]
        _, r2_origen = ajuste_origen(t, g)
        _, _, r2_const = ajuste_con_constante(t, g)
        pend = pendiente_loglog(xs, t)
        print(f"{desc:<24}{pend:>20.3f}{r2_origen:>14.4f}{r2_const:>22.4f}")
        filas.append({"experimento": desc, "pendiente_loglog": f"{pend:.3f}",
                      "r2_ajuste_origen": f"{r2_origen:.4f}",
                      "r2_ajuste_con_constante": f"{r2_const:.4f}"})
    with (DIR / "analisis_ajuste.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)
    print(f"\nEscrito: {DIR / 'analisis_ajuste.csv'}")


if __name__ == "__main__":
    main()