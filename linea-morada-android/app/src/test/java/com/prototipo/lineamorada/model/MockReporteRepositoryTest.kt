package com.prototipo.lineamorada.model

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Before
import org.junit.Test

/** PRUEBA UNITARIA del MODELO: corre en la JVM (./gradlew test), sin emulador. */
class MockReporteRepositoryTest {

    private lateinit var repo: MockReporteRepository

    private fun reporte(id: String, t: Long = 0L) = SolicitudAyuda(
        id = id,
        tipoApoyo = TipoApoyo.ORIENTACION_LEGAL,
        tipoViolencia = TipoViolencia.PSICOLOGICA,
        descripcion = "Descripción de prueba",
        ubicacionAproximada = "Bogotá",
        marcaTiempo = t,
    )

    @Before
    fun setUp() {
        repo = MockReporteRepository()
    }

    @Test
    fun `guardar y listar conserva el orden de insercion`() {
        repo.guardar(reporte("a"))
        repo.guardar(reporte("b"))

        assertEquals(listOf("a", "b"), repo.listar().map { it.id })
    }

    @Test
    fun `guardar un id duplicado falla y no reemplaza el original`() {
        repo.guardar(reporte("a"))
        val resultado = repo.guardar(reporte("a").copy(descripcion = "otra"))

        assertTrue(resultado.isFailure)
        assertEquals("Descripción de prueba", repo.buscarPorId("a")?.descripcion)
    }

    @Test
    fun `actualizarEstado cambia solo el estado`() {
        repo.guardar(reporte("a"))

        val actualizado = repo.actualizarEstado("a", EstadoReporte.EN_ATENCION).getOrThrow()

        assertEquals(EstadoReporte.EN_ATENCION, actualizado.estado)
        assertEquals(reporte("a").copy(estado = EstadoReporte.EN_ATENCION), repo.buscarPorId("a"))
    }

    @Test
    fun `actualizarEstado de un id inexistente falla`() {
        assertTrue(repo.actualizarEstado("x", EstadoReporte.ATENDIDO).isFailure)
        assertNull(repo.buscarPorId("x"))
    }

    @Test
    fun `listar devuelve una copia que no altera el repositorio`() {
        repo.guardar(reporte("a"))
        val lista = repo.listar()
        repo.guardar(reporte("b"))

        assertEquals(1, lista.size)
    }

    @Test
    fun `datos iniciales quedan disponibles`() {
        val sembrado = MockReporteRepository(listOf(reporte("s1"), reporte("s2")))
        assertEquals(2, sembrado.listar().size)
    }

    @Test
    fun `transiciones de estado`() {
        assertEquals(EstadoReporte.EN_ATENCION, EstadoReporte.PENDIENTE.siguiente())
        assertEquals(EstadoReporte.ATENDIDO, EstadoReporte.EN_ATENCION.siguiente())
        assertEquals(EstadoReporte.ATENDIDO, EstadoReporte.ATENDIDO.siguiente())
    }
}
