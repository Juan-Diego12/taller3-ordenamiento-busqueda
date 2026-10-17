import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Set;
import java.util.function.Consumer;

/**
 * Medicion oficial de los ordenamientos en Java (Punto 1).
 *
 * Uso (desde la raiz del repositorio):
 *   javac -d out java/src/*.java
 *   java -Xmx2g -cp out MedirOrdenamientos 1000 10000     (prueba)
 *   java -Xmx2g -cp out MedirOrdenamientos                (todos los tamanos)
 *
 * Por cada algoritmo, variante y tamano:
 *   - Carga los datos ANTES de medir.
 *   - Hace 1 ejecucion de calentamiento (JIT) que no se cuenta.
 *   - Hace 5 repeticiones, cada una sobre una copia nueva (la copia no se mide).
 *   - Verifica el resultado fuera del tiempo medido.
 *   - Escribe una fila en resultados/ordenamiento_java.csv apenas termina.
 *
 * Casos que no se ejecutan (ver README, seccion "Estimaciones"):
 *   - Si la prediccion para el nuevo tamano supera 5 minutos, se marca como estimado.
 *   - Si ocurre StackOverflowError, se documenta y se estima.
 */
public class MedirOrdenamientos {

    static final double LIMITE_MS = 300_000; // 5 minutos por ejecucion
    static final int REPETICIONES = 5;
    static final String[] VARIANTES = {"aleatorio", "ascendente", "descendente"};
    static final String SALIDA = "resultados/ordenamiento_java.csv";

    public static void main(String[] args) throws Exception {
        int[] tamanos = args.length > 0
                ? Arrays.stream(args).mapToInt(Integer::parseInt).toArray()
                : new int[]{1_000, 10_000, 100_000, 1_000_000};

        Map<String, Consumer<int[]>> algoritmos = new LinkedHashMap<>();
        algoritmos.put("InsertionSort", Ordenamientos::insertionSort);
        algoritmos.put("DualPivotQuickSort", Ordenamientos::dualPivotQuickSort);
        algoritmos.put("MergeSort", Ordenamientos::mergeSort);
        algoritmos.put("HeapSort", Ordenamientos::heapSort);
        algoritmos.put("RadixSort", Ordenamientos::radixSort);
        algoritmos.put("BucketSort", Ordenamientos::bucketSort);

        Map<String, Double> ultimoPromedio = new HashMap<>();
        Map<String, Integer> ultimoN = new HashMap<>();
        Set<String> fallaron = new HashSet<>();

        new java.io.File("resultados").mkdirs();
        try (PrintWriter csv = new PrintWriter(new FileWriter(SALIDA))) {
            csv.println("algoritmo,lenguaje,variante,n,t1_ms,t2_ms,t3_ms,t4_ms,t5_ms,"
                    + "promedio_ms,desviacion_ms,tipo,observacion");

            for (int n : tamanos) {
                for (String variante : VARIANTES) {
                    int[] original = Utilidades.leerArchivo("datos/" + variante + "_" + n + ".txt");
                    int[] esperado = Utilidades.copiar(original);
                    Arrays.sort(esperado);

                    for (Map.Entry<String, Consumer<int[]>> e : algoritmos.entrySet()) {
                        String alg = e.getKey();
                        String clave = alg + "|" + variante;
                        Double prev = ultimoPromedio.get(clave);
                        Double est = prev == null ? null
                                : prev * factor(alg, variante, ultimoN.get(clave), n);

                        if (fallaron.contains(clave)) {
                            fila(csv, alg, variante, n, new double[0], est, null, "estimado",
                                    "no se ejecuto: fallo con un n menor (StackOverflowError)");
                            guardar(ultimoPromedio, ultimoN, clave, n, est);
                            System.out.printf("%-20s %-12s n=%,9d  ESTIMADO (fallo previo)%n", alg, variante, n);
                            continue;
                        }

                        if (est != null && est > LIMITE_MS) {
                            fila(csv, alg, variante, n, new double[0], est, null, "estimado",
                                    String.format("no se ejecuto: prediccion %.0f s supera 5 min", est / 1000));
                            guardar(ultimoPromedio, ultimoN, clave, n, est);
                            System.out.printf("%-20s %-12s n=%,9d  ESTIMADO %,.1f s%n", alg, variante, n, est / 1000);
                            continue;
                        }

                        double[] tiempos = new double[REPETICIONES];
                        int hechas = 0;
                        try {
                            e.getValue().accept(Utilidades.copiar(original)); // calentamiento
                            for (int r = 0; r < REPETICIONES; r++) {
                                int[] copia = Utilidades.copiar(original);
                                long t0 = System.nanoTime();
                                e.getValue().accept(copia);
                                long t1 = System.nanoTime();
                                if (!Utilidades.verificar(copia, esperado)) {
                                    throw new IllegalStateException(alg + " no ordeno correctamente");
                                }
                                tiempos[hechas++] = (t1 - t0) / 1e6;
                                if (tiempos[hechas - 1] > LIMITE_MS) break;
                            }
                        } catch (StackOverflowError err) {
                            fallaron.add(clave);
                            fila(csv, alg, variante, n, new double[0], est, null, "estimado",
                                    "StackOverflowError: desbordamiento de la pila de llamadas");
                            guardar(ultimoPromedio, ultimoN, clave, n, est);
                            System.out.printf("%-20s %-12s n=%,9d  StackOverflowError -> estimado%n", alg, variante, n);
                            continue;
                        }

                        double[] t = Arrays.copyOf(tiempos, hechas);
                        double prom = promedio(t);
                        double desv = desviacion(t, prom);
                        if (hechas < REPETICIONES) {
                            fila(csv, alg, variante, n, t, prom, desv, "estimado",
                                    "una repeticion supero 5 min; se detuvo");
                        } else {
                            fila(csv, alg, variante, n, t, prom, desv, "medido", "");
                        }
                        guardar(ultimoPromedio, ultimoN, clave, n, prom);
                        System.out.printf("%-20s %-12s n=%,9d  %12.3f ms  (de %.3f)%n", alg, variante, n, prom, desv);
                    }
                }
            }
        }
        System.out.println("\nResultados guardados en " + SALIDA);
    }

