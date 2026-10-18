import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/**
 * Medicion oficial de las busquedas en Java (Punto 2).
 *
 * Uso (desde la raiz del repositorio):
 *   javac -d out java/src/*.java
 *   java -Xmx2g -cp out MedirBusquedas 1000 10000     (prueba)
 *   java -Xmx2g -cp out MedirBusquedas                (todos los tamanos)
 *
 * Experimento 1 (variante "claves"): para cada n, se buscan las 1000 claves de
 *   datos/claves_busqueda.txt (500 presentes y 500 ausentes) en el arreglo ascendente.
 * Experimento 2 (variantes "inicio", "centro" y "final"): con el tamano mas grande,
 *   se busca 1000 veces una clave ubicada al inicio, en el centro y al final.
 *
 * En ambos: calentamiento (20 pasadas, JIT) + 5 repeticiones. Se mide el tiempo total de las 1000
 * busquedas y se reporta tambien el tiempo promedio por busqueda en nanosegundos.
 * Antes de medir, y fuera del tiempo, se verifica que cada algoritmo responda bien.
 */
public class MedirBusquedas {

    interface Busqueda {
        int buscar(int[] arr, int x);
    }

    static final int REPETICIONES = 5;
    static final String SALIDA = "resultados/busqueda_java.csv";
    static volatile long control; // evita que el JIT elimine las busquedas por no usar su resultado

    public static void main(String[] args) throws Exception {
        int[] tamanos = args.length > 0
                ? Arrays.stream(args).mapToInt(Integer::parseInt).toArray()
                : new int[]{1_000, 10_000, 100_000, 1_000_000};
        int nMayor = Arrays.stream(tamanos).max().getAsInt();

        Map<String, Busqueda> algoritmos = new LinkedHashMap<>();
        algoritmos.put("Lineal", Busquedas::lineal);
        algoritmos.put("Binaria", Busquedas::binaria);
        algoritmos.put("Ternaria", Busquedas::ternaria);
        algoritmos.put("Saltos", Busquedas::saltos);
        algoritmos.put("Interpolacion", Busquedas::interpolacion);
        algoritmos.put("Exponencial", Busquedas::exponencial);

        int[] claves = Utilidades.leerArchivo("datos/claves_busqueda.txt");

        new java.io.File("resultados").mkdirs();
        try (PrintWriter csv = new PrintWriter(new FileWriter(SALIDA))) {
            csv.println("algoritmo,lenguaje,variante,n,t1_ms,t2_ms,t3_ms,t4_ms,t5_ms,promedio_ms,"
                    + "desviacion_ms,promedio_por_busqueda_ns,desviacion_por_busqueda_ns,tipo,observacion");

            for (int n : tamanos) {
                int[] arr = Utilidades.leerArchivo("datos/ascendente_" + n + ".txt");

                // Experimento 1: 1000 claves (500 presentes y 500 ausentes)
                for (Map.Entry<String, Busqueda> e : algoritmos.entrySet()) {
                    verificar(e.getKey(), e.getValue(), arr, claves);
                    medir(csv, e.getKey(), e.getValue(), arr, claves, "claves", n);
                }

                // Experimento 2: posicion de la clave (solo con el tamano mas grande)
                if (n == nMayor) {
                    String[] posiciones = {"inicio", "centro", "final"};
                    int[] indices = {0, n / 2, n - 1};
                    for (int p = 0; p < 3; p++) {
                        int[] repetida = new int[1000];
                        Arrays.fill(repetida, arr[indices[p]]);
                        for (Map.Entry<String, Busqueda> e : algoritmos.entrySet()) {
                            verificar(e.getKey(), e.getValue(), arr, repetida);
                            medir(csv, e.getKey(), e.getValue(), arr, repetida, posiciones[p], n);
                        }
                    }
                }
            }
        }
        System.out.println("\nResultados guardados en " + SALIDA + "  (control " + control + ")");
    }

    /** Comprueba, fuera del tiempo medido, que el algoritmo encuentre las presentes y no las ausentes. */
    static void verificar(String nombre, Busqueda b, int[] arr, int[] claves) {
        for (int k : claves) {
            boolean presente = Arrays.binarySearch(arr, k) >= 0;
            int r = b.buscar(arr, k);
            boolean ok = presente ? (r >= 0 && arr[r] == k) : r == -1;
            if (!ok) throw new IllegalStateException(nombre + " respondio mal para la clave " + k);
        }
    }

    static void medir(PrintWriter csv, String nombre, Busqueda b, int[] arr, int[] claves,
                      String variante, int n) {
        // Calentamiento: 20 pasadas de las 1000 busquedas (20.000 llamadas), para que el JIT
        // alcance a compilar el metodo por completo antes de medir. No se incluye en el promedio.
        for (int c = 0; c < 20; c++) {
            long s = 0;
            for (int k : claves) s += b.buscar(arr, k);
            control += s;
        }

        double[] t = new double[REPETICIONES];
        for (int r = 0; r < REPETICIONES; r++) {
            long suma = 0;
            long t0 = System.nanoTime();
            for (int k : claves) suma += b.buscar(arr, k);
            long t1 = System.nanoTime();
            control += suma;
            t[r] = (t1 - t0) / 1e6;
        }
        double prom = 0;
        for (double x : t) prom += x;
        prom /= REPETICIONES;
        double desv = 0;
        for (double x : t) desv += (x - prom) * (x - prom);
        desv = Math.sqrt(desv / (REPETICIONES - 1));

        double porBusquedaNs = prom * 1e6 / claves.length;
        double desvPorBusquedaNs = desv * 1e6 / claves.length;

        StringBuilder sb = new StringBuilder();
        sb.append(nombre).append(",Java,").append(variante).append(',').append(n);
        for (double x : t) sb.append(',').append(String.format(Locale.US, "%.4f", x));
        sb.append(String.format(Locale.US, ",%.4f,%.4f,%.2f,%.2f,medido,",
                prom, desv, porBusquedaNs, desvPorBusquedaNs));
        csv.println(sb);
        csv.flush();
        System.out.printf("%-14s %-8s n=%,9d  %14.2f ns por busqueda%n", nombre, variante, n, porBusquedaNs);
    }
}
