"""
Medicion oficial de los ordenamientos en Python (Punto 1).

Uso (desde la raiz del repositorio):
    python python/medir_ordenamientos.py 1000 10000          # prueba
    python python/medir_ordenamientos.py                     # todos los tamanos

Por cada algoritmo, variante y tamano:
  - Carga los datos ANTES de medir.
  - Hace 5 repeticiones, cada una sobre una copia nueva (la copia no se mide).
  - Verifica el resultado fuera del tiempo medido.
  - Escribe una fila en resultados/ordenamiento_python.csv apenas termina.
Python no tiene JIT, por eso no se hace calentamiento.

Casos que no se ejecutan (ver README, seccion "Estimaciones"):
  - Si la prediccion para el nuevo tamano supera 5 minutos, se marca como estimado.
  - Si ocurre RecursionError, se documenta y se estima.
"""
import math
import os
import statistics
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
import ordenamientos as o  # noqa: E402

LIMITE_MS = 300_000  # 5 minutos por ejecucion
REPETICIONES = 5
VARIANTES = ["aleatorio", "ascendente", "descendente"]
SALIDA = "resultados/ordenamiento_python.csv"

ALGORITMOS = {
    "InsertionSort": o.insertion_sort,
    "DualPivotQuickSort": o.dual_pivot_quick_sort,
    "MergeSort": o.merge_sort,
    "HeapSort": o.heap_sort,
    "RadixSort": o.radix_sort,
    "BucketSort": o.bucket_sort,
}


def leer(ruta):
    with open(ruta) as f:
        return [int(x) for x in f if x.strip()]


def complejidad(alg, variante, n):
    """Funcion de crecimiento teorica usada para predecir y estimar."""
    nlogn = n * math.log(n)
    if alg == "InsertionSort":
        return n if variante == "ascendente" else n * n
    if alg == "DualPivotQuickSort":
        return nlogn if variante == "aleatorio" else n * n
    if alg in ("MergeSort", "HeapSort"):
        return nlogn
    return n  # RadixSort y BucketSort


def factor(alg, variante, n_prev, n_nuevo):
    return complejidad(alg, variante, n_nuevo) / complejidad(alg, variante, n_prev)


def fila(csv, alg, variante, n, tiempos, promedio, desv, tipo, obs):
    t = [f"{x:.4f}" for x in tiempos] + [""] * (REPETICIONES - len(tiempos))
    prom = "" if promedio is None else f"{promedio:.4f}"
    de = "" if desv is None else f"{desv:.4f}"
    csv.write(",".join([alg, "Python", variante, str(n)] + t + [prom, de, tipo, obs]) + "\n")
    csv.flush()


def main():
    tamanos = [int(x) for x in sys.argv[1:]] or [1_000, 10_000, 100_000, 1_000_000]
    os.makedirs("resultados", exist_ok=True)
    ultimo = {}      # (alg, variante) -> (n, promedio_ms)
    fallaron = set()

    with open(SALIDA, "w") as csv:
        csv.write("algoritmo,lenguaje,variante,n,t1_ms,t2_ms,t3_ms,t4_ms,t5_ms,"
                  "promedio_ms,desviacion_ms,tipo,observacion\n")
        for n in tamanos:
            for variante in VARIANTES:
                original = leer(f"datos/{variante}_{n}.txt")
                esperado = sorted(original)
                for alg, funcion in ALGORITMOS.items():
                    clave = (alg, variante)
                    prev = ultimo.get(clave)
                    est = prev[1] * factor(alg, variante, prev[0], n) if prev else None

                    if clave in fallaron:
                        fila(csv, alg, variante, n, [], est, None, "estimado",
                             "no se ejecuto: fallo con un n menor (RecursionError)")
                        if est is not None:
                            ultimo[clave] = (n, est)
                        print(f"{alg:20} {variante:12} n={n:>9,}  ESTIMADO (fallo previo)")
                        continue

                    if est is not None and est > LIMITE_MS:
                        fila(csv, alg, variante, n, [], est, None, "estimado",
                             f"no se ejecuto: prediccion {est / 1000:.0f} s supera 5 min")
                        ultimo[clave] = (n, est)
                        print(f"{alg:20} {variante:12} n={n:>9,}  ESTIMADO {est / 1000:,.1f} s")
                        continue

                    tiempos = []
                    try:
                        for _ in range(REPETICIONES):
                            copia = original[:]
                            t0 = time.perf_counter_ns()
                            funcion(copia)
                            t1 = time.perf_counter_ns()
                            ms = (t1 - t0) / 1e6
                            if copia != esperado:
                                raise ValueError("el arreglo no quedo ordenado")
                            tiempos.append(ms)
                            if ms > LIMITE_MS:
                                break
                    except RecursionError:
                        fallaron.add(clave)
                        fila(csv, alg, variante, n, [], est, None, "estimado",
                             "RecursionError: se supero el limite de recursion de Python")
                        if est is not None:
                            ultimo[clave] = (n, est)
                        print(f"{alg:20} {variante:12} n={n:>9,}  RecursionError -> estimado")
                        continue

                    promedio = statistics.mean(tiempos)
                    desv = statistics.stdev(tiempos) if len(tiempos) > 1 else 0.0
                    if len(tiempos) < REPETICIONES:
                        fila(csv, alg, variante, n, tiempos, promedio, desv, "estimado",
                             "una repeticion supero 5 min; se detuvo")
                    else:
                        fila(csv, alg, variante, n, tiempos, promedio, desv, "medido", "")
                    ultimo[clave] = (n, promedio)
                    print(f"{alg:20} {variante:12} n={n:>9,}  {promedio:12.3f} ms  (de {desv:.3f})")

    print(f"\nResultados guardados en {SALIDA}")


if __name__ == "__main__":
    main()
