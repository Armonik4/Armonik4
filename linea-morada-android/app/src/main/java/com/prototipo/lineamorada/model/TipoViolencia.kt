package com.prototipo.lineamorada.model

/**
 * MODELO — Tipos de violencia contra la mujer.
 *
 * Basado en las categorías de la Ley 1257 de 2008 (física, psicológica, sexual,
 * económica y patrimonial). Validar con el equipo jurídico antes de producción.
 */
enum class TipoViolencia(val etiqueta: String) {
    FISICA("Física"),
    PSICOLOGICA("Psicológica"),
    SEXUAL("Sexual"),
    ECONOMICA("Económica"),
    PATRIMONIAL("Patrimonial"),
    OTRA("Otra / no estoy segura"),
}
