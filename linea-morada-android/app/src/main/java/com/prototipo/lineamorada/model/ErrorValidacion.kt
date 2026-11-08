package com.prototipo.lineamorada.model

/**
 * MODELO — Errores de validación del formulario.
 *
 * El Controlador decide QUÉ está mal; la Vista decide CÓMO mostrarlo (traduce
 * cada error a un string de recursos). Así no hay textos de UI en el Controlador.
 */
sealed interface ErrorValidacion {
    data object TipoApoyoNoSeleccionado : ErrorValidacion
    data object TipoViolenciaNoSeleccionado : ErrorValidacion
    data class DescripcionMuyCorta(val minimo: Int) : ErrorValidacion
    data class DescripcionMuyLarga(val maximo: Int) : ErrorValidacion
    data class UbicacionMuyLarga(val maximo: Int) : ErrorValidacion
}
