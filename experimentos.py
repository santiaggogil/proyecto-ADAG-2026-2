"""
experimentos.py — Validación experimental de la solución base (semillas fijas).

Mide el tiempo real de los dos algoritmos voraces para tamaños crecientes y lo
compara con el crecimiento que predice la función de eficiencia teórica.
También verifica empíricamente:
  * la optimalidad del reparto voraz (frente a programación dinámica), y
  * la cota (1 - 1/e) de la selección voraz (frente a fuerza bruta).

Uso:  python experimentos.py           (requiere matplotlib solo para las figuras)
Salida: salidas/experimentos/*.csv y salidas/figuras/*.png
"""
from __future__ import annotations

import csv
import math
import random
import statistics
import time
from pathlib import Path

from solucion import modelo, reparto, seleccion

RAIZ = Path(__file__).resolve().parent
DIR_CSV = RAIZ / "salidas" / "experimentos"
DIR_FIG = RAIZ / "salidas" / "figuras"
AZUL, NARANJA, TINTA, GRIS = "#2a78d6", "#eb6834", "#3d3d3a", "#d3d1c7"


def mediana_tiempo(funcion, repeticiones):
    tiempos = []
    for _ in range(repeticiones):
        t0 = time.perf_counter()
        funcion()
        tiempos.append(time.perf_counter() - t0)
    return statistics.median(tiempos)


def instancia_grafo(N, densidad, rng):
    coef = [rng.uniform(7, 13) for _ in range(N)]
    p = [[0.0] * N for _ in range(N)]
    for i in range(N):
        p[i][i] = 1.0
        for j in range(i + 1, N):
            if rng.random() < densidad:
                p[i][j] = p[j][i] = rng.uniform(0.1, 0.9)
    return coef, p


def ajustar_constante(medidos, teoricos):
    """c que minimiza Σ (t - c·g)^2  =>  c = Σ t·g / Σ g²."""
    return sum(t * g for t, g in zip(medidos, teoricos)) / sum(g * g for g in teoricos)


# ---------------------------------------------------------------------------
def exp_reparto_variando_B(rng):
    N, filas = 100, []
    coef = [rng.uniform(7, 13) for _ in range(N)]
    for B in [2000, 4000, 8000, 16000, 32000, 64000]:
        g = lambda i, x: modelo.ganancia_marginal_nodo(coef[i], x)
        t = mediana_tiempo(lambda: reparto.voraz_monticulo(g, [B] * N, B), 7)
        filas.append({"N": N, "B": B, "tiempo_s": t, "teorico": N + B * math.log2(N)})
    return filas


def exp_reparto_variando_N(rng):
    B, filas = 20000, []
    for N in [16, 64, 256, 1024, 4096, 16384]:
        coef = [rng.uniform(7, 13) for _ in range(N)]
        g = lambda i, x, coef=coef: modelo.ganancia_marginal_nodo(coef[i], x)
        t = mediana_tiempo(lambda: reparto.voraz_monticulo(g, [B] * N, B), 7)
        filas.append({"N": N, "B": B, "tiempo_s": t, "teorico": N + B * math.log2(N)})
    return filas


def _conteo_seleccion(N, k):
    # Evaluaciones de ganancia × costo τ = N, más la actualización O(N) por paso.
    return sum((N - s + 1) * N + N for s in range(1, k + 1))


def exp_seleccion_variando_N(rng):
    k, filas = 10, []
    for N in [50, 100, 200, 400, 800, 1600]:
        coef, p = instancia_grafo(N, 0.3, rng)
        t = mediana_tiempo(lambda: seleccion.voraz(modelo.CoberturaProbabilistica(coef, p),
                                                   list(range(N)), k), 3)
        filas.append({"N": N, "k": k, "tiempo_s": t, "teorico": _conteo_seleccion(N, k)})
    return filas


