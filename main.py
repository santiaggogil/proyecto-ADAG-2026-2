"""
main.py — Punto de entrada de la solución base.

Uso:
    python main.py                       # ejecuta todos los casos de la carpeta casos/
    python main.py casos/archivo.json    # ejecuta uno o varios archivos
    python main.py --sin-verificacion    # omite fuerza bruta y DP (solo algoritmos)

Por cada caso escribe en salidas/:
    resultado_<caso>.json   resultados completos, traza y verificaciones
    traza_<caso>.md         traza legible (selección, ganancias, reparto, restricciones)
y además salidas/tiempos.csv con el tiempo por caso.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from solucion import entrada, rondas, salida

RAIZ = Path(__file__).resolve().parent


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

    ap = argparse.ArgumentParser(description="Solución base ADAG G2: selección voraz + reparto voraz.")
    ap.add_argument("entradas", nargs="*", help="archivos JSON de entrada (por defecto: casos/*.json)")
    ap.add_argument("--salida", default=str(RAIZ / "salidas"), help="carpeta de resultados")
    ap.add_argument("--sin-verificacion", action="store_true",
                    help="no calcular óptimos por fuerza bruta / programación dinámica")
    ap.add_argument("--repeticiones", type=int, default=5, help="repeticiones para medir tiempo")
    args = ap.parse_args(argv)

    archivos = [Path(a) for a in args.entradas] or sorted((RAIZ / "casos").glob("*.json"))
    if not archivos:
        print("No se encontraron archivos de entrada.")
        return 1
    carpeta = Path(args.salida)
    carpeta.mkdir(parents=True, exist_ok=True)

    resultados, errores = [], 0
    for arch in archivos:
        try:
            inst = entrada.cargar(arch)
        except (entrada.ErrorEntrada, OSError) as e:
            print(f"[ERROR] {arch}: {e}")
            errores += 1
            continue
        res = rondas.ejecutar(inst, verificar=not args.sin_verificacion,
                              repeticiones=args.repeticiones)
        salida.guardar_json(res, carpeta / f"resultado_{inst.nombre}.json")
        salida.guardar_traza(res, carpeta / f"traza_{inst.nombre}.md")
        print(salida.resumen_consola(res))
        print()
        resultados.append(res)

    if resultados:
        salida.guardar_tiempos(resultados, carpeta / "tiempos.csv")
        print(f"Resultados escritos en: {carpeta}")
    return 1 if errores or not all(r["todas_las_restricciones_cumplen"] for r in resultados) else 0


if __name__ == "__main__":
    sys.exit(main())
