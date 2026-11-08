package com.prototipo.lineamorada.model

/**
 * MODELO — Contrato de acceso a datos de los reportes.
 *
 * El Controlador depende de esta interfaz, no de una implementación concreta.
 * Así se puede cambiar el mock en memoria por Room, Retrofit o Firebase sin tocar
 * el Controlador ni la Vista.
 *
 * Mejora futura: cuando haya E/S real, convertir estos métodos en `suspend`
 * (o exponer un `Flow<List<SolicitudAyuda>>`) para no bloquear el hilo principal.
 */
interface ReporteRepository {

    /** Guarda un reporte nuevo. Falla si ya existe uno con el mismo id. */
    fun guardar(reporte: SolicitudAyuda): Result<SolicitudAyuda>

    /** Devuelve todos los reportes, en orden de inserción. */
    fun listar(): List<SolicitudAyuda>

    /**
     * Devuelve una página del historial, del más reciente al más antiguo.
     * Pensado para la paginación: no copia ni ordena toda la colección.
     */
    fun listarRecientes(desde: Int, cantidad: Int): List<SolicitudAyuda>

    /** Cantidad total de reportes guardados. */
    fun contar(): Int

    /** Busca un reporte por id; `null` si no existe. */
    fun buscarPorId(id: String): SolicitudAyuda?

    /** Cambia el estado de un reporte. Falla si el id no existe. */
    fun actualizarEstado(id: String, nuevoEstado: EstadoReporte): Result<SolicitudAyuda>
}
