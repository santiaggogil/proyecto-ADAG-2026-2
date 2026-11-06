"""
seleccion.py — Parte 2: selección de participantes (Proyecto-2026B, Sec 3.3).

voraz:        algoritmo de la solución. En cada uno de los k pasos evalúa la
              ganancia marginal de todos los candidatos restantes y agrega el
              mejor. O(N·k) evaluaciones de ganancia; con CoberturaProbabilistica
              cada una cuesta τ = O(N), así que T(N, k) = O(k·N²).
              Garantía: f(S_voraz) >= (1 - 1/e)·OPT (Nemhauser, Wolsey y Fisher, 1978).
fuerza_bruta: óptimo exacto revisando los C(N, k) subconjuntos. Solo para
              verificar la cota en instancias pequeñas, como exige el documento.
"""
from __future__ import annotations

import math
from itertools import combinations

TOLERANCIA = 1e-12
COTA_NWF = 1.0 - 1.0 / math.e   # ≈ 0.6321


def voraz(estado, candidatos: list[int], k: int):
    """
    estado: objeto con métodos ganancia(v), agregar(v) y atributo valor
            (por ejemplo, modelo.CoberturaProbabilistica).
    candidatos: índices elegibles en esta ronda.
    Devuelve (seleccion, traza). Empates: gana el candidato que aparece primero.
    """
    restantes = list(candidatos)
    seleccion = []
    traza = []
    for paso in range(1, min(k, len(restantes)) + 1):          # k pasos
        ganancias = {}
        mejor_v, mejor_g = None, -math.inf
        for v in restantes:                                     # O(N) candidatos
            g = estado.ganancia(v)                              # τ
            ganancias[v] = g
            if g > mejor_g + TOLERANCIA:
                mejor_v, mejor_g = v, g
        estado.agregar(mejor_v)
        restantes.remove(mejor_v)
        seleccion.append(mejor_v)
        traza.append({"paso": paso, "ganancias_marginales": ganancias,
                      "elegido": mejor_v, "ganancia_elegida": mejor_g,
                      "utilidad_acumulada": estado.valor})
    return seleccion, traza


def fuerza_bruta(evaluar_f, candidatos: list[int], k: int):
    """Revisa todos los subconjuntos de tamaño k. Devuelve (mejor_S, valor, cuantos)."""
    mejor_S, mejor_val, cuantos = None, -math.inf, 0
    for S in combinations(candidatos, k):
        cuantos += 1
        val = evaluar_f(S)
        if val > mejor_val + TOLERANCIA:
            mejor_S, mejor_val = list(S), val
    return mejor_S, mejor_val, cuantos
