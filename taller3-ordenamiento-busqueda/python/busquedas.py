"""
Algoritmos de busqueda del Taller 3 (version Python).
Es una traduccion directa de java/src/Busquedas.java, basada en GeeksforGeeks.
Todos reciben una lista ordenada ascendentemente y retornan el indice de x, o -1 si no esta.
"""
import math


# ---------------------------------------------------------------
# Busqueda Lineal (referencia)
# ---------------------------------------------------------------
def lineal(arr, x):
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return -1


# ---------------------------------------------------------------
# Busqueda Binaria (iterativa)
# ---------------------------------------------------------------
def binaria(arr, x):
    return _binaria(arr, 0, len(arr) - 1, x)


def _binaria(arr, l, r, x):
    while l <= r:
        m = l + (r - l) // 2
        if arr[m] == x:
            return m
        if arr[m] < x:
            l = m + 1
        else:
            r = m - 1
    return -1


# ---------------------------------------------------------------
# Busqueda Ternaria (iterativa)
# ---------------------------------------------------------------
def ternaria(arr, x):
    l, r = 0, len(arr) - 1
    while r >= l:
        mid1 = l + (r - l) // 3
        mid2 = r - (r - l) // 3
        if arr[mid1] == x:
            return mid1
        if arr[mid2] == x:
            return mid2
        if x < arr[mid1]:
            r = mid1 - 1
        elif x > arr[mid2]:
            l = mid2 + 1
        else:
            l = mid1 + 1
            r = mid2 - 1
    return -1


# ---------------------------------------------------------------
# Busqueda por Saltos (Jump Search), salto = raiz de n
# ---------------------------------------------------------------
def saltos(arr, x):
    n = len(arr)
    if n == 0:
        return -1

    salto = math.isqrt(n)
    paso = salto
    prev = 0
    while arr[min(paso, n) - 1] < x:
        prev = paso
        paso += salto
        if prev >= n:
            return -1
    while arr[prev] < x:
        prev += 1
        if prev == min(paso, n):
            return -1
    if arr[prev] == x:
        return prev
    return -1


# ---------------------------------------------------------------
# Busqueda por Interpolacion (iterativa)
# ---------------------------------------------------------------
def interpolacion(arr, x):
    lo, hi = 0, len(arr) - 1
    while lo <= hi and arr[lo] <= x <= arr[hi]:
        if arr[hi] == arr[lo]:  # evita division entre cero si hay valores repetidos
            return lo if arr[lo] == x else -1
        pos = lo + (x - arr[lo]) * (hi - lo) // (arr[hi] - arr[lo])
        if arr[pos] == x:
            return pos
        if arr[pos] < x:
            lo = pos + 1
        else:
            hi = pos - 1
    return -1


# ---------------------------------------------------------------
# Busqueda Exponencial
# ---------------------------------------------------------------
def exponencial(arr, x):
    n = len(arr)
    if n == 0:
        return -1
    if n == 0:                 # Python
        return -1
    if arr[0] == x:
        return 0
    i = 1
    while i < n and arr[i] <= x:
        i *= 2
    return _binaria(arr, i // 2, min(i, n - 1), x)
