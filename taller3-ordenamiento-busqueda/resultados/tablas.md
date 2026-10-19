# Tablas de apoyo para el análisis

Generadas automáticamente por `python/graficas.py` a partir de los CSV de `resultados/`.

## Punto 1 · Factor de aumento del tiempo cuando n se multiplica por 10 (entrada aleatoria)

### Java

| Algoritmo | Teoría | 1.000 → 10.000 | 10.000 → 100.000 | 100.000 → 1.000.000 |
|---|---|---|---|---|
| Insertion Sort | ×100 (n²) | ×6,2 | ×82,4 | ×116,2 |
| Dual-Pivot QuickSort | ≈×12 a ×13 (n log n) | ×4,2 | ×12,1 | ×12,2 |
| Merge Sort | ≈×12 a ×13 (n log n) | ×5,1 | ×9,3 | ×12,2 |
| Heap Sort | ≈×12 a ×13 (n log n) | ×3,4 | ×9,9 | ×14,0 |
| Radix Sort | ×10 (n) | ×1,2 | ×7,1 | ×8,1 |
| Bucket Sort | ×10 (n, promedio) | ×5,3 | ×5,0 | ×22,6 |

### Python

| Algoritmo | Teoría | 1.000 → 10.000 | 10.000 → 100.000 | 100.000 → 1.000.000 |
|---|---|---|---|---|
| Insertion Sort | ×100 (n²) | ×119,9 | ×110,1 | ×100,0 (est.) |
| Dual-Pivot QuickSort | ≈×12 a ×13 (n log n) | ×13,8 | ×11,9 | ×13,8 |
| Merge Sort | ≈×12 a ×13 (n log n) | ×14,2 | ×11,0 | ×13,2 |
| Heap Sort | ≈×12 a ×13 (n log n) | ×17,5 | ×11,1 | ×14,9 |
| Radix Sort | ×10 (n) | ×12,3 | ×9,6 | ×15,3 |
| Bucket Sort | ×10 (n, promedio) | ×8,4 | ×13,3 | ×19,6 |

## Punto 1 · Casos estimados

| Algoritmo | Lenguaje | Variante | n | Tiempo estimado | Motivo |
|---|---|---|---|---|---|
| Dual-Pivot QuickSort | Java | ascendente | 100.000 | 2,3 s | StackOverflowError: desbordamiento de la pila de llamadas |
| Dual-Pivot QuickSort | Java | ascendente | 1.000.000 | 3,9 min | no se ejecuto: fallo con un n menor (StackOverflowError) |
| Dual-Pivot QuickSort | Java | descendente | 100.000 | 2,7 s | StackOverflowError: desbordamiento de la pila de llamadas |
| Dual-Pivot QuickSort | Java | descendente | 1.000.000 | 4,5 min | no se ejecuto: fallo con un n menor (StackOverflowError) |
| Dual-Pivot QuickSort | Python | ascendente | 10.000 | 1,2 s | RecursionError: se supero el limite de recursion de Python |
| Dual-Pivot QuickSort | Python | ascendente | 100.000 | 2,1 min | no se ejecuto: fallo con un n menor (RecursionError) |
| Dual-Pivot QuickSort | Python | ascendente | 1.000.000 | 3,4 h | no se ejecuto: fallo con un n menor (RecursionError) |
| Dual-Pivot QuickSort | Python | descendente | 10.000 | 1,3 s | RecursionError: se supero el limite de recursion de Python |
| Dual-Pivot QuickSort | Python | descendente | 100.000 | 2,1 min | no se ejecuto: fallo con un n menor (RecursionError) |
| Dual-Pivot QuickSort | Python | descendente | 1.000.000 | 3,5 h | no se ejecuto: fallo con un n menor (RecursionError) |
| Insertion Sort | Python | aleatorio | 1.000.000 | 5,4 h | no se ejecuto: prediccion 19481 s supera 5 min |
| Insertion Sort | Python | descendente | 100.000 | 5,4 min | no se ejecuto: prediccion 325 s supera 5 min |
| Insertion Sort | Python | descendente | 1.000.000 | 9,0 h | no se ejecuto: prediccion 32493 s supera 5 min |