def exp_seleccion_variando_k(rng):
    N, filas = 400, []
    coef, p = instancia_grafo(N, 0.3, rng)
    for k in [5, 10, 20, 40, 80, 160]:
        t = mediana_tiempo(lambda: seleccion.voraz(modelo.CoberturaProbabilistica(coef, p),
                                                   list(range(N)), k), 3)
        filas.append({"N": N, "k": k, "tiempo_s": t, "teorico": _conteo_seleccion(N, k)})
    return filas


def exp_razon_aproximacion(rng):
    """200 instancias de cobertura probabilística y 200 de cobertura clásica (N=12, k=4)."""
    filas = []
    for tipo in ("probabilistica", "conjuntos"):
        for rep in range(200):
            N, k = 12, 4
            if tipo == "probabilistica":
                coef, p = instancia_grafo(N, 0.4, rng)
                estado = modelo.CoberturaProbabilistica(coef, p)
                evaluar = lambda S, coef=coef, p=p: modelo.utilidad_conjunta(S, coef, p)
            else:
                conj = [set(rng.sample(range(20), rng.randint(1, 7))) for _ in range(N)]
                estado = modelo.CoberturaConjuntos(conj)
                evaluar = lambda S, conj=conj: float(len(set().union(*(conj[i] for i in S))))
            S, _ = seleccion.voraz(estado, list(range(N)), k)
            _, opt, _ = seleccion.fuerza_bruta(evaluar, list(range(N)), k)
            filas.append({"tipo": tipo, "instancia": rep, "voraz": evaluar(S), "optimo": opt,
                          "razon": evaluar(S) / opt if opt > 0 else 1.0})
    return filas


def exp_optimalidad_reparto(rng):
    filas = []
    for rep in range(300):
        n = rng.randint(2, 8)
        B = rng.randint(1, 40)
        coef = [rng.uniform(7, 13) for _ in range(n)]
        topes = [rng.randint(0, 15) for _ in range(n)]
        g = lambda i, x, coef=coef: modelo.ganancia_marginal_nodo(coef[i], x)
        _, uv, _ = reparto.voraz_monticulo(g, topes, B)
        ud, _ = reparto.dp_exacto(g, topes, B)
        filas.append({"instancia": rep, "N": n, "B": B, "voraz": uv, "dp": ud,
                      "diferencia": abs(uv - ud)})
    return filas


# ---------------------------------------------------------------------------
def guardar_csv(nombre, filas):
    with (DIR_CSV / nombre).open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)


def _estilo(ax, titulo, xlabel, ylabel):
    ax.set_title(titulo, loc="left", fontsize=12, color=TINTA)
    ax.set_xlabel(xlabel, color=TINTA)
    ax.set_ylabel(ylabel, color=TINTA)
    ax.grid(True, color=GRIS, linewidth=0.6)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(GRIS)
    ax.tick_params(colors=TINTA)


def figura_escalamiento(filas, eje_x, titulo, xlabel, etiqueta_teorica, archivo, logx=False):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    xs = [f[eje_x] for f in filas]
    ts = [f["tiempo_s"] * 1e3 for f in filas]
    gs = [f["teorico"] for f in filas]
    c = ajustar_constante(ts, gs)
    fig, ax = plt.subplots(figsize=(6.4, 3.8), dpi=200)
    ax.plot(xs, [c * g for g in gs], color=NARANJA, linewidth=2, linestyle="--",
            label=f"Teórico: c · {etiqueta_teorica}")
    ax.plot(xs, ts, color=AZUL, linewidth=2, marker="o", markersize=6, label="Medido (mediana)")
    if logx:
        ax.set_xscale("log", base=2)
    _estilo(ax, titulo, xlabel, "Tiempo (ms)")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(DIR_FIG / archivo)
    plt.close(fig)
    return c


