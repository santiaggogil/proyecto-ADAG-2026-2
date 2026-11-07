# Traza del caso `propio_01_pequeno_6_nodos`

N = 6, T = 2, k = 2, B = 8, presupuesto de costos = 8, aristas = 6

Modelo: u_i(x) = a_i * ln(1 + x);  f(S) = sum_j a_j * (1 - prod_{i in S} (1 - p_ij)), p_jj = 1

## Ronda 1

Elegibles (6): A, B, C, D, E, F

### 1. Selección de nodos (voraz submodular) y ganancias marginales

- Paso 1: elegido **A** (ganancia 20.8000, f acumulada 20.8000)
  - Ganancias de los candidatos: A=20.8000, C=18.9000, B=18.0000, D=17.6000, E=12.2000, F=12.2000
- Paso 2: elegido **D** (ganancia 17.0600, f acumulada 37.8600)
  - Ganancias de los candidatos: D=17.0600, E=12.2000, F=12.2000, C=1.8000, B=0.9000

Selección: A, D — f(S) = 37.8600

### 2. Reparto del presupuesto (voraz con montículo)

| Unidad | Nodo | Ganancia marginal | Unidades del nodo | Utilidad acumulada |
|---|---|---|---|---|
| 1 | A | 6.9315 | 1 | 6.9315 |
| 2 | D | 6.2383 | 1 | 13.1698 |
| 3 | A | 4.0547 | 2 | 17.2244 |
| 4 | D | 3.6492 | 2 | 20.8736 |
| 5 | A | 2.8768 | 3 | 23.7505 |
| 6 | D | 2.5891 | 3 | 26.3396 |
| 7 | A | 2.2314 | 4 | 28.5710 |
| 8 | D | 2.0083 | 4 | 30.5793 |

Reparto: A: 4, D: 4 — utilidad Σu_i(x_i) = 30.5793; usado 8 de 8

### 3. Verificación de restricciones

| Restricción | ¿Cumple? | Detalle |
|---|---|---|
| |S| = k | Sí | |S| = 2, k = 2, elegibles = 6 |
| S sin repetidos y solo con nodos elegibles | Sí | S = ['A', 'D'] |
| Σ x_i <= B | Sí | Σ x_i = 8, B = 8 |
| x_i enteros y 0 <= x_i <= presupuesto restante del nodo | Sí | A: 4 <= 8; D: 4 <= 8 |
| u_i creciente y cóncava (ganancias marginales >= 0 y no crecientes) | Sí | revisado para cada nodo seleccionado hasta su tope |
| Costo de participación <= presupuesto de costos (variante 1, no impuesta en la base) | Sí (informativa) | costo = 7, presupuesto = 8 |
| f(S_voraz) >= (1 - 1/e)·OPT | Sí | razón = 1.000000 >= 0.632121 |
| Reparto voraz = óptimo por programación dinámica | Sí | voraz = 30.579320, DP = 30.579320 |

Tiempo: selección 0.018 ms, reparto 0.007 ms

## Ronda 2

Elegibles (6): A, B, C, D, E, F

### 1. Selección de nodos (voraz submodular) y ganancias marginales

- Paso 1: elegido **A** (ganancia 20.8000, f acumulada 20.8000)
  - Ganancias de los candidatos: A=20.8000, C=18.9000, B=18.0000, D=17.6000, E=12.2000, F=12.2000
- Paso 2: elegido **D** (ganancia 17.0600, f acumulada 37.8600)
  - Ganancias de los candidatos: D=17.0600, E=12.2000, F=12.2000, C=1.8000, B=0.9000

Selección: A, D — f(S) = 37.8600

### 2. Reparto del presupuesto (voraz con montículo)

| Unidad | Nodo | Ganancia marginal | Unidades del nodo | Utilidad acumulada |
|---|---|---|---|---|
| 1 | A | 6.9315 | 1 | 6.9315 |
| 2 | D | 6.2383 | 1 | 13.1698 |
| 3 | A | 4.0547 | 2 | 17.2244 |
| 4 | D | 3.6492 | 2 | 20.8736 |
| 5 | A | 2.8768 | 3 | 23.7505 |
| 6 | D | 2.5891 | 3 | 26.3396 |
| 7 | A | 2.2314 | 4 | 28.5710 |
| 8 | D | 2.0083 | 4 | 30.5793 |

Reparto: A: 4, D: 4 — utilidad Σu_i(x_i) = 30.5793; usado 8 de 8

### 3. Verificación de restricciones

| Restricción | ¿Cumple? | Detalle |
|---|---|---|
| |S| = k | Sí | |S| = 2, k = 2, elegibles = 6 |
| S sin repetidos y solo con nodos elegibles | Sí | S = ['A', 'D'] |
| Σ x_i <= B | Sí | Σ x_i = 8, B = 8 |
| x_i enteros y 0 <= x_i <= presupuesto restante del nodo | Sí | A: 4 <= 4; D: 4 <= 4 |
| u_i creciente y cóncava (ganancias marginales >= 0 y no crecientes) | Sí | revisado para cada nodo seleccionado hasta su tope |
| Costo de participación <= presupuesto de costos (variante 1, no impuesta en la base) | Sí (informativa) | costo = 7, presupuesto = 8 |
| f(S_voraz) >= (1 - 1/e)·OPT | Sí | razón = 1.000000 >= 0.632121 |
| Reparto voraz = óptimo por programación dinámica | Sí | voraz = 30.579320, DP = 30.579320 |

Tiempo: selección 0.019 ms, reparto 0.006 ms

## Resumen

- Gasto total por nodo: A: 8, B: 0, C: 0, D: 8, E: 0, F: 0
- Topes por nodo respetados: Sí
- Utilidad conjunta total (Σ_t f(S_t)): 75.7200
- Utilidad de reparto total (Σ_t Σ_i u_i(x_i)): 61.1586
- Tiempo del algoritmo (mediana de 5): 0.060 ms
- Todas las restricciones obligatorias cumplen: Sí
