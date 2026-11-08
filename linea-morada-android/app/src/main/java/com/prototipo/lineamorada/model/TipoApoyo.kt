package com.prototipo.lineamorada.model

/**
 * MODELO — Tipo de apoyo que solicita la persona.
 *
 * `etiqueta` es un dato de dominio (el nombre del servicio), no un texto de UI.
 * Si la app se traduce, conviene moverla a recursos de strings en la Vista.
 */
enum class TipoApoyo(val etiqueta: String) {
    EMERGENCIA("Emergencia / riesgo inmediato"),
    ORIENTACION_LEGAL("Orientación legal"),
    ORIENTACION_PSICOLOGICA("Orientación psicológica"),
    INFORMACION_GENERAL("Información y prevención"),
}