def figura_razon(filas, archivo):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6.4, 3.8), dpi=200)
    for tipo, color, nombre in (("probabilistica", AZUL, "Cobertura probabilística (modelo)"),
                                ("conjuntos", NARANJA, "Cobertura clásica")):
        rs = [f["razon"] for f in filas if f["tipo"] == tipo]
        ax.hist(rs, bins=[0.60 + 0.01 * i for i in range(41)], color=color, alpha=0.75,
                label=nombre, edgecolor="white", linewidth=0.8)
    ax.axvline(1 - 1 / math.e, color=TINTA, linewidth=1.2, linestyle=":")
    ax.text(1 - 1 / math.e + 0.006, ax.get_ylim()[1] * 0.45, "cota garantizada\n1 − 1/e ≈ 0,632",
            color=TINTA, fontsize=9)
    _estilo(ax, "Razón voraz / óptimo en 400 instancias (N = 12, k = 4)",
            "Razón f(S_voraz) / OPT", "Número de instancias")
    ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(0.30, 0.95))
    fig.tight_layout()
    fig.savefig(DIR_FIG / archivo)
    plt.close(fig)


def main():
    DIR_CSV.mkdir(parents=True, exist_ok=True)
    DIR_FIG.mkdir(parents=True, exist_ok=True)
    rng = random.Random(2026)

    e1 = exp_reparto_variando_B(rng); guardar_csv("parte1_variando_B.csv", e1)
    e2 = exp_reparto_variando_N(rng); guardar_csv("parte1_variando_N.csv", e2)
    e3 = exp_seleccion_variando_N(rng); guardar_csv("parte2_variando_N.csv", e3)
    e4 = exp_seleccion_variando_k(rng); guardar_csv("parte2_variando_k.csv", e4)
    e5 = exp_razon_aproximacion(rng); guardar_csv("parte2_razon_aproximacion.csv", e5)
    e6 = exp_optimalidad_reparto(rng); guardar_csv("parte1_optimalidad.csv", e6)

    try:
        figura_escalamiento(e1, "B", "Parte 1: tiempo del reparto voraz al crecer B (N = 100)",
                            "Presupuesto B (unidades)", "(N + B·log₂N)", "fig_parte1_B.png")
        figura_escalamiento(e2, "N", "Parte 1: tiempo del reparto voraz al crecer N (B = 20 000)",
                            "Número de nodos N (escala log₂)", "(N + B·log₂N)", "fig_parte1_N.png",
                            logx=True)
        figura_escalamiento(e3, "N", "Parte 2: tiempo de la selección voraz al crecer N (k = 10)",
                            "Número de candidatos N", "Σ (N−s+2)·N", "fig_parte2_N.png")
        figura_escalamiento(e4, "k", "Parte 2: tiempo de la selección voraz al crecer k (N = 400)",
                            "Cupo k", "Σ (N−s+2)·N", "fig_parte2_k.png")
        figura_razon(e5, "fig_razon_aproximacion.png")
    except ImportError:
        print("matplotlib no está instalado: se omiten las figuras (los CSV sí se generaron).")

    for nombre, filas in (("Parte 1, variando B", e1), ("Parte 1, variando N", e2),
                          ("Parte 2, variando N", e3), ("Parte 2, variando k", e4)):
        print(nombre)
        for f in filas:
            print("   ", {k: (round(v, 6) if isinstance(v, float) else v) for k, v in f.items()})
    for tipo in ("probabilistica", "conjuntos"):
        rs = [f["razon"] for f in e5 if f["tipo"] == tipo]
        print(f"Razón {tipo}: min={min(rs):.4f} media={statistics.mean(rs):.4f} "
              f"óptimo exacto en {sum(r > 1 - 1e-9 for r in rs)}/{len(rs)}")
    print(f"Reparto: voraz = DP en {sum(f['diferencia'] < 1e-9 for f in e6)}/{len(e6)} "
          f"(máx. diferencia {max(f['diferencia'] for f in e6):.2e})")


if __name__ == "__main__":
    main()
