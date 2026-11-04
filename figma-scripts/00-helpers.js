/*
 * SaludConecta · Kit de wireframes Lo-Fi
 * Helpers compartidos para la Figma Plugin API (MCP: use_figma).
 *
 * Pega este bloque al inicio de cada script antes de construir una pantalla.
 * Paleta 100% escala de grises: los wireframes de baja fidelidad no usan color.
 */

await Promise.all(['Regular', 'Medium', 'Semi Bold', 'Bold']
  .map(s => figma.loadFontAsync({ family: 'Inter', style: s })));

// gris 0..1
const g = v => ({ type: 'SOLID', color: { r: v, g: v, b: v } });

// Texto
const T = (c, o = {}) => {
  const { s = 14, st = 'Regular', col = 0.13, w = 0, al = 'LEFT' } = o;
  const t = figma.createText();
  t.fontName = { family: 'Inter', style: st };
  t.characters = c;
  t.fontSize = s;
  t.lineHeight = { unit: 'PERCENT', value: 140 };
  t.fills = [g(col)];
  t.textAlignHorizontal = al;
  if (w) { t.textAutoResize = 'HEIGHT'; t.resize(w, t.height); }
  return t;
};

// Rectángulo / línea de texto simulada
const R = (w, h, o = {}) => {
  const { fill = 0.88, r = 0, stroke = null } = o;
  const x = figma.createRectangle();
  x.resize(w, h);
  x.cornerRadius = r;
  x.fills = [g(fill)];
  if (stroke !== null) { x.strokes = [g(stroke)]; x.strokeWeight = 1; }
  return x;
};

// Auto-layout SIN relleno por defecto (evita cajas blancas sobre fondos oscuros)
const AL = (d, p = {}) => { const f = figma.createAutoLayout(d, p); f.fills = []; return f; };

// Espaciador elástico
const SPC = p => { const s = figma.createFrame(); s.resize(10, 10); s.fills = []; p.appendChild(s); s.layoutSizingHorizontal = 'FILL'; return s; };

// Avatar / imagen circular
const CIRC = (d, fill = 0.92) => {
  const e = figma.createEllipse();
  e.resize(d, d);
  e.fills = [g(fill)];
  e.strokes = [g(0.72)];
  e.strokeWeight = 1;
  return e;
};

// Caja de imagen con "X" (convención de wireframe lo-fi)
const IMG = (w, h) => {
  const f = figma.createFrame();
  f.resize(w, h);
  f.name = 'Imagen';
  f.fills = [g(0.97)];
  f.strokes = [g(0.72)];
  f.strokeWeight = 1;
  const v = figma.createVector();
  f.appendChild(v);
  v.vectorPaths = [{ windingRule: 'NONE', data: `M 0 0 L ${w} ${h} M ${w} 0 L 0 ${h}` }];
  v.fills = []; v.strokes = [g(0.72)]; v.strokeWeight = 1;
  v.x = 0; v.y = 0;
  v.constraints = { horizontal: 'STRETCH', vertical: 'STRETCH' };
  return f;
};

// Botón de acción (CTA). primary = relleno oscuro
const BTN = (label, o = {}) => {
  const { primary = true, w = 350, h = 52, s = 16 } = o;
  const b = AL('HORIZONTAL', { name: 'Botón · ' + label, primaryAxisAlignItems: 'CENTER', counterAxisAlignItems: 'CENTER' });
  b.resize(w, h);
  b.cornerRadius = 10;
  b.fills = [g(primary ? 0.2 : 1)];
  if (!primary) { b.strokes = [g(0.4)]; b.strokeWeight = 1.5; }
  b.appendChild(T(label, { s, st: 'Semi Bold', col: primary ? 1 : 0.2 }));
  return b;
};

// Chip / filtro
const CHIP = (label, active = false, o = {}) => {
  const { s = 11 } = o;
  const c = AL('HORIZONTAL', { name: 'Chip', paddingLeft: 12, paddingRight: 12, paddingTop: 6, paddingBottom: 6, primaryAxisAlignItems: 'CENTER', counterAxisAlignItems: 'CENTER' });
  c.cornerRadius = 16;
  c.fills = [g(active ? 0.25 : 1)];
  c.strokes = [g(active ? 0.25 : 0.75)];
  c.strokeWeight = 1;
  c.appendChild(T(label, { s, col: active ? 1 : 0.35, st: 'Medium' }));
  return c;
};

