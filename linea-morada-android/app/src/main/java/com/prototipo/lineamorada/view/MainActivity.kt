package com.prototipo.lineamorada.view

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.view.View
import android.widget.ArrayAdapter
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.recyclerview.widget.LinearLayoutManager
import com.google.android.material.snackbar.Snackbar
import com.prototipo.lineamorada.R
import com.prototipo.lineamorada.controller.ReporteController
import com.prototipo.lineamorada.databinding.ActivityMainBinding
import com.prototipo.lineamorada.di.ServiceLocator
import com.prototipo.lineamorada.model.ErrorValidacion
import com.prototipo.lineamorada.model.SolicitudAyuda

/**
 * VISTA — Solo dibuja y reenvía eventos.
 *
 * Qué hace:   inflar el layout, pasar los clics al Controlador y pintar lo que
 *             el Controlador le manda (métodos de ReporteView).
 * Qué NO hace: validar, crear objetos del Modelo, ordenar listas ni hablar con
 *             el repositorio.
 *
 * PRUEBA DE UI (androidTest/MainActivityTest con Espresso):
 *  - Enviar con el formulario vacío muestra los errores.
 *  - Enviar un formulario válido agrega el reporte al historial.
 *  - Tocar un reporte cambia su estado en pantalla.
 */
class MainActivity : AppCompatActivity(), ReporteView {

    private lateinit var binding: ActivityMainBinding
    private lateinit var controller: ReporteController

    private val historialAdapter = ReporteAdapter { reporte ->
        controller.avanzarEstado(reporte.id)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        aplicarInsets()

        binding.rvHistorial.layoutManager = LinearLayoutManager(this)
        binding.rvHistorial.adapter = historialAdapter

        // El Controlador recibe la Vista (this) y el Repositorio como dependencias.
        controller = ReporteController(this, ServiceLocator.reporteRepository)

        binding.btnEnviarAlerta.setOnClickListener {
            controller.enviarAlerta(
                posicionTipoApoyo = binding.spinnerTipoApoyo.selectedItemPosition,
                posicionTipoViolencia = binding.spinnerTipoViolencia.selectedItemPosition,
                descripcion = binding.etDescripcion.text?.toString().orEmpty(),
                ubicacion = binding.etUbicacion.text?.toString().orEmpty(),
            )
        }
        binding.btnLlamarEmergencia.setOnClickListener { controller.llamarEmergencia() }

        controller.iniciar()
    }

    override fun onDestroy() {
        controller.destruir()
        super.onDestroy()
    }

    // ---------- ReporteView: órdenes que llegan del Controlador ----------

    override fun mostrarTiposDeApoyo(opciones: List<String>) {
        binding.spinnerTipoApoyo.adapter =
            adaptadorSpinner(getString(R.string.hint_tipo_apoyo), opciones)
    }

    override fun mostrarTiposDeViolencia(opciones: List<String>) {
        binding.spinnerTipoViolencia.adapter =
            adaptadorSpinner(getString(R.string.hint_tipo_violencia), opciones)
    }

    override fun mostrarHistorial(reportes: List<SolicitudAyuda>) {
        historialAdapter.submitList(reportes)
        binding.tvHistorialVacio.visibility = if (reportes.isEmpty()) View.VISIBLE else View.GONE
        binding.rvHistorial.visibility = if (reportes.isEmpty()) View.GONE else View.VISIBLE
    }

    override fun mostrarErroresValidacion(errores: List<ErrorValidacion>) {
        limpiarErrores()
        errores.forEach { error ->
            when (error) {
                ErrorValidacion.TipoApoyoNoSeleccionado ->
                    mostrarErrorSpinner(binding.tvErrorTipoApoyo, R.string.error_tipo_apoyo)
                ErrorValidacion.TipoViolenciaNoSeleccionado ->
                    mostrarErrorSpinner(binding.tvErrorTipoViolencia, R.string.error_tipo_violencia)
                is ErrorValidacion.DescripcionMuyCorta ->
                    binding.tilDescripcion.error = getString(R.string.error_descripcion_corta, error.minimo)
                is ErrorValidacion.DescripcionMuyLarga ->
                    binding.tilDescripcion.error = getString(R.string.error_descripcion_larga, error.maximo)
                is ErrorValidacion.UbicacionMuyLarga ->
                    binding.tilUbicacion.error = getString(R.string.error_ubicacion_larga, error.maximo)
            }
        }
    }

    override fun limpiarErrores() {
        binding.tvErrorTipoApoyo.visibility = View.GONE
        binding.tvErrorTipoViolencia.visibility = View.GONE
        binding.tilDescripcion.error = null
        binding.tilUbicacion.error = null
    }

    override fun limpiarFormulario() {
        binding.spinnerTipoApoyo.setSelection(0)
        binding.spinnerTipoViolencia.setSelection(0)
        binding.etDescripcion.text?.clear()
        binding.etUbicacion.text?.clear()
    }

    override fun mostrarConfirmacion(reporte: SolicitudAyuda) {
        Snackbar.make(binding.root, R.string.confirmacion_enviada, Snackbar.LENGTH_LONG).show()
    }

    override fun mostrarAvisoEmergencia() {
        AlertDialog.Builder(this)
            .setTitle(R.string.emergencia_titulo)
            .setMessage(R.string.emergencia_mensaje)
            .setPositiveButton(R.string.emergencia_llamar) { _, _ -> controller.llamarEmergencia() }
            .setNegativeButton(R.string.cerrar, null)
            .show()
    }

    override fun mostrarErrorGuardado() {
        Snackbar.make(binding.root, R.string.error_guardado, Snackbar.LENGTH_LONG).show()
    }

    override fun abrirMarcador(numero: String) {
        // ACTION_DIAL solo abre el marcador con el número: no necesita permiso CALL_PHONE.
        startActivity(Intent(Intent.ACTION_DIAL, Uri.parse("tel:$numero")))
    }

    // ---------- Ayudantes puramente visuales ----------

    private fun adaptadorSpinner(hint: String, opciones: List<String>) =
        ArrayAdapter(this, android.R.layout.simple_spinner_item, listOf(hint) + opciones).apply {
            setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        }

    private fun mostrarErrorSpinner(textView: android.widget.TextView, mensaje: Int) {
        textView.setText(mensaje)
        textView.visibility = View.VISIBLE
    }

    private fun aplicarInsets() {
        ViewCompat.setOnApplyWindowInsetsListener(binding.root) { v, insets ->
            val barras = insets.getInsets(
                WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.ime(),
            )
            v.setPadding(barras.left, barras.top, barras.right, barras.bottom)
            insets
        }
    }
}
