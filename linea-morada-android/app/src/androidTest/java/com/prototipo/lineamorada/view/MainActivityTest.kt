package com.prototipo.lineamorada.view

import androidx.test.espresso.Espresso.onData
import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.action.ViewActions.click
import androidx.test.espresso.action.ViewActions.closeSoftKeyboard
import androidx.test.espresso.action.ViewActions.replaceText
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.matcher.ViewMatchers.isDisplayed
import androidx.test.espresso.matcher.ViewMatchers.withId
import androidx.test.espresso.matcher.ViewMatchers.withText
import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import com.prototipo.lineamorada.R
import com.prototipo.lineamorada.di.ServiceLocator
import com.prototipo.lineamorada.model.MockReporteRepository
import com.prototipo.lineamorada.model.TipoApoyo
import com.prototipo.lineamorada.model.TipoViolencia
import org.hamcrest.Matchers.allOf
import org.hamcrest.Matchers.`is`
import org.hamcrest.Matchers.instanceOf
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import org.junit.rules.RuleChain
import org.junit.rules.TestWatcher
import org.junit.runner.Description
import org.junit.runner.RunWith

/**
 * PRUEBA DE UI (instrumentada) de la VISTA con Espresso.
 * Se ejecuta en emulador o dispositivo: ./gradlew connectedAndroidTest
 */
@RunWith(AndroidJUnit4::class)
class MainActivityTest {

    // Repositorio limpio ANTES de abrir la Activity, para que cada prueba empiece igual.
    private val repositorioLimpio = object : TestWatcher() {
        override fun starting(description: Description) {
            ServiceLocator.reporteRepository = MockReporteRepository()
        }
    }

    @get:Rule
    val reglas: RuleChain = RuleChain
        .outerRule(repositorioLimpio)
        .around(ActivityScenarioRule(MainActivity::class.java))

    @Before
    fun cerrarTeclado() {
        onView(withId(R.id.raiz)).perform(closeSoftKeyboard())
    }

    @Test
    fun enviarFormularioVacioMuestraErrores() {
        onView(withId(R.id.btnEnviarAlerta)).perform(click())

        onView(withId(R.id.tvErrorTipoApoyo)).check(matches(isDisplayed()))
        onView(withId(R.id.tvErrorTipoViolencia)).check(matches(isDisplayed()))
    }

    @Test
    fun enviarFormularioValidoAgregaReporteAlHistorial() {
        seleccionar(R.id.spinnerTipoApoyo, TipoApoyo.ORIENTACION_LEGAL.etiqueta)
        seleccionar(R.id.spinnerTipoViolencia, TipoViolencia.ECONOMICA.etiqueta)
        onView(withId(R.id.etDescripcion))
            .perform(replaceText("Necesito asesoría para una denuncia"), closeSoftKeyboard())
        onView(withId(R.id.btnEnviarAlerta)).perform(click())

        onView(withText("Necesito asesoría para una denuncia")).check(matches(isDisplayed()))
        onView(withText("Pendiente")).check(matches(isDisplayed()))
    }

    @Test
    fun tocarUnReporteAvanzaSuEstado() {
        enviarFormularioValidoAgregaReporteAlHistorial()

        onView(withText("Necesito asesoría para una denuncia")).perform(click())

        onView(withText("En atención")).check(matches(isDisplayed()))
    }

    private fun seleccionar(spinnerId: Int, opcion: String) {
        onView(withId(spinnerId)).perform(click())
        onData(allOf(`is`(instanceOf(String::class.java)), `is`(opcion))).perform(click())
    }
}
