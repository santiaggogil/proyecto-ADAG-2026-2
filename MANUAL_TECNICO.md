tplotlib
# Manual técnico — Solución base

**ADAG 2026-B · Grupo 2 · Reparto de presupuesto y selección de participantes**

## 1. Propósito

Este programa resuelve el **problema base** del Subproyecto 2 sobre los casos de la profesora y sobre casos propios. En cada ronda hace dos cosas:

- **Selecciona** `k` participantes con el algoritmo voraz submodular (Parte 2, Proyecto-2026B, Sec. 3.3).
- **Reparte** el presupuesto de ruido `B` entre ellos con el algoritmo voraz por ganancia marginal implementado con un montículo (Parte 1, Sec. 3.2).

El programa genera la evidencia que exige la Guía de la primera entrega para el G2:

- resultados;
- tiempo por caso;
- traza: selección de nodos, ganancias marginales, reparto del presupuesto y verificación de restricciones.

## 2. Requisitos y ejecución

- Python ≥ 3.10, probado con 3.13. Solo biblioteca estándar: `json`, `heapq`, `math`, `itertools`, `time`, `statistics`, `csv`, `argparse`, `unittest`.

| Acción | Comando (PowerShell, desde la carpeta del proyecto) |
|---|---|
| Ejecutar todos los casos de `casos/` | `python main.py` |
| Ejecutar un caso | `python main.py casos\entrada_G2_red_15_nodos.json` |
| Ejecutar sin verificación de óptimos | `python main.py --sin-verificacion` |
| Cambiar repeticiones de la medición de tiempo | `python main.py --repeticiones 20` |
| Ejecutar las pruebas | `python -m unittest -v` |
| Generar casos sintéticos | `python generar_casos.py` |

Los resultados se obtienen sin editar la lógica del algoritmo: basta con pasar otro archivo de entrada. Esto cumple la condición de **reproducibilidad** de la Guía.

## 3. Arquitectura

```
            ┌────────────┐   Instancia   ┌───────────┐
archivo ───►│ entrada.py │──────────────►│ rondas.py │──► salida.py ──► salidas/
 .json      └────────────┘               └─────┬─────┘
                                               │ usa
                         ┌─────────────────────┼──────────────────────┐
                         ▼                     ▼                      ▼
                   seleccion.py            reparto.py             modelo.py
                (voraz + fuerza bruta)  (voraz + DP verificador)  (u_i(x), f(S))
```

| Módulo | Responsabilidad | Relación con la teoría |
|---|---|---|
| `entrada.py` | Lee y valida el JSON y construye `Instancia`. Es **el único** módulo que conoce el formato; los nombres de las claves están en el diccionario `CLAVES`. | Define la entrada formal del problema |
| `modelo.py` | Fórmulas de utilidad. `CoberturaProbabilistica` mantiene el estado incremental de f para el voraz. | Supuestos de modelado (Sec. 5) |
| `seleccion.py` | `voraz` (solución) y `fuerza_bruta` (óptimo exacto para verificar) | Parte 2, Teorema 3.3.1 |
| `reparto.py` | `voraz_monticulo` (solución) y `dp_exacto` (verificador) | Parte 1, Teorema 3.2.1 |
| `rondas.py` | Ejecuta las T rondas, mide tiempos y verifica restricciones | Figura 3.1 |
| `salida.py` | Escribe JSON, traza en Markdown y CSV de tiempos | Evidencias de la Guía |

**Principio de diseño.** Los algoritmos son **genéricos**:

- `reparto.voraz_monticulo` recibe una función `ganancia(i, x)`;
- `seleccion.voraz` recibe cualquier objeto con los métodos `ganancia(v)` y `agregar(v)`.

Por eso:

- si cambia el **formato** de la entrada, se edita solo `entrada.py`;
- si cambian las **fórmulas** de utilidad, se edita solo `modelo.py`.

## 4. Formato de entrada

El archivo es un JSON con tres secciones. Los campos marcados como opcionales toman el valor por defecto indicado.

**`parametros`**

