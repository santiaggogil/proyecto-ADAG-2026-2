# Traza del caso `entrada_G2_red_15_nodos`

N = 15, T = 3, k = 5, B = 30, presupuesto de costos = 24, aristas = 105

Modelo: u_i(x) = a_i * ln(1 + x);  f(S) = sum_j a_j * (1 - prod_{i in S} (1 - p_ij)), p_jj = 1

## Ronda 1

Elegibles (15): N01, N02, N03, N04, N05, N06, N07, N08, N09, N10, N11, N12, N13, N14, N15

### 1. Selección de nodos (voraz submodular) y ganancias marginales

- Paso 1: elegido **N11** (ganancia 103.4900, f acumulada 103.4900)
  - Ganancias de los candidatos: N11=103.4900, N09=95.7000, N07=88.8050, N14=82.9850, N05=82.6000, N03=77.9200, N12=75.4400, N02=75.3850, N04=74.3400, N01=74.1100, N10=73.6150, N06=72.8050, N08=72.2150, N15=44.0750, N13=40.2100
- Paso 2: elegido **N14** (ganancia 24.2782, f acumulada 127.7683)
  - Ganancias de los candidatos: N14=24.2782, N09=23.3850, N07=22.0060, N12=21.5590, N05=20.7650, N03=19.8290, N02=19.3220, N04=19.1130, N01=19.0670, N10=18.9680, N06=18.8060, N08=18.6880, N15=16.4213, N13=16.1210
- Paso 3: elegido **N09** (ganancia 9.9327, f acumulada 137.7010)
  - Ganancias de los candidatos: N09=9.9327, N07=9.3122, N12=9.1110, N15=9.0157, N05=8.7537, N03=8.3325, N02=8.1044, N04=8.0103, N01=7.9896, N10=7.9451, N06=7.8722, N08=7.8191, N13=6.6639
- Paso 4: elegido **N15** (ganancia 5.5306, f acumulada 143.2316)
  - Ganancias de los candidatos: N15=5.5306, N13=4.1325, N12=3.9942, N07=3.6402, N10=3.5494, N05=3.5006, N03=3.3953, N02=3.3382, N04=3.3147, N01=3.3095, N06=3.2802, N08=3.2669
- Paso 5: elegido **N13** (ganancia 2.3479, f acumulada 145.5795)
  - Ganancias de los candidatos: N13=2.3479, N12=2.2442, N07=1.9787, N10=1.9106, N05=1.8740, N03=1.7950, N02=1.7522, N04=1.7346, N01=1.7307, N06=1.7087, N08=1.6987

Selección: N11, N14, N09, N15, N13 — f(S) = 145.5795

### 2. Reparto del presupuesto (voraz con montículo)

| Unidad | Nodo | Ganancia marginal | Unidades del nodo | Utilidad acumulada |
|---|---|---|---|---|
| 1 | N14 | 7.0008 | 1 | 7.0008 |
| 2 | N09 | 6.8622 | 1 | 13.8629 |
| 3 | N15 | 6.5849 | 1 | 20.4478 |
| 4 | N13 | 5.7531 | 1 | 26.2010 |
| 5 | N11 | 5.2679 | 1 | 31.4689 |
| 6 | N14 | 4.0952 | 2 | 35.5641 |
| 7 | N09 | 4.0141 | 2 | 39.5782 |
| 8 | N15 | 3.8519 | 2 | 43.4301 |
| 9 | N13 | 3.3654 | 2 | 46.7955 |
| 10 | N11 | 3.0815 | 2 | 49.8770 |
| 11 | N14 | 2.9056 | 3 | 52.7826 |
| 12 | N09 | 2.8481 | 3 | 55.6306 |
| 13 | N15 | 2.7330 | 3 | 58.3636 |
| 14 | N13 | 2.3878 | 3 | 60.7514 |
| 15 | N14 | 2.2537 | 4 | 63.0051 |
| 16 | N09 | 2.2091 | 4 | 65.2143 |
| 17 | N11 | 2.1864 | 3 | 67.4006 |
| 18 | N15 | 2.1199 | 4 | 69.5205 |
| 19 | N13 | 1.8521 | 4 | 71.3726 |
| 20 | N14 | 1.8414 | 5 | 73.2140 |
| 21 | N09 | 1.8050 | 5 | 75.0190 |
| 22 | N15 | 1.7321 | 5 | 76.7511 |
| 23 | N11 | 1.6959 | 4 | 78.4470 |
| 24 | N14 | 1.5569 | 6 | 80.0039 |
| 25 | N09 | 1.5261 | 6 | 81.5300 |
| 26 | N13 | 1.5133 | 5 | 83.0432 |
| 27 | N15 | 1.4644 | 6 | 84.5077 |
| 28 | N11 | 1.3856 | 5 | 85.8933 |
| 29 | N14 | 1.3487 | 7 | 87.2420 |
| 30 | N09 | 1.3220 | 7 | 88.5640 |

