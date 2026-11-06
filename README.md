# ADAG 2026-B · Grupo 2 — Reparto de presupuesto y selección de participantes

Solución base de la primera entrega. En cada ronda:

1. **Parte 2 – Selección:** el algoritmo voraz submodular elige `k` participantes (garantía `1 − 1/e`, Nemhauser, Wolsey y Fisher, 1978).
2. **Parte 1 – Reparto:** el algoritmo voraz con montículo reparte el presupuesto `B` entre los elegidos (óptimo exacto, `O(N + B log N)`).

El proceso se repite durante las `T` rondas del archivo, respetando el presupuesto total de cada nodo.

## Requisitos

- Python 3.10 o superior (probado con Python 3.13).
- La solución usa solo la biblioteca estándar. `matplotlib` es opcional y solo se usa en `experimentos.py` para dibujar las figuras.

## Ejecución (Windows / PowerShell)

```powershell
cd proyecto_adag_g2
python main.py                                        # todos los casos de casos/
python main.py casos\entrada_G2_red_15_nodos.json     # solo el caso de la profesora
python main.py ruta\a\otro_caso.json                  # cualquier archivo con el mismo formato
python main.py --sin-verificacion                     # solo algoritmos (sin fuerza bruta ni DP)
```

En Linux/macOS, use `python3` y `/` en las rutas.

### Salidas (carpeta `salidas/`)

| Archivo | Contenido |
|---|---|
| `resultado_<caso>.json` | Resultados completos: selección, ganancias marginales, reparto, verificación, tiempos |
| `traza_<caso>.md` | La misma traza en formato legible (tablas por ronda) |
| `tiempos.csv` | Tiempo por caso (mediana y mínimo de 5 repeticiones) |

El programa termina con código 0 si todas las restricciones obligatorias se cumplen.

## Pruebas

```powershell
python -m unittest -v
```

Hay 25 pruebas. Comprueban las propiedades de las funciones (concavidad, monotonía, submodularidad), comparan el voraz de reparto con una programación dinámica exacta en 300 instancias aleatorias, verifican la cota `1 − 1/e` frente a la fuerza bruta, validan la lectura de la entrada y ejecutan todos los casos de extremo a extremo.

## Validación experimental

```powershell
pip install matplotlib        # solo para las figuras (opcional)
python experimentos.py        # tiempos vs. tamaño, optimalidad y razón de aproximación
```

Escribe `salidas/experimentos/*.csv` y `salidas/figuras/*.png` (semilla fija 2026).

## Generar casos sintéticos

```powershell
python generar_casos.py                                     # regenera los casos aleatorios propios
python generar_casos.py --N 40 --k 5 --B 30 --T 3 --semilla 7 --salida casos\mi_caso.json
```

## Estructura

```
main.py               punto de entrada (línea de comandos)
generar_casos.py      generador de instancias con semilla fija
experimentos.py       validación experimental (tiempos y garantías)
solucion/
  entrada.py          ÚNICO módulo que conoce el formato del JSON (si cambia la entrada, se edita solo este)
  modelo.py           fórmulas de utilidad u_i(x) y f(S) (decisiones de modelado)
  seleccion.py        Parte 2: voraz submodular + fuerza bruta (verificación)
  reparto.py          Parte 1: voraz con montículo + programación dinámica (verificación)
  rondas.py           orquestación de las T rondas y verificación de restricciones
  salida.py           escritura de JSON, traza y tiempos
casos/                entrada de la profesora + casos propios
salidas/              resultados generados
tests/                pruebas unitarias y de integración
MANUAL_TECNICO.md     manual técnico
```

Los detalles del algoritmo, los formatos, los supuestos y las limitaciones están en `MANUAL TECNICO.pdf`.