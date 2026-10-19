"""
Genera las graficas y tablas del Taller 3 a partir de los CSV de la carpeta resultados/.

Uso (desde la raiz del repositorio):
    pip install matplotlib
    python python/graficas.py

Salidas:
  graficas/   10 graficas en PNG (Punto 1 y Punto 2)
  resultados/tablas.md   tablas de apoyo para el analisis (factores de crecimiento,
                         casos estimados, posicion de la clave y calculo de k)

Reglas del taller que se cumplen:
  - Escala logaritmica en el eje del tiempo (y en ambos ejes en las graficas de crecimiento).
  - Valores estimados dibujados distinto: linea punteada con marcador hueco en las lineas,
    barra rayada en los graficos de barras.
  - Valores de tiempo visibles sobre cada barra.
"""
import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

RES = "resultados"
GRAF = "graficas"

ORDENAMIENTOS = ["InsertionSort", "DualPivotQuickSort", "MergeSort", "HeapSort", "RadixSort", "BucketSort"]
NOMBRE_ORD = {
    "InsertionSort": "Insertion Sort",
    "DualPivotQuickSort": "Dual-Pivot QuickSort",
    "MergeSort": "Merge Sort",
    "HeapSort": "Heap Sort",
    "RadixSort": "Radix Sort",
    "BucketSort": "Bucket Sort",
}
TEORIA_ORD = {
    "InsertionSort": "×100 (n²)",
    "DualPivotQuickSort": "≈×12 a ×13 (n log n)",
    "MergeSort": "≈×12 a ×13 (n log n)",
    "HeapSort": "≈×12 a ×13 (n log n)",
    "RadixSort": "×10 (n)",
    "BucketSort": "×10 (n, promedio)",
}

BUSQUEDAS = ["Lineal", "Binaria", "Ternaria", "Saltos", "Interpolacion", "Exponencial"]
NOMBRE_BUS = {
    "Lineal": "Lineal",
    "Binaria": "Binaria",
    "Ternaria": "Ternaria",
    "Saltos": "Por saltos",
    "Interpolacion": "Interpolación",
    "Exponencial": "Exponencial",
}
TEORIA_BUS = {
    "Lineal": "×10 (n)",
    "Binaria": "crece poco (log n)",
    "Ternaria": "crece poco (log n)",
    "Saltos": "×3,16 (√n)",
    "Interpolacion": "casi constante (log log n)",
    "Exponencial": "crece poco (log n)",
}

COLORES = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
COLOR_VARIANTE = {"aleatorio": "#4c72b0", "ascendente": "#55a868", "descendente": "#c44e52"}
COLOR_LENGUAJE = {"Java": "#e07b39", "Python": "#3b75af"}


# ---------------------------------------------------------------
# Lectura y formato
# ---------------------------------------------------------------
def leer(archivo, campo_valor):
    """Retorna {(algoritmo, lenguaje, variante, n): (valor, estimado, observacion)}."""
    datos = {}
    ruta = os.path.join(RES, archivo)
    if not os.path.exists(ruta):
        print(f"AVISO: no existe {ruta}")
        return datos
    with open(ruta, newline="") as f:
        for fila in csv.DictReader(f):
            valor = fila[campo_valor]
            datos[(fila["algoritmo"], fila["lenguaje"], fila["variante"], int(fila["n"]))] = (
                float(valor) if valor else None,
                fila["tipo"] == "estimado",
                fila.get("observacion", ""),
            )
    return datos


def num(v, dec=2):
    """Numero con formato colombiano: 1.234,56"""
    return f"{v:,.{dec}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def fmt_ms(v):
    if v is None:
        return "sin dato"
    if v < 1:
        return f"{num(v, 3)} ms"
    if v < 10:
        return f"{num(v, 2)} ms"
    if v < 1000:
        return f"{num(v, 1)} ms"
    if v < 60_000:
        return f"{num(v / 1000, 1)} s"
    if v < 3_600_000:
        return f"{num(v / 60_000, 1)} min"
    return f"{num(v / 3_600_000, 1)} h"


def fmt_ns(v):
    if v is None:
        return "sin dato"
    if v < 1000:
        return f"{num(v, 1)} ns"
    if v < 1_000_000:
        return f"{num(v / 1000, 1)} µs"
    return f"{num(v / 1_000_000, 1)} ms"


def tamanos(datos):
    return sorted({k[3] for k in datos})


def etiqueta_n(n):
    return num(n, 0)


