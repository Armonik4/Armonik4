# Práctica: diagnóstico de una funcionalidad — Historial de reportes

**Asignatura:** Desarrollo de Aplicaciones Móviles · Validación y optimización del rendimiento\
**Aplicación:** Línea Morada (prototipo Android, MVC en Kotlin)\
**Ciclo aplicado:** medir → diagnosticar → mejorar → volver a medir

---

## 1. Funcionalidad seleccionada

**Enviar una alerta y refrescar el historial de reportes.**

Es la acción principal de la app: la persona llena el formulario, toca **Enviar alerta**
y el reporte aparece arriba en el historial. Para un servicio de atención de violencia
de género, esta respuesta tiene que ser inmediata aunque el historial crezca mucho
(por ejemplo, en la vista de una operadora que acumula miles de casos).

## 2. Acción repetible y escenario

| Elemento | Definición |
|---|---|
| Acción repetible | Con N reportes ya guardados, enviar una alerta válida (Orientación legal · Física · descripción de 28 caracteres · "Cali"). |
| Escenarios | N = 1.000, 10.000 y 50.000 reportes precargados. |
| Calentamiento | 30 envíos que no se miden, para que el compilador JIT no distorsione los primeros resultados. |
| Observación | Promedio de 50 envíos seguidos. |
| Observaciones por escenario | 5 (la práctica pide al menos 3). Se reporta la **mediana**. |
| Prueba automatizada | `app/src/test/.../rendimiento/HistorialRendimientoTest.kt` (`./gradlew test`) |

## 3. Indicadores y herramienta

| Indicador | Qué mide | Herramienta |
|---|---|---|
| Tiempo por envío (ms) | Desde que el Controlador recibe el clic hasta que la Vista recibe el historial | `System.nanoTime()` en prueba JUnit |
| Memoria asignada por envío (KB) | Objetos que se crean en cada envío (listas copiadas, ordenadas) | `ThreadMXBean.getCurrentThreadAllocatedBytes()` |
| Filas entregadas a la Vista | Tamaño de la lista que recibe el `RecyclerView` / `DiffUtil` | Vista falsa de pruebas (`FakeReporteView`) |

**Entorno de medición:** JVM OpenJDK 21 en un servidor Linux de 4 núcleos.
Repositorio en memoria: la red no interviene. Esto **no** es un teléfono. Los
valores absolutos en milisegundos no se trasladan tal cual a un dispositivo, pero sí
la tendencia (cómo crece el costo con N). La sección 8 explica cómo repetirlo en el
teléfono con el Profiler de Android Studio.

## 4. Medición inicial (antes)

| N reportes | Obs 1 | Obs 2 | Obs 3 | Obs 4 | Obs 5 | **Mediana ms/envío** | KB/envío | Filas a la Vista |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1.000 | 0,080 | 0,043 | 0,062 | 0,052 | 0,252 | **0,062** | 39 | 1.080 |
| 10.000 | 0,644 | 0,599 | 0,263 | 0,548 | 0,306 | **0,548** | 591 | 10.080 |
| 50.000 | 2,437 | 2,400 | 2,372 | 2,586 | 2,202 | **2,400** | 2.935 | 50.080 |

La observación 5 con N=1.000 (0,252 ms) es atípica, probablemente por una
recolección de basura o por el JIT. Por eso se usa la mediana y no el promedio.

## 5. Síntoma, posible causa y evidencia

**Síntoma:** el tiempo y la memoria de cada envío crecen **en proporción al tamaño
del historial**. Pasar de 1.000 a 50.000 reportes (×50) multiplica el tiempo por ~39
y la memoria por ~75. Además, la Vista recibe **todas** las filas en cada envío.

**Hipótesis (causa):** en `ReporteController.actualizarVista()`, cada envío hacía:

```kotlin
val historial = repository.listar().sortedByDescending { it.marcaTiempo }
view?.mostrarHistorial(historial)
```

1. `listar()` copia la colección completa (N objetos).
2. `sortedByDescending` crea otra lista de N y la ordena: O(N log N).
3. La Vista recibe N filas y `DiffUtil` tiene que compararlas todas, aunque en
   pantalla solo caben unas 5 a 10.

**Evidencia:** la columna "Filas a la Vista" es siempre N + reportes enviados, y la
memoria por envío crece al mismo ritmo que N. Es el mismo patrón del ejemplo de la
clase ("una lista tarda 4 segundos"): se procesa todo cuando solo se necesita una parte.

## 6. Mejora aplicada

Se siguieron dos buenas prácticas de la sesión: *cargar listas progresivamente o
usar paginación* y *evitar consultas redundantes*.

| Capa | Cambio |
|---|---|
| Modelo | `MockReporteRepository` mantiene un **índice ya ordenado** por fecha (`TreeSet`). Nuevos métodos en `ReporteRepository`: `listarRecientes(desde, cantidad)` y `contar()`. |
| Controlador | `actualizarVista()` pide solo las filas visibles (páginas de **50**). Nuevo `cargarMasHistorial()` suma una página más. |
| Vista | `MainActivity` escucha el desplazamiento del `RecyclerView` y, a 10 filas del final, le pide al Controlador la página siguiente. |

