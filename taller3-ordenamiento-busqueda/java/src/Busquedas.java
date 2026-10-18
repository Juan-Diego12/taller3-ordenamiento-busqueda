/**
 * Algoritmos de busqueda del Taller 3.
 * Implementaciones basadas en GeeksforGeeks (ver README para las fuentes).
 * Todos reciben un arreglo ordenado ascendentemente y retornan el indice de x, o -1 si no esta.
 */
public class Busquedas {

    // ---------------------------------------------------------------
    // Busqueda Lineal (referencia)
    // ---------------------------------------------------------------
    public static int lineal(int[] arr, int x) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == x) return i;
        }
        return -1;
    }

    // ---------------------------------------------------------------
    // Busqueda Binaria (iterativa)
    // ---------------------------------------------------------------
    public static int binaria(int[] arr, int x) {
        return binaria(arr, 0, arr.length - 1, x);
    }

    static int binaria(int[] arr, int l, int r, int x) {
        while (l <= r) {
            int m = l + (r - l) / 2;
            if (arr[m] == x) return m;
            if (arr[m] < x) l = m + 1;
            else r = m - 1;
        }
        return -1;
    }

    // ---------------------------------------------------------------
    // Busqueda Ternaria (iterativa)
    // ---------------------------------------------------------------
    public static int ternaria(int[] arr, int x) {
        int l = 0, r = arr.length - 1;
        while (r >= l) {
            int mid1 = l + (r - l) / 3;
            int mid2 = r - (r - l) / 3;
            if (arr[mid1] == x) return mid1;
            if (arr[mid2] == x) return mid2;
            if (x < arr[mid1]) {
                r = mid1 - 1;
            } else if (x > arr[mid2]) {
                l = mid2 + 1;
            } else {
                l = mid1 + 1;
                r = mid2 - 1;
            }
        }
        return -1;
    }

    // ---------------------------------------------------------------
    // Busqueda por Saltos (Jump Search), salto = raiz de n
    // ---------------------------------------------------------------
    public static int saltos(int[] arr, int x) {
        int n = arr.length;
        if (n == 0) return -1;
        int salto = (int) Math.floor(Math.sqrt(n));
        int paso = salto;
        int prev = 0;
        while (arr[Math.min(paso, n) - 1] < x) {
            prev = paso;
            paso += salto;
            if (prev >= n) return -1;
        }
        while (arr[prev] < x) {
            prev++;
            if (prev == Math.min(paso, n)) return -1;
        }
        if (arr[prev] == x) return prev;
        return -1;
    }

    // ---------------------------------------------------------------
    // Busqueda por Interpolacion (iterativa)
    // ---------------------------------------------------------------
    public static int interpolacion(int[] arr, int x) {
        int lo = 0, hi = arr.length - 1;
        while (lo <= hi && x >= arr[lo] && x <= arr[hi]) {
            if (arr[hi] == arr[lo]) {          // evita division entre cero si hay valores repetidos
                return arr[lo] == x ? lo : -1;
            }
            int pos = lo + (int) ((long) (x - arr[lo]) * (hi - lo) / (arr[hi] - arr[lo]));
            if (arr[pos] == x) return pos;
            if (arr[pos] < x) lo = pos + 1;
            else hi = pos - 1;
        }
        return -1;
    }

    // ---------------------------------------------------------------
    // Busqueda Exponencial
    // ---------------------------------------------------------------
    public static int exponencial(int[] arr, int x) {
        int n = arr.length;
        if (n == 0) return -1;
        if (arr[0] == x) return 0;
        int i = 1;
        while (i < n && arr[i] <= x) i *= 2;
        return binaria(arr, i / 2, Math.min(i, n - 1), x);
    }
}