# ---------------------------------------------------------------
# Graficas
# ---------------------------------------------------------------
def grafica_crecimiento(datos, lenguaje, variante, algoritmos, nombres, titulo, eje_y, archivo):
    fig, ax = plt.subplots(figsize=(9, 6))
    ns = tamanos(datos)
    for i, alg in enumerate(algoritmos):
        puntos = [(n, *datos[(alg, lenguaje, variante, n)][:2])
                  for n in ns if (alg, lenguaje, variante, n) in datos
                  and datos[(alg, lenguaje, variante, n)][0] is not None]
        color = COLORES[i % len(COLORES)]
        for (n1, v1, e1), (n2, v2, e2) in zip(puntos, puntos[1:]):
            ax.plot([n1, n2], [v1, v2], color=color, linewidth=2,
                    linestyle="--" if (e1 or e2) else "-")
        for n, v, e in puntos:
            ax.plot(n, v, marker="o", markersize=7, color=color,
                    markerfacecolor="white" if e else color, markeredgewidth=2)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks(ns)
    ax.set_xticklabels([etiqueta_n(n) for n in ns])
    ax.set_xlabel("Tamaño del arreglo (n, escala logarítmica)")
    ax.set_ylabel(eje_y)
    ax.set_title(titulo)
    ax.grid(True, which="both", alpha=0.3)

    leyenda = [Line2D([0], [0], color=COLORES[i % len(COLORES)], linewidth=2, label=nombres[a])
               for i, a in enumerate(algoritmos)]
    leyenda += [Line2D([0], [0], color="gray", linewidth=2, marker="o", label="Medido"),
                Line2D([0], [0], color="gray", linewidth=2, linestyle="--", marker="o",
                       markerfacecolor="white", label="Estimado")]
    ax.legend(handles=leyenda, loc="upper left", fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(GRAF, archivo), dpi=150)
    plt.close(fig)
    print(f"  {archivo}")


def grafica_barras(series, algoritmos, nombres, colores, titulo, eje_y, archivo, formato):
    """series: lista de (etiqueta, {alg: (valor, estimado)})."""
    fig, ax = plt.subplots(figsize=(12, 6.5))
    k = len(series)
    ancho = 0.8 / k
    maximo = 0
    for j, (etiqueta, valores) in enumerate(series):
        for i, alg in enumerate(algoritmos):
            valor, estimado = valores.get(alg, (None, False))
            x = i - 0.4 + ancho * (j + 0.5)
            if valor is None:
                ax.text(x, 1, "sin dato", ha="center", va="bottom", rotation=90, fontsize=8)
                continue
            maximo = max(maximo, valor)
            ax.bar(x, valor, width=ancho, color=colores[etiqueta],
                   hatch="///" if estimado else None, edgecolor="black", linewidth=0.6)
            texto = formato(valor) + (" (est.)" if estimado else "")
            ax.text(x, valor * 1.15, texto, ha="center", va="bottom", rotation=90, fontsize=8)

    ax.set_yscale("log")
    if maximo:
        ax.set_ylim(top=maximo * 60)
    ax.set_xticks(range(len(algoritmos)))
    ax.set_xticklabels([nombres[a] for a in algoritmos])
    ax.set_ylabel(eje_y)
    ax.set_title(titulo)
    ax.grid(True, axis="y", which="both", alpha=0.3)
    leyenda = [Patch(facecolor=colores[e], edgecolor="black", label=e.capitalize()) for e, _ in series]
    leyenda.append(Patch(facecolor="white", edgecolor="black", hatch="///", label="Estimado"))
    ax.legend(handles=leyenda, loc="upper left", fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(GRAF, archivo), dpi=150)
    plt.close(fig)
    print(f"  {archivo}")


def valores(datos, algoritmos, lenguaje, variante, n):
    salida = {}
    for alg in algoritmos:
        if (alg, lenguaje, variante, n) in datos:
            v, e, _ = datos[(alg, lenguaje, variante, n)]
            salida[alg] = (v, e)
    return salida


