"""
Generador de datos del Taller 3 (Ordenamiento y Busqueda).

Se ejecuta UNA sola vez desde la raiz del repositorio:
    python python/generar_datos.py

Crea en la carpeta datos/:
  - aleatorio_N.txt, ascendente_N.txt y descendente_N.txt para N = 1000, 10000, 100000 y 1000000
  - claves_busqueda.txt con 1000 claves (500 presentes y 500 ausentes)

Decisiones de diseno:
  - Semilla fija (42) para que cualquiera pueda reproducir exactamente los mismos datos.
  - Se genera un solo arreglo de 1.000.000 y los tamanos menores son sus primeros N elementos.
    Asi el arreglo de 1.000 esta contenido en todos los demas.
  - Las 500 claves presentes se toman del arreglo de 1.000, por lo que estan presentes en TODOS los tamanos.
  - Las 500 claves ausentes no aparecen en el arreglo de 1.000.000, por lo que estan ausentes en TODOS los tamanos.
"""
import os
import random

SEMILLA = 42
TAMANOS = [1_000, 10_000, 100_000, 1_000_000]
MINIMO = 10_000_000
MAXIMO = 99_999_999
CARPETA = "datos"


def guardar(ruta, numeros):
    with open(ruta, "w") as f:
        f.write("\n".join(map(str, numeros)))
        f.write("\n")


def main():
    os.makedirs(CARPETA, exist_ok=True)
    random.seed(SEMILLA)

    n_max = max(TAMANOS)
    base = [random.randint(MINIMO, MAXIMO) for _ in range(n_max)]

    for n in TAMANOS:
        datos = base[:n]
        guardar(f"{CARPETA}/aleatorio_{n}.txt", datos)
        guardar(f"{CARPETA}/ascendente_{n}.txt", sorted(datos))
        guardar(f"{CARPETA}/descendente_{n}.txt", sorted(datos, reverse=True))
        print(f"n = {n:>9,}: archivos aleatorio, ascendente y descendente creados")

    # Claves de busqueda
    presentes = random.sample(sorted(set(base[:TAMANOS[0]])), 500)
    todos = set(base)
    ausentes = []
    vistos = set()
    while len(ausentes) < 500:
        x = random.randint(MINIMO, MAXIMO)
        if x not in todos and x not in vistos:
            ausentes.append(x)
            vistos.add(x)

    claves = presentes + ausentes
    random.shuffle(claves)
    guardar(f"{CARPETA}/claves_busqueda.txt", claves)
    print("claves_busqueda.txt creado (500 presentes + 500 ausentes)")


if __name__ == "__main__":
    main()
