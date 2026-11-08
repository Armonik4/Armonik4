#!/usr/bin/env python3
"""
SaludConecta · Generador del paquete completo de wireframes en SVG.

Produce las 10 pantallas (390x844) + la página de user flow, listas para
arrastrar a Figma. Cada elemento interactivo va envuelto en un <g id="...">
para que al importar quede con nombre propio en el panel de capas y se pueda
conectar el prototipo sin buscar a ciegas.

Convenciones lo-fi del enunciado:
  - Solo escala de grises, sin color ni fotos.
  - Las imágenes son CUADROS CON UNA X.
  - Los bloques de texto de relleno son líneas horizontales grises.
  - Los CTA son grandes y de alto contraste.

Uso:  python3 figma-scripts/build-svg.py
"""
import os
import re
import html

FONT = "Inter, 'Helvetica Neue', Arial, sans-serif"
W, H = 390, 844
PAD, CW = 20, 350

_prefix = ""


def set_prefix(p):
    global _prefix
    _prefix = p


def gid(name, body):
    """Envuelve en un grupo con id -> Figma lo usa como nombre de capa."""
    safe = re.sub(r"[^0-9A-Za-z_\-áéíóúüñÁÉÍÓÚÜÑ]", "_", name)
    safe = re.sub(r"_+", "_", safe).strip("_")
    return f'<g id="{_prefix}{safe}">{body}</g>'


def gray(v):
    n = round(v * 255)
    return f"rgb({n},{n},{n})"


def tw(s, size, weight=400):
    """Ancho aproximado de un texto en Inter."""
    return len(s) * size * (0.60 if weight >= 500 else 0.565)


def rect(x, y, w, h, fill=None, stroke=None, r=0, sw=1, dash=None, op=None):
    p = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"']
    if r:
        p.append(f' rx="{r}"')
    p.append(f' fill="{gray(fill) if fill is not None else "none"}"')
    if stroke is not None:
        p.append(f' stroke="{gray(stroke)}" stroke-width="{sw}"')
    if dash:
        p.append(f' stroke-dasharray="{dash}"')
    if op is not None:
        p.append(f' opacity="{op}"')
    p.append("/>")
    return "".join(p)


def text(x, y, s, size=14, weight=400, fill=0.13, anchor="start"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{gray(fill)}" text-anchor="{anchor}" '
            f'dominant-baseline="middle">{html.escape(s)}</text>')


def path(d, stroke=0.6, sw=1, cap="butt"):
    return (f'<path d="{d}" fill="none" stroke="{gray(stroke)}" stroke-width="{sw}" '
            f'stroke-linecap="{cap}" stroke-linejoin="round"/>')


def xbox(x, y, w, h, r=6, fill=0.97, stroke=0.6):
    """Cuadro con X: el marcador de imagen que pide el enunciado."""
    i = 2
    return (rect(x, y, w, h, fill=fill, stroke=stroke, r=r) +
            path(f"M{x+i} {y+i} L{x+w-i} {y+h-i} M{x+w-i} {y+i} L{x+i} {y+h-i}", stroke))


def avatar(x, y, size, name="Foto"):
    return gid(f"IMG_{name}", xbox(x, y, size, size))


def line_ph(x, y, w, h=9, fill=0.86):
    """Línea horizontal que simula texto."""
    return rect(x, y, w, h, fill=fill, r=h / 2)


def icon(x, y, s=26, fill=1.0, stroke=0.55, name=None):
    b = rect(x, y, s, s, fill=fill, stroke=stroke, r=6)
    return gid(f"ICO_{name}", b) if name else b


def chip(x, y, label, active=False, size=11, fixed_w=None, name=None):
    w = fixed_w if fixed_w else tw(label, size, 500) + 24
    h = size + 15
    b = (rect(x, y, w, h, fill=0.25 if active else 1.0,
              stroke=0.25 if active else 0.75, r=h / 2) +
         text(x + w / 2, y + h / 2, label, size=size, weight=500,
              fill=1.0 if active else 0.35, anchor="middle"))
    return (gid(f"CHIP_{name or label}", b), w, h)


def button(x, y, w, h, label, primary=True, size=14, name=None):
    b = (rect(x, y, w, h, fill=0.2 if primary else 1.0,
              stroke=None if primary else 0.4, r=10, sw=1.5) +
         text(x + w / 2, y + h / 2, label, size=size, weight=600,
              fill=1.0 if primary else 0.2, anchor="middle"))
    return gid(f"BTN_{name or label}", b)


def field(x, y, w, label, h=48, name=None):
    b = (rect(x, y, w, h, fill=1.0, stroke=0.72, r=8) +
         rect(x + 14, y + h / 2 - 9, 18, 18, fill=0.85, r=4) +
         text(x + 42, y + h / 2, label, size=14, fill=0.5))
    return gid(f"INPUT_{name or label}", b)


def status_bar(dark=False):
    o = [rect(0, 0, W, 44, fill=0.18 if dark else 1.0),
         text(20, 22, "9:41", size=12, weight=600, fill=1.0 if dark else 0.13)]
    for x, w in [(330, 10), (344, 12), (360, 20)]:
        o.append(rect(x, 17, w, 10, fill=0.75, r=2))
    return gid("Status_bar", "".join(o))


def app_bar(title, right=True, y=44, back=True):
    o = [rect(0, y, W, 46, fill=1.0)]
    if back:
        o.append(icon(16, y + 10, 26, name="Atras"))
    o.append(text(54 if back else 20, y + 24, title, size=16, weight=600))
    if right:
        o.append(icon(348, y + 10, 26, name="Accion_superior"))
    return gid(f"AppBar_{title}", "".join(o))


def nav_bar(labels, active, y=780):
    o = [rect(0, y, W, 64, fill=0.99), rect(0, y, W, 1, fill=0.8)]
    step = W / len(labels)
    for i, lab in enumerate(labels):
        cx = step * i + step / 2
        item = (rect(cx - 11, y + 12, 22, 22, fill=0.3 if i == active else 0.82, r=6) +
                text(cx, y + 46, lab, size=10, weight=600 if i == active else 400,
                     fill=0.2 if i == active else 0.5, anchor="middle"))
        o.append(gid(f"NAV_{lab}", item))
    return gid("Nav_inferior", "".join(o))


def action_bar(left_top, left_big, btn_label, btn_name, y=756):
    o = [rect(0, y, W, 88, fill=1.0), rect(0, y, W, 1, fill=0.8),
         text(PAD, y + 24, left_top, size=11, fill=0.45),
         text(PAD, y + 45, left_big, size=18, weight=700)]
    bw = 190
    o.append(button(W - PAD - bw, y + 17, bw, 54, btn_label, size=16, name=btn_name))
    return gid("Barra_de_accion", "".join(o))


def frame(inner, w=W, h=H):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">' + rect(0, 0, w, h, fill=1.0, stroke=0.55) +
            inner + "</svg>")


def section(y, label):
    return text(PAD, y + 10, label, size=14, weight=600), y + 24


# ==========================================================================
# 1 · LOGIN
# ==========================================================================
def s01_login():
    set_prefix("01_")
    o = [status_bar()]
    y = 74

    o.append(gid("Logo", xbox(W / 2 - 38, y, 76, 76, r=14)))
    y += 88
    o.append(text(W / 2, y, "SaludConecta", size=22, weight=700, anchor="middle"))
    y += 24
    o.append(text(W / 2, y, "Tu cita médica en pocos pasos", size=13, fill=0.5,
                  anchor="middle"))
    y += 34

    o.append(text(PAD, y + 10, "Iniciar sesión", size=20, weight=600))
    y += 34

    o.append(button(PAD, y, 169, 44, "Soy Paciente", True, 14, "Rol_Paciente"))
    o.append(button(PAD + 181, y, 169, 44, "Soy Médico", False, 14, "Rol_Medico"))
    y += 60

    o.append(text(PAD, y, "Correo electrónico", size=12, weight=500, fill=0.45))
    y += 12
    o.append(field(PAD, y, CW, "paciente@correo.com", name="Correo"))
    y += 62

    o.append(text(PAD, y, "Contraseña", size=12, weight=500, fill=0.45))
    y += 12
    o.append(field(PAD, y, CW, "••••••••", name="Contrasena"))
    y += 62

    o.append(gid("CHK_Recordarme",
                 rect(PAD, y - 8, 16, 16, fill=1.0, stroke=0.5, r=3) +
                 text(PAD + 24, y, "Recordarme", size=12, fill=0.45)))
    o.append(gid("LINK_Olvidaste_contrasena",
                 text(W - PAD, y, "¿Olvidaste tu contraseña?", size=12, weight=500,
                      fill=0.3, anchor="end")))
    y += 24

    o.append(button(PAD, y, CW, 52, "Ingresar", True, 16, "Ingresar"))
    y += 64
    o.append(button(PAD, y, CW, 48, "Ingresar con huella / Face ID", False, 14,
                    "Biometrico"))
    y += 66

    o.append(rect(PAD, y, 155, 1, fill=0.85))
    o.append(text(W / 2, y, "o", size=12, fill=0.5, anchor="middle"))
    o.append(rect(W - PAD - 155, y, 155, 1, fill=0.85))
    y += 30

    o.append(text(W / 2 - 12, y, "¿No tienes cuenta?", size=13, fill=0.45,
                  anchor="end"))
    o.append(gid("LINK_Registrate",
                 text(W / 2 - 4, y, "Regístrate", size=13, weight=600, fill=0.15)))
    return frame("".join(o))