## Punto 2 · Factor de aumento del tiempo por búsqueda cuando n se multiplica por 10

### Java

| Algoritmo | Teoría | 1.000 → 10.000 | 10.000 → 100.000 | 100.000 → 1.000.000 |
|---|---|---|---|---|
| Lineal | ×10 (n) | ×7,4 | ×11,7 | ×10,1 |
| Binaria | crece poco (log n) | ×1,1 | ×1,0 | ×1,6 |
| Ternaria | crece poco (log n) | ×0,6 | ×0,8 | ×2,0 |
| Por saltos | ×3,16 (√n) | ×1,3 | ×2,4 | ×3,0 |
| Interpolación | casi constante (log log n) | ×0,7 | ×1,0 | ×1,4 |
| Exponencial | crece poco (log n) | ×0,7 | ×1,3 | ×1,4 |

### Python

| Algoritmo | Teoría | 1.000 → 10.000 | 10.000 → 100.000 | 100.000 → 1.000.000 |
|---|---|---|---|---|
| Lineal | ×10 (n) | ×10,8 | ×10,1 | ×10,8 |
| Binaria | crece poco (log n) | ×1,3 | ×1,4 | ×1,3 |
| Ternaria | crece poco (log n) | ×1,2 | ×1,4 | ×1,2 |
| Por saltos | ×3,16 (√n) | ×3,6 | ×2,7 | ×3,2 |
| Interpolación | casi constante (log log n) | ×1,4 | ×0,9 | ×1,5 |
| Exponencial | crece poco (log n) | ×1,5 | ×1,4 | ×1,4 |

## Punto 2 · Posición de la clave (tiempo promedio por búsqueda, n = 1.000.000)

### Java

| Algoritmo | Inicio | Centro | Final |
|---|---|---|---|
| Lineal | 5,5 ns | 90,3 µs | 193,6 µs |
| Binaria | 51,9 ns | 48,5 ns | 69,9 ns |
| Ternaria | 63,5 ns | 37,6 ns | 49,6 ns |
| Por saltos | 10,2 ns | 505,9 ns | 2,5 µs |
| Interpolación | 9,2 ns | 23,2 ns | 5,6 ns |
| Exponencial | 12,1 ns | 91,0 ns | 59,7 ns |

### Python

| Algoritmo | Inicio | Centro | Final |
|---|---|---|---|
| Lineal | 269,8 ns | 13,0 ms | 26,0 ms |
| Binaria | 1,8 µs | 2,2 µs | 2,1 µs |
| Ternaria | 3,0 µs | 2,3 µs | 2,2 µs |
| Por saltos | 399,9 ns | 68,9 µs | 259,8 µs |
| Interpolación | 291,1 ns | 686,9 ns | 394,4 ns |
| Exponencial | 102,0 ns | 2,3 µs | 2,8 µs |

## Punto 3 · ¿Ordenar o no ordenar? (n = 1.000.000)

### Java

- Mejor ordenamiento (Java, n = 1.000.000, aleatorio): **Radix Sort**, 46,49 ms
- Búsqueda lineal: 0,138801 ms por búsqueda
- Búsqueda binaria: 0,000146 ms por búsqueda
- Condición: T_ordenar + k · T_binaria < k · T_lineal  →  k > T_ordenar / (T_lineal − T_binaria)
- k > 46,49 / (0,138801 − 0,000146) = 335,3
- **Conviene ordenar a partir de k = 336 búsquedas.**

### Python

- Mejor ordenamiento (Python, n = 1.000.000, aleatorio): **Bucket Sort**, 1.107,93 ms
- Búsqueda lineal: 20,273659 ms por búsqueda
- Búsqueda binaria: 0,002423 ms por búsqueda
- Condición: T_ordenar + k · T_binaria < k · T_lineal  →  k > T_ordenar / (T_lineal − T_binaria)
- k > 1.107,93 / (20,273659 − 0,002423) = 54,7
- **Conviene ordenar a partir de k = 55 búsquedas.**
