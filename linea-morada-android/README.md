# Línea Morada — Prototipo Android (MVC, Kotlin)

Prototipo base para apoyar la gestión de la **Línea Morada** en Colombia (prevención y
atención de violencia de género, orientación legal/psicológica y reportes de emergencia).
La arquitectura es **MVC** con las responsabilidades bien separadas, pensada para pruebas
funcionales, QA y mejoras de rendimiento más adelante.

> Es un prototipo. Los datos viven **solo en memoria** y se pierden al cerrar la app.
> Todavía no se envía nada a ningún servicio real.

## Cómo abrirlo

1. Android Studio (Ladybug o más reciente) → **Open** → elegir la carpeta `linea-morada-android/`.
2. Esperar la sincronización de Gradle (AGP 8.7.3, Kotlin 2.0.21, Gradle 8.11.1, JDK 17+).
3. Ejecutar en un emulador o dispositivo con API 24 o superior.

```bash
./gradlew test                  # pruebas unitarias (JVM): Modelo y Controlador
./gradlew connectedAndroidTest  # pruebas de UI (Espresso): necesita emulador/dispositivo
```

## Estructura

```
app/src/main/java/com/prototipo/lineamorada/
├── model/                        MODELO: datos y reglas, sin Android
│   ├── SolicitudAyuda.kt         data class del reporte (id, tipos, descripción, ubicación, marca de tiempo, estado)
│   ├── TipoApoyo.kt              emergencia, orientación legal, psicológica, información
│   ├── TipoViolencia.kt          física, psicológica, sexual, económica, patrimonial, otra
│   ├── EstadoReporte.kt          PENDIENTE → EN_ATENCION → ATENDIDO
│   ├── ErrorValidacion.kt        errores tipados (la Vista los traduce a texto)
│   ├── ReporteRepository.kt      interfaz: guardar, listar, buscarPorId, actualizarEstado
│   └── MockReporteRepository.kt  implementación en memoria, segura entre hilos
├── view/                         VISTA: solo dibuja y reenvía eventos
│   ├── ReporteView.kt            contrato que usa el Controlador (Kotlin puro)
│   ├── MainActivity.kt           implementa ReporteView
│   └── ReporteAdapter.kt         RecyclerView con ListAdapter + DiffUtil
├── controller/
│   └── ReporteController.kt      valida, crea el Modelo, guarda y actualiza la Vista
└── di/ServiceLocator.kt          entrega el repositorio (sobrevive a la rotación)

app/src/main/res/layout/activity_main.xml   pantalla: Spinners, EditText, botón, historial
app/src/main/res/layout/item_reporte.xml    fila del historial
app/src/test/...                             pruebas unitarias JVM (19 casos)
app/src/androidTest/...                      pruebas de UI con Espresso
```

## Cómo fluyen los datos

```
Usuaria toca "Enviar alerta"
  → MainActivity pasa los valores crudos (posiciones de los Spinners y textos)
  → ReporteController.enviarAlerta()
       ├─ validar()                    → si hay errores: view.mostrarErroresValidacion()
       ├─ crea SolicitudAyuda (trim, id, marca de tiempo, PENDIENTE)
       ├─ repository.guardar()
       └─ view.limpiarFormulario() / mostrarConfirmacion() / actualizarVista()
                                        (+ mostrarAvisoEmergencia() si el tipo es EMERGENCIA)
```

Cómo se mantiene la separación:

- **Modelo**: no importa nada de Android ni de UI.
- **Vista**: no valida, no crea objetos del Modelo, no ordena listas, no habla con el repositorio.
- **Controlador**: depende de las interfaces `ReporteView` y `ReporteRepository`, no de
  `MainActivity` ni de una base de datos concreta. Por eso se prueba con una vista falsa
  y el repositorio mock. El reloj y el generador de ids se inyectan para que las pruebas
  den siempre el mismo resultado.

## Dónde probar cada capa

| Capa | Tipo de prueba | Archivo | Qué cubre |
|---|---|---|---|
| Modelo | Unitaria (JVM) | `MockReporteRepositoryTest` | guardar/listar, id duplicado, actualizar un id inexistente, copia defensiva, transiciones de estado |
| Controlador | Unitaria (JVM) | `ReporteControllerTest` + `FakeReporteView` | cada regla de validación y sus límites, guardado correcto, aviso de emergencia, orden del historial, ciclo de estados, fallo del repositorio, `destruir()` |
| Vista | UI (Espresso) | `MainActivityTest` | errores con el formulario vacío, envío válido que aparece en el historial, tocar una fila cambia su estado |

## Decisiones del prototipo

- **Dos Spinners**: el formulario pide el *tipo de apoyo* y el Modelo pide el *tipo de violencia*, así que hay uno para cada dato.
- **Ubicación aproximada** escrita por la persona (opcional, máximo 100 caracteres). No se usa GPS para no pedir permisos ni exponer la ubicación exacta.
- **Al tocar un reporte** avanza su estado. Simula a la operadora para probar `actualizarEstado` desde la UI.
- **Botón "Llamar al 123"**: usa `ACTION_DIAL`, que abre el marcador con el número pero no llama sola y no necesita permiso.
- **El RecyclerView no va dentro de un ScrollView**, para que siga reciclando filas.

## Próximos pasos sugeridos

- Pasar el repositorio a `suspend`/`Flow` y conectarlo a Room o a una API (Retrofit), sin cambiar la Vista.
- Inyección de dependencias con Hilt o Koin en lugar de `ServiceLocator`.
- Seguridad y privacidad: cifrar los datos en reposo, ocultar la pantalla en "recientes" (`FLAG_SECURE`), un botón de **salida rápida** y un ícono/nombre discreto. Cumplir la Ley 1581 de 2012 (habeas data).
- Validar con la entidad responsable los números oficiales de atención (por ejemplo, la Línea 155 nacional y las líneas locales) antes de mostrarlos en la app.
- Accesibilidad: probar con TalkBack y revisar el contraste.
