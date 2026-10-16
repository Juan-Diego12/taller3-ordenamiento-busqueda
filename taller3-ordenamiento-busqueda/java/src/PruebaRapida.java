import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.function.Consumer;

/**
 * Prueba rapida del viernes: ejecuta cada algoritmo UNA vez por variante y verifica el resultado.
 * NO es la medicion oficial (esa tiene calentamiento, 5 repeticiones y CSV).
 *
 * Uso (desde la raiz del repositorio):
 *   javac -d out java/src/*.java
 *   java -cp out PruebaRapida 1000
 */
public class PruebaRapida {

    public static void main(String[] args) throws Exception {
        int n = args.length > 0 ? Integer.parseInt(args[0]) : 1000;
        String[] variantes = {"aleatorio", "ascendente", "descendente"};

        Map<String, Consumer<int[]>> algoritmos = new LinkedHashMap<>();
        algoritmos.put("InsertionSort", Ordenamientos::insertionSort);
        algoritmos.put("DualPivotQuickSort", Ordenamientos::dualPivotQuickSort);
        algoritmos.put("MergeSort", Ordenamientos::mergeSort);
        algoritmos.put("HeapSort", Ordenamientos::heapSort);
        algoritmos.put("RadixSort", Ordenamientos::radixSort);
        algoritmos.put("BucketSort", Ordenamientos::bucketSort);

        boolean todoBien = true;
        for (String variante : variantes) {
            int[] original = Utilidades.leerArchivo("datos/" + variante + "_" + n + ".txt");
            int[] esperado = Utilidades.copiar(original);
            Arrays.sort(esperado);

            System.out.println("\n== n = " + n + ", variante = " + variante + " ==");
            for (Map.Entry<String, Consumer<int[]>> e : algoritmos.entrySet()) {
                int[] copia = Utilidades.copiar(original);
                try {
                    long ini = System.nanoTime();
                    e.getValue().accept(copia);
                    long fin = System.nanoTime();
                    boolean ok = Utilidades.verificar(copia, esperado);
                    todoBien &= ok;
                    System.out.printf("%-20s %12.3f ms   %s%n",
                            e.getKey(), (fin - ini) / 1e6, ok ? "OK" : "ERROR: mal ordenado");
                } catch (StackOverflowError err) {
                    todoBien = false;
                    System.out.printf("%-20s StackOverflowError (documentar)%n", e.getKey());
                }
            }
        }
        System.out.println(todoBien ? "\nTodos los algoritmos ordenaron correctamente."
                                    : "\nHay algoritmos con errores: revisar.");
    }
}
