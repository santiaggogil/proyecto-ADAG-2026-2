# Traza del caso `propio_03_topes_agotados_5_nodos`

N = 5, T = 3, k = 3, B = 10, presupuesto de costos = 12, aristas = 5

Modelo: u_i(x) = a_i * ln(1 + x);  f(S) = sum_j a_j * (1 - prod_{i in S} (1 - p_ij)), p_jj = 1

## Ronda 1

Elegibles (5): P1, P2, P3, P4, P5

### 1. Selección de nodos (voraz submodular) y ganancias marginales

- Paso 1: elegido **P3** (ganancia 19.2000, f acumulada 19.2000)
  - Ganancias de los candidatos: P3=19.2000, P2=18.2000, P4=17.1000, P5=15.2000, P1=14.2000
- Paso 2: elegido **P5** (ganancia 13.5200, f acumulada 32.7200)
  - Ganancias de los candidatos: P5=13.5200, P1=12.7600, P4=9.9000, P2=6.2000
- Paso 3: elegido **P1** (ganancia 8.9600, f acumulada 41.6800)
  - Ganancias de los candidatos: P1=8.9600, P2=5.6000, P4=1.0800

Selección: P3, P5, P1 — f(S) = 41.6800

### 2. Reparto del presupuesto (voraz con montículo)

| Unidad | Nodo | Ganancia marginal | Unidades del nodo | Utilidad acumulada |
|---|---|---|---|---|
| 1 | P3 | 8.3178 | 1 | 8.3178 |
| 2 | P1 | 6.9315 | 1 | 15.2492 |
| 3 | P5 | 6.2383 | 1 | 21.4876 |
| 4 | P3 | 4.8656 | 2 | 26.3531 |
| 5 | P1 | 4.0547 | 2 | 30.4078 |
| 6 | P5 | 3.6492 | 2 | 34.0570 |
| 7 | P3 | 3.4522 | 3 | 37.5092 |
| 8 | P1 | 2.8768 | 3 | 40.3860 |
| 9 | P3 | 2.6777 | 4 | 43.0637 |
| 10 | P1 | 2.2314 | 4 | 45.2951 |

Reparto: P3: 4, P5: 2, P1: 4 — utilidad Σu_i(x_i) = 45.2951; usado 10 de 10

### 3. Verificación de restricciones

| Restricción | ¿Cumple? | Detalle |
|---|---|---|
| |S| = k | Sí | |S| = 3, k = 3, elegibles = 5 |
| S sin repetidos y solo con nodos elegibles | Sí | S = ['P3', 'P5', 'P1'] |
| Σ x_i <= B | Sí | Σ x_i = 10, B = 10 |
| x_i enteros y 0 <= x_i <= presupuesto restante del nodo | Sí | P3: 4 <= 4; P5: 2 <= 2; P1: 4 <= 4 |
| u_i creciente y cóncava (ganancias marginales >= 0 y no crecientes) | Sí | revisado para cada nodo seleccionado hasta su tope |
| Costo de participación <= presupuesto de costos (variante 1, no impuesta en la base) | Sí (informativa) | costo = 11, presupuesto = 12 |
| f(S_voraz) >= (1 - 1/e)·OPT | Sí | razón = 1.000000 >= 0.632121 |
| Reparto voraz = óptimo por programación dinámica | Sí | voraz = 45.295145, DP = 45.295145 |

Tiempo: selección 0.013 ms, reparto 0.005 ms

## Ronda 2

Elegibles (2): P2, P4

### 1. Selección de nodos (voraz submodular) y ganancias marginales

- Paso 1: elegido **P2** (ganancia 18.2000, f acumulada 18.2000)
  - Ganancias de los candidatos: P2=18.2000, P4=17.1000
- Paso 2: elegido **P4** (ganancia 14.2200, f acumulada 32.4200)
  - Ganancias de los candidatos: P4=14.2200

Selección: P2, P4 — f(S) = 32.4200

### 2. Reparto del presupuesto (voraz con montículo)

| Unidad | Nodo | Ganancia marginal | Unidades del nodo | Utilidad acumulada |
|---|---|---|---|---|
| 1 | P2 | 5.5452 | 1 | 5.5452 |
| 2 | P4 | 4.1589 | 1 | 9.7041 |
| 3 | P2 | 3.2437 | 2 | 12.9478 |
| 4 | P4 | 2.4328 | 2 | 15.3806 |
| 5 | P2 | 2.3015 | 3 | 17.6820 |
| 6 | P2 | 1.7851 | 4 | 19.4672 |

Reparto: P2: 4, P4: 2 — utilidad Σu_i(x_i) = 19.4672; usado 6 de 10

### 3. Verificación de restricciones

| Restricción | ¿Cumple? | Detalle |
|---|---|---|
| |S| = k | Sí | |S| = 2, k = 3, elegibles = 2 |
| S sin repetidos y solo con nodos elegibles | Sí | S = ['P2', 'P4'] |
| Σ x_i <= B | Sí | Σ x_i = 6, B = 10 |
| x_i enteros y 0 <= x_i <= presupuesto restante del nodo | Sí | P2: 4 <= 4; P4: 2 <= 2 |
| u_i creciente y cóncava (ganancias marginales >= 0 y no crecientes) | Sí | revisado para cada nodo seleccionado hasta su tope |
| Costo de participación <= presupuesto de costos (variante 1, no impuesta en la base) | Sí (informativa) | costo = 6, presupuesto = 12 |
| f(S_voraz) >= (1 - 1/e)·OPT | Sí | razón = 1.000000 >= 0.632121 |
| Reparto voraz = óptimo por programación dinámica | Sí | voraz = 19.467177, DP = 19.467177 |

Tiempo: selección 0.006 ms, reparto 0.004 ms

## Ronda 3

Elegibles (0): 

### 1. Selección de nodos (voraz submodular) y ganancias marginales


Selección:  — f(S) = 0.0000

### 2. Reparto del presupuesto (voraz con montículo)

| Unidad | Nodo | Ganancia marginal | Unidades del nodo | Utilidad acumulada |
|---|---|---|---|---|

Reparto:  — utilidad Σu_i(x_i) = 0.0000; usado 0 de 10

### 3. Verificación de restricciones

| Restricción | ¿Cumple? | Detalle |
|---|---|---|
| |S| = k | Sí | |S| = 0, k = 3, elegibles = 0 |
| S sin repetidos y solo con nodos elegibles | Sí | S = [] |
| Σ x_i <= B | Sí | Σ x_i = 0, B = 10 |
| x_i enteros y 0 <= x_i <= presupuesto restante del nodo | Sí |  |
| u_i creciente y cóncava (ganancias marginales >= 0 y no crecientes) | Sí | revisado para cada nodo seleccionado hasta su tope |
| Costo de participación <= presupuesto de costos (variante 1, no impuesta en la base) | Sí (informativa) | costo = 0, presupuesto = 12 |
| f(S_voraz) >= (1 - 1/e)·OPT | Sí | razón = 1.000000 >= 0.632121 |
| Reparto voraz = óptimo por programación dinámica | Sí | voraz = 0.000000, DP = 0.000000 |

Tiempo: selección 0.001 ms, reparto 0.001 ms

## Resumen

- Gasto total por nodo: P1: 4, P2: 4, P3: 4, P4: 2, P5: 2
- Topes por nodo respetados: Sí
- Utilidad conjunta total (Σ_t f(S_t)): 74.1000
- Utilidad de reparto total (Σ_t Σ_i u_i(x_i)): 64.7623
- Tiempo del algoritmo (mediana de 5): 0.035 ms
- Todas las restricciones obligatorias cumplen: Sí