Reparto: N11: 5, N14: 7, N09: 7, N15: 6, N13: 5 — utilidad Σu_i(x_i) = 88.5640; usado 30 de 30

### 3. Verificación de restricciones

| Restricción | ¿Cumple? | Detalle |
|---|---|---|
| |S| = k | Sí | |S| = 5, k = 5, elegibles = 15 |
| S sin repetidos y solo con nodos elegibles | Sí | S = ['N11', 'N14', 'N09', 'N15', 'N13'] |
| Σ x_i <= B | Sí | Σ x_i = 30, B = 30 |
| x_i enteros y 0 <= x_i <= presupuesto restante del nodo | Sí | N11: 5 <= 18; N14: 7 <= 18; N09: 7 <= 18; N15: 6 <= 18; N13: 5 <= 18 |
| u_i creciente y cóncava (ganancias marginales >= 0 y no crecientes) | Sí | revisado para cada nodo seleccionado hasta su tope |
| Costo de participación <= presupuesto de costos (variante 1, no impuesta en la base) | Sí (informativa) | costo = 23, presupuesto = 24 |
| f(S_voraz) >= (1 - 1/e)·OPT | Sí | razón = 0.997754 >= 0.632121 |
| Reparto voraz = óptimo por programación dinámica | Sí | voraz = 88.563953, DP = 88.563953 |

Tiempo: selección 0.086 ms, reparto 0.014 ms

## Ronda 2

Elegibles (15): N01, N02, N03, N04, N05, N06, N07, N08, N09, N10, N11, N12, N13, N14, N15

### 1. Selección de nodos (voraz submodular) y ganancias marginales

- Paso 1: elegido **N11** (ganancia 103.4900, f acumulada 103.4900)
  - Ganancias de los candidatos: N11=103.4900, N09=95.7000, N07=88.8050, N14=82.9850, N05=82.6000, N03=77.9200, N12=75.4400, N02=75.3850, N04=74.3400, N01=74.1100, N10=73.6150, N06=72.8050, N08=72.2150, N15=44.0750, N13=40.2100
- Paso 2: elegido **N14** (ganancia 24.2782, f acumulada 127.7683)
  - Ganancias de los candidatos: N14=24.2782, N09=23.3850, N07=22.0060, N12=21.5590, N05=20.7650, N03=19.8290, N02=19.3220, N04=19.1130, N01=19.0670, N10=18.9680, N06=18.8060, N08=18.6880, N15=16.4213, N13=16.1210
- Paso 3: elegido **N09** (ganancia 9.9327, f acumulada 137.7010)
  - Ganancias de los candidatos: N09=9.9327, N07=9.3122, N12=9.1110, N15=9.0157, N05=8.7537, N03=8.3325, N02=8.1044, N04=8.0103, N01=7.9896, N10=7.9451, N06=7.8722, N08=7.8191, N13=6.6639
- Paso 4: elegido **N15** (ganancia 5.5306, f acumulada 143.2316)
  - Ganancias de los candidatos: N15=5.5306, N13=4.1325, N12=3.9942, N07=3.6402, N10=3.5494, N05=3.5006, N03=3.3953, N02=3.3382, N04=3.3147, N01=3.3095, N06=3.2802, N08=3.2669
- Paso 5: elegido **N13** (ganancia 2.3479, f acumulada 145.5795)
  - Ganancias de los candidatos: N13=2.3479, N12=2.2442, N07=1.9787, N10=1.9106, N05=1.8740, N03=1.7950, N02=1.7522, N04=1.7346, N01=1.7307, N06=1.7087, N08=1.6987

Selección: N11, N14, N09, N15, N13 — f(S) = 145.5795

### 2. Reparto del presupuesto (voraz con montículo)