La funcionalidad no cambia: el reporte nuevo sigue apareciendo primero y el orden
sigue siendo del más reciente al más antiguo. Hay 4 pruebas unitarias nuevas
(orden, páginas, límites y actualización de estado) y **las 23 pruebas pasan**.

## 7. Medición posterior (después) y comparación

Misma prueba, mismos escenarios y mismo entorno.

| N reportes | Obs 1 | Obs 2 | Obs 3 | Obs 4 | Obs 5 | **Mediana ms/envío** | KB/envío | Filas a la Vista |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1.000 | 0,011 | 0,007 | 0,005 | 0,005 | 0,005 | **0,005** | 2 | 50 |
| 10.000 | 0,006 | 0,008 | 0,005 | 0,004 | 0,007 | **0,006** | 2 | 50 |
| 50.000 | 0,005 | 0,001 | 0,002 | 0,001 | 0,002 | **0,002** | 2 | 50 |

**Reducción (%) = ((Inicial − Final) / Inicial) × 100**

| N reportes | Tiempo antes → después | Reducción de tiempo | Memoria antes → después | Reducción de memoria | Filas a la Vista |
|---:|---|---:|---|---:|---|
| 1.000 | 0,062 → 0,005 ms | 91,9 % | 39 → 2 KB | 94,9 % | 1.080 → 50 |
| 10.000 | 0,548 → 0,006 ms | 98,9 % | 591 → 2 KB | 99,7 % | 10.080 → 50 |
| 50.000 | 2,400 → 0,002 ms | 99,9 % | 2.935 → 2 KB | 99,9 % | 50.080 → 50 |

Ejemplo con N = 10.000: (0,548 − 0,006) / 0,548 × 100 = **98,9 %**.

**Lo más importante:** después de la mejora, el costo por envío **ya no depende del
tamaño del historial**: es prácticamente igual con 1.000 que con 50.000 reportes.

**Límites de esta medición:**
- Los tiempos "después" (0,001 a 0,011 ms) están cerca de la resolución del
  temporizador. Se deben leer como "menos de 0,01 ms", no como cifras exactas.
- Es una medición en la JVM de un servidor. En un teléfono los milisegundos serán
  otros. Hay que confirmarlo con el Profiler (sección 8).
- **Costo de la mejora:** guardar pasa de O(1) a O(log N), por el índice ordenado.
  Además, la persona ve 50 filas y las demás se cargan al desplazarse.

## 8. Cómo repetirlo en el teléfono (Android Studio Profiler)

Sigue los pasos de la demostración de clase y llena la tabla con tus datos.

1. En `di/ServiceLocator.kt`, cambia `REPORTES_DE_PRUEBA = 0` por `10_000`.
2. Abre el proyecto y elige **Run ▸ Profile 'app'** (o el ícono de Profiler).
3. Elige el proceso `com.prototipo.lineamorada` y abre **CPU** y **Memory**.
4. Envía la misma alerta 3 veces (Orientación legal · Física · "Necesito orientación urgente" · "Cali").
5. Relaciona cada pico de CPU o de memoria con el toque en **Enviar alerta**.
6. Para medir el "antes", usa el commit anterior a la mejora (`git checkout 325a73d -- linea-morada-android/app/src/main`), haz el paso 1 y repite. Después vuelve con `git checkout HEAD -- linea-morada-android/app/src/main`.
7. Al terminar, deja `REPORTES_DE_PRUEBA = 0`.

| Dato | Antes | Después |
|---|---|---|
| Dispositivo / versión de Android | | |
| Conexión | No aplica (sin red) | No aplica (sin red) |
| Observación 1 (pico de CPU o duración, ms) | | |
| Observación 2 | | |
| Observación 3 | | |
| Memoria tras 3 envíos (MB) | | |
| ¿Hubo cuadros lentos (más de 16,7 ms a 60 Hz)? | | |

Una gráfica aislada no demuestra por sí sola que exista un problema. Compara siempre
las mismas acciones, en el mismo dispositivo y con los mismos datos.

## 9. Socialización (respuestas para el equipo)

- **¿Qué evaluamos?** Enviar una alerta y refrescar el historial, la acción principal de la app.
- **¿Qué observamos y medimos?** Tiempo por envío, memoria asignada por envío y filas entregadas a la pantalla, con 1.000, 10.000 y 50.000 reportes y 5 observaciones por escenario.
- **¿Qué problema o hipótesis identificamos?** En cada envío se copiaba y ordenaba el historial completo y se mandaba entero a la pantalla, así que el costo crecía con N.
- **¿Qué mejora implementamos?** Un índice ordenado en el repositorio más paginación de 50 filas en el Controlador y la Vista.
- **¿Qué evidencia respalda la conclusión?** Las tablas de las secciones 4 y 7: más del 98 % de reducción con 10.000 o más reportes, costo constante sin importar N y las 23 pruebas en verde (la funcionalidad no se rompió).
- **¿Podemos dar por terminada una app que funciona pero responde lento?** No. El rendimiento es parte de la calidad. En una línea de atención de violencia, una respuesta lenta puede hacer que la persona abandone la solicitud. Una percepción ("se siente lento") se convierte en una prueba observable, se diagnostica antes de optimizar y cada mejora se vuelve a medir y se documenta.
