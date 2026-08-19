#!/usr/bin/env python3
"""
Genera los entregables pendientes como SVG importables a Figma.

Motivo: el plan Starter de Figma permite solo 20 llamadas MCP al mes y la cuota
se agotó construyendo las 9 primeras pantallas. Estos SVG se arrastran al archivo
de Figma y quedan como capas editables, sin consumir cuota.

Salida:
  docs/svg/10-mis-citas.svg   -> pantalla 10, marco de 390x844
  docs/svg/02-user-flow.svg   -> página de user flow (dos carriles)
"""
import os
import html

FONT = "Inter, 'Helvetica Neue', Arial, sans-serif"


def gray(v):
    n = round(v * 255)
    return f"rgb({n},{n},{n})"


def rect(x, y, w, h, fill=None, stroke=None, r=0, sw=1, dash=None, name=""):
    parts = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"']
    if r:
        parts.append(f' rx="{r}"')
    parts.append(f' fill="{gray(fill) if fill is not None else "none"}"')
    if stroke is not None:
        parts.append(f' stroke="{gray(stroke)}" stroke-width="{sw}"')
    if dash:
        parts.append(f' stroke-dasharray="{dash}"')
    if name:
        parts.append(f' data-name="{html.escape(name)}"')
    parts.append("/>")
    return "".join(parts)


def circle(cx, cy, rad, fill=0.92, stroke=0.72):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rad:.1f}" fill="{gray(fill)}" '
            f'stroke="{gray(stroke)}" stroke-width="1"/>')


def text(x, y, s, size=14, weight=400, fill=0.13, anchor="start"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{gray(fill)}" text-anchor="{anchor}" '
            f'dominant-baseline="middle">{html.escape(s)}</text>')


def chip(x, y, label, active=False, size=10):
    w = len(label) * size * 0.62 + 24
    h = size + 14
    out = [rect(x, y, w, h, fill=0.25 if active else 1.0,
                stroke=0.25 if active else 0.75, r=h / 2)]
    out.append(text(x + w / 2, y + h / 2, label, size=size, weight=500,
                    fill=1.0 if active else 0.35, anchor="middle"))
    return "".join(out), w, h


def button(x, y, w, h, label, primary=True, size=13):
    out = [rect(x, y, w, h, fill=0.2 if primary else 1.0,
                stroke=None if primary else 0.4, r=10, sw=1.5)]
    out.append(text(x + w / 2, y + h / 2, label, size=size, weight=600,
                    fill=1.0 if primary else 0.2, anchor="middle"))
    return "".join(out)


def status_bar(o):
    o.append(text(20, 22, "9:41", size=12, weight=600))
    for i, w in enumerate([10, 12, 20]):
        xs = [330, 344, 360]
        o.append(rect(xs[i], 17, w, 10, fill=0.75, r=2))


def nav_bar(o, y, labels, active):
    o.append(rect(0, y, 390, 64, fill=0.99))
    o.append(rect(0, y, 390, 1, fill=0.8))
    step = 390 / len(labels)
    for i, lab in enumerate(labels):
        cx = step * i + step / 2
        o.append(rect(cx - 11, y + 12, 22, 22, fill=0.3 if i == active else 0.82, r=6))
        o.append(text(cx, y + 46, lab, size=10, fill=0.2 if i == active else 0.5,
                      anchor="middle"))


# --------------------------------------------------------------------------
# Pantalla 10 · Mis Citas
# --------------------------------------------------------------------------
def screen_mis_citas():
    W, H, PAD, CW = 390, 844, 20, 350
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">',
         rect(0, 0, W, H, fill=1.0, stroke=0.55)]

    status_bar(o)

    # App bar
    o.append(text(PAD, 66, "Mis Citas", size=20, weight=700))
    o.append(rect(344, 53, 26, 26, fill=1.0, stroke=0.55, r=6))

    y = 100
    # Tabs
    for i, lab in enumerate(["Próximas (2)", "Historial (8)"]):
        cx = PAD + CW / 4 + (CW / 2) * i
        o.append(text(cx, y + 9, lab, size=13, weight=600 if i == 0 else 400,
                      fill=0.13 if i == 0 else 0.5, anchor="middle"))
        o.append(rect(PAD + (CW / 2) * i, y + 24, CW / 2, 3 if i == 0 else 1,
                      fill=0.2 if i == 0 else 0.85))
    y += 39

    # Banner de recordatorio
    o.append(rect(PAD, y, CW, 44, fill=0.94, stroke=0.7, r=10, dash="5 4"))
    o.append(rect(PAD + 12, y + 11, 22, 22, fill=0.6, r=6))
    o.append(text(PAD + 44, y + 22, "Recordatorio: tu próxima cita es mañana a las 10:30 AM.",
                  size=12, fill=0.25))
    y += 56

    def cita(y, estado, activo, nombre, spec, fecha, acciones):
        h = 140
        o.append(rect(PAD, y, CW, h, fill=1.0, stroke=0.75, r=10))
        o.append(circle(PAD + 12 + 23, y + 12 + 29, 23))
        tx = PAD + 12 + 46 + 12
        o.append(text(tx, y + 24, nombre, size=14, weight=600))
        o.append(text(tx, y + 43, spec, size=11, fill=0.45))
        o.append(text(tx, y + 62, fecha, size=12, weight=500, fill=0.2))
        cs, cw, ch = chip(PAD + CW - 12 - (len(estado) * 6.2 + 24), y + 24 - ch_off,
                          estado, activo)
        o.append(cs)
        o.append(rect(PAD + 12, y + 82, CW - 24, 1, fill=0.88))
        bw = (CW - 24 - 8) / 2
        for i, a in enumerate(acciones):
            o.append(button(PAD + 12 + i * (bw + 8), y + 92, bw, 36, a,
                            primary=(i == len(acciones) - 1), size=12))
        return h

    ch_off = 6
    y += cita(y, "Confirmada", True, "Dra. Laura Gómez",
              "Cardiología · Presencial", "Mié 21 Ago · 10:30 AM",
              ["Reprogramar", "Ver detalle"]) + 12
    y += cita(y, "Pendiente", False, "Dr. Andrés Rojas",
              "Medicina General · Virtual", "Vie 30 Ago · 4:00 PM",
              ["Cancelar", "Ver detalle"]) + 12

    o.append(text(PAD, y + 9, "Historial de consultas", size=14, weight=600))
    y += 30

    for nombre, spec in [("Dra. Laura Gómez", "Cardiología · 12 Jun 2025"),
                         ("Dr. Andrés Rojas", "Medicina General · 03 Mar 2025")]:
        o.append(rect(PAD, y, CW, 56, fill=0.98, stroke=0.8, r=8))
        o.append(circle(PAD + 12 + 18, y + 28, 18))
        o.append(text(PAD + 12 + 36 + 10, y + 21, nombre, size=13, weight=600))
        o.append(text(PAD + 12 + 36 + 10, y + 38, spec, size=11, fill=0.45))
        cs, cw, _ = chip(PAD + CW - 12 - 82, y + 16, "Ver resumen", False)
        o.append(cs)
        y += 68

    nav_bar(o, 780, ["Inicio", "Buscar", "Mis Citas", "Perfil"], 2)
    o.append("</svg>")
    return "\n".join(o)


