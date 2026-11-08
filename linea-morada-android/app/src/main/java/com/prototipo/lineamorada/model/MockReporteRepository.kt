package com.prototipo.lineamorada.model

/**
 * MODELO — Repositorio simulado que guarda los reportes en memoria.
 *
 * - No necesita base de datos: los datos se pierden al cerrar el proceso.
 * - Es seguro entre hilos (`synchronized`), por si después se llama desde corrutinas.
 * - Acepta datos iniciales para preparar escenarios de QA.
 *
 * PRUEBA UNITARIA (MockReporteRepositoryTest): guardar, listar, buscar,
 * id duplicado y actualizar un id inexistente. No necesita emulador.
 */
class MockReporteRepository(
    datosIniciales: List<SolicitudAyuda> = emptyList(),
) : ReporteRepository {

    // LinkedHashMap conserva el orden de inserción y busca por id en O(1).
    private val reportes = LinkedHashMap<String, SolicitudAyuda>()
    private val lock = Any()

    init {
        datosIniciales.forEach { reportes[it.id] = it }
    }

    override fun guardar(reporte: SolicitudAyuda): Result<SolicitudAyuda> = synchronized(lock) {
        if (reportes.containsKey(reporte.id)) {
            Result.failure(IllegalStateException("Ya existe un reporte con id ${reporte.id}"))
        } else {
            reportes[reporte.id] = reporte
            Result.success(reporte)
        }
    }

    // Devuelve una copia para que nadie modifique la lista interna desde afuera.
    override fun listar(): List<SolicitudAyuda> = synchronized(lock) {
        reportes.values.toList()
    }

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
        Result.success(actualizado)
    }

    /** Solo para pruebas: deja el repositorio vacío entre casos. */
    fun limpiar() = synchronized(lock) { reportes.clear() }
}
