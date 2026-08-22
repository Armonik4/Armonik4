# Paquete SVG · SaludConecta

22 pantallas + 2 diagramas de user flow, listas para importar a Figma. Cada elemento
interactivo lleva su propio nombre de capa, para que conectar el prototipo sea buscar
por nombre y arrastrar.

## Contenido

| Archivo | Pantalla | Rol |
|---|---|---|
| `00-hoja-completa.svg` | Las 22 pantallas en una lámina, 6 por fila | — |
| `01-login.svg` | Login · Credenciales, con selector de rol | Ambos |
| `02-home-paciente.svg` | Home: buscador destacado + especialidades | Paciente |
| `03-resultado-busqueda.svg` | Lista de médicos con filtros rápidos | Paciente |
| `04-detalle-medico.svg` | Perfil del médico + CTA "Reservar Cita" | Paciente |
| `05-agenda-fecha-hora.svg` | Calendario y franjas horarias | Paciente |
| `06-confirmacion.svg` | Pantalla de éxito con resumen | Paciente |
| `07-dashboard-medico.svg` | Panel del médico: agenda del día | Médico |
| `08-hoja-vida-paciente.svg` | Historia clínica del paciente | Médico |
| `09-hoja-vida-medico.svg` | Hoja de vida profesional con especialidad | Ambos |
| `10-mis-citas.svg` | Próximas citas, historial y recordatorio | Paciente |
| `11-registro.svg` | Crear cuenta, con stepper de 3 pasos | Ambos |
| `12-filtros.svg` | Filtros avanzados como hoja modal | Paciente |
| `13-valoraciones.svg` | Opiniones y distribución de estrellas | Paciente |
| `14-detalle-cita.svg` | Detalle de una cita reservada + mapa | Paciente |
| `15-cancelar-cita.svg` | Confirmación destructiva con política | Paciente |
| `16-pago.svg` | Métodos de pago y resumen del cobro | Paciente |
| `17-teleconsulta.svg` | Videollamada, interfaz oscura | Ambos |
| `18-notificaciones.svg` | Bandeja agrupada por fecha | Paciente |
| `19-perfil-paciente.svg` | Cuenta, salud y ajustes | Paciente |
| `20-panel-pacientes.svg` | Lista de pacientes citados | Médico |
| `21-gestion-agenda.svg` | Bloquear horarios y disponibilidad | Médico |
| `22-registrar-consulta.svg` | Nota rápida e historia clínica | Médico |
| `23-user-flow.svg` | Recorrido principal, dos carriles | — |
| `24-user-flow-secundarios.svg` | Ramas secundarias | — |

Todas las pantallas miden **390 × 844 px** (iPhone 14).

## Por qué estas 22

Las 8 obligatorias del enunciado son la 1, 2, 3, 4, 6, 7, 8 y 9. El resto no es relleno:
cada una es **el destino de un botón que ya existía**. La 11 es a dónde lleva "Regístrate"
del login; la 12 es el botón de filtros del Home; la 13 es la pestaña "Valoraciones" del
perfil del médico; la 21 y la 20 son los dos requerimientos funcionales del médico
—gestión de agenda y panel de pacientes— que antes solo existían como botones sin
pantalla propia.

## Cómo importarlos

**Rápido:** arrastra `00-hoja-completa.svg`. Entran las 22 de una vez, ya distribuidas
y tituladas. Desagrupa con `Ctrl/Cmd + Shift + G` para separarlas.

**Recomendado** (deja cada pantalla como frame de verdad, necesario para prototipar):

1. Arrastra los archivos `01`–`22` al lienzo.
2. Selecciona uno, `Ctrl/Cmd + Alt + G` para envolverlo en un frame.
3. Fija **W 390 · H 844** en el panel derecho.
4. Renombra el frame (ej. `16 · Método de pago`).
5. Los dos user flow van en una página aparte.

## Nombres de capa

| Prefijo | Qué agrupa |
|---|---|
| `BTN_` | Botones |
| `LINK_` | Enlaces de texto |
| `NAV_` | Destinos de la barra inferior |
| `TAB_` | Pestañas |
| `CHIP_` | Filtros, horarios y estados seleccionables |
| `CARD_` | Tarjetas que abren un detalle |
| `INPUT_` | Campos y áreas de texto |
| `OPT_` | Filas de menú con chevron |
| `SWITCH_` / `SLIDER_` | Controles de estado y rango |
| `ICO_` | Iconos (atrás, notificaciones, filtros) |
| `IMG_` | Cuadros con X: marcadores de imagen |
| `PACIENTE_`, `FRANJA_`, `NOTIF_`, `PAGO_`, `RESENA_`, `CAT_`, `DIA_`, `ITEM_`, `DATO_` | Elementos de lista |