# ==========================================================================
# 2 · HOME (PACIENTE)
# ==========================================================================
def s02_home():
    set_prefix("02_")
    o = [status_bar()]
    y = 62

    o.append(text(PAD, y + 12, "Hola, Daniel", size=20, weight=700))
    o.append(text(PAD, y + 34, "Ubicación: Bogotá, Chapinero", size=12, fill=0.45))
    o.append(icon(288, y + 4, 26, name="Notificaciones"))
    o.append(avatar(324, y - 2, 40, "Perfil_usuario"))
    y += 62

    search = (rect(PAD, y, CW, 56, fill=0.97, stroke=0.5, r=12, sw=1.5) +
              rect(PAD + 14, y + 18, 20, 20, fill=0.7, r=10) +
              text(PAD + 46, y + 28, "Buscar médico o especialidad", size=14, fill=0.45))
    o.append(gid("INPUT_Buscador_destacado", search))
    o.append(gid("BTN_Filtros", rect(W - PAD - 48, y + 8, 40, 40, fill=0.25, r=8)))
    y += 70

    cx = PAD
    for lab, act in [("Cerca de mí", True), ("Disponible hoy", False),
                     ("Mejor valorados", False)]:
        s, w, h = chip(cx, y, lab, act)
        o.append(s)
        cx += w + 8
    y += 38

    o.append(text(PAD, y + 10, "Especialidades", size=16, weight=600))
    o.append(gid("LINK_Ver_todas",
                 text(W - PAD, y + 10, "Ver todas", size=12, weight=500, fill=0.4,
                      anchor="end")))
    y += 30

    cats = ["Medicina General", "Pediatría", "Odontología",
            "Dermatología", "Cardiología", "Psicología"]
    bw, bh = (CW - 20) / 3, 80
    for i, name in enumerate(cats):
        col, row = i % 3, i // 3
        bx, by = PAD + col * (bw + 10), y + row * (bh + 10)
        card = (rect(bx, by, bw, bh, fill=0.985, stroke=0.78, r=10) +
                rect(bx + bw / 2 - 15, by + 14, 30, 30, fill=0.85, r=8) +
                text(bx + bw / 2, by + 60, name, size=10, fill=0.25, anchor="middle"))
        o.append(gid(f"CAT_{name}", card))
    y += bh * 2 + 10 + 22

    o.append(text(PAD, y + 10, "Tu próxima cita", size=16, weight=600))
    y += 30

    card = (rect(PAD, y, CW, 72, fill=0.98, stroke=0.75, r=10) +
            xbox(PAD + 12, y + 12, 48, 48) +
            text(PAD + 72, y + 22, "Dra. Laura Gómez", size=14, weight=600) +
            text(PAD + 72, y + 40, "Cardiología · Clínica Norte", size=12, fill=0.45) +
            text(PAD + 72, y + 56, "Mié 21 Ago · 10:30 AM", size=12, weight=500,
                 fill=0.2))
    o.append(gid("CARD_Proxima_cita", card))
    o.append(button(W - PAD - 64, y + 19, 64, 34, "Ver", False, 12, "Ver_proxima_cita"))

    o.append(nav_bar(["Inicio", "Buscar", "Mis Citas", "Perfil"], 0))
    return frame("".join(o))


# ==========================================================================
# 3 · RESULTADO DE BÚSQUEDA
# ==========================================================================
def s03_resultados():
    set_prefix("03_")
    o = [status_bar(), app_bar("Cardiología")]
    y = 102

    o.append(gid("INPUT_Buscador",
                 rect(PAD, y, CW, 44, fill=0.97, stroke=0.72, r=10) +
                 rect(PAD + 12, y + 14, 16, 16, fill=0.7, r=8) +
                 text(PAD + 38, y + 22, "cardiólogo cerca de mí", size=13, fill=0.4)))
    y += 56

    cx = PAD
    for lab, act in [("Cercanía", True), ("Disponibilidad", False),
                     ("Precio", False), ("Valoración", False)]:
        s, w, h = chip(cx, y, lab, act)
        o.append(s)
        cx += w + 7
    y += 38

    o.append(text(PAD, y, "12 médicos encontrados", size=12, fill=0.45))
    o.append(gid("LINK_Ordenar",
                 text(W - PAD, y, "Ordenar por: Cercanía", size=12, weight=500,
                      fill=0.3, anchor="end")))
    y += 20

    docs = [("Dra. Laura Gómez", "Cardióloga · 12 años exp.",
             "4.9 (128 opiniones) · a 1.2 km", "$90.000", "Hoy 3:00 PM", True),
            ("Dr. Andrés Rojas", "Cardiólogo · 8 años exp.",
             "4.7 (86 opiniones) · a 2.4 km", "$75.000", "Hoy 5:30 PM", True),
            ("Dra. Paula Medina", "Cardióloga · 15 años exp.",
             "4.8 (203 opiniones) · a 3.1 km", "$110.000", "Mañana 8:00 AM", False),
            ("Dr. Julián Torres", "Cardiólogo · 5 años exp.",
             "4.5 (41 opiniones) · a 4.0 km", "$65.000", "Mañana 11:00 AM", False)]
    for nombre, spec, meta, precio, slot, act in docs:
        card = (rect(PAD, y, CW, 100, fill=1.0, stroke=0.75, r=10) +
                xbox(PAD + 12, y + 12, 56, 56) +
                text(PAD + 80, y + 26, nombre, size=14, weight=600) +
                text(PAD + 80, y + 45, spec, size=12, fill=0.45) +
                text(PAD + 80, y + 62, meta, size=11, fill=0.45) +
                text(PAD + 80, y + 82, precio, size=13, weight=700))
        o.append(gid(f"CARD_{nombre}", card))
        s, cw, chh = chip(W - PAD - 12 - (tw(slot, 10, 500) + 24), y + 72, slot, act,
                          size=10, name=f"Horario_{nombre}")
        o.append(s)
        y += 110

    o.append(nav_bar(["Inicio", "Buscar", "Mis Citas", "Perfil"], 1))
    return frame("".join(o))


# ==========================================================================
# 4 · DETALLE DEL MÉDICO
# ==========================================================================
def s04_detalle():
    set_prefix("04_")
    o = [status_bar(), app_bar("Perfil del médico")]
    y = 104

    o.append(avatar(PAD, y, 84, "Foto_medico"))
    o.append(text(PAD + 98, y + 14, "Dra. Laura Gómez", size=19, weight=700))
    o.append(text(PAD + 98, y + 36, "Cardióloga · Reg. Méd. 45872", size=13, fill=0.45))
    o.append(text(PAD + 98, y + 54, "Clínica Norte · a 1.2 km", size=12, fill=0.45))
    o.append(rect(PAD + 98, y + 68, 56, 12, fill=0.55, r=6))
    o.append(text(PAD + 162, y + 74, "4.9 · 128 opiniones", size=11, fill=0.35))
    y += 98

    bw = (CW - 20) / 3
    for i, (v, l) in enumerate([("12 años", "Experiencia"), ("4.9/5", "Valoración"),
                                ("1.240", "Pacientes")]):
        bx = PAD + i * (bw + 10)
        o.append(rect(bx, y, bw, 56, fill=0.98, stroke=0.78, r=10))
        o.append(text(bx + bw / 2, y + 21, v, size=14, weight=700, anchor="middle"))
        o.append(text(bx + bw / 2, y + 39, l, size=10, fill=0.45, anchor="middle"))
    y += 70

    tw3 = CW / 3
    for i, lab in enumerate(["Sobre mí", "Valoraciones", "Ubicación"]):
        tx = PAD + i * tw3
        t = (text(tx + tw3 / 2, y + 8, lab, size=13, weight=600 if i == 0 else 400,
                  fill=0.13 if i == 0 else 0.5, anchor="middle") +
             rect(tx, y + 24, tw3, 3 if i == 0 else 1, fill=0.2 if i == 0 else 0.85))
        o.append(gid(f"TAB_{lab}", t))
    y += 44

    o.append(text(PAD, y + 8, "Currículum / Sobre mí", size=15, weight=600))
    y += 26
    for w in [CW, CW, CW, 230]:
        o.append(line_ph(PAD, y, w))
        y += 17
    y += 6
    o.append(text(PAD, y, "Universidad Nacional · Especialización en Cardiología",
                  size=12, fill=0.45))
    y += 18
    o.append(text(PAD, y, "Miembro de la Sociedad Colombiana de Cardiología",
                  size=12, fill=0.45))
    y += 26

    o.append(text(PAD, y + 8, "Próximos horarios disponibles", size=15, weight=600))
    y += 28
    cx = PAD
    for lab, act in [("Hoy 3:00 PM", True), ("Hoy 4:00 PM", False),
                     ("Hoy 5:30 PM", False)]:
        s, w, h = chip(cx, y, lab, act, size=12, name=f"Horario_{lab}")
        o.append(s)
        cx += w + 8

    o.append(action_bar("Precio consulta", "$90.000", "Reservar Cita", "Reservar_Cita"))
    return frame("".join(o))


