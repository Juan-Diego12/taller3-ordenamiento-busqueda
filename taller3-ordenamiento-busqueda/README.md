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
```

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

## Fuentes

Implementaciones basadas en GeeksforGeeks (verificar cada enlace antes de la entrega):

c
