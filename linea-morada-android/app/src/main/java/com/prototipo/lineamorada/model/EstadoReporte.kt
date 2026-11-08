package com.prototipo.lineamorada.model

/**
 * MODELO — Ciclo de vida de un reporte.
 *
 * PRUEBA UNITARIA: `siguiente()` es una función pura; verificar cada transición
 * y que ATENDIDO sea un estado final (ver MockReporteRepositoryTest).
 */
enum class EstadoReporte(val etiqueta: String) {
    PENDIENTE("Pendiente"),
    EN_ATENCION("En atención"),
    ATENDIDO("Atendido");

    /** Devuelve el estado que sigue; ATENDIDO no avanza más. */
    fun siguiente(): EstadoReporte = when (this) {
        PENDIENTE -> EN_ATENCION
        EN_ATENCION -> ATENDIDO
        ATENDIDO -> ATENDIDO
    }
}
