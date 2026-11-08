package com.prototipo.lineamorada.model

import java.util.TreeSet

/**
 * MODELO — Repositorio simulado que guarda los reportes en memoria.
 *
 * - No necesita base de datos: los datos se pierden al cerrar el proceso.
 * - Es seguro entre hilos (`synchronized`), por si después se llama desde corrutinas.
 * - Acepta datos iniciales para preparar escenarios de QA.
 *
 * Rendimiento: además del mapa por id, mantiene un índice ya ordenado del más
 * reciente al más antiguo. Así `listarRecientes()` entrega una página sin copiar
 * ni ordenar toda la colección en cada envío (ver docs/rendimiento-historial.md).
 *
 * PRUEBA UNITARIA (MockReporteRepositoryTest): guardar, listar, paginar, buscar,
 * id duplicado y actualizar un id inexistente. No necesita emulador.
 */
class MockReporteRepository(
    datosIniciales: List<SolicitudAyuda> = emptyList(),
) : ReporteRepository {

    // LinkedHashMap conserva el orden de inserción y busca por id en O(1).
    private val reportes = LinkedHashMap<String, SolicitudAyuda>()

    // Índice ordenado por fecha (más reciente primero); el id desempata.
    // Insertar cuesta O(log n) y leer una página cuesta O(desde + cantidad).
    private val porFecha = TreeSet(
        compareByDescending<SolicitudAyuda> { it.marcaTiempo }.thenBy { it.id },
    )
    private val lock = Any()

    init {
        datosIniciales.forEach { if (reportes.putIfAbsent(it.id, it) == null) porFecha.add(it) }
    }

    override fun guardar(reporte: SolicitudAyuda): Result<SolicitudAyuda> = synchronized(lock) {
        if (reportes.containsKey(reporte.id)) {
            Result.failure(IllegalStateException("Ya existe un reporte con id ${reporte.id}"))
        } else {
            reportes[reporte.id] = reporte
            porFecha.add(reporte)
            Result.success(reporte)
        }
    }

    // Devuelve una copia para que nadie modifique la lista interna desde afuera.
    override fun listar(): List<SolicitudAyuda> = synchronized(lock) {
        reportes.values.toList()
    }

    override fun listarRecientes(desde: Int, cantidad: Int): List<SolicitudAyuda> = synchronized(lock) {
        if (desde < 0 || cantidad <= 0) return@synchronized emptyList()
        porFecha.asSequence().drop(desde).take(cantidad).toList()
    }

    override fun contar(): Int = synchronized(lock) { reportes.size }

    override fun buscarPorId(id: String): SolicitudAyuda? = synchronized(lock) {
        reportes[id]
    }

    override fun actualizarEstado(
        id: String,
        nuevoEstado: EstadoReporte,
    ): Result<SolicitudAyuda> = synchronized(lock) {
        val actual = reportes[id]
            ?: return@synchronized Result.failure(NoSuchElementException("No existe el reporte $id"))
        val actualizado = actual.copy(estado = nuevoEstado)
        reportes[id] = actualizado
        // Fecha e id no cambian, así que ocupa la misma posición en el índice.
        porFecha.remove(actual)
        porFecha.add(actualizado)
        Result.success(actualizado)
    }

    /** Solo para pruebas: deja el repositorio vacío entre casos. */
    fun limpiar() = synchronized(lock) {
        reportes.clear()
        porFecha.clear()
    }
}
