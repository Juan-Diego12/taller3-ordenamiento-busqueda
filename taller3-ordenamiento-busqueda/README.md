# Taller 3: Ordenamiento y Búsqueda

Comparación experimental de algoritmos de ordenamiento y búsqueda en un lenguaje compilado (Java) y uno interpretado (Python).

## Estructura

```
datos/        Archivos de prueba (se generan con python/generar_datos.py)
java/src/     Implementaciones en Java
python/       Generador de datos e implementaciones en Python
resultados/   Mediciones en CSV
graficas/     Gráficas generadas
```

## Cómo ejecutar

Desde la raíz del repositorio:

```
python python/generar_datos.py          # una sola vez
javac -d out java/src/*.java
java -cp out PruebaRapida 1000          # prueba rápida de los ordenamientos

java -Xmx2g -cp out MedirOrdenamientos  # medición oficial en Java
python python/medir_ordenamientos.py    # medición oficial en Python
```

Los resultados quedan en `resultados/ordenamiento_java.csv` y `resultados/ordenamiento_python.csv`.

## Datos de prueba

- Semilla fija: 42.
- Enteros aleatorios de 8 dígitos (10.000.000 a 99.999.999).
- Se genera un arreglo de 1.000.000 y los tamaños menores son sus primeros n elementos.
- Para cada tamaño hay tres variantes: `aleatorio_n.txt`, `ascendente_n.txt` y `descendente_n.txt`.
- `claves_busqueda.txt`: 1.000 claves. Las 500 presentes se tomaron del arreglo de 1.000, así que están en todos los tamaños. Las 500 ausentes no aparecen en el arreglo de 1.000.000, así que no están en ningún tamaño.

## Decisiones de implementación

- **Dual-Pivot QuickSort:** pivotes en el primer y el último elemento.
- **Radix Sort:** LSD en base 10 con counting sort por dígito (8 pasadas para números de 8 dígitos).
- **Bucket Sort:** n cubetas. Cada valor v va a la cubeta `(v - 10.000.000) * n / 90.000.000`. Cada cubeta se ordena con Insertion Sort.

## Medición del tiempo

- Los datos se cargan antes de medir; la lectura de archivos no se cuenta.
- Java: `System.nanoTime()`, con una ejecución de calentamiento (JIT) que no se incluye en el promedio.
- Python: `time.perf_counter_ns()`, sin calentamiento (no tiene JIT).
- 5 repeticiones, cada una sobre una copia nueva del arreglo (la copia no se mide).
- Después de cada repetición, y fuera del tiempo medido, se verifica que el arreglo quedó ordenado y con los mismos elementos.
- Se reporta el promedio y la desviación estándar muestral.

## Estimaciones

Antes de ejecutar un tamaño, se predice su tiempo a partir del promedio medido en el tamaño anterior y la complejidad teórica del caso:

```
tiempo estimado(n nuevo) = tiempo medido(n anterior) × f(n nuevo) / f(n anterior)
```

| Algoritmo | f(n) usada |
|---|---|
| Insertion Sort | n (ascendente), n² (aleatorio y descendente) |
| Dual-Pivot QuickSort | n log n (aleatorio), n² (ascendente y descendente) |
| Merge Sort, Heap Sort | n log n |
| Radix Sort, Bucket Sort | n |

- Si la predicción supera 5 minutos, el caso no se ejecuta y se registra como `estimado`.
- Si ocurre `StackOverflowError` (Java) o `RecursionError` (Python), se registra el error en la columna `observacion` y el tiempo se estima con la misma fórmula. Los tamaños mayores de ese caso también se estiman.

## Fuentes

Implementaciones basadas en GeeksforGeeks (verificar cada enlace antes de la entrega):

- Insertion Sort: https://www.geeksforgeeks.org/insertion-sort-algorithm/
- Dual-Pivot QuickSort: https://www.geeksforgeeks.org/dual-pivot-quicksort/
- Merge Sort: https://www.geeksforgeeks.org/merge-sort/
- Heap Sort: https://www.geeksforgeeks.org/heap-sort/
- Radix Sort: https://www.geeksforgeeks.org/radix-sort/
- Bucket Sort: https://www.geeksforgeeks.org/bucket-sort-2/
