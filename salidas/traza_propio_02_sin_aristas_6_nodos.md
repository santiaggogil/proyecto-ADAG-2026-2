# Traza del caso `propio_02_sin_aristas_6_nodos`

N = 6, T = 1, k = 3, B = 9, presupuesto de costos = None, aristas = 0

Modelo: u_i(x) = a_i * ln(1 + x);  f(S) = sum_j a_j * (1 - prod_{i in S} (1 - p_ij)), p_jj = 1

## Ronda 1

Elegibles (6): N1, N2, N3, N4, N5, N6

### 1. Selección de nodos (voraz submodular) y ganancias marginales

- Paso 1: elegido **N4** (ganancia 12.0000, f acumulada 12.0000)
  - Ganancias de los candidatos: N4=12.0000, N2=9.0000, N5=7.0000, N3=5.0000, N1=3.0000, N6=1.0000
- Paso 2: elegido **N2** (ganancia 9.0000, f acumulada 21.0000)
  - Ganancias de los candidatos: N2=9.0000, N5=7.0000, N3=5.0000, N1=3.0000, N6=1.0000
- Paso 3: elegido **N5** (ganancia 7.0000, f acumulada 28.0000)
  - Ganancias de los candidatos: N5=7.0000, N3=5.0000, N1=3.0000, N6=1.0000

Selección: N4, N2, N5 — f(S) = 28.0000

### 2. Reparto del presupuesto (voraz con montículo)

| Unidad | Nodo | Ganancia marginal | Unidades del nodo | Utilidad acumulada |
|---|---|---|---|---|
| 1 | N4 | 8.3178 | 1 | 8.3178 |
| 2 | N2 | 6.2383 | 1 | 14.5561 |
| 3 | N4 | 4.8656 | 2 | 19.4217 |
| 4 | N5 | 4.8520 | 1 | 24.2737 |
| 5 | N2 | 3.6492 | 2 | 27.9229 |
| 6 | N4 | 3.4522 | 3 | 31.3751 |
| 7 | N5 | 2.8383 | 2 | 34.2133 |
| 8 | N4 | 2.6777 | 4 | 36.8911 |
| 9 | N2 | 2.5891 | 3 | 39.4802 |

Reparto: N4: 4, N2: 3, N5: 2 — utilidad Σu_i(x_i) = 39.4802; usado 9 de 9

### 3. Verificación de restricciones

| Restricción | ¿Cumple? | Detalle |
|---|---|---|
| |S| = k | Sí | |S| = 3, k = 3, elegibles = 6 |
| S sin repetidos y solo con nodos elegibles | Sí | S = ['N4', 'N2', 'N5'] |
| Σ x_i <= B | Sí | Σ x_i = 9, B = 9 |
| x_i enteros y 0 <= x_i <= presupuesto restante del nodo | Sí | N4: 4 <= 9; N2: 3 <= 9; N5: 2 <= 9 |
| u_i creciente y cóncava (ganancias marginales >= 0 y no crecientes) | Sí | revisado para cada nodo seleccionado hasta su tope |
| f(S_voraz) >= (1 - 1/e)·OPT | Sí | razón = 1.000000 >= 0.632121 |
| Reparto voraz = óptimo por programación dinámica | Sí | voraz = 39.480190, DP = 39.480190 |

Tiempo: selección 0.014 ms, reparto 0.005 ms

## Resumen

- Gasto total por nodo: N1: 0, N2: 3, N3: 0, N4: 4, N5: 2, N6: 0
- Topes por nodo respetados: Sí
- Utilidad conjunta total (Σ_t f(S_t)): 28.0000
- Utilidad de reparto total (Σ_t Σ_i u_i(x_i)): 39.4802
- Tiempo del algoritmo (mediana de 5): 0.023 ms
- Todas las restricciones obligatorias cumplen: Sí