| Clave | Símbolo | Tipo | Obligatoria |
|---|---|---|---|
| `numero_nodos` | N | entero ≥ 1 (debe coincidir con la lista de nodos) | no |
| `numero_rondas` | T | entero ≥ 1 | no (1) |
| `cupo_participantes_por_ronda_k` | k | entero, 1 ≤ k < N | sí |
| `presupuesto_ruido_por_ronda_B` | B | entero ≥ 0 | sí |
| `presupuesto_costos_participacion_por_ronda` | — | entero ≥ 0 | no (solo se verifica) |

**`nodos`** (lista): `id` (texto único), `coeficiente_utilidad` (a_i ≥ 0), `presupuesto_total_nodo` (entero; por defecto T·B, es decir, sin tope efectivo) y `costo_participacion` (entero; por defecto 0).

**`grafo`** (lista, opcional): aristas `{u, v, peso_influencia}` con peso en [0, 1].

**Validaciones** (lanzan `ErrorEntrada` con un mensaje claro):
- claves obligatorias ausentes;
- tipos incorrectos;
- k ≥ N;
- N declarado distinto del número de nodos;
- identificadores repetidos;
- aristas hacia nodos inexistentes, lazos o aristas repetidas con pesos distintos;
- pesos fuera de [0, 1].

## 5. Supuestos de modelado

Los documentos exigen propiedades de las funciones, pero no sus fórmulas. Se adoptan estas, justificadas y demostradas en el informe:

1. **Utilidad de un nodo (Parte 1):** u_i(x) = a_i · ln(1 + x).
   - Ganancia marginal: Δ_i(x) = a_i · ln(1 + 1/(x+1)), que es mayor que 0 (u_i creciente) y no crece con x (u_i cóncava).
2. **Utilidad conjunta (Parte 2):** cobertura probabilística ponderada,
   f(S) = Σ_j a_j · (1 − Π_{i∈S}(1 − p_ij)).
   - Cumple f(∅) = 0, es monótona y es submodular.
   - Con pesos 0/1 y coeficientes iguales a 1, se convierte en Cobertura Máxima, la función de la reducción.
3. **Grafo no dirigido:** p_ij = p_ji = peso de la arista {i, j}. Además, p_ii = 1 (un participante se cubre a sí mismo) y p_ij = 0 si no hay arista.
4. **Rondas:** se ejecutan las T rondas del archivo **sin fallas**, porque q no viene en la entrada y las fallas corresponden a la variante 2. El presupuesto total de cada nodo es un tope acumulado; solo son elegibles los nodos con presupuesto restante ≥ 1.
5. **Costos de participación:** el presupuesto de costos corresponde a la variante 1 (Khuller et al., 1999). En la solución base **no se impone**; se **verifica y reporta**.
6. **Empates:** gana el nodo que aparece primero en el archivo. El resultado es determinista.

## 6. Algoritmos

### 6.1 Selección voraz (`seleccion.voraz`)

```
S ← ∅ ; r_j ← 1 para todo j                    # r_j = Π_{i∈S}(1 − p_ij)
repetir k veces:
    para cada candidato v ∉ S:                   # ≤ N candidatos
        Δ(v|S) ← Σ_j a_j · r_j · p_vj             # τ = O(N)
    v* ← argmax Δ(v|S)
    S ← S ∪ {v*};  r_j ← r_j · (1 − p_v*j)        # O(N)
```

- **Costo:** k pasos × N candidatos × O(N) = **O(k·N²)** por ronda. Es la forma O(N·k·τ) del documento, con τ = O(N) gracias al vector incremental r. Sin ese vector, evaluar f desde cero costaría O(|S|·N) y el total sería O(k²·N²).
- **Garantía:** f(S_voraz) ≥ (1 − 1/e)·OPT ≈ 0,632·OPT, porque f es monótona, submodular y f(∅) = 0, con restricción |S| = k (Nemhauser, Wolsey y Fisher, 1978).

### 6.2 Reparto voraz con montículo (`reparto.voraz_monticulo`)

