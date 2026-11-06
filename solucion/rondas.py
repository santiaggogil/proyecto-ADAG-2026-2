"""
rondas.py — Orquestación de la solución base y verificación de restricciones.

Flujo de cada ronda (Proyecto-2026B, Figura 3.1):
  1. Elegibles: nodos con presupuesto total restante >= 1.
  2. Parte 2: voraz submodular elige k participantes.
  3. Parte 1: voraz con montículo reparte B entre ellos, sin exceder el
     presupuesto restante de cada uno.
  4. Se actualiza el presupuesto restante de cada nodo.
Se repite T veces. No hay fallas (q no viene en la entrada: es una variante).

Costo total: O(T · (k·N² + N + B log N)), que coincide con la forma
O(T · (N k τ + N + B log N)) del documento con τ = O(N).
"""
from __future__ import annotations

import math
import statistics
import time

from . import modelo, reparto, seleccion
from .entrada import Instancia

LIMITE_FUERZA_BRUTA = 200_000   # máximo de subconjuntos C(N,k) a revisar al verificar

def _resolver(inst: Instancia):
    """Ejecuta las T rondas (solo los algoritmos). Devuelve datos crudos por ronda."""
    restante = list(inst.tope)
    rondas = []
    for t in range(1, inst.T + 1):
        elegibles = [i for i in range(inst.N) if restante[i] >= 1]
        k_ronda = min(inst.k, len(elegibles))

        t0 = time.perf_counter()
        estado = modelo.CoberturaProbabilistica(inst.coef, inst.p)
        S, traza_sel = seleccion.voraz(estado, elegibles, k_ronda)
        t1 = time.perf_counter()

        topes_ronda = [restante[i] for i in S]
        ganancia = lambda idx, x, S=S: modelo.ganancia_marginal_nodo(inst.coef[S[idx]], x)
        x, util_rep, traza_rep = reparto.voraz_monticulo(ganancia, topes_ronda, inst.B)
        t2 = time.perf_counter()

        restante_antes = list(restante)
        for idx, i in enumerate(S):
            restante[i] -= x[idx]

        rondas.append({"t": t, "elegibles": elegibles, "k_ronda": k_ronda, "S": S,
                       "f_S": estado.valor, "traza_sel": traza_sel, "x": x,
                       "util_rep": util_rep, "traza_rep": traza_rep,
                       "restante_antes": restante_antes, "restante_despues": list(restante),
                       "t_sel": t1 - t0, "t_rep": t2 - t1})
    return rondas, restante


