"""
salida.py — Escritura de resultados: JSON completo, traza legible y resumen de tiempos.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path


def guardar_json(resultado: dict, ruta: Path) -> None:
    ruta.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")


def _f(v: float) -> str:
    return f"{v:.4f}"


def traza_markdown(res: dict) -> str:
    par = res["parametros"]
    L = [f"# Traza del caso `{res['caso']}`", "",
         f"N = {par['N']}, T = {par['T']}, k = {par['k']}, B = {par['B']}, "
         f"presupuesto de costos = {par['presupuesto_costos']}, aristas = {par['aristas']}", "",
         f"Modelo: u_i(x) = {res['modelo']['u_i(x)']};  f(S) = {res['modelo']['f(S)']}", ""]
    for r in res["rondas"]:
        L += [f"## Ronda {r['ronda']}", "",
              f"Elegibles ({len(r['elegibles'])}): {', '.join(r['elegibles'])}", "",
              "### 1. Selección de nodos (voraz submodular) y ganancias marginales", ""]
        for p in r["traza_seleccion"]:
            orden = sorted(p["ganancias_marginales"].items(), key=lambda kv: -kv[1])
            gs = ", ".join(f"{n}={_f(g)}" for n, g in orden)
            L += [f"- Paso {p['paso']}: elegido **{p['elegido']}** "
                  f"(ganancia {_f(p['ganancia_elegida'])}, f acumulada {_f(p['utilidad_acumulada'])})",
                  f"  - Ganancias de los candidatos: {gs}"]
        L += ["", f"Selección: {', '.join(r['seleccion'])} — f(S) = {_f(r['utilidad_conjunta_f_S'])}", "",
              "### 2. Reparto del presupuesto (voraz con montículo)", "",
              "| Unidad | Nodo | Ganancia marginal | Unidades del nodo | Utilidad acumulada |",
              "|---|---|---|---|---|"]
        for u in r["traza_reparto"]:
            L.append(f"| {u['unidad']} | {u['nodo']} | {_f(u['ganancia_marginal'])} | "
                     f"{u['unidades_del_nodo']} | {_f(u['utilidad_acumulada'])} |")
        rep = ", ".join(f"{n}: {x}" for n, x in r["reparto"].items())
        L += ["", f"Reparto: {rep} — utilidad Σu_i(x_i) = {_f(r['utilidad_reparto'])}; "
                  f"usado {r['presupuesto_usado']} de {par['B']}", "",
              "### 3. Verificación de restricciones", "",
              "| Restricción | ¿Cumple? | Detalle |", "|---|---|---|"]
        for c in r["verificacion"]:
            marca = ("Sí" if c["cumple"] else "NO") + (" (informativa)" if c["informativa"] else "")
            L.append(f"| {c['restriccion']} | {marca} | {c['detalle']} |")
        L += ["", f"Tiempo: selección {r['tiempo_ms']['seleccion']:.3f} ms, "
                  f"reparto {r['tiempo_ms']['reparto']:.3f} ms", ""]
    L += ["## Resumen", "",
          f"- Gasto total por nodo: " + ", ".join(f"{n}: {g}" for n, g in res["gasto_total_por_nodo"].items()),
          f"- Topes por nodo respetados: {'Sí' if res['topes_por_nodo_respetados'] else 'NO'}",
          f"- Utilidad conjunta total (Σ_t f(S_t)): {_f(res['utilidad_conjunta_total'])}",
          f"- Utilidad de reparto total (Σ_t Σ_i u_i(x_i)): {_f(res['utilidad_reparto_total'])}",
          f"- Tiempo del algoritmo (mediana de {res['tiempo_algoritmo_ms']['repeticiones']}): "
          f"{res['tiempo_algoritmo_ms']['mediana']:.3f} ms",
          f"- Todas las restricciones obligatorias cumplen: "
          f"{'Sí' if res['todas_las_restricciones_cumplen'] else 'NO'}", ""]
    return "\n".join(L)


def guardar_traza(res: dict, ruta: Path) -> None:
    ruta.write_text(traza_markdown(res), encoding="utf-8")


def guardar_tiempos(resultados: list[dict], ruta: Path) -> None:
    with ruta.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["caso", "N", "k", "B", "T", "tiempo_mediana_ms", "tiempo_minimo_ms",
                    "utilidad_conjunta_total", "utilidad_reparto_total", "restricciones_cumplen"])
        for r in resultados:
            p = r["parametros"]
            w.writerow([r["caso"], p["N"], p["k"], p["B"], p["T"],
                        f"{r['tiempo_algoritmo_ms']['mediana']:.4f}",
                        f"{r['tiempo_algoritmo_ms']['minimo']:.4f}",
                        f"{r['utilidad_conjunta_total']:.6f}", f"{r['utilidad_reparto_total']:.6f}",
                        r["todas_las_restricciones_cumplen"]])


def resumen_consola(res: dict) -> str:
    L = [f"Caso: {res['caso']}  (N={res['parametros']['N']}, k={res['parametros']['k']}, "
         f"B={res['parametros']['B']}, T={res['parametros']['T']})"]
    for r in res["rondas"]:
        rep = ", ".join(f"{n}:{x}" for n, x in r["reparto"].items())
        L.append(f"  Ronda {r['ronda']}: S = {r['seleccion']}  f(S) = {r['utilidad_conjunta_f_S']:.4f}")
        L.append(f"           reparto = {rep}  utilidad = {r['utilidad_reparto']:.4f}")
        opt = r["comparacion_con_optimo"].get("seleccion", {})
        if "razon" in opt:
            L.append(f"           óptimo f = {opt['f_optimo']:.4f}  razón voraz/óptimo = {opt['razon']:.4f}")
    L.append(f"  Tiempo algoritmo (mediana): {res['tiempo_algoritmo_ms']['mediana']:.3f} ms")
    L.append(f"  Restricciones obligatorias: {'CUMPLEN' if res['todas_las_restricciones_cumplen'] else 'FALLAN'}")
    return "\n".join(L)