// Barra de estado del sistema
const STATUS = (dark = false) => {
  const b = AL('HORIZONTAL', { name: 'Status bar', paddingLeft: 20, paddingRight: 20, counterAxisAlignItems: 'CENTER', itemSpacing: 6 });
  b.resize(390, 44);
  b.fills = [g(dark ? 0.18 : 1)];
  b.appendChild(T('9:41', { s: 12, st: 'Semi Bold', col: dark ? 1 : 0.13 }));
  SPC(b);
  [10, 12, 20].forEach(w => b.appendChild(R(w, 10, { fill: 0.75, r: 2 })));
  return b;
};

// Marco de pantalla 390x844 (iPhone 14)
const SCREEN = (name, x, y, page) => {
  const f = AL('VERTICAL', { name });
  f.resize(390, 844);
  f.fills = [g(1)];
  f.strokes = [g(0.55)];
  f.strokeWeight = 1;
  f.clipsContent = true;
  (page || figma.currentPage).appendChild(f);
  f.x = x; f.y = y;
  return f;
};

// Área de contenido elástica entre la status bar y la nav inferior
const CONTENT = (f, o = {}) => {
  const { pad = 20, gap = 16 } = o;
  const c = AL('VERTICAL', { name: 'Contenido', itemSpacing: gap, paddingLeft: pad, paddingRight: pad, paddingTop: pad, paddingBottom: pad });
  f.appendChild(c);
  c.layoutSizingHorizontal = 'FILL';
  c.layoutSizingVertical = 'FILL';
  return c;
};

// Barra superior con botón atrás
const APPBAR = (f, title, right) => {
  const b = AL('HORIZONTAL', { name: 'App bar', paddingLeft: 16, paddingRight: 16, paddingTop: 8, paddingBottom: 10, counterAxisAlignItems: 'CENTER', itemSpacing: 12 });
  b.appendChild(R(26, 26, { fill: 1, r: 6, stroke: 0.55 }));
  b.appendChild(T(title, { s: 16, st: 'Semi Bold' }));
  SPC(b);
  if (right) b.appendChild(R(26, 26, { fill: 1, r: 6, stroke: 0.55 }));
  f.appendChild(b);
  b.layoutSizingHorizontal = 'FILL';
  return b;
};

// Navegación inferior (4 destinos). labels cambia según el rol.
const NAV = (f, active, labels) => {
  const wrap = AL('VERTICAL', { name: 'Nav inferior', itemSpacing: 0 });
  wrap.resize(390, 64);
  wrap.fills = [g(0.99)];
  const div = R(390, 1, { fill: 0.8 });
  wrap.appendChild(div);
  div.layoutSizingHorizontal = 'FILL';
  const row = AL('HORIZONTAL', { itemSpacing: 0, paddingTop: 10, counterAxisAlignItems: 'CENTER' });
  wrap.appendChild(row);
  row.layoutSizingHorizontal = 'FILL';
  labels.forEach((it, i) => {
    const cl = AL('VERTICAL', { itemSpacing: 5, counterAxisAlignItems: 'CENTER' });
    row.appendChild(cl);
    cl.layoutSizingHorizontal = 'FILL';
    cl.appendChild(R(22, 22, { fill: i === active ? 0.3 : 0.82, r: 6 }));
    cl.appendChild(T(it, { s: 10, col: i === active ? 0.2 : 0.5 }));
  });
  f.appendChild(wrap);
  wrap.layoutSizingHorizontal = 'FILL';
  return wrap;
};

// Barra de acción inferior fija (precio + CTA)
const BAR = f => {
  const w = AL('VERTICAL', { name: 'Barra de acción', itemSpacing: 0 });
  f.appendChild(w);
  w.layoutSizingHorizontal = 'FILL';
  const d = R(390, 1, { fill: 0.8 });
  w.appendChild(d);
  d.layoutSizingHorizontal = 'FILL';
  const r = AL('HORIZONTAL', { paddingLeft: 20, paddingRight: 20, paddingTop: 14, paddingBottom: 20, itemSpacing: 14, counterAxisAlignItems: 'CENTER' });
  w.appendChild(r);
  r.layoutSizingHorizontal = 'FILL';
  r.fills = [g(1)];
  return r;
};