| Unidad | Nodo | Ganancia marginal | Unidades del nodo | Utilidad acumulada |
|---|---|---|---|---|
| 1 | N14 | 7.0008 | 1 | 7.0008 |
| 2 | N09 | 6.8622 | 1 | 13.8629 |
| 3 | N15 | 6.5849 | 1 | 20.4478 |
| 4 | N13 | 5.7531 | 1 | 26.2010 |
| 5 | N11 | 5.2679 | 1 | 31.4689 |
| 6 | N14 | 4.0952 | 2 | 35.5641 |
| 7 | N09 | 4.0141 | 2 | 39.5782 |
| 8 | N15 | 3.8519 | 2 | 43.4301 |
| 9 | N13 | 3.3654 | 2 | 46.7955 |
| 10 | N11 | 3.0815 | 2 | 49.8770 |
| 11 | N14 | 2.9056 | 3 | 52.7826 |
| 12 | N09 | 2.8481 | 3 | 55.6306 |
| 13 | N15 | 2.7330 | 3 | 58.3636 |
| 14 | N13 | 2.3878 | 3 | 60.7514 |
| 15 | N14 | 2.2537 | 4 | 63.0051 |
| 16 | N09 | 2.2091 | 4 | 65.2143 |
| 17 | N11 | 2.1864 | 3 | 67.4006 |
| 18 | N15 | 2.1199 | 4 | 69.5205 |
| 19 | N13 | 1.8521 | 4 | 71.3726 |
| 20 | N14 | 1.8414 | 5 | 73.2140 |
| 21 | N09 | 1.8050 | 5 | 75.0190 |
| 22 | N15 | 1.7321 | 5 | 76.7511 |
| 23 | N11 | 1.6959 | 4 | 78.4470 |
| 24 | N14 | 1.5569 | 6 | 80.0039 |
| 25 | N09 | 1.5261 | 6 | 81.5300 |
| 26 | N13 | 1.5133 | 5 | 83.0432 |
| 27 | N15 | 1.4644 | 6 | 84.5077 |
| 28 | N11 | 1.3856 | 5 | 85.8933 |
| 29 | N14 | 1.3487 | 7 | 87.2420 |
| 30 | N09 | 1.3220 | 7 | 88.5640 |

Reparto: N11: 5, N14: 7, N09: 7, N15: 6, N13: 5 — utilidad Σu_i(x_i) = 88.5640; usado 30 de 30

### 3. Verificación de restricciones

| Restricción | ¿Cumple? | Detalle |
|---|---|---|
| |S| = k | Sí | |S| = 5, k = 5, elegibles = 15 |
| S sin repetidos y solo con nodos elegibles | Sí | S = ['N11', 'N14', 'N09', 'N15', 'N13'] |
| Σ x_i <= B | Sí | Σ x_i = 30, B = 30 |
| x_i enteros y 0 <= x_i <= presupuesto restante del nodo | Sí | N11: 5 <= 13; N14: 7 <= 11; N09: 7 <= 11; N15: 6 <= 12; N13: 5 <= 13 |
| u_i creciente y cóncava (ganancias marginales >= 0 y no crecientes) | Sí | revisado para cada nodo seleccionado hasta su tope |
| Costo de participación <= presupuesto de costos (variante 1, no impuesta en la base) | Sí (informativa) | costo = 23, presupuesto = 24 |
| f(S_voraz) >= (1 - 1/e)·OPT | Sí | razón = 0.997754 >= 0.632121 |
| Reparto voraz = óptimo por programación dinámica | Sí | voraz = 88.563953, DP = 88.563953 |

Tiempo: selección 0.087 ms, reparto 0.014 ms

## Ronda 3

Elegibles (15): N01, N02, N03, N04, N05, N06, N07, N08, N09, N10, N11, N12, N13, N14, N15

### 1. Selección de nodos (voraz submodular) y ganancias marginales

- Paso 1: elegido **N11** (ganancia 103.4900, f acumulada 103.4900)
  - Ganancias de los candidatos: N11=103.4900, N09=95.7000, N07=88.8050, N14=82.9850, N05=82.6000, N03=77.9200, N12=75.4400, N02=75.3850, N04=74.3400, N01=74.1100, N10=73.6150, N06=72.8050, N08=72.2150, N15=44.0750, N13=40.2100
- Paso 2: elegido **N14** (ganancia 24.2782, f acumulada 127.7683)
  - Ganancias de los candidatos: N14=24.2782, N09=23.3850, N07=22.0060, N12=21.5590, N05=20.7650, N03=19.8290, N02=19.3220, N04=19.1130, N01=19.0670, N10=18.9680, N06=18.8060, N08=18.6880, N15=16.4213, N13=16.1210
- Paso 3: elegido **N09** (ganancia 9.9327, f acumulada 137.7010)
  - Ganancias de los candidatos: N09=9.9327, N07=9.3122, N12=9.1110, N15=9.0157, N05=8.7537, N03=8.3325, N02=8.1044, N04=8.0103, N01=7.9896, N10=7.9451, N06=7.8722, N08=7.8191, N13=6.6639
- Paso 4: elegido **N15** (ganancia 5.5306, f acumulada 143.2316)
  - Ganancias de los candidatos: N15=5.5306, N13=4.1325, N12=3.9942, N07=3.6402, N10=3.5494, N05=3.5006, N03=3.3953, N02=3.3382, N04=3.3147, N01=3.3095, N06=3.2802, N08=3.2669
