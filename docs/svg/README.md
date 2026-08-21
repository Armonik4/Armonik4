# Paquete SVG · SaludConecta

Las 10 pantallas del wireframe + la página de user flow, listas para importar a Figma.
Cada elemento interactivo lleva su propio nombre de capa, para que conectar el prototipo
sea buscar por nombre y arrastrar.

## Contenido

| Archivo | Qué es | Tamaño |
|---|---|---|
| `00-hoja-completa.svg` | Las 10 pantallas en una sola lámina, ya ordenadas en 2 filas de 5 | 2270 × 2058 |
| `01-login.svg` | Login · Credenciales, con selector de rol | 390 × 844 |
| `02-home-paciente.svg` | Home del paciente: buscador destacado + especialidades | 390 × 844 |
| `03-resultado-busqueda.svg` | Lista de médicos con filtros | 390 × 844 |
| `04-detalle-medico.svg` | Perfil del médico + CTA "Reservar Cita" | 390 × 844 |
| `05-agenda-fecha-hora.svg` | Calendario y franjas horarias | 390 × 844 |
| `06-confirmacion.svg` | Pantalla de éxito con resumen de la cita | 390 × 844 |
| `07-dashboard-medico.svg` | Panel del médico: agenda del día | 390 × 844 |
| `08-hoja-vida-paciente.svg` | Historia clínica del paciente | 390 × 844 |
| `09-hoja-vida-medico.svg` | Hoja de vida profesional con especialidad | 390 × 844 |
| `10-mis-citas.svg` | Próximas citas, historial y recordatorio | 390 × 844 |
| `11-user-flow.svg` | Los dos recorridos (paciente y médico) | 1620 × 620 |

## Cómo importarlos

**Opción rápida:** arrastra `00-hoja-completa.svg` al lienzo. Entran las 10 pantallas
de una vez, ya distribuidas y con su título encima. Después desagrupa (`Ctrl/Cmd +
Shift + G`) para separarlas.

**Opción recomendada** (deja cada pantalla como un frame de verdad, que es lo que
necesitas para prototipar):

1. Arrastra los archivos `01`–`10` al lienzo, uno por uno o todos juntos.
2. Selecciona uno y pulsa `Ctrl/Cmd + Alt + G` para envolverlo en un frame.
3. En el panel derecho fija **W 390 · H 844**.
4. Renombra el frame con doble clic en la capa (ej. `4 · Detalle del Médico`).
5. Repite. Al final, `11-user-flow.svg` va en una página aparte.

## Nombres de capa

Cada capa lleva un prefijo que dice qué es. Búscalos con el buscador del panel de capas.

| Prefijo | Qué agrupa |
|---|---|
| `BTN_` | Botones — lo que vas a conectar |
| `LINK_` | Enlaces de texto (también conectables) |
| `NAV_` | Cada destino de la barra inferior |
| `TAB_` | Pestañas |
| `CHIP_` | Filtros y horarios seleccionables |
| `CARD_` | Tarjetas que abren un detalle |
| `INPUT_` | Campos de formulario |
| `ICO_` | Iconos (atrás, notificaciones, filtros) |
| `IMG_` | Cuadros con X: marcadores de imagen |
| `CAT_`, `DIA_`, `ITEM_`, `DATO_`, `HIST_`, `CITA_` | Elementos de lista y datos |

Van con el número de pantalla al frente: `04_BTN_Reservar_Cita`.

## Mapa de conexiones del prototipo

Pestaña **Prototype** → arrastra el nodo azul desde la capa hasta la pantalla destino →
`On click · Navigate to`.

### Recorrido del paciente

| Desde | Capa | Va a |
|---|---|---|
| 1 Login | `01_BTN_Ingresar` | 2 Home |
| 1 Login | `01_BTN_Rol_Medico` | 7 Dashboard |
| 2 Home | `02_INPUT_Buscador_destacado` | 3 Resultados |
| 2 Home | `02_CAT_Cardiología` | 3 Resultados |
| 2 Home | `02_BTN_Ver_proxima_cita` | 4 Detalle |
| 3 Resultados | `03_CARD_Dra_Laura_Gómez` | 4 Detalle |
| 3 Resultados | `03_ICO_Atras` | 2 Home |
| 4 Detalle | `04_BTN_Reservar_Cita` | 5 Agenda |
| 4 Detalle | `04_CHIP_Horario_Hoy_3_00_PM` | 5 Agenda |
| 4 Detalle | `04_ICO_Atras` | 3 Resultados |
| 5 Agenda | `05_BTN_Confirmar_Cita` | 6 Confirmación |
| 5 Agenda | `05_ICO_Atras` | 4 Detalle |
| 6 Confirmación | `06_BTN_Ver_mis_citas` | 10 Mis Citas |
| 6 Confirmación | `06_LINK_Volver_al_inicio` | 2 Home |
| 10 Mis Citas | `10_BTN_Ver_detalle_Dra_Laura_Gómez` | 4 Detalle |

### Recorrido del médico

| Desde | Capa | Va a |
|---|---|---|
| 7 Dashboard | `07_CITA_8_00_Camila_Ruiz` | 8 Hoja de Vida Paciente |
| 7 Dashboard | `07_NAV_Pacientes` | 8 Hoja de Vida Paciente |
| 7 Dashboard | `07_NAV_Perfil` | 9 Hoja de Vida Médico |
| 8 Hoja de Vida | `08_ICO_Atras` | 7 Dashboard |
| 9 Hoja de Vida | `09_BTN_Reservar_Cita` | 5 Agenda |

### Barra inferior (repetir en 2, 3 y 10)

`NAV_Inicio` → 2 Home · `NAV_Buscar` → 3 Resultados · `NAV_Mis_Citas` → 10 Mis Citas ·
`NAV_Perfil` → 8 Hoja de Vida Paciente

> Truco: conecta la barra una sola vez, conviértela en componente
> (`Ctrl/Cmd + Alt + K`) y reemplaza las demás por instancias. Las conexiones viajan
> con el componente.

## Regenerar

```bash
python3 figma-scripts/build-svg.py
```

Edita textos, tamaños o pantallas en `figma-scripts/build-svg.py` y vuelve a correrlo.
