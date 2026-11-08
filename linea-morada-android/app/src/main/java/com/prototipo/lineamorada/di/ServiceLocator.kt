package com.prototipo.lineamorada.di

import com.prototipo.lineamorada.model.MockReporteRepository
import com.prototipo.lineamorada.model.ReporteRepository
import com.prototipo.lineamorada.model.SolicitudAyuda
import com.prototipo.lineamorada.model.TipoApoyo
import com.prototipo.lineamorada.model.TipoViolencia

/**
 * Inyección de dependencias manual, mínima.
 *
 * El repositorio vive mientras viva el proceso, así que los reportes no se
 * pierden al rotar la pantalla (la Activity se recrea, el repositorio no).
 *
 * PRUEBA DE UI: en un test instrumentado se puede reemplazar `reporteRepository`
 * por un MockReporteRepository con datos iniciales antes de abrir la Activity.
 * Mejora futura: cambiar esto por Hilt o Koin cuando crezca el proyecto.
 */
object ServiceLocator {

    /**
     * PRUEBA DE RENDIMIENTO con el Profiler: cambia este valor (por ejemplo a
     * 10_000) para que la app arranque con muchos reportes falsos y se note el
     * costo del historial. Debe quedar en 0 en uso normal.
     */
    private const val REPORTES_DE_PRUEBA = 0

    @Volatile
    var reporteRepository: ReporteRepository = MockReporteRepository(reportesDePrueba(REPORTES_DE_PRUEBA))

    private fun reportesDePrueba(cantidad: Int) = List(cantidad) { i ->
        SolicitudAyuda(
            id = "prueba-$i",
            tipoApoyo = TipoApoyo.entries[i % TipoApoyo.entries.size],
            tipoViolencia = TipoViolencia.entries[i % TipoViolencia.entries.size],
            descripcion = "Reporte de prueba número $i",
            ubicacionAproximada = "Bogotá",
            marcaTiempo = i * 60_000L,
        )
    }
}
