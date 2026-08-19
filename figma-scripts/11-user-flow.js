/*
 * PENDIENTE DE EJECUTAR · Página "02 · User Flow" (Paso 1 de la guía de la tarea)
 * Dibuja los dos flujos de usuario con cajas y flechas.
 * Requiere: pegar antes el contenido de 00-helpers.js
 * Nota: en archivos de diseño (no FigJam) no existen conectores; se usan cajas + flechas de texto.
 */

const page2 = figma.root.children.find(p => p.name.indexOf('User Flow') > -1);
await figma.setCurrentPageAsync(page2);

const created = [];

// Caja de paso del flujo
const STEP = (num, titulo, sub, destacado) => {
  const b = AL('VERTICAL', { name: 'Paso · ' + titulo, itemSpacing: 6, paddingLeft: 14, paddingRight: 14, paddingTop: 12, paddingBottom: 12 });
  b.resize(180, 10);
  b.cornerRadius = 12;
  b.fills = [g(destacado ? 0.2 : 1)];
  b.strokes = [g(destacado ? 0.2 : 0.6)];
  b.strokeWeight = 1.5;
  b.layoutSizingVertical = 'HUG';
  const tag = AL('HORIZONTAL', { paddingLeft: 8, paddingRight: 8, paddingTop: 3, paddingBottom: 3 });
  tag.cornerRadius = 10;
  tag.fills = [g(destacado ? 0.35 : 0.92)];
  tag.appendChild(T(num, { s: 10, st: 'Bold', col: destacado ? 1 : 0.3 }));
  b.appendChild(tag);
  const t1 = T(titulo, { s: 14, st: 'Semi Bold', col: destacado ? 1 : 0.13 });
  b.appendChild(t1); t1.textAutoResize = 'HEIGHT'; t1.layoutSizingHorizontal = 'FILL';
  const t2 = T(sub, { s: 11, col: destacado ? 0.8 : 0.45 });
  b.appendChild(t2); t2.textAutoResize = 'HEIGHT'; t2.layoutSizingHorizontal = 'FILL';
  return b;
};

const ARROW = () => T('→', { s: 22, col: 0.45 });

// Carril horizontal con pasos y flechas intercaladas
const LANE = (titulo, descripcion, pasos, x, y) => {
  const lane = AL('VERTICAL', { name: 'Carril · ' + titulo, itemSpacing: 16, paddingLeft: 24, paddingRight: 24, paddingTop: 20, paddingBottom: 24 });
  figma.currentPage.appendChild(lane);
  lane.x = x; lane.y = y;
  lane.cornerRadius = 16;
  lane.fills = [g(0.97)];
  lane.strokes = [g(0.85)];
  lane.strokeWeight = 1;
  const head = AL('VERTICAL', { itemSpacing: 4 });
  lane.appendChild(head);
  head.appendChild(T(titulo, { s: 20, st: 'Bold' }));
  head.appendChild(T(descripcion, { s: 13, col: 0.45 }));
  const row = AL('HORIZONTAL', { itemSpacing: 12, counterAxisAlignItems: 'CENTER' });
  lane.appendChild(row);
  pasos.forEach((p, i) => {
    if (i > 0) row.appendChild(ARROW());
    row.appendChild(STEP(String(i + 1).padStart(2, '0'), p[0], p[1], !!p[2]));
  });
  created.push(lane.id);
  return lane;
};

// Título de la página
const head = AL('VERTICAL', { itemSpacing: 6 });
figma.currentPage.appendChild(head);
head.x = 0; head.y = -140;
head.appendChild(T('User Flow · SaludConecta', { s: 44, st: 'Bold' }));
head.appendChild(T('Paso 1 de la guía: trazar el camino antes de dibujar. Dos roles, dos recorridos.', { s: 18, col: 0.4 }));
created.push(head.id);

LANE(
  'Flujo Paciente',
  'Camino principal: sacar una cita en 5 toques desde el Home.',
  [
    ['Login', 'Elige rol: Paciente'],
    ['Home', 'Buscador + especialidades'],
    ['Resultados', 'Filtra por cercanía/precio'],
    ['Detalle Médico', 'Currículum y valoraciones'],
    ['Agenda', 'Fecha, hora y modalidad'],
    ['Confirmación', 'Cita agendada', true],
    ['Mis Citas', 'Historial y recordatorios']
  ],
  0, 0
);

LANE(
  'Flujo Médico Especialista',
  'Camino principal: revisar la agenda del día y gestionar disponibilidad.',
  [
    ['Login', 'Elige rol: Médico'],
    ['Dashboard', 'Resumen de la agenda del día', true],
    ['Panel Pacientes', 'Personas citadas hoy'],
    ['Hoja de Vida Paciente', 'Antecedentes y alergias'],
    ['Nota rápida', 'Registra la consulta'],
    ['Gestión de Agenda', 'Bloquear o confirmar horarios']
  ],
  0, 380
);

return { createdNodeIds: created };