# ==========================================================================
# 5 · AGENDA (FECHA Y HORA)
# ==========================================================================
def s05_agenda():
    set_prefix("05_")
    o = [status_bar(), app_bar("Seleccionar fecha y hora", right=False)]
    y = 104

    card = (rect(PAD, y, CW, 64, fill=0.98, stroke=0.75, r=10) +
            xbox(PAD + 12, y + 10, 44, 44) +
            text(PAD + 68, y + 25, "Dra. Laura Gómez", size=14, weight=600) +
            text(PAD + 68, y + 43, "Cardiología · $90.000", size=12, fill=0.45))
    o.append(gid("CARD_Medico_seleccionado", card))
    y += 78

    o.append(icon(PAD, y, 26, name="Mes_anterior"))
    o.append(text(W / 2, y + 13, "Agosto 2025", size=15, weight=600, anchor="middle"))
    o.append(icon(W - PAD - 26, y, 26, name="Mes_siguiente"))
    y += 40

    dias = [("Lun", "18"), ("Mar", "19"), ("Mié", "20"), ("Jue", "21"),
            ("Vie", "22"), ("Sáb", "23"), ("Dom", "24")]
    dw = (CW - 6 * 6) / 7
    for i, (d, n) in enumerate(dias):
        bx = PAD + i * (dw + 6)
        sel = i == 3
        b = (rect(bx, y, dw, 56, fill=0.22 if sel else 1.0,
                  stroke=0.22 if sel else 0.78, r=10) +
             text(bx + dw / 2, y + 18, d, size=10, fill=0.85 if sel else 0.5,
                  anchor="middle") +
             text(bx + dw / 2, y + 38, n, size=14, weight=600,
                  fill=1.0 if sel else 0.15, anchor="middle"))
        o.append(gid(f"DIA_{d}_{n}", b))
    y += 70

    def slots(y, titulo, items):
        o.append(text(PAD, y + 8, titulo, size=14, weight=600))
        y += 26
        sw_ = (CW - 16) / 3
        for i, (lab, act) in enumerate(items):
            col, row = i % 3, i // 3
            bx, by = PAD + col * (sw_ + 8), y + row * 42
            s, _, _ = chip(bx, by, lab, act, size=12, fixed_w=sw_,
                           name=f"Hora_{lab}")
            o.append(s)
        return y + 42 * ((len(items) + 2) // 3) + 6

    y = slots(y, "Mañana", [("8:00 AM", False), ("8:30 AM", False), ("9:00 AM", False),
                            ("10:00 AM", False), ("11:30 AM", False), ("12:00 M", False)])
    y = slots(y, "Tarde", [("2:00 PM", False), ("3:00 PM", True), ("4:00 PM", False),
                           ("5:30 PM", False), ("6:00 PM", False), ("6:30 PM", False)])

    o.append(text(PAD, y + 8, "Tipo de consulta", size=14, weight=600))
    y += 26
    o.append(button(PAD, y, 169, 44, "Presencial", True, 13, "Presencial"))
    o.append(button(PAD + 181, y, 169, 44, "Virtual", False, 13, "Virtual"))

    o.append(action_bar("Jue 21 Ago · 3:00 PM", "Total $90.000", "Confirmar Cita",
                        "Confirmar_Cita"))
    return frame("".join(o))


# ==========================================================================
# 6 · CONFIRMACIÓN
# ==========================================================================
def s06_confirmacion():
    set_prefix("06_")
    o = [status_bar()]
    y = 78

    check = (rect(W / 2 - 48, y, 96, 96, fill=0.2, r=48) +
             path(f"M{W/2-22} {y+50} L{W/2-6} {y+66} L{W/2+22} {y+30}",
                  stroke=1.0, sw=6, cap="round"))
    o.append(gid("Icono_exito", check))
    y += 110

    o.append(text(W / 2, y, "¡Cita agendada con éxito!", size=22, weight=700,
                  anchor="middle"))
    y += 28
    o.append(text(W / 2, y, "Te enviamos la confirmación al correo y un", size=13,
                  fill=0.45, anchor="middle"))
    y += 19
    o.append(text(W / 2, y, "recordatorio 1 hora antes.", size=13, fill=0.45,
                  anchor="middle"))
    y += 30

    card_y = y
    rows = [("Fecha", "Jue 21 Ago, 2025"), ("Hora", "3:00 PM"),
            ("Modalidad", "Presencial"), ("Dirección", "Cra. 15 #98-30, Cons. 402"),
            ("Código de cita", "SC-48219")]
    ch = 16 + 48 + 14 + 1 + 14 + len(rows) * 26 + 8 + 1 + 14 + 20 + 16
    body = [rect(PAD, card_y, CW, ch, fill=0.985, stroke=0.75, r=12),
            xbox(PAD + 16, card_y + 16, 48, 48),
            text(PAD + 76, card_y + 32, "Dra. Laura Gómez", size=15, weight=600),
            text(PAD + 76, card_y + 52, "Cardiología · Clínica Norte", size=12,
                 fill=0.45)]
    ry = card_y + 16 + 48 + 14
    body.append(rect(PAD + 16, ry, CW - 32, 1, fill=0.85))
    ry += 14
    for k, v in rows:
        body.append(text(PAD + 16, ry + 10, k, size=12, fill=0.45))
        body.append(text(W - PAD - 16, ry + 10, v, size=13, weight=600, anchor="end"))
        ry += 26
    ry += 8
    body.append(rect(PAD + 16, ry, CW - 32, 1, fill=0.85))
    ry += 14
    body.append(text(PAD + 16, ry + 10, "Total a pagar", size=12, fill=0.45))
    body.append(text(W - PAD - 16, ry + 10, "$90.000", size=14, weight=700,
                     anchor="end"))
    o.append(gid("CARD_Resumen_cita", "".join(body)))
    y = card_y + ch + 20

    o.append(button(PAD, y, CW, 52, "Ver mis citas", True, 16, "Ver_mis_citas"))
    y += 62
    o.append(button(PAD, y, CW, 48, "Agregar al calendario", False, 14, "Calendario"))
    y += 62
    o.append(gid("LINK_Volver_al_inicio",
                 text(W / 2, y, "Volver al inicio", size=13, weight=500, fill=0.4,
                      anchor="middle")))
    return frame("".join(o))


# ==========================================================================
# 7 · DASHBOARD (MÉDICO)
# ==========================================================================
def s07_dashboard():
    set_prefix("07_")
    o = [status_bar(dark=True)]

    hero_h = 144
    hero = [rect(0, 44, W, hero_h, fill=0.18),
            xbox(PAD, 56, 46, 46, r=8, fill=0.28, stroke=0.55),
            text(PAD + 60, 72, "Dr. Andrés Rojas", size=18, weight=700, fill=1.0),
            text(PAD + 60, 92, "Panel del médico · Cardiología", size=12, fill=0.75),
            rect(W - PAD - 28, 65, 28, 28, fill=0.3, r=8)]
    sw_ = (CW - 20) / 3
    for i, (v, l) in enumerate([("8", "Citas hoy"), ("6", "Confirmadas"),
                                ("2", "Pendientes")]):
        bx = PAD + i * (sw_ + 10)
        hero.append(rect(bx, 118, sw_, 60, fill=0.28, r=10))
        hero.append(text(bx + sw_ / 2, 138, v, size=18, weight=700, fill=1.0,
                         anchor="middle"))
        hero.append(text(bx + sw_ / 2, 160, l, size=10, fill=0.78, anchor="middle"))
    o.append(gid("Header_medico", "".join(hero)))

    y = 44 + hero_h + 18
    o.append(text(PAD, y, "Agenda de hoy · Mié 21 Ago", size=15, weight=600))
    o.append(gid("LINK_Ver_semana",
                 text(W - PAD, y, "Ver semana", size=12, weight=500, fill=0.4,
                      anchor="end")))
    y += 20

    citas = [("8:00", "Camila Ruiz", "Control post-operatorio", "Confirmada", True),
             ("9:00", "Jorge Pineda", "Dolor torácico", "Confirmada", True),
             ("10:30", "María Salazar", "Lectura de exámenes", "Pendiente", False),
             ("11:30", "Felipe Cárdenas", "Control anual", "Confirmada", True),
             ("2:00", "Sara Duarte", "Teleconsulta", "Pendiente", False)]
    for hora, nombre, motivo, estado, conf in citas:
        row = [text(PAD + 24, y + 24, hora, size=12, weight=700, anchor="middle"),
               text(PAD + 24, y + 40, "30 min", size=9, fill=0.5, anchor="middle"),
               rect(PAD + 56, y, CW - 56, 60, fill=0.99 if conf else 1.0,
                    stroke=0.75, r=10),
               xbox(PAD + 68, y + 13, 34, 34),
               text(PAD + 112, y + 24, nombre, size=13, weight=600),
               text(PAD + 112, y + 42, motivo, size=11, fill=0.45)]
        o.append(gid(f"CITA_{hora}_{nombre}", "".join(row)))
        s, cw, _ = chip(W - PAD - 12 - (tw(estado, 10, 500) + 24), y + 18, estado,
                        conf, size=10, name=f"Estado_{hora}")
        o.append(s)
        y += 68

    y += 4
    o.append(button(PAD, y, 169, 44, "Bloquear horario", False, 12, "Bloquear_horario"))
    o.append(button(PAD + 181, y, 169, 44, "Confirmar disponibilidad", True, 11,
                    "Confirmar_disponibilidad"))

    o.append(nav_bar(["Agenda", "Pacientes", "Historial", "Perfil"], 0))
    return frame("".join(o))


# ==========================================================================
# 8 · HOJA DE VIDA DE PACIENTES
# ==========================================================================
def s08_hv_paciente():
    set_prefix("08_")
    o = [status_bar(), app_bar("Hoja de vida del paciente")]
    y = 102

    o.append(avatar(PAD, y, 68, "Foto_paciente"))
    o.append(text(PAD + 82, y + 16, "Camila Ruiz Martínez", size=17, weight=700))
    o.append(text(PAD + 82, y + 38, "Paciente · 34 años · Femenino", size=12, fill=0.45))
    o.append(text(PAD + 82, y + 56, "CC 1.020.458.771", size=11, fill=0.5))
    y += 82

    def grid2(y, pairs):
        bw = (CW - 8) / 2
        for i, (k, v) in enumerate(pairs):
            col, row = i % 2, i // 2
            bx, by = PAD + col * (bw + 8), y + row * 60
            b = (rect(bx, by, bw, 52, fill=0.98, stroke=0.78, r=8) +
                 text(bx + 12, by + 17, k, size=10, fill=0.45) +
                 text(bx + 12, by + 35, v, size=13, weight=600))
            o.append(gid(f"DATO_{k}", b))
        return y + 60 * ((len(pairs) + 1) // 2) + 4

    y = grid2(y, [("Tipo de sangre", "O+"), ("EPS", "Sura"),
                  ("Teléfono", "300 458 2210"), ("Peso / Talla", "62 kg · 1.65 m")])

    def chips_row(y, titulo, items):
        o.append(text(PAD, y + 8, titulo, size=14, weight=600))
        y += 26
        cx = PAD
        for lab, act in items:
            s, w, h = chip(cx, y, lab, act)
            o.append(s)
            cx += w + 8
        return y + 36

    y = chips_row(y, "Antecedentes médicos",
                  [("Hipertensión", True), ("Asma", False), ("Cirugía 2019", False)])
    y = chips_row(y, "Alergias", [("Penicilina", True), ("Polen", False)])

    def item(y, titulo, sub, meta):
        b = [rect(PAD, y, CW, 62, fill=1.0, stroke=0.78, r=8),
             rect(PAD + 12, y + 16, 8, 8, fill=0.55, r=4),
             text(PAD + 30, y + 20, titulo, size=13, weight=600),
             text(PAD + 30, y + 38, sub, size=11, fill=0.45),
             text(PAD + 30, y + 52, meta, size=10, fill=0.55)]
        o.append(gid(f"ITEM_{titulo}", "".join(b)))
        return y + 70

    o.append(text(PAD, y + 8, "Medicamentos actuales", size=14, weight=600))
    y += 26
    y = item(y, "Losartán 50 mg", "1 tableta cada 12 horas", "Desde: Mar 2024")
    y = item(y, "Salbutamol inhalador", "2 puff si presenta crisis", "Según necesidad")

    o.append(text(PAD, y + 8, "Consultas previas", size=14, weight=600))
    y += 26
    y = item(y, "12 Jun 2025 · Dra. Laura Gómez",
             "Control de tensión arterial. Se ajusta dosis.", "Cardiología")

    o.append(button(PAD, y + 6, CW, 48, "Agregar nota rápida", True, 15, "Nota_rapida"))
    return frame("".join(o))


# ==========================================================================
# 9 · HOJA DE VIDA MÉDICOS (CON ESPECIALIDAD)
# ==========================================================================
def s09_hv_medico():
    set_prefix("09_")
    o = [status_bar(), app_bar("Hoja de vida profesional")]
    y = 102

    o.append(avatar(PAD, y, 68, "Foto_medico"))
    o.append(text(PAD + 82, y + 14, "Dra. Laura Gómez", size=17, weight=700))
    o.append(text(PAD + 82, y + 34, "Reg. Méd. 45872 · Clínica Norte", size=11,
                  fill=0.5))
    s, w, h = chip(PAD + 82, y + 46, "Cardiología", True, name="Especialidad_principal")
    o.append(s)
    s2, w2, _ = chip(PAD + 82 + w + 8, y + 46, "12 años exp.", False)
    o.append(s2)
    y += 88

    bw = (CW - 8) / 2
    for i, (k, v) in enumerate([("Valoración", "4.9 / 5"), ("Pacientes", "1.240"),
                                ("Consulta", "$90.000"),
                                ("Idiomas", "Español · Inglés")]):
        col, row = i % 2, i // 2
        bx, by = PAD + col * (bw + 8), y + row * 60
        b = (rect(bx, by, bw, 52, fill=0.98, stroke=0.78, r=8) +
             text(bx + 12, by + 17, k, size=10, fill=0.45) +
             text(bx + 12, by + 35, v, size=13, weight=600))
        o.append(gid(f"DATO_{k}", b))
    y += 124

    o.append(text(PAD, y + 8, "Especialidad y subespecialidades", size=14, weight=600))
    y += 26
    cx, cy = PAD, y
    for lab, act in [("Cardiología clínica", True), ("Ecocardiografía", False),
                     ("Hipertensión arterial", False), ("Cardiología deportiva", False)]:
        wd = tw(lab, 11, 500) + 24
        if cx + wd > W - PAD:
            cx, cy = PAD, cy + 34
        s, wd, _ = chip(cx, cy, lab, act)
        o.append(s)
        cx += wd + 8
    y = cy + 44

    def item(y, titulo, sub, meta):
        b = [rect(PAD, y, CW, 62, fill=1.0, stroke=0.78, r=8),
             rect(PAD + 12, y + 16, 8, 8, fill=0.55, r=4),
             text(PAD + 30, y + 20, titulo, size=13, weight=600),
             text(PAD + 30, y + 38, sub, size=11, fill=0.45),
             text(PAD + 30, y + 52, meta, size=10, fill=0.55)]
        o.append(gid(f"ITEM_{titulo}", "".join(b)))
        return y + 70

    o.append(text(PAD, y + 8, "Formación académica", size=14, weight=600))
    y += 26
    y = item(y, "Especialización en Cardiología",
             "Universidad Nacional de Colombia", "2012 - 2015")

    o.append(text(PAD, y + 8, "Experiencia laboral", size=14, weight=600))
    y += 26
    y = item(y, "Cardióloga · Clínica Norte",
             "Consulta externa y hemodinamia", "2016 - Actual")

    o.append(text(PAD, y + 8, "Certificaciones", size=14, weight=600))
    y += 26
    cx = PAD
    for lab in ["ACLS 2024", "Soc. Col. de Cardiología"]:
        s, wd, _ = chip(cx, y, lab, False)
        o.append(s)
        cx += wd + 8
    y += 42

    o.append(button(PAD, y, CW, 50, "Reservar Cita", True, 16, "Reservar_Cita"))
    return frame("".join(o))


# ==========================================================================
# 10 · MIS CITAS
# ==========================================================================
def s10_mis_citas():
    set_prefix("10_")
    o = [status_bar()]
    o.append(text(PAD, 66, "Mis Citas", size=20, weight=700))
    o.append(icon(344, 53, 26, name="Filtrar"))
    y = 100

    for i, lab in enumerate(["Próximas (2)", "Historial (8)"]):
        tx = PAD + (CW / 2) * i
        t = (text(tx + CW / 4, y + 9, lab, size=13, weight=600 if i == 0 else 400,
                  fill=0.13 if i == 0 else 0.5, anchor="middle") +
             rect(tx, y + 24, CW / 2, 3 if i == 0 else 1, fill=0.2 if i == 0 else 0.85))
        o.append(gid(f"TAB_{lab}", t))
    y += 39

    ban = (rect(PAD, y, CW, 44, fill=0.94, stroke=0.7, r=10, dash="5 4") +
           rect(PAD + 12, y + 11, 22, 22, fill=0.6, r=6) +
           text(PAD + 44, y + 22,
                "Recordatorio: tu próxima cita es mañana a las 10:30 AM.",
                size=12, fill=0.25))
    o.append(gid("Banner_recordatorio", ban))
    y += 56

    def cita(y, estado, act, nombre, spec, fecha, acciones):
        b = [rect(PAD, y, CW, 140, fill=1.0, stroke=0.75, r=10),
             xbox(PAD + 12, y + 12, 46, 46),
             text(PAD + 70, y + 24, nombre, size=14, weight=600),
             text(PAD + 70, y + 43, spec, size=11, fill=0.45),
             text(PAD + 70, y + 62, fecha, size=12, weight=500, fill=0.2),
             rect(PAD + 12, y + 82, CW - 24, 1, fill=0.88)]
        o.append(gid(f"CARD_{nombre}", "".join(b)))
        s, _, _ = chip(W - PAD - 12 - (tw(estado, 10, 500) + 24), y + 18, estado, act,
                       size=10, name=f"Estado_{nombre}")
        o.append(s)
        bwid = (CW - 24 - 8) / 2
        for i, a in enumerate(acciones):
            o.append(button(PAD + 12 + i * (bwid + 8), y + 92, bwid, 36, a,
                            primary=(i == len(acciones) - 1), size=12,
                            name=f"{a}_{nombre}"))
        return y + 152

    y = cita(y, "Confirmada", True, "Dra. Laura Gómez", "Cardiología · Presencial",
             "Mié 21 Ago · 10:30 AM", ["Reprogramar", "Ver detalle"])
    y = cita(y, "Pendiente", False, "Dr. Andrés Rojas", "Medicina General · Virtual",
             "Vie 30 Ago · 4:00 PM", ["Cancelar", "Ver detalle"])

    o.append(text(PAD, y + 9, "Historial de consultas", size=14, weight=600))
    y += 30
    for nombre, spec in [("Dra. Laura Gómez", "Cardiología · 12 Jun 2025"),
                         ("Dr. Andrés Rojas", "Medicina General · 03 Mar 2025")]:
        b = (rect(PAD, y, CW, 56, fill=0.98, stroke=0.8, r=8) +
             xbox(PAD + 12, y + 10, 36, 36) +
             text(PAD + 58, y + 21, nombre, size=13, weight=600) +
             text(PAD + 58, y + 38, spec, size=11, fill=0.45))
        o.append(gid(f"HIST_{nombre}", b))
        s, _, _ = chip(W - PAD - 12 - 84, y + 16, "Ver resumen", False, size=10,
                       name=f"Resumen_{nombre}")
        o.append(s)
        y += 68

    o.append(nav_bar(["Inicio", "Buscar", "Mis Citas", "Perfil"], 2))
    return frame("".join(o))


# ==========================================================================
# USER FLOW
# ==========================================================================
BOX_W, BOX_H, ARROW_W, GAP = 180, 90, 30, 12


def flow_lane(o, x, y, titulo, descripcion, pasos, tag="L"):
    n = len(pasos)
    lane_w = 48 + n * BOX_W + (n - 1) * (ARROW_W + GAP * 2)
    lane_h = 24 + 52 + 16 + BOX_H + 24
    o.append(rect(x, y, lane_w, lane_h, fill=0.97, stroke=0.85, r=16))
    o.append(text(x + 24, y + 36, titulo, size=20, weight=700))
    o.append(text(x + 24, y + 60, descripcion, size=13, fill=0.45))
    bx, by = x + 24, y + 92
    for i, (t, sub, dest) in enumerate(pasos):
        if i > 0:
            o.append(text(bx + GAP + ARROW_W / 2, by + BOX_H / 2, "→", size=22,
                          fill=0.45, anchor="middle"))
            bx += GAP + ARROW_W + GAP
        b = [rect(bx, by, BOX_W, BOX_H, fill=0.2 if dest else 1.0,
                  stroke=0.2 if dest else 0.6, r=12, sw=1.5),
             rect(bx + 14, by + 12, 26, 18, fill=0.35 if dest else 0.92, r=9),
             text(bx + 27, by + 21, f"{i+1:02d}", size=10, weight=700,
                  fill=1.0 if dest else 0.3, anchor="middle"),
             text(bx + 14, by + 46, t, size=14, weight=600,
                  fill=1.0 if dest else 0.13),
             text(bx + 14, by + 68, sub, size=10, fill=0.8 if dest else 0.45)]
        o.append(gid(f"PASO_{tag}_{i+1:02d}_{t}", "".join(b)))
        bx += BOX_W
    return lane_w, lane_h


def s11_user_flow():
    set_prefix("FLOW_")
    paciente = [("Login", "Elige rol: Paciente", False),
                ("Home", "Buscador + especialidades", False),
                ("Resultados", "Filtra por cercanía", False),
                ("Detalle Médico", "Currículum y precio", False),
                ("Agenda", "Fecha, hora y modalidad", False),
                ("Confirmación", "Cita agendada", True),
                ("Mis Citas", "Historial y recordatorios", False)]
    medico = [("Login", "Elige rol: Médico", False),
              ("Dashboard", "Agenda del día", True),
              ("Panel Pacientes", "Citados hoy", False),
              ("Hoja de Vida", "Antecedentes y alergias", False),
              ("Nota rápida", "Registra la consulta", False),
              ("Gestión Agenda", "Bloquear horarios", False)]

    tmp = []
    w1, h1 = flow_lane(tmp, 0, 0, "x", "x", paciente)
    FW, FH = w1 + 80, 110 + h1 + 32 + h1 + 40

    o = [rect(0, 0, FW, FH, fill=1.0),
         text(40, 46, "User Flow · SaludConecta", size=34, weight=700),
         text(40, 80, "Paso 1 de la guía: trazar el camino antes de dibujar. "
                      "Dos roles, dos recorridos.", size=15, fill=0.4)]
    y = 110
    _, h = flow_lane(o, 40, y, "Flujo Paciente",
                     "Camino principal: sacar una cita en 5 toques desde el Home.",
                     paciente, tag="Paciente")
    y += h + 32
    flow_lane(o, 40, y, "Flujo Médico Especialista",
              "Camino principal: revisar la agenda del día y gestionar disponibilidad.",
              medico, tag="Medico")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{FW}" height="{FH}" '
            f'viewBox="0 0 {FW} {FH}">' + "".join(o) + "</svg>")


# ==========================================================================
# Componentes extra para las pantallas complementarias
# ==========================================================================
def switch(x, y, on, name=None):
    w, h = 42, 24
    b = (rect(x, y, w, h, fill=0.25 if on else 0.86, r=12) +
         f'<circle cx="{x + w - 12 if on else x + 12}" cy="{y + h/2}" r="9" '
         f'fill="{gray(1.0)}"/>')
    return gid(f"SWITCH_{name}", b) if name else b


def slider(x, y, w, pct, name=None):
    b = (rect(x, y + 8, w, 4, fill=0.86, r=2) +
         rect(x, y + 8, w * pct, 4, fill=0.25, r=2) +
         f'<circle cx="{x + w*pct:.1f}" cy="{y + 10}" r="10" fill="{gray(1.0)}" '
         f'stroke="{gray(0.3)}" stroke-width="2"/>')
    return gid(f"SLIDER_{name}", b) if name else b


def stars(x, y, val, size=12, gap=3):
    return "".join(rect(x + i * (size + gap), y, size, size,
                        fill=0.3 if i < round(val) else 0.86, r=2)
                   for i in range(5))


def chevron(x, y):
    return path(f"M{x} {y} L{x+6} {y+5} L{x} {y+10}", 0.5, 1.5, "round")


def option_row(y, label, sub=None, name=None):
    b = [rect(PAD, y, CW, 52, fill=1.0, stroke=0.8, r=8),
         rect(PAD + 12, y + 16, 20, 20, fill=0.85, r=5),
         text(PAD + 44, y + 20 if sub else y + 26, label, size=13, weight=500)]
    if sub:
        b.append(text(PAD + 44, y + 37, sub, size=10, fill=0.5))
    b.append(chevron(W - PAD - 22, y + 21))
    return gid(f"OPT_{name or label}", "".join(b))


def sheet_top(y, titulo, right=None):
    b = [rect(0, y, W, H - y + 30, fill=1.0, stroke=0.5, r=20),
         rect(W / 2 - 20, y + 12, 40, 4, fill=0.8, r=2),
         text(PAD, y + 40, titulo, size=18, weight=700)]
    if right:
        b.append(text(W - PAD, y + 40, right, size=12, weight=500, fill=0.4,
                      anchor="end"))
    return "".join(b)


def textarea(y, label, lineas=3, name=None):
    h = 24 + lineas * 18
    b = [rect(PAD, y, CW, h, fill=1.0, stroke=0.72, r=8),
         text(PAD + 14, y + 18, label, size=12, fill=0.5)]
    for i in range(lineas - 1):
        b.append(line_ph(PAD + 14, y + 32 + i * 18, CW - 28 - (0 if i < lineas - 2 else 120),
                         8, 0.9))
    return gid(f"INPUT_{name or label}", "".join(b)), y + h + 12


# ==========================================================================
# 11 · REGISTRO / CREAR CUENTA
# ==========================================================================
def s11_registro():
    set_prefix("11_")
    o = [status_bar(), app_bar("Crear cuenta", right=False)]
    y = 104

    for i, lab in enumerate(["Datos", "Verificación", "Listo"]):
        cx = PAD + 30 + i * 145
        act = i == 0
        o.append(rect(cx - 13, y, 26, 26, fill=0.22 if act else 1.0,
                      stroke=0.22 if act else 0.75, r=13))
        o.append(text(cx, y + 13, str(i + 1), size=12, weight=700,
                      fill=1.0 if act else 0.5, anchor="middle"))
        o.append(text(cx, y + 40, lab, size=10, fill=0.3 if act else 0.5,
                      anchor="middle"))
        if i < 2:
            o.append(rect(cx + 16, y + 12, 113, 2, fill=0.85))
    y += 66

    o.append(text(PAD, y, "Quiero registrarme como", size=12, weight=500, fill=0.45))
    y += 14
    o.append(button(PAD, y, 169, 44, "Paciente", True, 14, "Rol_Paciente"))
    o.append(button(PAD + 181, y, 169, 44, "Médico", False, 14, "Rol_Medico"))
    y += 60

    for lab, nm in [("Nombre completo", "Nombre"), ("Cédula de ciudadanía", "Documento"),
                    ("Correo electrónico", "Correo"), ("Teléfono celular", "Telefono"),
                    ("Contraseña", "Contrasena"),
                    ("Confirmar contraseña", "Confirmar")]:
        o.append(field(PAD, y, CW, lab, name=nm))
        y += 58

    o.append(gid("CHK_Terminos",
                 rect(PAD, y, 18, 18, fill=1.0, stroke=0.5, r=3) +
                 text(PAD + 28, y + 9, "Acepto los términos y la política de datos",
                      size=11, fill=0.45)))
    y += 34

    o.append(button(PAD, y, CW, 52, "Crear cuenta", True, 16, "Crear_cuenta"))
    y += 66
    o.append(text(W / 2 - 12, y, "¿Ya tienes cuenta?", size=13, fill=0.45, anchor="end"))
    o.append(gid("LINK_Iniciar_sesion",
                 text(W / 2 - 4, y, "Inicia sesión", size=13, weight=600, fill=0.15)))
    return frame("".join(o))


# ==========================================================================
# 12 · FILTROS AVANZADOS (hoja modal)
# ==========================================================================
def s12_filtros():
    set_prefix("12_")
    o = [status_bar(), app_bar("Cardiología")]
    y = 102
    for i in range(3):
        o.append(rect(PAD, y + i * 60, CW, 50, fill=0.99, stroke=0.85, r=10))
        o.append(rect(PAD + 12, y + i * 60 + 13, 24, 24, fill=0.92, r=6))
        o.append(line_ph(PAD + 48, y + i * 60 + 16, 150, 8, 0.9))
        o.append(line_ph(PAD + 48, y + i * 60 + 30, 100, 7, 0.92))
    o.append(gid("Fondo_atenuado", rect(0, 44, W, H - 44, fill=0.1, op=0.55)))

    sy = 236
    o.append(gid("Hoja_de_filtros", sheet_top(sy, "Filtros", "Limpiar todo")))
    y = sy + 66

    def blk(y, titulo, items, size=11):
        o.append(text(PAD, y, titulo, size=12, weight=600))
        y += 20
        cx = PAD
        for lab, act in items:
            s, wd, _ = chip(cx, y, lab, act, size=size)
            o.append(s)
            cx += wd + 8
        return y + 38

    y = blk(y, "Especialidad", [("Cardiología", True), ("General", False),
                                ("Pediatría", False)])
    o.append(text(PAD, y, "Distancia máxima", size=12, weight=600))
    o.append(text(W - PAD, y, "Hasta 5 km", size=11, fill=0.4, anchor="end"))
    y += 18
    o.append(slider(PAD, y, CW, 0.42, "Distancia"))
    y += 40

    o.append(text(PAD, y, "Precio de consulta", size=12, weight=600))
    o.append(text(W - PAD, y, "$50.000 – $120.000", size=11, fill=0.4, anchor="end"))
    y += 18
    o.append(slider(PAD, y, CW, 0.7, "Precio"))
    y += 40

    y = blk(y, "Disponibilidad", [("Hoy", True), ("Mañana", False),
                                  ("Esta semana", False)])
    y = blk(y, "Valoración mínima", [("4.5+", True), ("4.0+", False), ("3.0+", False)])

    o.append(text(PAD, y, "Modalidad", size=12, weight=600))
    y += 20
    o.append(button(PAD, y, 169, 40, "Presencial", True, 13, "Presencial"))
    o.append(button(PAD + 181, y, 169, 40, "Virtual", False, 13, "Virtual"))

    o.append(button(PAD, H - 72, CW, 52, "Aplicar filtros · 12 resultados", True, 15,
                    "Aplicar_filtros"))
    return frame("".join(o))


# ==========================================================================
# 13 · VALORACIONES Y OPINIONES
# ==========================================================================
def s13_valoraciones():
    set_prefix("13_")
    o = [status_bar(), app_bar("Valoraciones")]
    y = 104

    o.append(rect(PAD, y, CW, 110, fill=0.98, stroke=0.78, r=12))
    o.append(text(PAD + 60, y + 40, "4.9", size=40, weight=700, anchor="middle"))
    o.append(stars(PAD + 24, y + 64, 5, 11, 2))
    o.append(text(PAD + 60, y + 92, "128 opiniones", size=10, fill=0.5,
                  anchor="middle"))
    bx = PAD + 130
    for i, (n, pct) in enumerate([(5, 0.86), (4, 0.10), (3, 0.03), (2, 0.01), (1, 0.0)]):
        by = y + 20 + i * 16
        o.append(text(bx, by, str(n), size=10, fill=0.5))
        o.append(rect(bx + 12, by - 4, 150, 7, fill=0.9, r=3))
        o.append(rect(bx + 12, by - 4, 150 * pct, 7, fill=0.35, r=3))
    y += 126

    cx = PAD
    for lab, act in [("Todas", True), ("5 estrellas", False), ("Recientes", False)]:
        s, wd, _ = chip(cx, y, lab, act)
        o.append(s)
        cx += wd + 8
    y += 40

    reseñas = [("Marcela T.", "Hace 3 días", 5,
                ["Explicó todo con mucha paciencia y me",
                 "entregó los resultados el mismo día."]),
               ("Iván R.", "Hace 1 semana", 5,
                ["Puntual y muy clara con el tratamiento.",
                 "El consultorio queda fácil de encontrar."]),
               ("Diana P.", "Hace 2 semanas", 4,
                ["Buena atención, aunque esperé 15 minutos",
                 "más de lo agendado."])]
    for nombre, fecha, val, lineas in reseñas:
        h = 108
        b = [rect(PAD, y, CW, h, fill=1.0, stroke=0.78, r=10),
             xbox(PAD + 12, y + 12, 40, 40),
             text(PAD + 64, y + 26, nombre, size=13, weight=600),
             text(PAD + 64, y + 44, fecha, size=10, fill=0.5),
             stars(W - PAD - 12 - 68, y + 18, val, 11, 3)]
        for i, ln in enumerate(lineas):
            b.append(text(PAD + 14, y + 72 + i * 18, ln, size=11, fill=0.35))
        o.append(gid(f"RESENA_{nombre}", "".join(b)))
        y += h + 10

    o.append(button(PAD, y, CW, 46, "Ver las 128 opiniones", False, 14, "Ver_todas"))
    return frame("".join(o))


# ==========================================================================
# 14 · DETALLE DE LA CITA (PACIENTE)
# ==========================================================================
def s14_detalle_cita():
    set_prefix("14_")
    o = [status_bar(), app_bar("Detalle de la cita")]
    y = 104

    s, wd, _ = chip(PAD, y, "Confirmada", True, size=12, name="Estado")
    o.append(s)
    o.append(text(W - PAD, y + 13, "Código SC-48219", size=11, fill=0.45, anchor="end"))
    y += 42

    card = (rect(PAD, y, CW, 78, fill=0.98, stroke=0.75, r=10) +
            xbox(PAD + 12, y + 14, 50, 50) +
            text(PAD + 74, y + 28, "Dra. Laura Gómez", size=15, weight=600) +
            text(PAD + 74, y + 47, "Cardiología · Clínica Norte", size=12, fill=0.45) +
            text(PAD + 74, y + 63, "Reg. Méd. 45872", size=10, fill=0.55))
    o.append(gid("CARD_Medico", card))
    y += 92

    rows = [("Fecha", "Miércoles 21 de agosto"), ("Hora", "10:30 AM · 30 min"),
            ("Modalidad", "Presencial"), ("Consultorio", "Torre B · Cons. 402"),
            ("Valor pagado", "$90.000")]
    o.append(rect(PAD, y, CW, len(rows) * 28 + 16, fill=1.0, stroke=0.78, r=10))
    ry = y + 16
    for k, v in rows:
        o.append(text(PAD + 14, ry, k, size=12, fill=0.45))
        o.append(text(W - PAD - 14, ry, v, size=12, weight=600, anchor="end"))
        ry += 28
    y += len(rows) * 28 + 30

    o.append(gid("IMG_Mapa", xbox(PAD, y, CW, 110, r=10)))
    o.append(text(PAD + CW / 2, y + 55, "Mapa · Cra. 15 #98-30", size=12, fill=0.4,
                  anchor="middle"))
    y += 124

    o.append(text(PAD, y, "Recomendaciones", size=13, weight=600))
    y += 20
    for t in ["Llega 15 minutos antes con tu documento.",
              "Trae los exámenes de sangre más recientes."]:
        o.append(text(PAD, y, "· " + t, size=11, fill=0.45))
        y += 18
    y += 8

    bw = (CW - 10) / 2
    o.append(button(PAD, y, bw, 44, "Reprogramar", False, 13, "Reprogramar"))
    o.append(button(PAD + bw + 10, y, bw, 44, "Cancelar cita", False, 13, "Cancelar"))
    y += 54
    o.append(button(PAD, y, CW, 48, "Cómo llegar", True, 15, "Como_llegar"))
    return frame("".join(o))


# ==========================================================================
# 15 · CANCELAR CITA (CONFIRMACIÓN)
# ==========================================================================
def s15_cancelar():
    set_prefix("15_")
    o = [status_bar(), app_bar("Detalle de la cita")]
    y = 104
    for i in range(4):
        o.append(rect(PAD, y + i * 62, CW, 52, fill=0.99, stroke=0.85, r=10))
        o.append(line_ph(PAD + 14, y + i * 62 + 18, 180, 8, 0.9))
        o.append(line_ph(PAD + 14, y + i * 62 + 32, 120, 7, 0.92))
    o.append(gid("Fondo_atenuado", rect(0, 44, W, H - 44, fill=0.1, op=0.55)))

    mx, my, mw, mh = 26, 190, 338, 430
    m = [rect(mx, my, mw, mh, fill=1.0, r=16),
         rect(mx + mw / 2 - 32, my + 28, 64, 64, fill=1.0, stroke=0.25, r=32, sw=2),
         text(mx + mw / 2, my + 60, "!", size=34, weight=700, anchor="middle"),
         text(mx + mw / 2, my + 118, "¿Cancelar esta cita?", size=19, weight=700,
              anchor="middle"),
         text(mx + mw / 2, my + 146, "Faltan menos de 24 horas. Según la política",
              size=11, fill=0.45, anchor="middle"),
         text(mx + mw / 2, my + 164, "de la clínica se retiene el 20% del valor.",
              size=11, fill=0.45, anchor="middle"),
         rect(mx + 20, my + 186, mw - 40, 62, fill=0.97, stroke=0.82, r=8),
         xbox(mx + 32, my + 198, 38, 38),
         text(mx + 82, my + 210, "Dra. Laura Gómez", size=12, weight=600),
         text(mx + 82, my + 228, "Mié 21 Ago · 10:30 AM", size=11, fill=0.45),
         text(mx + 20, my + 268, "Motivo de la cancelación", size=11, weight=600)]
    o.append(gid("Modal_cancelar", "".join(m)))

    cx, cy = mx + 20, my + 282
    for lab, act in [("Ya no puedo", True), ("Otro horario", False),
                     ("Otro", False)]:
        s, wd, _ = chip(cx, cy, lab, act, size=10, name=f"Motivo_{lab}")
        o.append(s)
        cx += wd + 8
        if cx > mx + mw - 90:
            cx, cy = mx + 20, cy + 32

    o.append(button(mx + 20, my + 330, mw - 40, 48, "Sí, cancelar la cita", True, 15,
                    "Confirmar_cancelacion"))
    o.append(button(mx + 20, my + 386, mw - 40, 44, "No, volver", False, 14,
                    "Volver"))
    return frame("".join(o))


# ==========================================================================
# 16 · MÉTODO DE PAGO
# ==========================================================================
def s16_pago():
    set_prefix("16_")
    o = [status_bar(), app_bar("Pago de la consulta", right=False)]
    y = 104

    rows = [("Consulta cardiología", "$90.000"), ("Servicio de plataforma", "$3.000")]
    o.append(rect(PAD, y, CW, 118, fill=0.98, stroke=0.78, r=10))
    ry = y + 24
    for k, v in rows:
        o.append(text(PAD + 14, ry, k, size=12, fill=0.45))
        o.append(text(W - PAD - 14, ry, v, size=12, weight=500, anchor="end"))
        ry += 26
    o.append(rect(PAD + 14, ry - 8, CW - 28, 1, fill=0.85))
    o.append(text(PAD + 14, ry + 18, "Total a pagar", size=13, weight=600))
    o.append(text(W - PAD - 14, ry + 18, "$93.000", size=17, weight=700, anchor="end"))
    y += 134

    o.append(text(PAD, y, "Método de pago", size=14, weight=600))
    y += 22
    metodos = [("Tarjeta terminada en 4821", "Visa · vence 09/27", True),
               ("PSE · Débito bancario", "Bancolombia, Davivienda…", False),
               ("Nequi / Daviplata", "Pago desde la app", False),
               ("Efectivo en el consultorio", "Se paga al llegar", False)]
    for titulo, sub, sel in metodos:
        b = [rect(PAD, y, CW, 58, fill=1.0, stroke=0.25 if sel else 0.78, r=10,
                  sw=1.5 if sel else 1),
             rect(PAD + 14, y + 19, 20, 20, fill=1.0, stroke=0.4, r=10),
             text(PAD + 48, y + 23, titulo, size=13, weight=600),
             text(PAD + 48, y + 41, sub, size=10, fill=0.5)]
        if sel:
            b.append(f'<circle cx="{PAD+24}" cy="{y+29}" r="6" fill="{gray(0.25)}"/>')
        o.append(gid(f"PAGO_{titulo}", "".join(b)))
        y += 66

    y += 4
    o.append(gid("CHK_Guardar_metodo",
                 rect(PAD, y, 18, 18, fill=1.0, stroke=0.5, r=3) +
                 text(PAD + 28, y + 9, "Guardar este método para próximas citas",
                      size=11, fill=0.45)))

    o.append(action_bar("Total a pagar", "$93.000", "Pagar y confirmar",
                        "Pagar_y_confirmar"))
    return frame("".join(o))


# ==========================================================================
# 17 · TELECONSULTA (VIDEOLLAMADA)
# ==========================================================================
def s17_teleconsulta():
    set_prefix("17_")
    o = [rect(0, 0, W, H, fill=0.15), status_bar(dark=True)]

    o.append(gid("IMG_Video_medico", xbox(0, 44, W, 560, r=0, fill=0.22, stroke=0.35)))
    o.append(text(W / 2, 300, "Video de la Dra. Laura Gómez", size=13, fill=0.6,
                  anchor="middle"))

    o.append(gid("IMG_Video_propio",
                 xbox(W - PAD - 100, 64, 100, 140, r=10, fill=0.28, stroke=0.4)))
    o.append(text(W - PAD - 50, 190, "Tú", size=10, fill=0.7, anchor="middle"))

    b = (rect(PAD, 60, 150, 28, fill=0.3, r=14) +
         f'<circle cx="{PAD+16}" cy="74" r="5" fill="{gray(0.85)}"/>' +
         text(PAD + 30, 74, "Conexión estable", size=11, fill=0.85))
    o.append(gid("Estado_conexion", b))

    o.append(text(PAD, 636, "Dra. Laura Gómez", size=18, weight=700, fill=1.0))
    o.append(text(PAD, 658, "Cardiología · En consulta 12:45", size=12, fill=0.65))

    ctrls = [("Micrófono", False), ("Cámara", False), ("Chat", False),
             ("Compartir", False), ("Colgar", True)]
    cw_ = 58
    total = len(ctrls) * cw_ + (len(ctrls) - 1) * 12
    cx = (W - total) / 2
    for lab, danger in ctrls:
        b = (f'<circle cx="{cx+cw_/2}" cy="720" r="27" fill="{gray(0.85 if danger else 0.3)}"/>'
             + rect(cx + cw_ / 2 - 10, 710, 20, 20, fill=0.15 if danger else 0.75, r=5)
             + text(cx + cw_ / 2, 762, lab, size=9, fill=0.7, anchor="middle"))
        o.append(gid(f"BTN_{lab}", b))
        cx += cw_ + 12

    o.append(text(W / 2, 800, "La consulta se guardará en tu historial",
                  size=10, fill=0.5, anchor="middle"))
    return frame("".join(o))


# ==========================================================================
# 18 · NOTIFICACIONES
# ==========================================================================
def s18_notificaciones():
    set_prefix("18_")
    o = [status_bar()]
    o.append(icon(16, 54, 26, name="Atras"))
    o.append(text(54, 68, "Notificaciones", size=18, weight=700))
    o.append(gid("LINK_Marcar_leidas",
                 text(W - PAD, 68, "Marcar leídas", size=11, weight=500, fill=0.4,
                      anchor="end")))
    y = 104

    def grupo(y, titulo, items):
        o.append(text(PAD, y, titulo, size=12, weight=600, fill=0.4))
        y += 20
        for tit, cuerpo, tiempo, nuevo in items:
            b = [rect(PAD, y, CW, 74, fill=0.985 if nuevo else 1.0, stroke=0.8, r=10),
                 rect(PAD + 12, y + 14, 32, 32, fill=0.85, r=8),
                 text(PAD + 56, y + 22, tit, size=13, weight=600),
                 text(PAD + 56, y + 42, cuerpo, size=11, fill=0.45),
                 text(PAD + 56, y + 60, tiempo, size=10, fill=0.55)]
            if nuevo:
                b.append(f'<circle cx="{W-PAD-18}" cy="{y+22}" r="5" '
                         f'fill="{gray(0.25)}"/>')
            o.append(gid(f"NOTIF_{tit}", "".join(b)))
            y += 82
        return y + 10

    y = grupo(y, "HOY", [
        ("Tu cita es mañana", "Dra. Laura Gómez · 10:30 AM", "Hace 2 horas", True),
        ("Cita confirmada", "El médico confirmó tu reserva SC-48219", "Hace 5 horas",
         True)])
    y = grupo(y, "ESTA SEMANA", [
        ("Resultados disponibles", "Ya puedes ver tu examen de sangre", "Lunes", False),
        ("Nuevo horario disponible", "Dr. Andrés Rojas abrió cupos el viernes",
         "Domingo", False),
        ("Califica tu consulta", "Cuéntanos cómo te fue con la Dra. Medina",
         "Domingo", False)])

    o.append(nav_bar(["Inicio", "Buscar", "Mis Citas", "Perfil"], 0))
    return frame("".join(o))


# ==========================================================================
# 19 · PERFIL DEL PACIENTE
# ==========================================================================
def s19_perfil_paciente():
    set_prefix("19_")
    o = [status_bar()]
    o.append(text(PAD, 66, "Mi perfil", size=20, weight=700))
    o.append(icon(344, 53, 26, name="Ajustes"))
    y = 100

    o.append(rect(PAD, y, CW, 100, fill=0.98, stroke=0.78, r=12))
    o.append(avatar(PAD + 16, y + 16, 68, "Foto_perfil"))
    o.append(text(PAD + 98, y + 34, "Daniel León", size=17, weight=700))
    o.append(text(PAD + 98, y + 54, "daniel.leon@correo.com", size=11, fill=0.5))
    o.append(text(PAD + 98, y + 70, "CC 1.020.458.771 · 28 años", size=10, fill=0.55))
    y += 114

    o.append(button(PAD, y, CW, 44, "Editar perfil", False, 14, "Editar_perfil"))
    y += 60

    o.append(text(PAD, y, "Mi salud", size=13, weight=600, fill=0.4))
    y += 20
    for lab, sub, nm in [("Hoja de vida médica", "Antecedentes, alergias, medicamentos",
                          "Hoja_vida"),
                         ("Historial de consultas", "8 consultas registradas",
                          "Historial"),
                         ("Documentos y exámenes", "5 archivos", "Documentos")]:
        o.append(option_row(y, lab, sub, nm))
        y += 60

    y += 8
    o.append(text(PAD, y, "Cuenta", size=13, weight=600, fill=0.4))
    y += 20
    for lab, sub, nm in [("Métodos de pago", "Visa terminada en 4821", "Pagos"),
                         ("Notificaciones", "Recordatorios activos", "Notificaciones"),
                         ("Ayuda y soporte", None, "Ayuda")]:
        o.append(option_row(y, lab, sub, nm))
        y += 60

    o.append(button(PAD, 700, CW, 44, "Cerrar sesión", False, 14, "Cerrar_sesion"))
    o.append(nav_bar(["Inicio", "Buscar", "Mis Citas", "Perfil"], 3))
    return frame("".join(o))


# ==========================================================================
# 20 · PANEL DE PACIENTES (MÉDICO)
# ==========================================================================
def s20_panel_pacientes():
    set_prefix("20_")
    o = [status_bar()]
    o.append(text(PAD, 66, "Pacientes", size=20, weight=700))
    o.append(icon(344, 53, 26, name="Filtrar"))
    y = 100

    o.append(gid("INPUT_Buscar_paciente",
                 rect(PAD, y, CW, 44, fill=0.97, stroke=0.72, r=10) +
                 rect(PAD + 12, y + 14, 16, 16, fill=0.7, r=8) +
                 text(PAD + 38, y + 22, "Buscar por nombre o documento", size=13,
                      fill=0.45)))
    y += 56

    cx = PAD
    for lab, act in [("Hoy (8)", True), ("Esta semana (24)", False),
                     ("Todos (312)", False)]:
        s, wd, _ = chip(cx, y, lab, act)
        o.append(s)
        cx += wd + 8
    y += 38

    o.append(text(PAD, y, "8 pacientes citados hoy", size=12, fill=0.45))
    o.append(gid("LINK_Exportar",
                 text(W - PAD, y, "Exportar lista", size=11, weight=500, fill=0.35,
                      anchor="end")))
    y += 20

    pacientes = [("Camila Ruiz", "34 años · O+", "8:00 AM · Control post-operatorio",
                  "Atendida", True),
                 ("Jorge Pineda", "51 años · A-", "9:00 AM · Dolor torácico",
                  "En consulta", True),
                 ("María Salazar", "29 años · B+", "10:30 AM · Lectura de exámenes",
                  "En espera", False),
                 ("Felipe Cárdenas", "63 años · O-", "11:30 AM · Control anual",
                  "En espera", False),
                 ("Sara Duarte", "41 años · AB+", "2:00 PM · Teleconsulta",
                  "Pendiente", False)]
    for nombre, datos, motivo, estado, act in pacientes:
        b = [rect(PAD, y, CW, 76, fill=1.0, stroke=0.78, r=10),
             xbox(PAD + 12, y + 16, 44, 44),
             text(PAD + 68, y + 24, nombre, size=13, weight=600),
             text(PAD + 68, y + 42, datos, size=10, fill=0.5),
             text(PAD + 68, y + 60, motivo, size=11, fill=0.4)]
        o.append(gid(f"PACIENTE_{nombre}", "".join(b)))
        s, _, _ = chip(W - PAD - 12 - (tw(estado, 10, 500) + 24), y + 14, estado, act,
                       size=10, name=f"Estado_{nombre}")
        o.append(s)
        y += 84

    o.append(nav_bar(["Agenda", "Pacientes", "Historial", "Perfil"], 1))
    return frame("".join(o))


# ==========================================================================
# 21 · GESTIÓN DE AGENDA (MÉDICO)
# ==========================================================================
def s21_gestion_agenda():
    set_prefix("21_")
    o = [status_bar(), app_bar("Gestión de agenda")]
    y = 104

    dias = [("Lun", "18"), ("Mar", "19"), ("Mié", "20"), ("Jue", "21"),
            ("Vie", "22"), ("Sáb", "23"), ("Dom", "24")]
    dw = (CW - 6 * 6) / 7
    for i, (d, n) in enumerate(dias):
        bx = PAD + i * (dw + 6)
        sel = i == 3
        b = (rect(bx, y, dw, 52, fill=0.22 if sel else 1.0,
                  stroke=0.22 if sel else 0.78, r=10) +
             text(bx + dw / 2, y + 17, d, size=10, fill=0.85 if sel else 0.5,
                  anchor="middle") +
             text(bx + dw / 2, y + 36, n, size=14, weight=600,
                  fill=1.0 if sel else 0.15, anchor="middle"))
        o.append(gid(f"DIA_{d}_{n}", b))
    y += 66

    o.append(text(PAD, y, "Jueves 21 de agosto", size=15, weight=600))
    o.append(gid("LINK_Copiar_horario",
                 text(W - PAD, y, "Copiar a otro día", size=11, weight=500, fill=0.4,
                      anchor="end")))
    y += 24

    resumen = [("5", "Disponibles"), ("3", "Reservadas"), ("2", "Bloqueadas")]
    bw = (CW - 20) / 3
    for i, (v, l) in enumerate(resumen):
        bx = PAD + i * (bw + 10)
        o.append(rect(bx, y, bw, 50, fill=0.98, stroke=0.78, r=10))
        o.append(text(bx + bw / 2, y + 19, v, size=16, weight=700, anchor="middle"))
        o.append(text(bx + bw / 2, y + 36, l, size=10, fill=0.45, anchor="middle"))
    y += 64

    franjas = [("8:00 AM", "Reservada · Camila Ruiz", "reservada"),
               ("9:00 AM", "Reservada · Jorge Pineda", "reservada"),
               ("10:00 AM", "Disponible para reservas", "libre"),
               ("10:30 AM", "Reservada · María Salazar", "reservada"),
               ("11:00 AM", "Disponible para reservas", "libre"),
               ("12:00 M", "Bloqueado · Almuerzo", "bloqueada"),
               ("2:00 PM", "Disponible para reservas", "libre")]
    for hora, desc, estado in franjas:
        bloq = estado == "bloqueada"
        res = estado == "reservada"
        b = [rect(PAD, y, CW, 54, fill=0.965 if bloq else 1.0, stroke=0.78, r=10),
             rect(PAD, y, 4, 54, fill=0.25 if res else (0.6 if bloq else 0.85)),
             text(PAD + 16, y + 22, hora, size=13, weight=600,
                  fill=0.45 if bloq else 0.13),
             text(PAD + 16, y + 40, desc, size=10, fill=0.5)]
        o.append(gid(f"FRANJA_{hora}", "".join(b)))
        o.append(switch(W - PAD - 54, y + 15, not bloq, f"Franja_{hora}"))
        y += 62

    o.append(button(PAD, y + 4, CW, 48, "Bloquear un rango de horas", False, 14,
                    "Bloquear_rango"))
    o.append(action_bar("Cambios sin guardar", "3 franjas", "Guardar cambios",
                        "Guardar_cambios"))
    return frame("".join(o))


# ==========================================================================
# 22 · REGISTRAR CONSULTA / NOTA RÁPIDA (MÉDICO)
# ==========================================================================
def s22_registrar_consulta():
    set_prefix("22_")
    o = [status_bar(), app_bar("Registrar consulta", right=False)]
    y = 104

    o.append(rect(PAD, y, CW, 66, fill=0.98, stroke=0.75, r=10))
    o.append(xbox(PAD + 12, y + 11, 44, 44))
    o.append(text(PAD + 68, y + 26, "Camila Ruiz Martínez", size=14, weight=600))
    o.append(text(PAD + 68, y + 45, "34 años · O+ · Hipertensión", size=11, fill=0.45))
    s, _, _ = chip(W - PAD - 12 - 74, y + 20, "8:00 AM", True, size=10, name="Hora")
    o.append(s)
    y += 80

    o.append(text(PAD, y, "Motivo de consulta", size=12, weight=600))
    y += 18
    blk, y = textarea(y, "Control post-operatorio. Refiere mejoría…", 3, "Motivo")
    o.append(blk)

    o.append(text(PAD, y, "Diagnóstico", size=12, weight=600))
    y += 18
    cx = PAD
    for lab, act in [("Hipertensión", True), ("Arritmia", False), ("Otro", False)]:
        s, wd, _ = chip(cx, y, lab, act, size=10, name=f"Dx_{lab}")
        o.append(s)
        cx += wd + 8
    y += 36
    blk, y = textarea(y, "CIE-10: I10 · Hipertensión esencial", 2, "Diagnostico")
    o.append(blk)

    o.append(text(PAD, y, "Tratamiento y órdenes", size=12, weight=600))
    y += 18
    blk, y = textarea(y, "Losartán 50 mg cada 12 h. Control en 3 meses.", 3,
                      "Tratamiento")
    o.append(blk)

    o.append(gid("BTN_Adjuntar",
                 rect(PAD, y, CW, 52, fill=1.0, stroke=0.6, r=10, dash="5 4") +
                 text(W / 2, y + 26, "+  Adjuntar examen o imagen", size=12,
                      weight=500, fill=0.4, anchor="middle")))
    y += 66

    bw = (CW - 10) / 2
    o.append(button(PAD, y, bw, 46, "Guardar borrador", False, 13, "Borrador"))
    o.append(button(PAD + bw + 10, y, bw, 46, "Firmar y guardar", True, 13,
                    "Firmar_guardar"))
    return frame("".join(o))


# ==========================================================================
# USER FLOW · tercer carril con los recorridos secundarios
# ==========================================================================
def s23_user_flow_extendido():
    set_prefix("FLOW2_")
    secundarios = [("Registro", "Crear cuenta nueva", False),
                   ("Filtros", "Especialidad, precio, distancia", False),
                   ("Valoraciones", "Opiniones del médico", False),
                   ("Pago", "Tarjeta, PSE o efectivo", True),
                   ("Detalle de cita", "Reprogramar o cancelar", False),
                   ("Teleconsulta", "Videollamada", False)]
    tmp = []
    w1, h1 = flow_lane(tmp, 0, 0, "x", "x", secundarios)
    FW, FH = w1 + 80, 110 + h1 + 40

    o = [rect(0, 0, FW, FH, fill=1.0),
         text(40, 46, "Flujos secundarios · SaludConecta", size=30, weight=700),
         text(40, 78, "Ramas que salen del recorrido principal: registro, filtros, "
                      "pago, gestión de la cita y teleconsulta.", size=14, fill=0.4)]
    flow_lane(o, 40, 110, "Ramas del paciente",
              "Cada una es el destino de un botón que existe en el flujo principal.",
              secundarios, tag="Secundario")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{FW}" height="{FH}" '
            f'viewBox="0 0 {FW} {FH}">' + "".join(o) + "</svg>")


