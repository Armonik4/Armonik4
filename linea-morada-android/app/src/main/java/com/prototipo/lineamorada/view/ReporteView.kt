package com.prototipo.lineamorada.view

import com.prototipo.lineamorada.model.ErrorValidacion
import com.prototipo.lineamorada.model.SolicitudAyuda

/**
 * VISTA — Contrato entre el Controlador y la pantalla.
 *
 * El Controlador solo conoce esta interfaz, nunca `MainActivity` directamente.
 * Por eso:
 *  - El Controlador no importa nada de Android y se prueba en la JVM.
 *  - En las pruebas unitarias se usa una vista falsa (FakeReporteView) que
 *    registra lo que el Controlador le pidió mostrar.
 *
 * Convención de los Spinners: la posición 0 es siempre el texto guía
 * ("Selecciona…"); las opciones reales empiezan en la posición 1.
 */
interface ReporteView {
    fun mostrarTiposDeApoyo(opciones: List<String>)
    fun mostrarTiposDeViolencia(opciones: List<String>)
    fun mostrarHistorial(reportes: List<SolicitudAyuda>)
    fun mostrarErroresValidacion(errores: List<ErrorValidacion>)
    fun limpiarErrores()
    fun limpiarFormulario()
    fun mostrarConfirmacion(reporte: SolicitudAyuda)
    fun mostrarAvisoEmergencia()
    fun mostrarErrorGuardado()
    fun abrirMarcador(numero: String)
}
