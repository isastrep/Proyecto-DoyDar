# -*- coding: utf-8 -*-
"""Genera un diagrama ER SIMPLE (estilo Chen: rectángulos + rombos + elipses) para «Doy Dar».
Aspecto oscuro: shapes negras con borde y texto blancos, como el ejemplo de los compañeros."""
import xml.sax.saxutils as sax

FILL = '#000000'
STROKE = '#FFFFFF'
FONT = '#FFFFFF'

def shape(id, value, style, cx, cy, w, h):
    x = cx - w / 2
    y = cy - h / 2
    return ('<mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">'
            '<mxGeometry x="%s" y="%s" width="%s" height="%s" as="geometry"/></mxCell>'
            % (id, sax.escape(value), sax.escape(style, {'"': '&quot;'}), x, y, w, h))

def entidad(id, name, cx, cy, w=160, h=50):
    style = ('rounded=0;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;fontColor=%s;'
             'fontSize=13;' % (FILL, STROKE, FONT))
    return shape(id, name, style, cx, cy, w, h)

def rombo(id, name, cx, cy, w=140, h=70):
    style = ('shape=rhombus;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;fontColor=%s;'
             'fontSize=13;' % (FILL, STROKE, FONT))
    return shape(id, name, style, cx, cy, w, h)

def elipse(id, name, cx, cy, w=150, h=55):
    style = ('shape=ellipse;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;fontColor=%s;'
             'fontSize=13;' % (FILL, STROKE, FONT))
    return shape(id, name, style, cx, cy, w, h)

def edge(id, src, tgt):
    style = ('edgeStyle=none;html=1;endArrow=none;startArrow=none;rounded=0;strokeColor=#FFFFFF;'
             'strokeWidth=1.5;exitX=None;exitY=None')
    style = style.replace(';exitX=None;exitY=None', '')
    return ('<mxCell id="%s" style="%s" edge="1" parent="1" source="%s" target="%s">'
            '<mxGeometry relative="1" as="geometry"/></mxCell>' % (id, style, src, tgt))

def etiqueta(id, parent_edge, text, pos):
    """Etiqueta 1 / N clavada a un tramo de arista (pos -0.7 origen, 0.7 destino)."""
    style = ('edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];'
             'fontColor=#FFFFFF;fontSize=12;fontStyle=1')
    return ('<mxCell id="%s" value="%s" style="%s" vertex="1" connectable="0" parent="%s">'
            '<mxGeometry x="%s" relative="1" as="geometry"/></mxCell>'
            % (id, text, style, parent_edge, pos))


C = []  # celdas

# Relación = mensaje (rombos) con sus dos tramos por relación
def relacion(base, d_name, d_xy, a_id, a_xy, b_id, b_xy, uno, muchos, cardinal_a='1', cardinal_b='N'):
    """a --[1]--> rombo --[N]--> b"""
    C.append(rombo(base + '_d', d_name, d_xy[0], d_xy[1]))
    C.append(edge(base + '_e1', a_id, base + '_d'))
    C.append(edge(base + '_e2', base + '_d', b_id))
    C.append(etiqueta(base + '_l1', base + '_e1', cardinal_a, -0.6))
    C.append(etiqueta(base + '_l2', base + '_e2', cardinal_b, 0.6))


# ── ENTIDADES ──
C.append(entidad('usuario', 'USUARIO', 480, 125))
C.append(entidad('testimonio', 'TESTIMONIO', 200, 125))
C.append(entidad('categoria', 'CATEGORIA', 840, 125))
C.append(entidad('foto', 'FOTO', 160, 345))
C.append(entidad('anuncio', 'ANUNCIO', 500, 345))
C.append(entidad('conversacion', 'CONVERSACION', 840, 585, w=170))
C.append(entidad('mensaje', 'MENSAJE', 600, 745))

# ── RELACIONES ──
relacion('publica', 'Publica', (470, 235), 'usuario', None, 'anuncio', None, 1, 1)
relacion('tiene', 'Tiene', (335, 345), 'anuncio', None, 'foto', None, 1, 1, '1', 'N')
relacion('clasifica', 'Clasifica', (675, 230), 'anuncio', None, 'categoria', None, 1, 1, 'N', 'M')
relacion('abre', 'Abre', (675, 468), 'anuncio', None, 'conversacion', None, 1, 1, '1', 'N')
relacion('incluye', 'Incluye', (725, 682), 'conversacion', None, 'mensaje', None, 1, 1, '1', 'N')
relacion('cuenta', 'Cuenta', (320, 125), 'usuario', None, 'testimonio', None, 1, 1, '1', 'N')

# ── ATRIBUTOS (elipses) ──
C.append(elipse('correo', 'Correo', 480, 42))
C.append(edge('ea1', 'usuario', 'correo'))
C.append(elipse('alojamiento', 'Alojamiento', 500, 470))
C.append(edge('ea2', 'anuncio', 'alojamiento'))
C.append(elipse('fecha', 'Fecha y hora', 600, 855))
C.append(edge('ea3', 'mensaje', 'fecha'))


xml = ('<mxfile host="app.diagrams.net">'
       '<diagram name="ER simple Doy Dar" id="er-simple-doydar">'
       '<mxGraphModel dx="1000" dy="700" grid="1" gridSize="10" guides="1" tooltips="1" connect="1"'
       ' arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="826"'
       ' math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>'
       + '\n'.join(C) +
       '</root></mxGraphModel></diagram></mxfile>')

with open(r'C:\Users\ivans\Projecte ESDIB\Doy Dar - Entregables\diagrama-er-simple-doy-dar.drawio', 'w', encoding='utf-8') as fh:
    fh.write(xml)

print('Diagrama simple generado.')