SCREENS = [
    ("01-login", s01_login, "1 · Login - Credenciales"),
    ("02-home-paciente", s02_home, "2 · Home (Paciente)"),
    ("03-resultado-busqueda", s03_resultados, "3 · Resultado de Búsqueda"),
    ("04-detalle-medico", s04_detalle, "4 · Detalle del Médico"),
    ("05-agenda-fecha-hora", s05_agenda, "5 · Agenda · Fecha y hora"),
    ("06-confirmacion", s06_confirmacion, "6 · Confirmación"),
    ("07-dashboard-medico", s07_dashboard, "7 · Dashboard (Médico)"),
    ("08-hoja-vida-paciente", s08_hv_paciente, "8 · Hoja de Vida de Pacientes"),
    ("09-hoja-vida-medico", s09_hv_medico, "9 · Hoja de Vida Médicos"),
    ("10-mis-citas", s10_mis_citas, "10 · Mis Citas (Paciente)"),
    ("11-registro", s11_registro, "11 · Registro / Crear cuenta"),
    ("12-filtros", s12_filtros, "12 · Filtros avanzados"),
    ("13-valoraciones", s13_valoraciones, "13 · Valoraciones y opiniones"),
    ("14-detalle-cita", s14_detalle_cita, "14 · Detalle de la cita"),
    ("15-cancelar-cita", s15_cancelar, "15 · Cancelar cita"),
    ("16-pago", s16_pago, "16 · Método de pago"),
    ("17-teleconsulta", s17_teleconsulta, "17 · Teleconsulta"),
    ("18-notificaciones", s18_notificaciones, "18 · Notificaciones"),
    ("19-perfil-paciente", s19_perfil_paciente, "19 · Perfil del Paciente"),
    ("20-panel-pacientes", s20_panel_pacientes, "20 · Panel de Pacientes (Médico)"),
    ("21-gestion-agenda", s21_gestion_agenda, "21 · Gestión de Agenda (Médico)"),
    ("22-registrar-consulta", s22_registrar_consulta, "22 · Registrar Consulta"),
]