# --------------------------------------------------------------------------
# User Flow
# --------------------------------------------------------------------------
BOX_W, BOX_H, ARROW_W, GAP = 180, 90, 30, 12


def flow_lane(o, x, y, titulo, descripcion, pasos):
    n = len(pasos)
    lane_w = 48 + n * BOX_W + (n - 1) * (ARROW_W + GAP * 2)
    lane_h = 24 + 52 + 16 + BOX_H + 24
    o.append(rect(x, y, lane_w, lane_h, fill=0.97, stroke=0.85, r=16))
    o.append(text(x + 24, y + 36, titulo, size=20, weight=700))
    o.append(text(x + 24, y + 60, descripcion, size=13, fill=0.45))

    bx = x + 24
    by = y + 24 + 52 + 16
    for i, (t, sub, destacado) in enumerate(pasos):
        if i > 0:
            o.append(text(bx + GAP + ARROW_W / 2, by + BOX_H / 2, "→", size=22,
                          fill=0.45, anchor="middle"))
            bx += GAP + ARROW_W + GAP
        o.append(rect(bx, by, BOX_W, BOX_H, fill=0.2 if destacado else 1.0,
                      stroke=0.2 if destacado else 0.6, r=12, sw=1.5))
        num = f"{i + 1:02d}"
        o.append(rect(bx + 14, by + 12, 26, 18, fill=0.35 if destacado else 0.92, r=9))
        o.append(text(bx + 27, by + 21, num, size=10, weight=700,
                      fill=1.0 if destacado else 0.3, anchor="middle"))
        o.append(text(bx + 14, by + 46, t, size=14, weight=600,
                      fill=1.0 if destacado else 0.13))
        o.append(text(bx + 14, by + 68, sub, size=10,
                      fill=0.8 if destacado else 0.45))
        bx += BOX_W
    return lane_w, lane_h


def user_flow():
    paciente = [
        ("Login", "Elige rol: Paciente", False),
        ("Home", "Buscador + especialidades", False),
        ("Resultados", "Filtra por cercanía", False),
        ("Detalle Médico", "Currículum y precio", False),
        ("Agenda", "Fecha, hora y modalidad", False),
        ("Confirmación", "Cita agendada", True),
        ("Mis Citas", "Historial y recordatorios", False),
    ]
    medico = [
        ("Login", "Elige rol: Médico", False),
        ("Dashboard", "Agenda del día", True),
        ("Panel Pacientes", "Citados hoy", False),
        ("Hoja de Vida", "Antecedentes y alergias", False),
        ("Nota rápida", "Registra la consulta", False),
        ("Gestión Agenda", "Bloquear horarios", False),
    ]
    tmp = []
    w1, h1 = flow_lane(tmp, 0, 0, "x", "x", paciente)
    W = w1 + 80
    H = 120 + h1 + 40 + h1 + 40

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">',
         rect(0, 0, W, H, fill=1.0)]
    o.append(text(40, 46, "User Flow · SaludConecta", size=34, weight=700))
    o.append(text(40, 80, "Paso 1 de la guía: trazar el camino antes de dibujar. "
                          "Dos roles, dos recorridos.", size=15, fill=0.4))

    y = 110
    _, h = flow_lane(o, 40, y, "Flujo Paciente",
                     "Camino principal: sacar una cita en 5 toques desde el Home.",
                     paciente)
    y += h + 32
    flow_lane(o, 40, y, "Flujo Médico Especialista",
              "Camino principal: revisar la agenda del día y gestionar disponibilidad.",
              medico)
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "docs", "svg")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "10-mis-citas.svg"), "w") as f:
        f.write(screen_mis_citas())
    with open(os.path.join(out, "02-user-flow.svg"), "w") as f:
        f.write(user_flow())
    print("SVG generados en", out)