Van con el número de pantalla al frente: `16_BTN_Pagar_y_confirmar`.

## Mapa de conexiones

Pestaña **Prototype** → arrastra el nodo azul desde la capa hasta la pantalla destino →
`On click · Navigate to`.

### Entrada

| Desde | Capa | Va a |
|---|---|---|
| 1 Login | `01_BTN_Ingresar` | 2 Home |
| 1 Login | `01_BTN_Rol_Medico` | 7 Dashboard |
| 1 Login | `01_LINK_Registrate` | 11 Registro |
| 11 Registro | `11_BTN_Crear_cuenta` | 2 Home |
| 11 Registro | `11_LINK_Iniciar_sesion` | 1 Login |

### Reservar una cita (recorrido principal)

| Desde | Capa | Va a |
|---|---|---|
| 2 Home | `02_INPUT_Buscador_destacado` | 3 Resultados |
| 2 Home | `02_CAT_Cardiología` | 3 Resultados |
| 2 Home | `02_BTN_Filtros` | 12 Filtros |
| 3 Resultados | `03_CARD_Dra_Laura_Gómez` | 4 Detalle |
| 3 Resultados | `03_ICO_Accion_superior` | 12 Filtros |
| 12 Filtros | `12_BTN_Aplicar_filtros` | 3 Resultados |
| 4 Detalle | `04_BTN_Reservar_Cita` | 5 Agenda |
| 4 Detalle | `04_TAB_Valoraciones` | 13 Valoraciones |
| 13 Valoraciones | `13_ICO_Atras` | 4 Detalle |
| 5 Agenda | `05_BTN_Confirmar_Cita` | 16 Pago |
| 16 Pago | `16_BTN_Pagar_y_confirmar` | 6 Confirmación |
| 6 Confirmación | `06_BTN_Ver_mis_citas` | 10 Mis Citas |
| 6 Confirmación | `06_LINK_Volver_al_inicio` | 2 Home |

### Gestionar una cita ya reservada

| Desde | Capa | Va a |
|---|---|---|
| 10 Mis Citas | `10_BTN_Ver_detalle_Dra_Laura_Gómez` | 14 Detalle de la cita |
| 10 Mis Citas | `10_BTN_Ver_detalle_Dr_Andrés_Rojas` | 17 Teleconsulta |
| 14 Detalle | `14_BTN_Cancelar` | 15 Cancelar cita |
| 14 Detalle | `14_BTN_Reprogramar` | 5 Agenda |
| 15 Cancelar | `15_BTN_Confirmar_cancelacion` | 10 Mis Citas |
| 15 Cancelar | `15_BTN_Volver` | 14 Detalle de la cita |

### Cuenta del paciente

| Desde | Capa | Va a |
|---|---|---|
| 2 Home | `02_ICO_Notificaciones` | 18 Notificaciones |
| 19 Perfil | `19_OPT_Hoja_vida` | 8 Hoja de Vida |
| 19 Perfil | `19_OPT_Pagos` | 16 Pago |
| 19 Perfil | `19_OPT_Notificaciones` | 18 Notificaciones |
| 19 Perfil | `19_BTN_Cerrar_sesion` | 1 Login |

### Recorrido del médico

| Desde | Capa | Va a |
|---|---|---|
| 7 Dashboard | `07_CITA_8_00_Camila_Ruiz` | 8 Hoja de Vida |
| 7 Dashboard | `07_BTN_Bloquear_horario` | 21 Gestión de Agenda |
| 7 Dashboard | `07_BTN_Confirmar_disponibilidad` | 21 Gestión de Agenda |
| 20 Pacientes | `20_PACIENTE_Camila_Ruiz` | 8 Hoja de Vida |
| 8 Hoja de Vida | `08_BTN_Nota_rapida` | 22 Registrar Consulta |
| 22 Registrar | `22_BTN_Firmar_guardar` | 8 Hoja de Vida |
| 21 Gestión | `21_BTN_Guardar_cambios` | 7 Dashboard |

### Barras inferiores

**Paciente** (pantallas 2, 3, 10, 18, 19): `NAV_Inicio` → 2 · `NAV_Buscar` → 3 ·
`NAV_Mis_Citas` → 10 · `NAV_Perfil` → 19

**Médico** (pantallas 7 y 20): `NAV_Agenda` → 7 · `NAV_Pacientes` → 20 ·
`NAV_Historial` → 22 · `NAV_Perfil` → 9

> Truco: conecta una barra, conviértela en componente (`Ctrl/Cmd + Alt + K`) y reemplaza
> las demás por instancias. Las conexiones viajan con el componente.

## Regenerar

```bash
python3 figma-scripts/build-svg.py
```
