package com.prototipo.lineamorada.rendimiento

import com.prototipo.lineamorada.controller.FakeReporteView
import com.prototipo.lineamorada.controller.ReporteController
import com.prototipo.lineamorada.model.MockReporteRepository
import com.prototipo.lineamorada.model.SolicitudAyuda
import com.prototipo.lineamorada.model.TipoApoyo
import com.prototipo.lineamorada.model.TipoViolencia
import org.junit.Assert.assertEquals
import org.junit.Test
import java.lang.management.ManagementFactory

/**
 * PRUEBA DE RENDIMIENTO (JVM) — Práctica "diagnóstico de una funcionalidad".
 *
 * Funcionalidad: enviar una alerta y refrescar el historial.
 * Acción repetible: con N reportes ya guardados, enviar una alerta válida.
 * Indicadores:
 *  - tiempo del controlador por envío (ms), hasta que la vista recibe el historial
 *  - memoria asignada por envío (KB), medida con ThreadMXBean
 *  - filas entregadas a la vista (tamaño de la lista que dibuja el RecyclerView)
 * Observaciones: 5 por escenario; cada una es el promedio de 50 envíos seguidos,
 * después de 30 envíos de calentamiento (para que el JIT no distorsione).
 *
 * Mide la lógica del Modelo y el Controlador en la JVM del computador, no en el
 * teléfono. El costo de dibujar se mide aparte con el Profiler de Android Studio.
 * No compara tiempos con un umbral (eso haría la prueba inestable): solo
 * imprime la tabla y verifica que la funcionalidad siga correcta.
 */
class HistorialRendimientoTest {

    private val escenarios = listOf(1_000, 10_000, 50_000)
    private val observaciones = 5
    private val enviosPorObservacion = 50
    private val calentamiento = 30

    private val mx = ManagementFactory.getThreadMXBean() as com.sun.management.ThreadMXBean

    @Test
    fun medirEnvioDeAlertaConHistorialGrande() {
        println("\n=== Enviar alerta + refrescar historial ===")
        println("N reportes | obs | ms/envío | KB/envío | filas a la vista")
        for (n in escenarios) {
            val resultados = (1..observaciones).map { obs -> medir(n, obs) }
            val ms = resultados.map { it.first }.sorted()
            val kb = resultados.map { it.second }.sorted()
            println(
                "N=%,d → mediana %.3f ms (min %.3f, max %.3f) · mediana %,.0f KB/envío"
                    .format(n, ms[ms.size / 2], ms.first(), ms.last(), kb[kb.size / 2]),
            )
        }
    }

    private fun medir(n: Int, obs: Int): Pair<Double, Double> {
        val view = FakeReporteView()
        val repo = MockReporteRepository(semilla(n))
        var reloj = n.toLong() * 1_000
        var id = 0
        val controller = ReporteController(view, repo, { reloj++ }, { "nuevo-${id++}" })
        val tipo = TipoApoyo.entries.indexOf(TipoApoyo.ORIENTACION_LEGAL) + 1
        val violencia = TipoViolencia.entries.indexOf(TipoViolencia.FISICA) + 1
        val enviar = { controller.enviarAlerta(tipo, violencia, "Necesito orientación urgente", "Cali") }

        repeat(calentamiento) { enviar() }

        val bytesAntes = mx.currentThreadAllocatedBytes
        val inicio = System.nanoTime()
        repeat(enviosPorObservacion) { enviar() }
        val nanos = System.nanoTime() - inicio
        val bytes = mx.currentThreadAllocatedBytes - bytesAntes

        val msPorEnvio = nanos / 1e6 / enviosPorObservacion
        val kbPorEnvio = bytes / 1024.0 / enviosPorObservacion
        println(
            "%,10d | %3d | %8.3f | %,8.0f | %,d"
                .format(n, obs, msPorEnvio, kbPorEnvio, view.historial.size),
        )

        // La funcionalidad sigue correcta: el último enviado aparece primero.
        assertEquals("nuevo-${id - 1}", view.historial.first().id)
        assertEquals(n + calentamiento + enviosPorObservacion, repo.listar().size)
        return msPorEnvio to kbPorEnvio
    }

    private fun semilla(n: Int) = List(n) { i ->
        SolicitudAyuda(
            id = "s-$i",
            tipoApoyo = TipoApoyo.entries[i % TipoApoyo.entries.size],
            tipoViolencia = TipoViolencia.entries[i % TipoViolencia.entries.size],
            descripcion = "Reporte de prueba número $i",
            ubicacionAproximada = "Bogotá",
            marcaTiempo = i.toLong() * 1_000,
        )
    }
}
