"""
Algoritmos de ordenamiento del Taller 3 (version Python).
Es una traduccion directa de java/src/Ordenamientos.java, basada en GeeksforGeeks.
Todos ordenan la lista recibida en forma ascendente.
"""

MINIMO = 10_000_000
RANGO = 90_000_000  # valores entre 10.000.000 y 99.999.999


# ---------------------------------------------------------------
# Insertion Sort
# ---------------------------------------------------------------
def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


# ---------------------------------------------------------------
# Dual-Pivot QuickSort (pivotes: primer y ultimo elemento)
# ---------------------------------------------------------------
def dual_pivot_quick_sort(arr):
    _dual_pivot_quick_sort(arr, 0, len(arr) - 1)


def _dual_pivot_quick_sort(arr, low, high):
    if low < high:
        lp, rp = _partition(arr, low, high)
        _dual_pivot_quick_sort(arr, low, lp - 1)
        _dual_pivot_quick_sort(arr, lp + 1, rp - 1)
        _dual_pivot_quick_sort(arr, rp + 1, high)


def _partition(arr, low, high):
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
    j = low + 1
    g = high - 1
    k = low + 1
    p = arr[low]
    q = arr[high]
    while k <= g:
        if arr[k] < p:
            arr[k], arr[j] = arr[j], arr[k]
            j += 1
        elif arr[k] >= q:
            while arr[g] > q and k < g:
                g -= 1
            arr[k], arr[g] = arr[g], arr[k]
            g -= 1
            if arr[k] < p:
                arr[k], arr[j] = arr[j], arr[k]
                j += 1
        k += 1
    j -= 1
    g += 1
    arr[low], arr[j] = arr[j], arr[low]
    arr[high], arr[g] = arr[g], arr[high]
    return j, g


# ---------------------------------------------------------------
# Merge Sort
# ---------------------------------------------------------------
def merge_sort(arr):
    _merge_sort(arr, 0, len(arr) - 1)


def _merge_sort(arr, l, r):
    if l < r:
        m = l + (r - l) // 2
        _merge_sort(arr, l, m)
        _merge_sort(arr, m + 1, r)
        _merge(arr, l, m, r)


def _merge(arr, l, m, r):
    L = arr[l:m + 1]
    R = arr[m + 1:r + 1]
    n1, n2 = len(L), len(R)
    i = j = 0
    k = l
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1


# ---------------------------------------------------------------
# Heap Sort
# ---------------------------------------------------------------
def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _heapify(arr, i, 0)


def _heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _heapify(arr, n, largest)


# ---------------------------------------------------------------
# Radix Sort (base 10, LSD)
# ---------------------------------------------------------------
def radix_sort(arr):
    n = len(arr)
    if n == 0:
        return
    maximo = max(arr)
    exp = 1
    while maximo // exp > 0:
        _count_sort(arr, n, exp)
        exp *= 10


def _count_sort(arr, n, exp):
    output = [0] * n
    count = [0] * 10
    for i in range(n):
        count[(arr[i] // exp) % 10] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    for i in range(n - 1, -1, -1):
        d = (arr[i] // exp) % 10
        output[count[d] - 1] = arr[i]
        count[d] -= 1
    arr[:] = output


# ---------------------------------------------------------------
# Bucket Sort
# Cubetas: n (una por elemento).
# Asignacion: indice = (valor - 10.000.000) * n // 90.000.000
# Cada cubeta se ordena con Insertion Sort (como en GeeksforGeeks).
# ---------------------------------------------------------------
def bucket_sort(arr):
    n = len(arr)
    if n <= 1:
        return
    cubetas = [[] for _ in range(n)]
    for v in arr:
        cubetas[(v - MINIMO) * n // RANGO].append(v)
    pos = 0
    for c in cubetas:
        for i in range(1, len(c)):
            key = c[i]
            j = i - 1
            while j >= 0 and c[j] > key:
                c[j + 1] = c[j]
                j -= 1
            c[j + 1] = key
        for v in c:
            arr[pos] = v
            pos += 1
