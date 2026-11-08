package com.prototipo.lineamorada.controller

import com.prototipo.lineamorada.model.ErrorValidacion
import com.prototipo.lineamorada.model.EstadoReporte
import com.prototipo.lineamorada.model.MockReporteRepository
import com.prototipo.lineamorada.model.ReporteRepository
import com.prototipo.lineamorada.model.SolicitudAyuda
import com.prototipo.lineamorada.model.TipoApoyo
import com.prototipo.lineamorada.model.TipoViolencia
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Before
import org.junit.Test

/**
 * PRUEBA UNITARIA del CONTROLADOR con repositorio mock y vista falsa.
 * Reloj e ids fijos, así que los resultados no cambian entre ejecuciones.
 */
class ReporteControllerTest {

    private lateinit var view: FakeReporteView
    private lateinit var repo: MockReporteRepository
    private lateinit var controller: ReporteController
    private var ahora = 1_000L
    private var siguienteId = 0

    // Posiciones de Spinner: 0 = texto guía, 1.. = opciones reales.
    private val posLegal = TipoApoyo.entries.indexOf(TipoApoyo.ORIENTACION_LEGAL) + 1
    private val posEmergencia = TipoApoyo.entries.indexOf(TipoApoyo.EMERGENCIA) + 1
    private val posFisica = TipoViolencia.entries.indexOf(TipoViolencia.FISICA) + 1
    private val descripcionValida = "Necesito orientación sobre una denuncia"

    @Before
    fun setUp() {
        view = FakeReporteView()
        repo = MockReporteRepository()
        controller = ReporteController(
            view = view,
            repository = repo,
            reloj = { ahora },
            generadorId = { "id-${siguienteId++}" },
        )
    }

    @Test
    fun `iniciar carga las opciones y el historial vacio`() {
        controller.iniciar()

        assertEquals(TipoApoyo.entries.map { it.etiqueta }, view.tiposApoyo)
        assertEquals(TipoViolencia.entries.map { it.etiqueta }, view.tiposViolencia)
        assertTrue(view.historial.isEmpty())
    }

    @Test
    fun `formulario vacio devuelve todos los errores y no guarda`() {
        controller.enviarAlerta(0, 0, "", "")

        assertEquals(
            listOf(
                ErrorValidacion.TipoApoyoNoSeleccionado,
                ErrorValidacion.TipoViolenciaNoSeleccionado,
                ErrorValidacion.DescripcionMuyCorta(ReporteController.MIN_DESCRIPCION),
            ),
            view.errores,
        )
        assertTrue(repo.listar().isEmpty())
    }

    @Test
    fun `la descripcion se valida sin contar los espacios`() {
        val errores = controller.validar(posLegal, posFisica, "   corta    ", "")
        assertEquals(listOf(ErrorValidacion.DescripcionMuyCorta(10)), errores)
    }

    @Test
    fun `limites de longitud de descripcion y ubicacion`() {
        assertTrue(controller.validar(posLegal, posFisica, "a".repeat(10), "").isEmpty())
        assertTrue(controller.validar(posLegal, posFisica, "a".repeat(500), "b".repeat(100)).isEmpty())
        assertEquals(
            listOf(ErrorValidacion.DescripcionMuyLarga(500), ErrorValidacion.UbicacionMuyLarga(100)),
            controller.validar(posLegal, posFisica, "a".repeat(501), "b".repeat(101)),
        )
    }

    @Test
    fun `posicion fuera de rango cuenta como no seleccionada`() {
        val errores = controller.validar(99, -1, descripcionValida, "")
        assertEquals(
            listOf(ErrorValidacion.TipoApoyoNoSeleccionado, ErrorValidacion.TipoViolenciaNoSeleccionado),
            errores,
        )
    }

    @Test
    fun `alerta valida se guarda limpia el formulario y actualiza el historial`() {
        controller.enviarAlerta(posLegal, posFisica, "  $descripcionValida  ", " Medellín ")

        val esperado = SolicitudAyuda(
            id = "id-0",
            tipoApoyo = TipoApoyo.ORIENTACION_LEGAL,
            tipoViolencia = TipoViolencia.FISICA,
            descripcion = descripcionValida,
            ubicacionAproximada = "Medellín",
            marcaTiempo = 1_000L,
            estado = EstadoReporte.PENDIENTE,
        )
        assertEquals(listOf(esperado), repo.listar())
        assertEquals(listOf(esperado), view.historial)
        assertEquals(listOf(esperado), view.confirmaciones)
        assertEquals(1, view.formularioLimpiado)
        assertEquals(0, view.avisosEmergencia)
    }

    @Test
    fun `una emergencia muestra el aviso del 123`() {
        controller.enviarAlerta(posEmergencia, posFisica, descripcionValida, "")
        assertEquals(1, view.avisosEmergencia)
    }

    @Test
    fun `el historial se muestra del mas reciente al mas antiguo`() {
        controller.enviarAlerta(posLegal, posFisica, descripcionValida, "")
        ahora = 2_000L
        controller.enviarAlerta(posLegal, posFisica, descripcionValida, "")

        assertEquals(listOf("id-1", "id-0"), view.historial.map { it.id })
    }

    @Test
    fun `avanzarEstado recorre el ciclo y se detiene en ATENDIDO`() {
        controller.enviarAlerta(posLegal, posFisica, descripcionValida, "")

        controller.avanzarEstado("id-0")
        assertEquals(EstadoReporte.EN_ATENCION, view.historial.single().estado)
        controller.avanzarEstado("id-0")
        controller.avanzarEstado("id-0")
        assertEquals(EstadoReporte.ATENDIDO, view.historial.single().estado)
    }

    @Test
    fun `si el repositorio falla la vista muestra el error y no limpia el formulario`() {
        val repoQueFalla = object : ReporteRepository by MockReporteRepository() {
            override fun guardar(reporte: SolicitudAyuda) =
                Result.failure<SolicitudAyuda>(RuntimeException("sin conexión"))
        }
        val c = ReporteController(view, repoQueFalla, { ahora }, { "x" })

        c.enviarAlerta(posLegal, posFisica, descripcionValida, "")

        assertEquals(1, view.erroresGuardado)
        assertEquals(0, view.formularioLimpiado)
    }

    @Test
    fun `llamarEmergencia abre el marcador con el 123`() {
        controller.llamarEmergencia()
        assertEquals("123", view.numeroMarcado)
    }

    @Test
    fun `despues de destruir el controlador ya no toca la vista`() {
        controller.destruir()
        controller.enviarAlerta(0, 0, "", "")
        assertTrue(view.errores.isEmpty())
    }
}
