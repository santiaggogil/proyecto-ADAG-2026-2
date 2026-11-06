"""
reparto.py — Parte 1: reparto óptimo del presupuesto (Proyecto-2026B, Sec 3.2).

voraz_monticulo: algoritmo de la solución (Algoritmo 3.2.1), O(N + B log N).
dp_exacto:       programación dinámica independiente, solo para VERIFICAR la
                 optimalidad del voraz en las pruebas (no es la solución).

Ambas funciones son genéricas: reciben `ganancia(i, x)`, la ganancia marginal de
la unidad número x+1 del nodo i, que debe ser no creciente en x (concavidad).
"""
from __future__ import annotations

import heapq
from typing import Callable

Ganancia = Callable[[int, int], float]


def voraz_monticulo(ganancia: Ganancia, topes: list[int], B: int):
    """
    Entrega las B unidades, una por una, al nodo de mayor ganancia marginal.

    topes[i]: máximo de unidades que puede recibir el nodo i (presupuesto
    restante del nodo). Si la suma de topes es menor que B, sobra presupuesto.

    Devuelve (x, utilidad_total, traza).
      x[i]   = unidades asignadas al nodo i
      traza  = lista con una entrada por unidad asignada

    Costo: heapify O(N) + B iteraciones × (heappop + heappush) O(log N)
           => O(N + B log N).
    Empates: el montículo compara (−ganancia, i), así que gana el índice menor.
    """
    n = len(topes)
    x = [0] * n
    monticulo = [(-ganancia(i, 0), i) for i in range(n) if topes[i] > 0]
    heapq.heapify(monticulo)                                   # O(N)
    utilidad = 0.0
    traza = []
    for unidad in range(1, B + 1):                             # a lo sumo B veces
        if not monticulo:
            break                                              # todos los topes agotados
        neg_g, i = heapq.heappop(monticulo)                    # O(log N)
        g = -neg_g
        x[i] += 1
        utilidad += g
        traza.append({"unidad": unidad, "nodo": i, "ganancia_marginal": g,
                      "unidades_del_nodo": x[i], "utilidad_acumulada": utilidad})
        if x[i] < topes[i]:
            heapq.heappush(monticulo, (-ganancia(i, x[i]), i))  # O(log N)
    return x, utilidad, traza


def dp_exacto(ganancia: Ganancia, topes: list[int], B: int):
    """
    Óptimo exacto por programación dinámica (verificador).
    mejor[i][b] = máxima utilidad usando los nodos 0..i-1 y a lo sumo b unidades.
    Costo O(N · B · min(tope, B)). Devuelve (valor_optimo, x).
    """
    n = len(topes)
    acum = []
    for i in range(n):
        lim = min(topes[i], B)
        u = [0.0]
        for xx in range(lim):
            u.append(u[-1] + ganancia(i, xx))
        acum.append(u)
    mejor = [[0.0] * (B + 1)]
    eleccion = []
    for i in range(n):
        fila, elec = [], []
        for b in range(B + 1):
            mejor_v, mejor_x = -1.0, 0
            for xx in range(min(len(acum[i]) - 1, b) + 1):
                v = mejor[i][b - xx] + acum[i][xx]
                if v > mejor_v:
                    mejor_v, mejor_x = v, xx
            fila.append(mejor_v)
            elec.append(mejor_x)
        mejor.append(fila)
        eleccion.append(elec)
    x = [0] * n
    b = B
    for i in range(n - 1, -1, -1):
        x[i] = eleccion[i][b]
        b -= x[i]
    return mejor[n][B], x
