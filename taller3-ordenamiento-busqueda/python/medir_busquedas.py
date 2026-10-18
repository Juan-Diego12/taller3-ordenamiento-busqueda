"""
Medicion oficial de las busquedas en Python (Punto 2).

Uso (desde la raiz del repositorio):
    python python/medir_busquedas.py 1000 10000      # prueba
    python python/medir_busquedas.py                 # todos los tamanos

Experimento 1 (variante "claves"): para cada n, se buscan las 1000 claves de
  datos/claves_busqueda.txt (500 presentes y 500 ausentes) en el arreglo ascendente.
Experimento 2 (variantes "inicio", "centro" y "final"): con el tamano mas grande,
  se busca 1000 veces una clave ubicada al inicio, en el centro y al final.

En ambos: 5 repeticiones (Python no tiene JIT, no hay calentamiento). Se mide el tiempo
total de las 1000 busquedas y se reporta tambien el promedio por busqueda en nanosegundos.
Antes de medir, y fuera del tiempo, se verifica que cada algoritmo responda bien.
"""
import bisect
import os
import statistics
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
import busquedas as b  # noqa: E402

REPETICIONES = 5
SALIDA = "resultados/busqueda_python.csv"

ALGORITMOS = {
    "Lineal": b.lineal,
    "Binaria": b.binaria,
    "Ternaria": b.ternaria,
    "Saltos": b.saltos,
    "Interpolacion": b.interpolacion,
    "Exponencial": b.exponencial,
}


def leer(ruta):
    with open(ruta) as f:
        return [int(x) for x in f if x.strip()]


def esta(arr, k):
    i = bisect.bisect_left(arr, k)
    return i < len(arr) and arr[i] == k


def verificar(nombre, funcion, arr, claves):
    for k in claves:
        r = funcion(arr, k)
        ok = (r >= 0 and arr[r] == k) if esta(arr, k) else r == -1
        if not ok:
            raise ValueError(f"{nombre} respondio mal para la clave {k}")


def medir(csv, nombre, funcion, arr, claves, variante, n):
    tiempos = []
    for _ in range(REPETICIONES):
        t0 = time.perf_counter_ns()
        for k in claves:
            funcion(arr, k)
        t1 = time.perf_counter_ns()
        tiempos.append((t1 - t0) / 1e6)
    prom = statistics.mean(tiempos)
    desv = statistics.stdev(tiempos)
    por_busqueda_ns = prom * 1e6 / len(claves)
    desv_por_busqueda_ns = desv * 1e6 / len(claves)
    t = ",".join(f"{x:.4f}" for x in tiempos)
    csv.write(f"{nombre},Python,{variante},{n},{t},{prom:.4f},{desv:.4f},"
              f"{por_busqueda_ns:.2f},{desv_por_busqueda_ns:.2f},medido,\n")
    csv.flush()
    print(f"{nombre:14} {variante:8} n={n:>9,}  {por_busqueda_ns:14.2f} ns por busqueda")


def main():
    tamanos = [int(x) for x in sys.argv[1:]] or [1_000, 10_000, 100_000, 1_000_000]
    n_mayor = max(tamanos)
    claves = leer("datos/claves_busqueda.txt")
    os.makedirs("resultados", exist_ok=True)

    with open(SALIDA, "w") as csv:
        csv.write("algoritmo,lenguaje,variante,n,t1_ms,t2_ms,t3_ms,t4_ms,t5_ms,promedio_ms,"
                  "desviacion_ms,promedio_por_busqueda_ns,desviacion_por_busqueda_ns,tipo,observacion\n")
        for n in tamanos:
            arr = leer(f"datos/ascendente_{n}.txt")

            # Experimento 1: 1000 claves (500 presentes y 500 ausentes)
            for nombre, funcion in ALGORITMOS.items():
                verificar(nombre, funcion, arr, claves)
                medir(csv, nombre, funcion, arr, claves, "claves", n)

            # Experimento 2: posicion de la clave (solo con el tamano mas grande)
            if n == n_mayor:
                for posicion, indice in (("inicio", 0), ("centro", n // 2), ("final", n - 1)):
                    repetida = [arr[indice]] * 1000
                    for nombre, funcion in ALGORITMOS.items():
                        verificar(nombre, funcion, arr, repetida[:1])
                        medir(csv, nombre, funcion, arr, repetida, posicion, n)

    print(f"\nResultados guardados en {SALIDA}")


if __name__ == "__main__":
    main()
