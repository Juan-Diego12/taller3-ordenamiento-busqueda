import java.util.ArrayList;

/**
 * Algoritmos de ordenamiento del Taller 3.
 * Implementaciones basadas en GeeksforGeeks (ver README para las fuentes).
 * Todos ordenan el arreglo recibido en forma ascendente.
 */
public class Ordenamientos {

    static final int MINIMO = 10_000_000;
    static final long RANGO = 90_000_000L; // valores entre 10.000.000 y 99.999.999

    // ---------------------------------------------------------------
    // Insertion Sort
    // ---------------------------------------------------------------
    public static void insertionSort(int[] arr) {
        int n = arr.length;
        for (int i = 1; i < n; i++) {
            int key = arr[i];
            int j = i - 1;
            while (j >= 0 && arr[j] > key) {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = key;
        }
    }

    // ---------------------------------------------------------------
    // Dual-Pivot QuickSort (pivotes: primer y ultimo elemento)
    // ---------------------------------------------------------------
    public static void dualPivotQuickSort(int[] arr) {
        dualPivotQuickSort(arr, 0, arr.length - 1);
    }

    private static void dualPivotQuickSort(int[] arr, int low, int high) {
        if (low < high) {
            int[] piv = partition(arr, low, high);
            dualPivotQuickSort(arr, low, piv[0] - 1);
            dualPivotQuickSort(arr, piv[0] + 1, piv[1] - 1);
            dualPivotQuickSort(arr, piv[1] + 1, high);
        }
    }

    private static int[] partition(int[] arr, int low, int high) {
        if (arr[low] > arr[high]) swap(arr, low, high);
        int j = low + 1;
        int g = high - 1, k = low + 1;
        int p = arr[low], q = arr[high];
        while (k <= g) {
            if (arr[k] < p) {
                swap(arr, k, j);
                j++;
            } else if (arr[k] >= q) {
                while (arr[g] > q && k < g) g--;
                swap(arr, k, g);
                g--;
                if (arr[k] < p) {
                    swap(arr, k, j);
                    j++;
                }
            }
            k++;
        }
        j--;
        g++;
        swap(arr, low, j);
        swap(arr, high, g);
        return new int[]{j, g};
    }

    // ---------------------------------------------------------------
    // Merge Sort
    // ---------------------------------------------------------------
    public static void mergeSort(int[] arr) {
        mergeSort(arr, 0, arr.length - 1);
    }

    private static void mergeSort(int[] arr, int l, int r) {
        if (l < r) {
            int m = l + (r - l) / 2;
            mergeSort(arr, l, m);
            mergeSort(arr, m + 1, r);
            merge(arr, l, m, r);
        }
    }

    private static void merge(int[] arr, int l, int m, int r) {
        int n1 = m - l + 1;
        int n2 = r - m;
        int[] L = new int[n1];
        int[] R = new int[n2];
        for (int i = 0; i < n1; i++) L[i] = arr[l + i];
        for (int j = 0; j < n2; j++) R[j] = arr[m + 1 + j];
        int i = 0, j = 0, k = l;
        while (i < n1 && j < n2) {
            if (L[i] <= R[j]) arr[k++] = L[i++];
            else arr[k++] = R[j++];
        }
        while (i < n1) arr[k++] = L[i++];
        while (j < n2) arr[k++] = R[j++];
    }

    // ---------------------------------------------------------------
    // Heap Sort
    // ---------------------------------------------------------------
    public static void heapSort(int[] arr) {
        int n = arr.length;
        for (int i = n / 2 - 1; i >= 0; i--) heapify(arr, n, i);
        for (int i = n - 1; i > 0; i--) {
            swap(arr, 0, i);
            heapify(arr, i, 0);
        }
    }

    private static void heapify(int[] arr, int n, int i) {
        int largest = i;
        int l = 2 * i + 1;
        int r = 2 * i + 2;
        if (l < n && arr[l] > arr[largest]) largest = l;
        if (r < n && arr[r] > arr[largest]) largest = r;
        if (largest != i) {
            swap(arr, i, largest);
            heapify(arr, n, largest);
        }
    }

    // ---------------------------------------------------------------
    // Radix Sort (base 10, LSD)
    // ---------------------------------------------------------------
    public static void radixSort(int[] arr) {
        int n = arr.length;
        if (n == 0) return;
        int max = arr[0];
        for (int v : arr) if (v > max) max = v;
        for (int exp = 1; max / exp > 0; exp *= 10) countSort(arr, n, exp);
    }

    private static void countSort(int[] arr, int n, int exp) {
        int[] output = new int[n];
        int[] count = new int[10];
        for (int i = 0; i < n; i++) count[(arr[i] / exp) % 10]++;
        for (int i = 1; i < 10; i++) count[i] += count[i - 1];
        for (int i = n - 1; i >= 0; i--) {
            int d = (arr[i] / exp) % 10;
            output[count[d] - 1] = arr[i];
            count[d]--;
        }
        System.arraycopy(output, 0, arr, 0, n);
    }

    // ---------------------------------------------------------------
    // Bucket Sort
    // Cubetas: n (una por elemento).
    // Asignacion: indice = (valor - 10.000.000) * n / 90.000.000
    // Cada cubeta se ordena con Insertion Sort (como en GeeksforGeeks).
    // ---------------------------------------------------------------
    public static void bucketSort(int[] arr) {
        int n = arr.length;
        if (n <= 1) return;

        @SuppressWarnings("unchecked")
        ArrayList<Integer>[] cubetas = new ArrayList[n];
        for (int i = 0; i < n; i++) cubetas[i] = new ArrayList<>();

        for (int v : arr) {
            int indice = (int) ((long) (v - MINIMO) * n / RANGO);
            cubetas[indice].add(v);
        }

        int pos = 0;
        for (ArrayList<Integer> c : cubetas) {
            for (int i = 1; i < c.size(); i++) {
                int key = c.get(i);
                int j = i - 1;
                while (j >= 0 && c.get(j) > key) {
                    c.set(j + 1, c.get(j));
                    j--;
                }
                c.set(j + 1, key);
            }
            for (int v : c) arr[pos++] = v;
        }
    }

    // ---------------------------------------------------------------
    private static void swap(int[] arr, int i, int j) {
        int t = arr[i];
        arr[i] = arr[j];
        arr[j] = t;
    }
}
