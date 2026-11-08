package com.prototipo.lineamorada.di

import com.prototipo.lineamorada.model.MockReporteRepository
import com.prototipo.lineamorada.model.ReporteRepository

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
    @Volatile
    var reporteRepository: ReporteRepository = MockReporteRepository()
}