# ---------------------------------------------------------------
# Tablas de apoyo (resultados/tablas.md)
# ---------------------------------------------------------------
def tabla_factores(datos, lenguaje, variante, algoritmos, nombres, teoria):
    ns = tamanos(datos)
    pares = list(zip(ns, ns[1:]))
    enc = ["Algoritmo", "Teoría"] + [f"{etiqueta_n(a)} → {etiqueta_n(b)}" for a, b in pares]
    lineas = ["| " + " | ".join(enc) + " |", "|" + "---|" * len(enc)]
    for alg in algoritmos:
        celdas = [nombres[alg], teoria[alg]]
        for a, b in pares:
            ka, kb = (alg, lenguaje, variante, a), (alg, lenguaje, variante, b)
            if ka in datos and kb in datos and datos[ka][0] and datos[kb][0]:
                f = datos[kb][0] / datos[ka][0]
                est = datos[ka][1] or datos[kb][1]
                celdas.append(f"×{num(f, 1)}" + (" (est.)" if est else ""))
            else:
                celdas.append("—")
        lineas.append("| " + " | ".join(celdas) + " |")
    return "\n".join(lineas)


def tabla_estimados(datos, nombres):
    lineas = ["| Algoritmo | Lenguaje | Variante | n | Tiempo estimado | Motivo |",
              "|---|---|---|---|---|---|"]
    for (alg, leng, var, n), (v, e, obs) in sorted(datos.items(), key=lambda x: (x[0][1], x[0][0], x[0][2], x[0][3])):
        if e:
            lineas.append(f"| {nombres.get(alg, alg)} | {leng} | {var} | {etiqueta_n(n)} | {fmt_ms(v)} | {obs} |")
    return "\n".join(lineas)


def tabla_posicion(datos, lenguaje, n):
    lineas = ["| Algoritmo | Inicio | Centro | Final |", "|---|---|---|---|"]
    for alg in BUSQUEDAS:
        celdas = [NOMBRE_BUS[alg]]
        for pos in ("inicio", "centro", "final"):
            clave = (alg, lenguaje, pos, n)
            celdas.append(fmt_ns(datos[clave][0]) if clave in datos else "—")
        lineas.append("| " + " | ".join(celdas) + " |")
    return "\n".join(lineas)


def calculo_k(ord_datos, bus_datos, lenguaje, n):
    medidos = {alg: ord_datos[(alg, lenguaje, "aleatorio", n)][0]
               for alg in ORDENAMIENTOS
               if (alg, lenguaje, "aleatorio", n) in ord_datos
               and not ord_datos[(alg, lenguaje, "aleatorio", n)][1]}
    if not medidos or ("Lineal", lenguaje, "claves", n) not in bus_datos:
        return f"No hay datos suficientes de {lenguaje} con n = {etiqueta_n(n)}."
    mejor = min(medidos, key=medidos.get)
    t_ord = medidos[mejor]
    t_lin = bus_datos[("Lineal", lenguaje, "claves", n)][0] / 1e6   # ns -> ms
    t_bin = bus_datos[("Binaria", lenguaje, "claves", n)][0] / 1e6
    k = t_ord / (t_lin - t_bin)
    k_min = int(k) + 1
    return (f"- Mejor ordenamiento ({lenguaje}, n = {etiqueta_n(n)}, aleatorio): "
            f"**{NOMBRE_ORD[mejor]}**, {num(t_ord, 2)} ms\n"
            f"- Búsqueda lineal: {num(t_lin, 6)} ms por búsqueda\n"
            f"- Búsqueda binaria: {num(t_bin, 6)} ms por búsqueda\n"
            f"- Condición: T_ordenar + k · T_binaria < k · T_lineal  →  k > T_ordenar / (T_lineal − T_binaria)\n"
            f"- k > {num(t_ord, 2)} / ({num(t_lin, 6)} − {num(t_bin, 6)}) = {num(k, 1)}\n"
            f"- **Conviene ordenar a partir de k = {num(k_min, 0)} búsquedas.**")


