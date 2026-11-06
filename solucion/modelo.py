"""
modelo.py — Funciones de utilidad del problema (decisiones de modelado).

Los documentos exigen propiedades (u_i creciente y cóncava; f monótona y
submodular) pero el archivo de entrada no fija sus fórmulas. Aquí se definen las
fórmulas adoptadas. Si se decide otro modelo, solo cambia este archivo: los
algoritmos (reparto.py, seleccion.py) son genéricos.

Parte 1 — utilidad de cada nodo:
    u_i(x) = a_i * ln(1 + x)
    Δ_i(x) = u_i(x+1) - u_i(x) = a_i * ln(1 + 1/(x+1))   (> 0 y decreciente en x)

Parte 2 — utilidad conjunta (cobertura probabilística ponderada):
    f(S) = Σ_j a_j * (1 - Π_{i∈S} (1 - p_ij)),   con p_jj = 1
    f(∅) = 0, monótona y submodular (demostración en el informe).
"""
from __future__ import annotations

import math


# Parte 1
def utilidad_nodo(a: float, x: int) -> float:
    """u(x) = a·ln(1 + x)."""
    return a * math.log1p(x)


def ganancia_marginal_nodo(a: float, x: int) -> float:
    """Δ(x) = u(x+1) - u(x) = a·ln(1 + 1/(x+1)). Costo O(1)."""
    return a * math.log1p(1.0 / (x + 1))


# Parte 2
def utilidad_conjunta(S, coef: list[float], p: list[list[float]]) -> float:
    """Evaluación directa de f(S). Costo O(|S|·N). Se usa para verificar."""
    total = 0.0
    for j in range(len(coef)):
        no_cubierto = 1.0
        for i in S:
            no_cubierto *= 1.0 - p[i][j]
        total += coef[j] * (1.0 - no_cubierto)
    return total


class CoberturaProbabilistica:
    """
    Estado incremental de f para el voraz.

    Mantiene r_j = Π_{i∈S} (1 - p_ij): la "probabilidad de que j siga sin cubrir".
    Entonces la ganancia marginal de v es
        Δ(v | S) = f(S ∪ {v}) - f(S) = Σ_j a_j · r_j · p_vj,
    que se calcula en O(N) (este es el τ del documento, Sec 3.3).
    """

    def __init__(self, coef: list[float], p: list[list[float]]):
        self.coef = coef
        self.p = p
        self.residuo = [1.0] * len(coef)
        self.valor = 0.0
        self.seleccionados: list[int] = []

    def ganancia(self, v: int) -> float:
        pv = self.p[v]
        return sum(a * r * w for a, r, w in zip(self.coef, self.residuo, pv))

    def agregar(self, v: int) -> float:
        g = self.ganancia(v)
        pv = self.p[v]
        for j in range(len(self.residuo)):
            self.residuo[j] *= 1.0 - pv[j]
        self.valor += g
        self.seleccionados.append(v)
        return g


class CoberturaConjuntos:
    """
    Cobertura clásica (Cobertura Máxima): f(S) = |∪_{i∈S} C_i|.
    No la usa el programa principal; sirve en las pruebas y es exactamente la
    función de la reducción de NP-dureza.
    """

    def __init__(self, conjuntos: list[set]):
        self.conjuntos = conjuntos
        self.cubiertos: set = set()
        self.valor = 0.0
        self.seleccionados: list[int] = []

    def ganancia(self, v: int) -> float:
        return float(len(self.conjuntos[v] - self.cubiertos))

    def agregar(self, v: int) -> float:
        g = self.ganancia(v)
        self.cubiertos |= self.conjuntos[v]
        self.valor += g
        self.seleccionados.append(v)
        return g
