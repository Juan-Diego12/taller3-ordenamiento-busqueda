import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Arrays;

/** Funciones de apoyo: lectura de archivos, copia y verificacion (todo FUERA del tiempo medido). */
public class Utilidades {

    /** Lee un archivo con un entero por linea. */
    public static int[] leerArchivo(String ruta) throws IOException {
        int[] datos = new int[16];
        int n = 0;
        try (BufferedReader br = new BufferedReader(new FileReader(ruta))) {
            String linea;
            while ((linea = br.readLine()) != null) {
                linea = linea.trim();
                if (linea.isEmpty()) continue;
                if (n == datos.length) datos = Arrays.copyOf(datos, n * 2);
                datos[n++] = Integer.parseInt(linea);
            }
        }
        return Arrays.copyOf(datos, n);
    }

    /** Copia nueva del arreglo original para cada repeticion. */
    public static int[] copiar(int[] arr) {
        return Arrays.copyOf(arr, arr.length);
    }

    /** Verifica que el arreglo este en orden ascendente. */
    public static boolean estaOrdenado(int[] arr) {
        for (int i = 1; i < arr.length; i++) {
            if (arr[i - 1] > arr[i]) return false;
        }
        return true;
    }

    /**
     * Verificacion completa: ademas de estar ordenado, debe tener exactamente
     * los mismos elementos que el original (detecta valores perdidos o duplicados por error).
     */
    public static boolean verificar(int[] resultado, int[] esperado) {
        return estaOrdenado(resultado) && Arrays.equals(resultado, esperado);
    }
}