- Paso 5: elegido **N13** (ganancia 2.3479, f acumulada 145.5795)
  - Ganancias de los candidatos: N13=2.3479, N12=2.2442, N07=1.9787, N10=1.9106, N05=1.8740, N03=1.7950, N02=1.7522, N04=1.7346, N01=1.7307, N06=1.7087, N08=1.6987

Selección: N11, N14, N09, N15, N13 — f(S) = 145.5795

### 2. Reparto del presupuesto (voraz con montículo)

| Unidad | Nodo | Ganancia marginal | Unidades del nodo | Utilidad acumulada |
|---|---|---|---|---|
| 1 | N14 | 7.0008 | 1 | 7.0008 |
| 2 | N09 | 6.8622 | 1 | 13.8629 |
| 3 | N15 | 6.5849 | 1 | 20.4478 |
| 4 | N13 | 5.7531 | 1 | 26.2010 |
| 5 | N11 | 5.2679 | 1 | 31.4689 |
| 6 | N14 | 4.0952 | 2 | 35.5641 |
| 7 | N09 | 4.0141 | 2 | 39.5782 |
| 8 | N15 | 3.8519 | 2 | 43.4301 |
| 9 | N13 | 3.3654 | 2 | 46.7955 |
| 10 | N11 | 3.0815 | 2 | 49.8770 |
| 11 | N14 | 2.9056 | 3 | 52.7826 |
| 12 | N09 | 2.8481 | 3 | 55.6306 |
| 13 | N15 | 2.7330 | 3 | 58.3636 |
| 14 | N13 | 2.3878 | 3 | 60.7514 |
| 15 | N14 | 2.2537 | 4 | 63.0051 |
| 16 | N09 | 2.2091 | 4 | 65.2143 |
| 17 | N11 | 2.1864 | 3 | 67.4006 |
| 18 | N15 | 2.1199 | 4 | 69.5205 |
| 19 | N13 | 1.8521 | 4 | 71.3726 |
| 20 | N15 | 1.7321 | 5 | 73.1046 |
| 21 | N11 | 1.6959 | 4 | 74.8005 |
| 22 | N13 | 1.5133 | 5 | 76.3138 |
| 23 | N15 | 1.4644 | 6 | 77.7782 |
| 24 | N11 | 1.3856 | 5 | 79.1639 |
| 25 | N13 | 1.2795 | 6 | 80.4433 |
| 26 | N11 | 1.1715 | 6 | 81.6149 |
| 27 | N13 | 1.1083 | 7 | 82.7232 |
| 28 | N11 | 1.0148 | 7 | 83.7380 |
| 29 | N13 | 0.9776 | 8 | 84.7156 |
| 30 | N11 | 0.8952 | 8 | 85.6108 |

Reparto: N11: 8, N14: 4, N09: 4, N15: 6, N13: 8 — utilidad Σu_i(x_i) = 85.6108; usado 30 de 30

### 3. Verificación de restricciones

| Restricción | ¿Cumple? | Detalle |
|---|---|---|
| |S| = k | Sí | |S| = 5, k = 5, elegibles = 15 |
| S sin repetidos y solo con nodos elegibles | Sí | S = ['N11', 'N14', 'N09', 'N15', 'N13'] |
| Σ x_i <= B | Sí | Σ x_i = 30, B = 30 |
| x_i enteros y 0 <= x_i <= presupuesto restante del nodo | Sí | N11: 8 <= 8; N14: 4 <= 4; N09: 4 <= 4; N15: 6 <= 6; N13: 8 <= 8 |
| u_i creciente y cóncava (ganancias marginales >= 0 y no crecientes) | Sí | revisado para cada nodo seleccionado hasta su tope |
| Costo de participación <= presupuesto de costos (variante 1, no impuesta en la base) | Sí (informativa) | costo = 23, presupuesto = 24 |
| f(S_voraz) >= (1 - 1/e)·OPT | Sí | razón = 0.997754 >= 0.632121 |
| Reparto voraz = óptimo por programación dinámica | Sí | voraz = 85.610775, DP = 85.610775 |

Tiempo: selección 0.087 ms, reparto 0.015 ms

## Resumen

- Gasto total por nodo: N01: 0, N02: 0, N03: 0, N04: 0, N05: 0, N06: 0, N07: 0, N08: 0, N09: 18, N10: 0, N11: 18, N12: 0, N13: 18, N14: 18, N15: 18
- Topes por nodo respetados: Sí
- Utilidad conjunta total (Σ_t f(S_t)): 436.7386
- Utilidad de reparto total (Σ_t Σ_i u_i(x_i)): 262.7387
- Tiempo del algoritmo (mediana de 5): 0.312 ms
- Todas las restricciones obligatorias cumplen: Sí
