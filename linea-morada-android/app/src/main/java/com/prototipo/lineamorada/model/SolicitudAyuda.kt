package com.prototipo.lineamorada.model

/**
 * MODELO — Solicitud de ayuda o reporte enviado a la Línea Morada.
 *
 * Es inmutable: para cambiar el estado se usa `copy(estado = ...)`, lo que hace
 * predecibles las pruebas y evita modificar por accidente un objeto compartido.
 *
 * No tiene dependencias de Android, así que se prueba en la JVM sin emulador.
 *
 * Privacidad: `descripcion` y `ubicacionAproximada` son datos sensibles.
 * No se deben escribir en Logcat ni en analítica.
 *
 * @property id Identificador único (UUID en el prototipo).
 * @property tipoApoyo Servicio solicitado (legal, psicológico, emergencia...).
 * @property tipoViolencia Tipo de violencia reportada.
 * @property descripcion Relato breve, ya validado y sin espacios sobrantes.
 * @property ubicacionAproximada Municipio/barrio que escribe la persona; vacío si no quiso darlo.
 * @property marcaTiempo Momento de creación, en milisegundos desde epoch (UTC).
 * @property estado Estado actual de la atención.
 */
data class SolicitudAyuda(
    val id: String,
    val tipoApoyo: TipoApoyo,
    val tipoViolencia: TipoViolencia,
    val descripcion: String,
    val ubicacionAproximada: String,
    val marcaTiempo: Long,
    val estado: EstadoReporte = EstadoReporte.PENDIENTE,
)
