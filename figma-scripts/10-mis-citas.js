/*
 * PENDIENTE DE EJECUTAR · Pantalla 10 · Mis Citas (Paciente)
 * Posición en el canvas: x=1880, y=980 (fila 2, columna 5) de la página "01 · Wireframes Lo-Fi".
 * Requiere: pegar antes el contenido de 00-helpers.js
 */

const page1 = figma.root.children[0];
const s10 = SCREEN('10 · Mis Citas (Paciente)', 1880, 980, page1);
s10.appendChild(STATUS());

const ab = AL('HORIZONTAL', { name: 'App bar', paddingLeft: 16, paddingRight: 16, paddingTop: 8, paddingBottom: 10, counterAxisAlignItems: 'CENTER', itemSpacing: 12 });
ab.appendChild(T('Mis Citas', { s: 20, st: 'Bold' }));
SPC(ab);
ab.appendChild(R(26, 26, { fill: 1, r: 6, stroke: 0.55 }));
s10.appendChild(ab);
ab.layoutSizingHorizontal = 'FILL';

const c = CONTENT(s10, { gap: 12, pad: 20 });

// Tabs Próximas / Historial
const tabs = AL('HORIZONTAL', { name: 'Tabs', itemSpacing: 0 });
c.appendChild(tabs);
tabs.layoutSizingHorizontal = 'FILL';
['Próximas (2)', 'Historial (8)'].forEach((l, i) => {
  const t = AL('VERTICAL', { itemSpacing: 8, counterAxisAlignItems: 'CENTER' });
  t.appendChild(T(l, { s: 13, st: i === 0 ? 'Semi Bold' : 'Regular', col: i === 0 ? 0.13 : 0.5 }));
  const u = R(60, i === 0 ? 3 : 1, { fill: i === 0 ? 0.2 : 0.85 });
  t.appendChild(u);
  tabs.appendChild(t);
  t.layoutSizingHorizontal = 'FILL';
  u.layoutSizingHorizontal = 'FILL';
});

// Banner de recordatorio (requisito: "recordatorios de próximas consultas")
const ban = AL('HORIZONTAL', { name: 'Recordatorio', itemSpacing: 10, counterAxisAlignItems: 'CENTER', paddingLeft: 12, paddingRight: 12, paddingTop: 10, paddingBottom: 10 });
c.appendChild(ban);
ban.layoutSizingHorizontal = 'FILL';
ban.cornerRadius = 10;
ban.fills = [g(0.94)];
ban.strokes = [g(0.7)];
ban.strokeWeight = 1;
ban.dashPattern = [5, 4];
ban.appendChild(R(22, 22, { fill: 0.6, r: 6 }));
const bt = T('Recordatorio: tu próxima cita es mañana a las 10:30 AM.', { s: 12, col: 0.25 });
ban.appendChild(bt);
bt.textAutoResize = 'HEIGHT';
bt.layoutSizingHorizontal = 'FILL';

const CITA = (estado, activo, nombre, spec, fecha, acciones) => {
  const cd = AL('VERTICAL', { name: 'Cita · ' + nombre, itemSpacing: 10, paddingLeft: 12, paddingRight: 12, paddingTop: 12, paddingBottom: 12 });
  cd.cornerRadius = 10; cd.fills = [g(1)]; cd.strokes = [g(0.75)]; cd.strokeWeight = 1;
  const top = AL('HORIZONTAL', { itemSpacing: 12, counterAxisAlignItems: 'CENTER' });
  cd.appendChild(top); top.layoutSizingHorizontal = 'FILL';
  top.appendChild(CIRC(46));
  const col = AL('VERTICAL', { itemSpacing: 3 });
  top.appendChild(col); col.layoutSizingHorizontal = 'FILL';
  const n = T(nombre, { s: 14, st: 'Semi Bold' });
  col.appendChild(n); n.textAutoResize = 'HEIGHT'; n.layoutSizingHorizontal = 'FILL'; n.maxLines = 1; n.textTruncation = 'ENDING';
  const sp = T(spec, { s: 11, col: 0.45 });
  col.appendChild(sp); sp.textAutoResize = 'HEIGHT'; sp.layoutSizingHorizontal = 'FILL';
  const fe = T(fecha, { s: 12, st: 'Medium', col: 0.2 });
  col.appendChild(fe); fe.textAutoResize = 'HEIGHT'; fe.layoutSizingHorizontal = 'FILL';
  top.appendChild(CHIP(estado, activo, { s: 10 }));
  const div = R(320, 1, { fill: 0.88 });
  cd.appendChild(div); div.layoutSizingHorizontal = 'FILL';
  const acts = AL('HORIZONTAL', { itemSpacing: 8 });
  cd.appendChild(acts); acts.layoutSizingHorizontal = 'FILL';
  acciones.forEach((a, i) => {
    const b = BTN(a, { primary: i === acciones.length - 1 && acciones.length > 1, w: 100, h: 36, s: 12 });
    acts.appendChild(b); b.layoutSizingHorizontal = 'FILL';
  });
  c.appendChild(cd); cd.layoutSizingHorizontal = 'FILL';
  return cd;
};
CITA('Confirmada', true, 'Dra. Laura Gómez', 'Cardiología · Presencial · Clínica Norte', 'Mié 21 Ago · 10:30 AM', ['Reprogramar', 'Ver detalle']);
CITA('Pendiente', false, 'Dr. Andrés Rojas', 'Medicina General · Virtual', 'Vie 30 Ago · 4:00 PM', ['Cancelar', 'Ver detalle']);

c.appendChild(T('Historial de consultas', { s: 14, st: 'Semi Bold' }));
const HIST = (nombre, spec, fecha) => {
  const r = AL('HORIZONTAL', { name: 'Historial · ' + nombre, itemSpacing: 10, counterAxisAlignItems: 'CENTER', paddingLeft: 12, paddingRight: 12, paddingTop: 10, paddingBottom: 10 });
  r.cornerRadius = 8; r.fills = [g(0.98)]; r.strokes = [g(0.8)]; r.strokeWeight = 1;
  r.appendChild(CIRC(36));
  const col = AL('VERTICAL', { itemSpacing: 2 });
  r.appendChild(col); col.layoutSizingHorizontal = 'FILL';
  const a = T(nombre, { s: 13, st: 'Semi Bold' });
  col.appendChild(a); a.textAutoResize = 'HEIGHT'; a.layoutSizingHorizontal = 'FILL'; a.maxLines = 1; a.textTruncation = 'ENDING';
  const b = T(spec + ' · ' + fecha, { s: 11, col: 0.45 });
  col.appendChild(b); b.textAutoResize = 'HEIGHT'; b.layoutSizingHorizontal = 'FILL'; b.maxLines = 1; b.textTruncation = 'ENDING';
  r.appendChild(CHIP('Ver resumen', false, { s: 10 }));
  c.appendChild(r); r.layoutSizingHorizontal = 'FILL';
  return r;
};
HIST('Dra. Laura Gómez', 'Cardiología', '12 Jun 2025');
HIST('Dr. Andrés Rojas', 'Medicina General', '03 Mar 2025');

NAV(s10, 2, ['Inicio', 'Buscar', 'Mis Citas', 'Perfil']);

return { createdNodeIds: [s10.id] };
