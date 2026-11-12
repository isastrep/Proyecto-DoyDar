# -*- coding: utf-8 -*-
"""Diagrama ER simple con atributos DENTRO de cada tabla (rectángulo con título + lista).
Estilo oscuro, rombos para las relaciones y cardinalidades 1/N."""
import xml.sax.saxutils as sax

FILL = '#000000'
STROKE = '#FFFFFF'
FONT = '#FFFFFF'
LINE = 15   # alto de cada línea de atributo

def tabla(id, name, attrs, cx, cy, w=220):
    """Rectángulo con el nombre de la entidad en negrita y los atributos debajo."""
    h = 20 + 20 + len(attrs) * LINE + 10
    lineas = '<b>%s</b>' % name + '<br>' + '<br>'.join(attrs)
    style = ('rounded=0;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;fontColor=%s;'
             'fontSize=11;align=left;verticalAlign=top;spacingTop=6;spacingLeft=8;'
             'fontStyle=0;' % (FILL, STROKE, FONT))
    x, y = cx - w / 2, cy - h / 2
    return ('<mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">'
            '<mxGeometry x="%s" y="%s" width="%s" height="%s" as="geometry"/></mxCell>'
            % (id, sax.escape(lineas), sax.escape(style, {'"': '&quot;'}), x, y, w, h))

def rombo(id, name, cx, cy, w=120, h=60):
    style = ('shape=rhombus;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;fontColor=%s;'
             'fontSize=12;' % (FILL, STROKE, FONT))
    x, y = cx - w / 2, cy - h / 2
    return ('<mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">'
            '<mxGeometry x="%s" y="%s" width="%s" height="%s" as="geometry"/></mxCell>'
            % (id, sax.escape(name), sax.escape(style, {'"': '&quot;'}), x, y, w, h))

def edge(id, src, tgt):
    style = ('edgeStyle=none;html=1;endArrow=none;startArrow=none;rounded=0;'
             'strokeColor=#FFFFFF;strokeWidth=1.5')
    return ('<mxCell id="%s" style="%s" edge="1" parent="1" source="%s" target="%s">'
            '<mxGeometry relative="1" as="geometry"/></mxCell>' % (id, style, src, tgt))

def tag(id, parent_edge, text, pos):
    style = ('edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];'
             'fontColor=#FFFFFF;fontSize=11;fontStyle=1')
    return ('<mxCell id="%s" value="%s" style="%s" vertex="1" connectable="0" parent="%s">'
            '<mxGeometry x="%s" relative="1" as="geometry"/></mxCell>'
            % (id, text, style, parent_edge, pos))


C = []

# ── ENTIDADES CON ATRIBUTOS ──
C.append(tabla('usuario', 'USUARIO', [
    'id_usuario', 'nombre', 'apellidos', 'fecha_nacimiento', 'genero', 'habilidades',
    'presentacion', 'correo_electronico', 'contrasena', 'telefono', 'municipio',
    'zona', 'dni_frente', 'dni_trasero', 'verificado', 'fecha_registro',
], 200, 250, w=220))

C.append(tabla('anuncio', 'ANUNCIO', [
    'id_anuncio', 'id_usuario (FK)', 'titulo', 'texto_ofrezco', 'texto_busco',
    'alojamiento', 'fecha_publicacion', 'estado',
], 620, 250))

C.append(tabla('categoria', 'CATEGORIA', ['id_categoria', 'nombre', 'icono'], 960, 250))

C.append(tabla('foto', 'FOTO_ANUNCIO', ['id_foto', 'id_anuncio (FK)', 'archivo', 'orden'], 620, 540))

C.append(tabla('conversacion', 'CONVERSACION', [
    'id_conversacion', 'id_usuario1 (FK)', 'id_usuario2 (FK)', 'fecha_inicio',
], 960, 560))

C.append(tabla('mensaje', 'MENSAJE', [
    'id_mensaje', 'id_conversacion (FK)', 'id_emisor (FK)', 'texto', 'fecha_hora', 'leido',
], 620, 810))

C.append(tabla('testimonio', 'TESTIMONIO', [
    'id_testimonio', 'nombre_visible', 'edad', 'cita', 'fecha',
], 200, 590))

# ── RELACIONES (rombos) ──
def relacion(base, rombo_nombre, rxy, origen, destino, card_a, card_b, rw=110):
    C.append(rombo(base + '_d', rombo_nombre, rxy[0], rxy[1], w=rw))
    C.append(edge(base + '_e1', origen, base + '_d'))
    C.append(edge(base + '_e2', base + '_d', destino))
    C.append(tag(base + '_l1', base + '_e1', card_a, -0.55))
    C.append(tag(base + '_l2', base + '_e2', card_b, 0.55))

relacion('publica', 'Publica', (415, 250), 'usuario', 'anuncio', '1', 'N')
relacion('clasifica', 'Clasifica', (790, 250), 'anuncio', 'categoria', 'N', 'M', rw=100)
relacion('tiene', 'Tiene', (620, 420), 'anuncio', 'foto', '1', 'N')
relacion('abre', 'Abre', (800, 430), 'anuncio', 'conversacion', '1', 'N')
relacion('incluye', 'Incluye', (800, 720), 'conversacion', 'mensaje', '1', 'N')
relacion('cuenta', 'Cuenta', (200, 450), 'usuario', 'testimonio', '1', 'N')

xml = ('<mxfile host="app.diagrams.net">'
       '<diagram name="ER simple con atributos" id="er-simple-atributos">'
       '<mxGraphModel dx="1000" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1"'
       ' arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="960"'
       ' math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>'
       + '\n'.join(C) +
       '</root></mxGraphModel></diagram></mxfile>')

with open(r'C:\Users\ivans\Projecte ESDIB\Doy Dar - Entregables\diagrama-er-simple-con-atributos.drawio', 'w', encoding='utf-8') as fh:
    fh.write(xml)

print('OK, generado diagrama simple con atributos. Tamaño:', len(xml))