```
x_i ← 0 ;  H ← montículo de máximos con (Δ_i(0), i)      # heapify O(N)
repetir B veces (o hasta vaciar H):
    (g, i) ← extraer máximo de H                           # O(log N)
    x_i ← x_i + 1
    si x_i < tope_i: insertar (Δ_i(x_i), i) en H           # O(log N)
```

- **Costo:** **O(N + B log N)**, con N = número de participantes de la ronda (aquí k).
- **Optimalidad:** por concavidad, la utilidad de un nodo es la suma de un **prefijo** de su lista de ganancias, y cada lista está ordenada de mayor a menor. El voraz toma las B mayores ganancias de todas las listas, y ningún reparto puede superar esa suma. El tope por nodo solo recorta cada lista, así que el argumento se mantiene.

### 6.3 Costo total del programa

- Lectura: O(N² + |E|), por la matriz p.
- Rondas: O(T · (k·N² + k + B log k)).
- Memoria: O(N²).

### 6.4 Verificadores (solo con verificación activa)

- `seleccion.fuerza_bruta`: revisa los C(N, k) subconjuntos en O(C(N, k)·k·N). Se omite si C(N, k) > 200.000; por ejemplo, el caso propio de 60 nodos tiene C(60, 6) ≈ 5·10⁷.
- `reparto.dp_exacto`: programación dinámica en O(k·B·min(tope, B)).

Los tiempos de verificación **no** se incluyen en el tiempo del algoritmo.

## 7. Salida

**`resultado_<caso>.json`.** Por cada ronda incluye:
- `elegibles` y `seleccion`;
- `utilidad_conjunta_f_S`;
- `traza_seleccion`: por paso, las ganancias marginales de todos los candidatos, el elegido y la utilidad acumulada;
- `reparto` y `utilidad_reparto`;
- `traza_reparto`: una fila por unidad (nodo, ganancia marginal, unidades del nodo, utilidad acumulada);
- `presupuesto_usado` y `presupuesto_sobrante`;
- `costo_participacion`;
- `tiempo_ms`;
- `verificacion`;
- `comparacion_con_optimo`.

Además, el archivo incluye `gasto_total_por_nodo`, `tiempo_algoritmo_ms` (mediana y mínimo de las repeticiones) y `todas_las_restricciones_cumplen`.

**`traza_<caso>.md`** contiene la misma información en tablas legibles. **`tiempos.csv`** tiene una fila por caso.

### Restricciones que se verifican en cada ronda

1. |S| = k, o el número de elegibles si son menos de k.
2. S sin repetidos y formado solo por nodos elegibles.
3. Σ x_i ≤ B.
4. x_i entero y 0 ≤ x_i ≤ presupuesto restante del nodo.
5. u_i creciente y cóncava para los seleccionados (comprobación numérica).
6. f(S_voraz) ≥ (1 − 1/e)·OPT, frente a la fuerza bruta.
7. Utilidad del voraz de reparto = óptimo por programación dinámica.
8. *(Informativa)* costo de participación ≤ presupuesto de costos.

Al final de las T rondas se verifica, además, que ningún nodo haya superado su presupuesto total.

## 8. Pruebas (`tests/`, 25 pruebas)

| Archivo | Qué comprueba |
|---|---|
| `test_entrada.py` | Lectura del caso de la profesora (N = 15, 105 aristas, p simétrica, p_ii = 1); campos opcionales; 8 tipos de error |
| `test_modelo.py` | u_i creciente y cóncava; f(∅) = 0; f monótona y submodular en 500 pares A ⊆ C aleatorios; ganancia incremental = diferencia de f; con pesos 0/1, f es cobertura |
| `test_reparto.py` | Ejemplo de clase (resultado 30 con (2, 2, 0)); B = 0; topes y sobrante; **voraz = DP en 300 instancias cóncavas aleatorias**; contraejemplo no cóncavo en el que el voraz falla |
| `test_seleccion.py` | Ejemplo de clase (voraz 5, óptimo 6); **cota 1 − 1/e en 230 instancias aleatorias**; sin aristas el voraz es óptimo; empates; k > candidatos |
| `test_integracion.py` | Todos los casos de `casos/` cumplen las restricciones; casos con resultado conocido |

### Casos propios (`casos/`)