    /** Funcion de crecimiento teorica usada para predecir y estimar. */
    static double complejidad(String alg, String variante, double n) {
        double nlogn = n * Math.log(n);
        switch (alg) {
            case "InsertionSort":
                return variante.equals("ascendente") ? n : n * n;
            case "DualPivotQuickSort":
                return variante.equals("aleatorio") ? nlogn : n * n;
            case "MergeSort":
            case "HeapSort":
                return nlogn;
            default: // RadixSort y BucketSort
                return n;
        }
    }

    static double factor(String alg, String variante, int nPrev, int nNuevo) {
        return complejidad(alg, variante, nNuevo) / complejidad(alg, variante, nPrev);
    }

    static void guardar(Map<String, Double> prom, Map<String, Integer> ns, String clave, int n, Double valor) {
        if (valor != null) {
            prom.put(clave, valor);
            ns.put(clave, n);
        }
    }

    static double promedio(double[] t) {
        double s = 0;
        for (double x : t) s += x;
        return s / t.length;
    }

    /** Desviacion estandar muestral (divide entre n - 1), igual que statistics.stdev de Python. */
    static double desviacion(double[] t, double prom) {
        if (t.length < 2) return 0;
        double s = 0;
        for (double x : t) s += (x - prom) * (x - prom);
        return Math.sqrt(s / (t.length - 1));
    }

    static void fila(PrintWriter csv, String alg, String variante, int n, double[] tiempos,
                     Double prom, Double desv, String tipo, String obs) {
        StringBuilder sb = new StringBuilder();
        sb.append(alg).append(",Java,").append(variante).append(',').append(n);
        for (int i = 0; i < REPETICIONES; i++) {
            sb.append(',');
            if (i < tiempos.length) sb.append(String.format(java.util.Locale.US, "%.4f", tiempos[i]));
        }
        sb.append(',').append(prom == null ? "" : String.format(java.util.Locale.US, "%.4f", prom));
        sb.append(',').append(desv == null ? "" : String.format(java.util.Locale.US, "%.4f", desv));
        sb.append(',').append(tipo).append(',').append(obs);
        csv.println(sb);
        csv.flush();
    }
}
