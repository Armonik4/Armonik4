# SaludConecta — Wireframes de Baja Fidelidad

**Tarea:** Diseño de App – Computación Móvil
**Herramienta:** Figma
**Archivo:** https://www.figma.com/design/BkE6lxKvKNOfmvFwCaypL2

---

## 1. Contexto

Aplicación móvil para programar citas médicas con dos tipos de usuario y necesidades
distintas: **Pacientes** y **Médicos Especialistas**.

Los wireframes son de **baja fidelidad** siguiendo la guía de la tarea:

- Sin color: toda la paleta es escala de grises.
- Sin fotografías: los avatares e imágenes son círculos y cajas con "X".
- Líneas horizontales grises para simular bloques de texto (ver "Currículum" en la pantalla 4).
- Botones de acción (CTA) grandes, de ancho completo y con alto contraste.
- El foco está en la **jerarquía de la información** y la **navegación**, no en el estilo.

## 2. User Flow (Paso 1)

**Paciente:**
Login → Home → Resultados de búsqueda → Detalle del médico → Agenda (fecha y hora) →
Confirmación → Mis Citas

**Médico especialista:**
Login → Dashboard (agenda del día) → Panel de pacientes → Hoja de vida del paciente →
Nota rápida → Gestión de agenda

## 3. Pantallas entregadas

El archivo de Figma tiene dos páginas: `01 · Wireframes Lo-Fi` y `02 · User Flow`.
Las pantallas usan el marco estándar de 390 × 844 px (iPhone 14).

### Fila 1 — Flujo de agendamiento

| # | Pantalla | Contenido clave |
|---|----------|-----------------|
| 1 | **Login - Credenciales** | Selector de rol (Paciente / Médico), correo, contraseña, recordarme, recuperar contraseña, acceso biométrico, registro |
| 2 | **Home (Paciente)** | Saludo + ubicación, **buscador destacado** (56 px, borde reforzado), filtros rápidos, grilla de 6 especialidades, tarjeta de próxima cita, nav inferior |
| 3 | **Resultado de Búsqueda** | Lista de médicos con información esencial: foto, nombre, especialidad, años de experiencia, valoración, distancia, precio y próximo horario disponible |
| 4 | **Detalle del Médico** | Encabezado del perfil, métricas, tabs, currículum, horarios disponibles y **botón prominente "Reservar Cita"** fijo en una barra inferior junto al precio |
| 5 | **Agenda · fecha y hora** | Selector de mes, semana con día activo, franjas de mañana y tarde, tipo de consulta (presencial/virtual), resumen + "Confirmar Cita" |

### Fila 2 — Confirmación, rol médico y hojas de vida

| # | Pantalla | Contenido clave |
|---|----------|-----------------|
| 6 | **Confirmación** | Pantalla de éxito con check, resumen completo de la cita (médico, fecha, hora, modalidad, dirección, código, total) y acciones siguientes |
| 7 | **Dashboard (Médico)** | **Header oscuro** que diferencia el rol, resumen del día (citas hoy / confirmadas / pendientes), agenda cronológica del día y acciones de gestión de agenda |
| 8 | **Hoja de Vida de Pacientes** | Datos personales, tipo de sangre, EPS, antecedentes, alergias, medicamentos actuales, consultas previas y "Agregar nota rápida" |
| 9 | **Hoja de Vida Médicos (con especialidad)** | Especialidad principal destacada + subespecialidades, valoración, tarifa, formación académica, experiencia laboral y certificaciones |
| 10 | **Mis Citas (Paciente)** | Tabs próximas/historial, banner de recordatorio, tarjetas con estado y acciones (reprogramar/cancelar) |

> Las 8 pantallas obligatorias son la 1–4 y 6–9. Las pantallas 5 y 10 se agregaron para
> cubrir los requerimientos funcionales de "Agenda: seleccionar fecha y hora" y
> "Mis Citas: historial y recordatorios".

## 4. Cómo se resuelven los criterios de evaluación

| Criterio | Cómo se resuelve |
|----------|------------------|
| **Usabilidad** — ¿es intuitivo el camino para sacar una cita? | 5 toques desde el Home: buscador → resultado → detalle → horario → confirmar. El buscador es el elemento más grande del Home y "Reservar Cita" es el único botón oscuro de su pantalla. |
| **Arquitectura** — ¿la información más importante está arriba? | En cada pantalla el primer bloque bajo la barra de estado responde a la pregunta principal: en el Home el buscador; en Resultados el nombre y precio; en el Detalle la identidad y credenciales del médico; en el Dashboard el resumen del día. |
| **Consistencia** — ¿los elementos se ven iguales en todas las pantallas? | Todo se construye con un mismo kit de componentes: `SCREEN`, `STATUS`, `APPBAR`, `CONTENT`, `NAV`, `BTN`, `CHIP`, `CIRC`. Mismo radio (10 px), mismo grosor de borde (1 px), misma escala tipográfica y el mismo padding de 20 px. |
| **Adaptabilidad** — ¿se diferencia la interfaz del médico de la del paciente? | El paciente navega en fondo claro con `Inicio / Buscar / Mis Citas / Perfil`. El médico entra a un dashboard con **header oscuro**, tarjetas de métricas invertidas y nav `Agenda / Pacientes / Historial / Perfil`. El rol se elige desde el login. |

## 5. Estado de la entrega

**Las 10 pantallas y la página de User Flow están dentro del archivo de Figma.**
Página `01 · Wireframes Lo-Fi`: las 10 pantallas en dos filas de cinco.
Página `02 · User Flow`: los dos carriles (paciente y médico).

Las pantallas 1–9 se construyeron directamente por MCP con la Figma Plugin API. La
pantalla 10 y el User Flow se incorporaron importando los SVG de `docs/svg/`, porque el
plan **Starter de Figma permite 20 llamadas MCP al mes** (no por hora ni por día) y esa
cuota se agotó construyendo las nueve primeras. La diferencia práctica es que esas dos
piezas no traen auto-layout nativo; visualmente son idénticas al resto.

### Desviación conocida frente al enunciado

El Paso 2 pide *"usar cuadros con una X para imágenes"*. Los avatares del diseño son
círculos grises, una convención lo-fi habitual pero distinta de lo que dice la guía. Las
líneas horizontales para simular texto sí están (bloque de currículum de la pantalla 4).
El helper `IMG()` de `figma-scripts/00-helpers.js` dibuja la caja con X y queda disponible
para hacer el cambio cuando haya cuota de MCP.

Otros dos requerimientos funcionales quedan cubiertos de forma implícita y no como pantalla
propia: la *gestión de agenda* del médico (bloquear horarios) vive como acciones en el
Dashboard, y el *panel de pacientes* está fusionado en la agenda cronológica del mismo
Dashboard.

## 6. Reconstruir o extender el diseño

La carpeta `figma-scripts/` contiene el código de la Figma Plugin API que genera el diseño.

- `00-helpers.js` — kit de componentes compartido (pegar siempre primero).
- `10-mis-citas.js` — pantalla 10, pendiente de ejecutar.
- `11-user-flow.js` — página de user flow, pendiente de ejecutar.
- `build-svg.py` — genera los dos entregables pendientes como SVG importables.

Para ejecutarlos: concatenar `00-helpers.js` con el script deseado y pasarlo a la
herramienta `use_figma` del MCP de Figma con el `fileKey` del archivo.