| Archivo | Propósito |
|---|---|
| `propio_01_pequeno_6_nodos` | Caso pequeño hecho a mano con dos grupos de nodos |
| `propio_02_sin_aristas_6_nodos` | Sin grafo, f es aditiva: el voraz debe ser óptimo y elegir los k coeficientes mayores |
| `propio_03_topes_agotados_5_nodos` | Topes pequeños: los nodos se agotan, los elegibles cambian y sobra presupuesto; la ronda 3 queda vacía |
| `propio_04_aleatorio_30_nodos` | Aleatorio con semilla 2026; la fuerza bruta aún es viable (C(30, 4) = 27.405) |
| `propio_05_aleatorio_60_nodos` | Aleatorio con semilla 2027; la fuerza bruta se omite por explosión combinatoria |

## 9. Resultados del caso de la profesora (`entrada_G2_red_15_nodos`)

N = 15, k = 5, B = 30, T = 3, topes de 18 por nodo.

| Ronda | Selección (orden voraz) | f(S) | Óptimo f (fuerza bruta, 3.003 subconjuntos) | Razón | Reparto x | Σ u_i(x_i) |
|---|---|---|---|---|---|---|
| 1 | N11, N14, N09, N15, N13 | 145,5795 | 145,9072 | 0,9978 | 5, 7, 7, 6, 5 | 88,5640 |
| 2 | igual | 145,5795 | 145,9072 | 0,9978 | 5, 7, 7, 6, 5 | 88,5640 |
| 3 | igual | 145,5795 | 145,9072 | 0,9978 | 8, 4, 4, 6, 8 | 85,6108 |

- **Selección óptima** (fuerza bruta): {N09, N11, N12, N13, N15}. El voraz difiere en un solo nodo (eligió N14 en lugar de N12) y obtiene el 99,78 % del óptimo, muy por encima de la cota del 63,2 %.
- **Reparto:** en cada ronda coincide con el óptimo de la programación dinámica y usa las 30 unidades.
- **Presupuesto total:** cada nodo seleccionado gasta exactamente su tope de 18 (5 × 18 = 90 = 3 × 30).
- **Costo de participación** de la selección: 23 ≤ 24, así que también cumple la restricción de la variante 1.
- **Tiempo del algoritmo:** menos de 1 ms por caso (ver `salidas/tiempos.csv`).

**Observación.** En la ronda 3, el reparto queda condicionado por los topes: los nodos N14 y N09 ya gastaron 14 unidades cada uno y solo pueden recibir 4. El reparto es óptimo **dentro de cada ronda**, pero repartir de forma miope ronda por ronda no tiene por qué ser óptimo para las T rondas juntas. Esa es precisamente la comparación de políticas de gasto que pide la variante 2.

## 10. Limitaciones

- Las fórmulas de u_i y f son **supuestos** (Sec. 5), porque la entrada no las fija. Cambiarlas solo requiere editar `modelo.py`.
- El grafo se interpreta como no dirigido. Si la profesora indica que es dirigido (u influye sobre v), basta con cambiar una línea de `entrada._cargar_grafo`.
- **No implementado todavía**, porque corresponde a las variantes de entregas posteriores:
  - fallas con probabilidad q;
  - selección con presupuesto de costos (algoritmo de Khuller et al.);
  - efecto del presupuesto entre vecinos (casos aditivo y de competencia);
  - experimentación con gráficas de tiempo frente a n.
- La fuerza bruta solo es viable en instancias pequeñas, precisamente porque el problema es NP-difícil.
- Los tiempos son del orden de microsegundos a milisegundos, por lo que dependen del equipo. Se reporta la mediana de varias repeticiones.

## 11. Cómo modificar

| Si cambia… | Edite… |
|---|---|
| El nombre de una clave del JSON | `CLAVES` en `solucion/entrada.py` |
| La estructura del JSON | `solucion/entrada.py` (funciones `_cargar_*`) |
| La fórmula de u_i o de f | `solucion/modelo.py` |
| El límite de la fuerza bruta | `LIMITE_FUERZA_BRUTA` en `solucion/rondas.py` |