def ejecutar(inst: Instancia, verificar: bool = True, repeticiones: int = 5) -> dict:
    """Resuelve el caso, mide tiempos y verifica restricciones. Devuelve un dict serializable."""
    # Medición de tiempo: se repite el cálculo y se reporta la mediana y el mínimo.
    duraciones = []
    for _ in range(max(1, repeticiones)):
        t0 = time.perf_counter()
        rondas, restante = _resolver(inst)
        duraciones.append(time.perf_counter() - t0)

    nombre = inst.ids
    t_ver0 = time.perf_counter()
    salida_rondas = []
    todo_cumple = True
    for r in rondas:
        S, x = r["S"], r["x"]
        ver = []

        def chequeo(nombre_r, cumple, detalle, informativa=False):
            ver.append({"restriccion": nombre_r, "cumple": bool(cumple),
                        "detalle": detalle, "informativa": informativa})

        chequeo("|S| = k", len(S) == r["k_ronda"],
                f"|S| = {len(S)}, k = {inst.k}, elegibles = {len(r['elegibles'])}")
        chequeo("S sin repetidos y solo con nodos elegibles",
                len(set(S)) == len(S) and set(S) <= set(r["elegibles"]),
                f"S = {[nombre[i] for i in S]}")
        usado = sum(x)
        chequeo("Σ x_i <= B", usado <= inst.B, f"Σ x_i = {usado}, B = {inst.B}")
        chequeo("x_i enteros y 0 <= x_i <= presupuesto restante del nodo",
                all(isinstance(xi, int) and 0 <= xi <= r["restante_antes"][i]
                    for xi, i in zip(x, S)),
                "; ".join(f"{nombre[i]}: {xi} <= {r['restante_antes'][i]}" for xi, i in zip(x, S)))
        concava = True
        for i in S:
            gs = [modelo.ganancia_marginal_nodo(inst.coef[i], z)
                  for z in range(min(r["restante_antes"][i], inst.B) + 1)]
            if any(gs[z + 1] > gs[z] + 1e-12 for z in range(len(gs) - 1)) or any(g < 0 for g in gs):
                concava = False
        chequeo("u_i creciente y cóncava (ganancias marginales >= 0 y no crecientes)", concava,
                "revisado para cada nodo seleccionado hasta su tope")
        costo = sum(inst.costo[i] for i in S)
        if inst.presupuesto_costos is not None:
            chequeo("Costo de participación <= presupuesto de costos (variante 1, no impuesta en la base)",
                    costo <= inst.presupuesto_costos,
                    f"costo = {costo}, presupuesto = {inst.presupuesto_costos}", informativa=True)

        optimo = {}
        if verificar:
            # Parte 2: óptimo por fuerza bruta (si es razonable) y cota (1 - 1/e)
            num = math.comb(len(r["elegibles"]), r["k_ronda"])
            if num <= LIMITE_FUERZA_BRUTA:
                evaluar = lambda T_: modelo.utilidad_conjunta(T_, inst.coef, inst.p)
                S_opt, f_opt, cuantos = seleccion.fuerza_bruta(evaluar, r["elegibles"], r["k_ronda"])
                razon = r["f_S"] / f_opt if f_opt > 0 else 1.0
                optimo["seleccion"] = {"subconjuntos_revisados": cuantos,
                                       "S_optimo": [nombre[i] for i in S_opt],
                                       "f_optimo": f_opt, "f_voraz": r["f_S"], "razon": razon,
                                       "cota_1_menos_1_e": seleccion.COTA_NWF}
                chequeo("f(S_voraz) >= (1 - 1/e)·OPT", razon >= seleccion.COTA_NWF - 1e-9,
                        f"razón = {razon:.6f} >= {seleccion.COTA_NWF:.6f}")
            else:
                optimo["seleccion"] = {"omitida": f"C({len(r['elegibles'])},{r['k_ronda']}) = {num} "
                                                  f"> {LIMITE_FUERZA_BRUTA} subconjuntos"}
            # Parte 1: óptimo por programación dinámica
            ganancia = lambda idx, z, S=S: modelo.ganancia_marginal_nodo(inst.coef[S[idx]], z)
            v_dp, x_dp = reparto.dp_exacto(ganancia, [r["restante_antes"][i] for i in S], inst.B)
            optimo["reparto"] = {"utilidad_dp": v_dp, "utilidad_voraz": r["util_rep"]}
            chequeo("Reparto voraz = óptimo por programación dinámica",
                    abs(v_dp - r["util_rep"]) <= 1e-9 * max(1.0, v_dp),
                    f"voraz = {r['util_rep']:.6f}, DP = {v_dp:.6f}")

        todo_cumple &= all(c["cumple"] for c in ver if not c["informativa"])

        salida_rondas.append({
            "ronda": r["t"],
            "elegibles": [nombre[i] for i in r["elegibles"]],
            "seleccion": [nombre[i] for i in S],
            "utilidad_conjunta_f_S": r["f_S"],
            "traza_seleccion": [{"paso": p["paso"],
                                 "ganancias_marginales": {nombre[v]: g for v, g in p["ganancias_marginales"].items()},
                                 "elegido": nombre[p["elegido"]],
                                 "ganancia_elegida": p["ganancia_elegida"],
                                 "utilidad_acumulada": p["utilidad_acumulada"]} for p in r["traza_sel"]],
            "reparto": {nombre[i]: xi for i, xi in zip(S, x)},
            "utilidad_reparto": r["util_rep"],
            "presupuesto_usado": sum(x),
            "presupuesto_sobrante": inst.B - sum(x),
            "traza_reparto": [{"unidad": u["unidad"], "nodo": nombre[S[u["nodo"]]],
                               "ganancia_marginal": u["ganancia_marginal"],
                               "unidades_del_nodo": u["unidades_del_nodo"],
                               "utilidad_acumulada": u["utilidad_acumulada"]} for u in r["traza_rep"]],
            "costo_participacion": costo,
            "presupuesto_restante_despues": {nombre[i]: r["restante_despues"][i] for i in S},
            "tiempo_ms": {"seleccion": r["t_sel"] * 1e3, "reparto": r["t_rep"] * 1e3},
            "verificacion": ver,
            "comparacion_con_optimo": optimo,
        })

    gasto = {nombre[i]: inst.tope[i] - restante[i] for i in range(inst.N)}
    cumple_topes = all(restante[i] >= 0 for i in range(inst.N))
    todo_cumple &= cumple_topes
    t_ver = time.perf_counter() - t_ver0

    return {
        "caso": inst.nombre,
        "parametros": {"N": inst.N, "T": inst.T, "k": inst.k, "B": inst.B,
                       "presupuesto_costos": inst.presupuesto_costos, "aristas": inst.num_aristas},
        "modelo": {"u_i(x)": "a_i * ln(1 + x)",
                   "f(S)": "sum_j a_j * (1 - prod_{i in S} (1 - p_ij)), p_jj = 1",
                   "grafo": "no dirigido"},
        "rondas": salida_rondas,
        "gasto_total_por_nodo": gasto,
        "topes_por_nodo_respetados": cumple_topes,
        "utilidad_conjunta_total": sum(r["utilidad_conjunta_f_S"] for r in salida_rondas),
        "utilidad_reparto_total": sum(r["utilidad_reparto"] for r in salida_rondas),
        "tiempo_algoritmo_ms": {"mediana": statistics.median(duraciones) * 1e3,
                                "minimo": min(duraciones) * 1e3,
                                "repeticiones": len(duraciones)},
        "tiempo_verificacion_ms": t_ver * 1e3,
        "todas_las_restricciones_cumplen": todo_cumple,
    }
