"""
entrada.py — Lectura y validación del archivo de entrada.

Este módulo es el ÚNICO que conoce el formato del archivo JSON. El resto del
programa trabaja exclusivamente con el objeto `Instancia`. Si la profesora
cambia el formato o el nombre de alguna clave, solo hay que modificar este
archivo (normalmente, solo el diccionario CLAVES).

Convenciones adoptadas (ver manual técnico, sección "Supuestos"):
  * El grafo es NO dirigido: cada arista {u, v} aparece una vez en el archivo y
    su peso se usa en ambos sentidos (p[u][v] = p[v][u]).
  * Un nodo se "cubre" completamente a sí mismo: p[i][i] = 1.
  * Si dos nodos no están unidos por una arista, p[i][j] = 0.
  * Campos opcionales: si faltan, se usan valores neutros (ver _cargar_nodos).
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

# Nombres de las claves del archivo. Cambiar aquí si cambia el formato.
CLAVES = {
    "parametros": "parametros",
    "N": "numero_nodos",
    "T": "numero_rondas",
    "k": "cupo_participantes_por_ronda_k",
    "B": "presupuesto_ruido_por_ronda_B",
    "presupuesto_costos": "presupuesto_costos_participacion_por_ronda",
    "grafo": "grafo",
    "arista_u": "u",
    "arista_v": "v",
    "peso": "peso_influencia",
    "nodos": "nodos",
    "id": "id",
    "coef": "coeficiente_utilidad",
    "tope": "presupuesto_total_nodo",
    "costo": "costo_participacion",
}


class ErrorEntrada(ValueError):
    """Error de formato o de contenido en el archivo de entrada."""


@dataclass
class Instancia:
    """Representación interna de un caso. Índices de nodo: 0..N-1."""

    nombre: str
    ids: list[str]                 # identificadores originales ("N01", ...)
    T: int                         # número de rondas
    k: int                         # cupo de participantes por ronda
    B: int                         # presupuesto de ruido por ronda (unidades enteras)
    presupuesto_costos: int | None # presupuesto de costos por ronda (variante 1; solo se verifica)
    coef: list[float]              # a_i: coeficiente de utilidad de cada nodo
    tope: list[int]                # presupuesto total de cada nodo para las T rondas
    costo: list[int]               # costo de participación de cada nodo
    p: list[list[float]]           # p[i][j]: influencia entre i y j (simétrica, p[i][i] = 1)
    num_aristas: int

    @property
    def N(self) -> int:
        return len(self.ids)


# Funciones auxiliares de validación
def _obtener(diccionario: dict, clave_logica: str, contexto: str, opcional=False, defecto=None):
    clave = CLAVES[clave_logica]
    if clave not in diccionario:
        if opcional:
            return defecto
        raise ErrorEntrada(f"Falta la clave '{clave}' en {contexto}.")
    return diccionario[clave]


def _entero(valor, nombre: str, minimo: int | None = None) -> int:
    if isinstance(valor, bool) or not isinstance(valor, (int, float)) or float(valor) != int(valor):
        raise ErrorEntrada(f"'{nombre}' debe ser un entero (recibido: {valor!r}).")
    valor = int(valor)
    if minimo is not None and valor < minimo:
        raise ErrorEntrada(f"'{nombre}' debe ser >= {minimo} (recibido: {valor}).")
    return valor


def _real(valor, nombre: str, minimo: float | None = None, maximo: float | None = None) -> float:
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ErrorEntrada(f"'{nombre}' debe ser un número (recibido: {valor!r}).")
    valor = float(valor)
    if minimo is not None and valor < minimo:
        raise ErrorEntrada(f"'{nombre}' debe ser >= {minimo} (recibido: {valor}).")
    if maximo is not None and valor > maximo:
        raise ErrorEntrada(f"'{nombre}' debe ser <= {maximo} (recibido: {valor}).")
    return valor

# Carga
def cargar(ruta: str | Path) -> Instancia:
    """Lee un archivo JSON y devuelve una Instancia validada."""
    ruta = Path(ruta)
    try:
        datos = json.loads(ruta.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ErrorEntrada(f"El archivo {ruta.name} no es un JSON válido: {e}") from e
    return desde_diccionario(datos, nombre=ruta.stem)


def desde_diccionario(datos: dict, nombre: str = "caso") -> Instancia:
    """Construye una Instancia a partir del diccionario ya leído del JSON."""
    if not isinstance(datos, dict):
        raise ErrorEntrada("La raíz del archivo debe ser un objeto JSON.")

    par = _obtener(datos, "parametros", "la raíz")
    ids, coef, tope, costo = _cargar_nodos(datos, par)
    N = len(ids)

    N_declarado = _entero(_obtener(par, "N", "parametros", opcional=True, defecto=N), CLAVES["N"], 1)
    if N_declarado != N:
        raise ErrorEntrada(f"'{CLAVES['N']}' = {N_declarado}, pero hay {N} nodos en la lista.")

    T = _entero(_obtener(par, "T", "parametros", opcional=True, defecto=1), CLAVES["T"], 1)
    k = _entero(_obtener(par, "k", "parametros"), CLAVES["k"], 1)
    if k >= N:
        raise ErrorEntrada(f"Se exige k < N (k = {k}, N = {N}).")
    B = _entero(_obtener(par, "B", "parametros"), CLAVES["B"], 0)
    pc = _obtener(par, "presupuesto_costos", "parametros", opcional=True)
    pc = None if pc is None else _entero(pc, CLAVES["presupuesto_costos"], 0)

    # Si el archivo no trae topes por nodo, no se limita el gasto individual.
    tope = [t if t is not None else T * B for t in tope]

    p, num_aristas = _cargar_grafo(datos, ids)

    return Instancia(nombre=nombre, ids=ids, T=T, k=k, B=B, presupuesto_costos=pc,
                     coef=coef, tope=tope, costo=costo, p=p, num_aristas=num_aristas)


def _cargar_nodos(datos: dict, par: dict):
    lista = _obtener(datos, "nodos", "la raíz")
    if not isinstance(lista, list) or not lista:
        raise ErrorEntrada(f"'{CLAVES['nodos']}' debe ser una lista no vacía.")
    ids, coef, tope, costo = [], [], [], []
    for pos, nodo in enumerate(lista):
        ctx = f"el nodo en la posición {pos}"
        ident = str(_obtener(nodo, "id", ctx))
        if ident in ids:
            raise ErrorEntrada(f"Identificador de nodo repetido: {ident}.")
        ids.append(ident)
        coef.append(_real(_obtener(nodo, "coef", ctx), f"{CLAVES['coef']} de {ident}", minimo=0.0))
        t = _obtener(nodo, "tope", ctx, opcional=True)
        tope.append(None if t is None else _entero(t, f"{CLAVES['tope']} de {ident}", 0))
        c = _obtener(nodo, "costo", ctx, opcional=True, defecto=0)
        costo.append(_entero(c, f"{CLAVES['costo']} de {ident}", 0))
    return ids, coef, tope, costo


def _cargar_grafo(datos: dict, ids: list[str]):
    N = len(ids)
    indice = {ident: i for i, ident in enumerate(ids)}
    p = [[0.0] * N for _ in range(N)]
    for i in range(N):
        p[i][i] = 1.0
    aristas = _obtener(datos, "grafo", "la raíz", opcional=True, defecto=[])
    if not isinstance(aristas, list):
        raise ErrorEntrada(f"'{CLAVES['grafo']}' debe ser una lista.")
    vistas = {}
    for pos, a in enumerate(aristas):
        ctx = f"la arista en la posición {pos}"
        u = str(_obtener(a, "arista_u", ctx))
        v = str(_obtener(a, "arista_v", ctx))
        for x in (u, v):
            if x not in indice:
                raise ErrorEntrada(f"La arista {u}-{v} menciona un nodo inexistente: {x}.")
        if u == v:
            raise ErrorEntrada(f"Arista de un nodo consigo mismo: {u}-{v}.")
        w = _real(_obtener(a, "peso", ctx), f"{CLAVES['peso']} de {u}-{v}", 0.0, 1.0)
        par = frozenset((u, v))
        if par in vistas and vistas[par] != w:
            raise ErrorEntrada(f"La arista {u}-{v} aparece repetida con pesos distintos.")
        vistas[par] = w
        i, j = indice[u], indice[v]
        p[i][j] = p[j][i] = w
    return p, len(vistas)
