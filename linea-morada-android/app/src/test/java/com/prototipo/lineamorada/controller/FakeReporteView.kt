package com.prototipo.lineamorada.controller

import com.prototipo.lineamorada.model.ErrorValidacion
import com.prototipo.lineamorada.model.SolicitudAyuda
import com.prototipo.lineamorada.view.ReporteView

/**
 * Vista falsa para las pruebas del Controlador: no dibuja nada,
 * solo guarda lo que el Controlador le pidió mostrar.
 */
class FakeReporteView : ReporteView {
    var tiposApoyo: List<String> = emptyList()
    var tiposViolencia: List<String> = emptyList()
    var historial: List<SolicitudAyuda> = emptyList()
    var errores: List<ErrorValidacion> = emptyList()
    var confirmaciones = mutableListOf<SolicitudAyuda>()
    var formularioLimpiado = 0
    var avisosEmergencia = 0
    var erroresGuardado = 0
    var numeroMarcado: String? = null

    override fun mostrarTiposDeApoyo(opciones: List<String>) { tiposApoyo = opciones }
    override fun mostrarTiposDeViolencia(opciones: List<String>) { tiposViolencia = opciones }
    override fun mostrarHistorial(reportes: List<SolicitudAyuda>) { historial = reportes }
    override fun mostrarErroresValidacion(errores: List<ErrorValidacion>) { this.errores = errores }
    override fun limpiarErrores() { errores = emptyList() }
    override fun limpiarFormulario() { formularioLimpiado++ }
    override fun mostrarConfirmacion(reporte: SolicitudAyuda) { confirmaciones += reporte }
    override fun mostrarAvisoEmergencia() { avisosEmergencia++ }
    override fun mostrarErrorGuardado() { erroresGuardado++ }
    override fun abrirMarcador(numero: String) { numeroMarcado = numero }
}