# ---------------------------------------------------------------
def main():
    os.makedirs(GRAF, exist_ok=True)
    ord_datos = {**leer("ordenamiento_java.csv", "promedio_ms"),
                 **leer("ordenamiento_python.csv", "promedio_ms")}
    bus_datos = {**leer("busqueda_java.csv", "promedio_por_busqueda_ns"),
                 **leer("busqueda_python.csv", "promedio_por_busqueda_ns")}
    bus_crec = {k: v for k, v in bus_datos.items() if k[2] == "claves"}

    print("Gráficas del Punto 1:")
    for leng in ("Java", "Python"):
        grafica_crecimiento(ord_datos, leng, "aleatorio", ORDENAMIENTOS, NOMBRE_ORD,
                            f"Punto 1 · Crecimiento del tiempo de ordenamiento · {leng} · entrada aleatoria",
                            "Tiempo promedio (ms, escala logarítmica)",
                            f"p1_crecimiento_{leng.lower()}.png")

    for n in [n for n in (1_000, 10_000, 100_000) if n in tamanos(ord_datos)]:
        series = [(var, valores(ord_datos, ORDENAMIENTOS, "Java", var, n))
                  for var in ("aleatorio", "ascendente", "descendente")]
        grafica_barras(series, ORDENAMIENTOS, NOMBRE_ORD, COLOR_VARIANTE,
                       f"Punto 1 · Efecto del orden de entrada · Java · n = {etiqueta_n(n)}",
                       "Tiempo promedio (ms, escala logarítmica)",
                       f"p1_orden_entrada_n{n}.png", fmt_ms)

    n_max = max(tamanos(ord_datos))
    series = [(leng, valores(ord_datos, ORDENAMIENTOS, leng, "aleatorio", n_max)) for leng in ("Java", "Python")]
    grafica_barras(series, ORDENAMIENTOS, NOMBRE_ORD, COLOR_LENGUAJE,
                   f"Punto 1 · Compilado frente a interpretado · entrada aleatoria · n = {etiqueta_n(n_max)}",
                   "Tiempo promedio (ms, escala logarítmica)",
                   f"p1_java_vs_python_n{n_max}.png", fmt_ms)

    print("Gráficas del Punto 2:")
    for leng in ("Java", "Python"):
        grafica_crecimiento(bus_crec, leng, "claves", BUSQUEDAS, NOMBRE_BUS,
                            f"Punto 2 · Tiempo promedio por búsqueda · {leng}",
                            "Tiempo promedio por búsqueda (ns, escala logarítmica)",
                            f"p2_crecimiento_{leng.lower()}.png")

    nb_max = max(tamanos(bus_crec))
    series = [(leng, valores(bus_crec, BUSQUEDAS, leng, "claves", nb_max)) for leng in ("Java", "Python")]
    grafica_barras(series, BUSQUEDAS, NOMBRE_BUS, COLOR_LENGUAJE,
                   f"Punto 2 · Compilado frente a interpretado · n = {etiqueta_n(nb_max)}",
                   "Tiempo promedio por búsqueda (ns, escala logarítmica)",
                   f"p2_java_vs_python_n{nb_max}.png", fmt_ns)

    n_pos = max(k[3] for k in bus_datos if k[2] == "inicio")
    md = [
        "# Tablas de apoyo para el análisis",
        "",
        "Generadas automáticamente por `python/graficas.py` a partir de los CSV de `resultados/`.",
        "",
        "## Punto 1 · Factor de aumento del tiempo cuando n se multiplica por 10 (entrada aleatoria)",
        "",
        "### Java", "", tabla_factores(ord_datos, "Java", "aleatorio", ORDENAMIENTOS, NOMBRE_ORD, TEORIA_ORD), "",
        "### Python", "", tabla_factores(ord_datos, "Python", "aleatorio", ORDENAMIENTOS, NOMBRE_ORD, TEORIA_ORD), "",
        "## Punto 1 · Casos estimados", "", tabla_estimados(ord_datos, NOMBRE_ORD), "",
        "## Punto 2 · Factor de aumento del tiempo por búsqueda cuando n se multiplica por 10", "",
        "### Java", "", tabla_factores(bus_crec, "Java", "claves", BUSQUEDAS, NOMBRE_BUS, TEORIA_BUS), "",
        "### Python", "", tabla_factores(bus_crec, "Python", "claves", BUSQUEDAS, NOMBRE_BUS, TEORIA_BUS), "",
        f"## Punto 2 · Posición de la clave (tiempo promedio por búsqueda, n = {etiqueta_n(n_pos)})", "",
        "### Java", "", tabla_posicion(bus_datos, "Java", n_pos), "",
        "### Python", "", tabla_posicion(bus_datos, "Python", n_pos), "",
        f"## Punto 3 · ¿Ordenar o no ordenar? (n = {etiqueta_n(n_max)})", "",
        "### Java", "", calculo_k(ord_datos, bus_crec, "Java", n_max), "",
        "### Python", "", calculo_k(ord_datos, bus_crec, "Python", n_max), "",
    ]
    with open(os.path.join(RES, "tablas.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"Tablas: {os.path.join(RES, 'tablas.md')}")


if __name__ == "__main__":
    main()
