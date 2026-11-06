# ADAG 2026-B · Grupo 2 — Reparto de presupuesto y selección de participantes

Solución base de la primera entrega del proyecto de Análisis y Diseño de Algoritmos (Universidad de Caldas).

En cada ronda, el programa toma dos decisiones:

1. **Parte II – Selección:** el algoritmo voraz submodular elige `k` participantes. Garantiza al menos `1 − 1/e ≈ 63,2 %` del óptimo (Nemhauser, Wolsey y Fisher, 1978) y cuesta `O(k·N²)`.
2. **Parte I – Reparto:** el algoritmo voraz con montículo reparte el presupuesto `B` entre los elegidos. Es óptimo exacto y cuesta `O(N + B log N)`.

El proceso se repite durante las `T` rondas del archivo de entrada, respetando el presupuesto total de cada nodo.


## Documentación

El informe técnico y el manual técnico se entregan aparte, en PDF:

- **Informe técnico:** formalización, prueba de NP-dificultad, demostraciones y resultados experimentales.
- **Manual técnico:** implementación, estructura del código, formatos de entrada y salida, ejecución y limitaciones.


## Requisitos

- Python 3.10 o superior (probado con Python 3.13.7).
- La solución usa solo la biblioteca estándar de Python.
- `matplotlib` es opcional y solo se usa en `experimentos.py` para dibujar las figuras.


## Obtener el proyecto

```
git clone https://github.com/santiaggogil/proyecto-ADAG-2026-2.git
cd proyecto-ADAG-2026-2
```

Todos los comandos de este README se ejecutan desde la carpeta raíz del proyecto, la que contiene `main.py`. Funcionan igual en CMD, PowerShell y la terminal de VS Code (Terminal → Nuevo terminal). En Linux o macOS, use `python3` en lugar de `python` y `/` en lugar de `\` en las rutas.


## Ejecución de la solución base

Ejecutar todos los casos de la carpeta `casos`:

```
python main.py
```

Ejecutar solo el caso de la profesora:

```
python main.py casos\entrada_G2_red_15_nodos.json
```

Ejecutar cualquier otro archivo con el mismo formato:

```
python main.py ruta\a\otro_caso.json
```

Ejecutar solo los algoritmos, sin calcular los óptimos exactos (fuerza bruta y programación dinámica):

```
python main.py --sin-verificacion
```

Usar más repeticiones para medir el tiempo (por defecto, 5):

```
python main.py --repeticiones 20
```

El programa termina con código 0 si todos los casos se leyeron bien y se cumplen todas las restricciones obligatorias.


## Salidas

La carpeta `salidas` se crea automáticamente al ejecutar. `main.py` genera:

- `resultado_<caso>.json`: resultados completos. Incluye la selección, las ganancias marginales, el reparto, la verificación de restricciones, la comparación con el óptimo y los tiempos.
- `traza_<caso>.md`: la misma traza en formato legible, con tablas por ronda.
- `tiempos.csv`: una fila por caso, con el tiempo (mediana y mínimo de 5 repeticiones), las utilidades y el cumplimiento de restricciones.


## Pruebas

```
python -m unittest -v
```

Debe terminar con `Ran 25 tests ... OK`. Las pruebas comprueban que:

- las funciones de utilidad cumplen sus propiedades: concavidad, monotonía y submodularidad;
- el voraz de reparto coincide con una programación dinámica exacta en 300 instancias aleatorias;
- el voraz de selección respeta la cota `1 − 1/e` frente a la fuerza bruta;
- la lectura de la entrada valida correctamente los datos;
- todos los casos de la carpeta `casos` se resuelven de extremo a extremo.


## Validación experimental

Instalar la dependencia opcional para las figuras:

```
pip install matplotlib
```

Medir los tiempos frente al tamaño y verificar la optimalidad y la razón de aproximación (semilla fija 2026). Genera `salidas\experimentos\*.csv` y `salidas\figuras\*.png`:

```
python experimentos.py
```

Calcular las pendientes log-log y los R² a partir de los CSV, sin volver a medir. Genera `salidas\experimentos\analisis_ajuste.csv`:

```
python analisis_experimentos.py
```

Para medir tiempos confiables, ejecute con el cargador conectado, en modo de energía «Máximo rendimiento» y con los demás programas cerrados.


## Generar casos sintéticos

Regenerar los casos aleatorios propios 04 y 05:

```
python generar_casos.py
```

Crear un caso nuevo con los parámetros indicados:

```
python generar_casos.py --N 40 --k 5 --B 30 --T 3 --densidad 0.3 --semilla 7 --salida casos\mi_caso.json
```

Los casos propios 01 a 03 se escribieron a mano para probar situaciones específicas.


## Estructura del proyecto

```
main.py                     punto de entrada de la solución base
experimentos.py             validación experimental (tiempos y garantías)
analisis_experimentos.py    cálculo de pendientes y R² a partir de los CSV
generar_casos.py            generador de instancias con semilla fija
requirements.txt            dependencias (solo matplotlib, opcional)
solucion/
    entrada.py              único módulo que conoce el formato del JSON
    modelo.py               fórmulas de utilidad u_i(x) y f(S)
    seleccion.py            Parte II: voraz submodular + fuerza bruta
    reparto.py              Parte I: voraz con montículo + programación dinámica
    rondas.py               orquestación de las T rondas y verificación
    salida.py               escritura de JSON, traza y tiempos
casos/                      entrada de la profesora + 5 casos propios
tests/                      25 pruebas unitarias y de integración
salidas/                    resultados generados al ejecutar
```


## Estado del proyecto

- **Solución base: completa.** Selección, reparto, T rondas con presupuesto por nodo, verificación, traza y experimentos.
- **Variantes obligatorias: pendientes para la segunda entrega.** Son tres: costos de participación, fallas por ronda y nodos relacionados por grafo. Están formuladas y analizadas en el informe.


## Autor

Santiago Gil Marín  
Análisis y Diseño de Algoritmos, 2026-B  
Docente: Luz Enith Guerrero Mendieta

