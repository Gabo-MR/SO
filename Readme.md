Practica 1: Hilos en Python
1. Interpretacion de cada trabajador
Los cuatro trabajadores son hilos que se ejecutan concurrentemente dentro de un mismo programa. Todos comparten una cola de 24 documentos y retiran los trabajos disponibles para procesarlos.
Trabajador 1:
Retira documentos de la cola compartida utilizando get_nowait(). Simula el procesamiento mediante time.sleep(tamaño * 0.1) y actualiza su contador y tamaño acumulado dentro de with lock:.
Trabajador 2:
Ejecuta el mismo procedimiento concurrentemente con los demas trabajadores. Retira documentos disponibles, simula su procesamiento y registra los resultados correspondientes.
Trabajador 3:
Participa en el procesamiento de los documentos utilizando la misma cola compartida. Cuenta los documentos completados y acumula sus tamaños, protegiendo las actualizaciones mediante Lock.
Trabajador 4:
Retira y procesa los documentos disponibles de la cola. Cuando intenta obtener un nuevo documento y la cola esta vacia, captura la excepcion queue.Empty y finaliza su ejecucion de manera controlada.

**Nota: Los cuatro trabajadores realizan la misma funcion. La cantidad de documentos que procesa cada uno puede variar segun la ejecucion concurrente. Entre todos deben completar los 24 documentos exactamente una vez.**

2. Respuestas a las preguntas de la practica
1. ¿Por que queue.Queue es apropiada para compartir trabajos?
Porque permite compartir documentos entre varios hilos de manera segura. Cada trabajador puede retirar documentos de una misma cola sin que dos trabajadores obtengan simultaneamente el mismo elemento. Ademas, permite controlar cuando la cola esta vacia mediante la excepcion queue.Empty.
2. ¿Que protege Lock y que pasaria si se actualizara el resumen sin el?
Lock protege el acceso al registro compartido de resultados, evitando que varios hilos modifiquen simultaneamente los datos de la seccion critica.
Si se actualizara el resumen sin utilizarlo, podrian producirse condiciones de carrera, ocasionando inconsistencias o perdida de actualizaciones en los resultados.
3. ¿Que cambiarias si cada documento tuviera que guardarse en un archivo real?
Se reemplazaria la simulacion por operaciones reales de lectura, clasificacion y escritura de archivos, utilizando funciones como open() de Python. Tambien se implementaria un manejo de excepciones para controlar posibles errores durante estas operaciones, manteniendo la cola compartida y los mecanismos de sincronizacion.