package com.prototipo.lineamorada.controller

import com.prototipo.lineamorada.model.ErrorValidacion
import com.prototipo.lineamorada.model.EstadoReporte
import com.prototipo.lineamorada.model.ReporteRepository
import com.prototipo.lineamorada.model.SolicitudAyuda
import com.prototipo.lineamorada.model.TipoApoyo
import com.prototipo.lineamorada.model.TipoViolencia
import com.prototipo.lineamorada.view.ReporteView
import java.util.UUID

/**
 * CONTROLADOR — Recibe los eventos de la Vista, valida, crea el Modelo,
 * lo guarda en el repositorio y le dice a la Vista qué mostrar.
 *
 * No importa nada de Android. `reloj` y `generadorId` se inyectan para que las
 * pruebas tengan resultados fijos (misma hora, mismo id).
 *
 * PRUEBA UNITARIA (ReporteControllerTest): se arma con un MockReporteRepository y
 * una FakeReporteView, y se revisa qué métodos de la vista se llamaron.
 */
class ReporteController(
    view: ReporteView,
    private val repository: ReporteRepository,
    private val reloj: () -> Long = System::currentTimeMillis,
    private val generadorId: () -> String = { UUID.randomUUID().toString() },
) {
    // Nullable para soltar la Activity en destruir() y evitar fugas de memoria.
    private var view: ReporteView? = view

    private val tiposApoyo: List<TipoApoyo> = TipoApoyo.entries
    private val tiposViolencia: List<TipoViolencia> = TipoViolencia.entries

    // Cuántas filas del historial se muestran; crece de a una página al desplazarse.
    private var filasVisibles = TAMANO_PAGINA

    /** Se llama una vez desde onCreate: carga los Spinners y el historial. */
    fun iniciar() {
        view?.mostrarTiposDeApoyo(tiposApoyo.map { it.etiqueta })
        view?.mostrarTiposDeViolencia(tiposViolencia.map { it.etiqueta })
        actualizarVista()
    }

    /**
     * Evento del botón "Enviar alerta". La Vista pasa los valores crudos tal
     * como están en pantalla; todo el procesamiento ocurre aquí.
     */
    fun enviarAlerta(
        posicionTipoApoyo: Int,
        posicionTipoViolencia: Int,
        descripcion: String,
        ubicacion: String,
    ) {
        val errores = validar(posicionTipoApoyo, posicionTipoViolencia, descripcion, ubicacion)
        if (errores.isNotEmpty()) {
            view?.mostrarErroresValidacion(errores)
            return
        }
        view?.limpiarErrores()

        val reporte = crearReporte(posicionTipoApoyo, posicionTipoViolencia, descripcion, ubicacion)

        repository.guardar(reporte)
            .onSuccess { guardado ->
                view?.limpiarFormulario()
                view?.mostrarConfirmacion(guardado)
                if (guardado.tipoApoyo == TipoApoyo.EMERGENCIA) {
                    view?.mostrarAvisoEmergencia()
                }
                actualizarVista()
            }
            .onFailure { view?.mostrarErrorGuardado() }
    }

    /**
     * Reglas de validación. Es pública y no tiene efectos secundarios, así
     * que se prueba directamente, caso por caso.
     *
     * @return Lista vacía si todo es válido.
     */
    fun validar(
        posicionTipoApoyo: Int,
        posicionTipoViolencia: Int,
        descripcion: String,
        ubicacion: String,
    ): List<ErrorValidacion> = buildList {
        if (tipoApoyoEn(posicionTipoApoyo) == null) {
            add(ErrorValidacion.TipoApoyoNoSeleccionado)
        }
        if (tipoViolenciaEn(posicionTipoViolencia) == null) {
            add(ErrorValidacion.TipoViolenciaNoSeleccionado)
        }
        val texto = descripcion.trim()
        when {
            texto.length < MIN_DESCRIPCION -> add(ErrorValidacion.DescripcionMuyCorta(MIN_DESCRIPCION))
            texto.length > MAX_DESCRIPCION -> add(ErrorValidacion.DescripcionMuyLarga(MAX_DESCRIPCION))
        }
        if (ubicacion.trim().length > MAX_UBICACION) {
            add(ErrorValidacion.UbicacionMuyLarga(MAX_UBICACION))
        }
    }

    /** Evento al tocar un reporte del historial: lo pasa al siguiente estado (simula a la operadora). */
    fun avanzarEstado(id: String) {
        val actual = repository.buscarPorId(id) ?: return
        val siguiente = actual.estado.siguiente()
        if (siguiente == actual.estado) return // ya está ATENDIDO
        repository.actualizarEstado(id, siguiente)
            .onSuccess { actualizarVista() }
            .onFailure { view?.mostrarErrorGuardado() }
    }

    /** Evento del botón de emergencia: abre el marcador; no llama sola. */
    fun llamarEmergencia() {
        view?.abrirMarcador(NUMERO_EMERGENCIAS)
    }

    /**
     * Envía a la Vista el historial (el más reciente primero), solo hasta las
     * filas visibles. Antes se copiaba y ordenaba toda la lista en cada envío.
     */
    fun actualizarVista() {
        view?.mostrarHistorial(repository.listarRecientes(0, filasVisibles))
    }

    /** Evento de la Vista al acercarse al final de la lista: muestra la página siguiente. */
    fun cargarMasHistorial() {
        if (filasVisibles >= repository.contar()) return // ya se ve todo
        filasVisibles += TAMANO_PAGINA
        actualizarVista()
    }

    /** Se llama desde onDestroy para soltar la referencia a la Activity. */
    fun destruir() {
        view = null
    }

    private fun crearReporte(
        posicionTipoApoyo: Int,
        posicionTipoViolencia: Int,
        descripcion: String,
        ubicacion: String,
    ) = SolicitudAyuda(
        id = generadorId(),
        tipoApoyo = requireNotNull(tipoApoyoEn(posicionTipoApoyo)),
        tipoViolencia = requireNotNull(tipoViolenciaEn(posicionTipoViolencia)),
        descripcion = descripcion.trim(),
        ubicacionAproximada = ubicacion.trim(),
        marcaTiempo = reloj(),
        estado = EstadoReporte.PENDIENTE,
    )

    // Posición 0 = texto guía, por eso se resta 1.
    private fun tipoApoyoEn(posicion: Int) = tiposApoyo.getOrNull(posicion - 1)
    private fun tipoViolenciaEn(posicion: Int) = tiposViolencia.getOrNull(posicion - 1)

    companion object {
        const val MIN_DESCRIPCION = 10
        const val MAX_DESCRIPCION = 500
        const val MAX_UBICACION = 100

        /** Filas del historial por página. */
        const val TAMANO_PAGINA = 50

        /** Línea nacional de emergencias en Colombia. */
        const val NUMERO_EMERGENCIAS = "123"
    }
}
