import threading
import queue
import time
import random
CANTIDAD_DOCUMENTOS = 24
CANTIDAD_TRABAJADORES = 4
def crear_documentos():
    """Genera 24 documentos simulados como (identificador, tamaño)."""
    return [
        (doc_id, random.randint(1, 5))
        for doc_id in range(1, CANTIDAD_DOCUMENTOS + 1)
    ]
def procesamiento_secuencial(documentos):
    """Procesa los mismos documentos uno por uno y mide el tiempo."""
    inicio = time.perf_counter()
    for doc_id, tamaño in documentos:
        time.sleep(tamaño * 0.1)
    return time.perf_counter() - inicio
def trabajador(nombre, trabajos, resultados, asignaciones, lock):
    """Retira y procesa trabajos hasta que la cola este vacia."""
    while True:
        try:
            doc_id, tamaño = trabajos.get_nowait()
        except queue.Empty:
            break
        try:
            print(f"{nombre} procesa Documento {doc_id:02d} (tamaño {tamaño})")
            time.sleep(tamaño * 0.1)
            print(f"{nombre} termino Documento {doc_id:02d}")
            # Seccion critica: proteger todos los registros compartidos.
            with lock:
                resultados[nombre]["cantidad"] += 1
                resultados[nombre]["tamaño_total"] += tamaño
                resultados[nombre]["documentos"].append(doc_id)
                asignaciones.append((doc_id, tamaño, nombre))
        finally:
            trabajos.task_done()
def main():
    documentos = crear_documentos()
    print("========== DOCUMENTOS RECIBIDOS ==========")
    for doc_id, tamaño in documentos:
        print(f"Documento {doc_id:02d} - tamaño simulado: {tamaño}")
    # Reto adicional: version secuencial con los mismos documentos.
    tiempo_secuencial = procesamiento_secuencial(documentos)
    trabajos = queue.Queue()
    for documento in documentos:
        trabajos.put(documento)
    resultados = {
        f"Trabajador-{i}": {
            "cantidad": 0, "tamaño_total": 0, "documentos": []
        }
        for i in range(1, CANTIDAD_TRABAJADORES + 1)
    }
    asignaciones = []
    lock = threading.Lock()
    hilos = []
    print("\n========== EJECUCION CON CUATRO HILOS ==========")
    inicio = time.perf_counter()
    for i in range(1, CANTIDAD_TRABAJADORES + 1):
        nombre = f"Trabajador-{i}"
        hilo = threading.Thread(
            target=trabajador,
            args=(nombre, trabajos, resultados, asignaciones, lock)
        )
        hilos.append(hilo)
        hilo.start()
    for hilo in hilos:
        hilo.join()
    tiempo_concurrente = time.perf_counter() - inicio
    print("\n========== ASIGNACION DE LOS 24 DOCUMENTOS ==========")
    for doc_id, tamaño, nombre in sorted(asignaciones):
        print(f"Documento {doc_id:02d} | Tamaño: {tamaño} | Asignado a: {nombre}")
    print("\n========== RESUMEN POR TRABAJADOR ==========")
    for nombre in sorted(resultados):
        datos = resultados[nombre]
        print(f"{nombre}: {datos['cantidad']} documentos | "
              f"Tamaño acumulado: {datos['tamaño_total']} | "
              f"IDs: {sorted(datos['documentos'])}")
    total = sum(d["cantidad"] for d in resultados.values())
    tamaño_total = sum(d["tamaño_total"] for d in resultados.values())
    ids = [doc_id for doc_id, _, _ in asignaciones]
    print("\n========== VERIFICACIONES ==========")
    v1 = total == CANTIDAD_DOCUMENTOS
    v2 = (len(ids) == CANTIDAD_DOCUMENTOS
          and len(set(ids)) == CANTIDAD_DOCUMENTOS
          and set(ids) == set(range(1, CANTIDAD_DOCUMENTOS + 1)))
    v3 = all(not hilo.is_alive() for hilo in hilos)
    v4 = tamaño_total == sum(t for _, t in documentos)
    print(f"1. Total procesado = {total}: {'CORRECTO' if v1 else 'ERROR'}")
    print(f"2. IDs unicos del 1 al 24: {'CORRECTO' if v2 else 'ERROR'}")
    print(f"3. Los cuatro hilos finalizaron: {'CORRECTO' if v3 else 'ERROR'}")
    print(f"4. Suma de tamaños correcta: {'CORRECTO' if v4 else 'ERROR'}")
    print("\n========== RESULTADO GENERAL ==========")
    print(f"TOTAL DE DOCUMENTOS PROCESADOS: {total}")
    print(f"TAMAÑO TOTAL PROCESADO: {tamaño_total}")
    print(f"Tiempo secuencial: {tiempo_secuencial:.4f} segundos")
    print(f"Tiempo con cuatro hilos: {tiempo_concurrente:.4f} segundos")

    assert v1 and v2 and v3 and v4, "Fallo una verificacion."
    print("\nTODAS LAS VERIFICACIONES FUERON EXITOSAS.")
if __name__ == "__main__":
    main()