COLS = 6


def hoja_completa():
    """Todas las pantallas en una sola lámina."""
    gapx, gapy = 60, 96
    filas = (len(SCREENS) + COLS - 1) // COLS
    sheet_w = 160 + COLS * W + (COLS - 1) * gapx
    sheet_h = 220 + filas * H + (filas - 1) * gapy + 80
    o = [rect(0, 0, sheet_w, sheet_h, fill=0.96),
         text(80, 90, "SaludConecta — Wireframes de Baja Fidelidad", size=48,
              weight=700),
         text(80, 145, f"Tarea Diseño de App · Computación Móvil   |   "
                       f"{len(SCREENS)} pantallas   |   Flujo: Login > Buscar "
                       f"Especialista > Seleccionar Horario > Pago > Confirmación",
              size=20, fill=0.4)]
    for i, (slug, fn, titulo) in enumerate(SCREENS):
        col, row = i % COLS, i // COLS
        x = 80 + col * (W + gapx)
        y = 220 + row * (H + gapy)
        inner = fn()
        inner = inner[inner.index(">") + 1:inner.rindex("</svg>")]
        o.append(text(x, y - 16, titulo, size=18, weight=600, fill=0.35))
        o.append(f'<g transform="translate({x},{y})">' + inner + "</g>")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{sheet_w}" '
            f'height="{sheet_h}" viewBox="0 0 {sheet_w} {sheet_h}">' +
            "".join(o) + "</svg>")


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "docs", "svg")
    os.makedirs(out, exist_ok=True)
    for slug, fn, _ in SCREENS:
        open(os.path.join(out, slug + ".svg"), "w").write(fn())
    open(os.path.join(out, "23-user-flow.svg"), "w").write(s11_user_flow())
    open(os.path.join(out, "24-user-flow-secundarios.svg"), "w").write(
        s23_user_flow_extendido())
    open(os.path.join(out, "00-hoja-completa.svg"), "w").write(hoja_completa())
    print(f"{len(SCREENS)} pantallas + 2 user flows + la lámina completa")
