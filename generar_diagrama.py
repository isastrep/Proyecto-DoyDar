# -*- coding: utf-8 -*-
"""Genera el diagrama Entidad-Relación de la BBDD del proyecto «Doy Dar» en formato .drawio"""
import xml.sax.saxutils as sax

ROW_H = 30

def cell(id, value, style, x, y, w, h):
    return ('<mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">'
            '<mxGeometry x="%s" y="%s" width="%s" height="%s" as="geometry"/></mxCell>'
            % (id, sax.escape(value), sax.escape(style, {'"': '&quot;'}), x, y, w, h))

def table(id, name, x, y, w, attrs, fill, stroke):
    """attrs: lista de tuplas (texto, es_clave)"""
    h = ROW_H + len(attrs) * ROW_H
    parts = []
    # Tabla (cabecera)
    tbl_style = ('shape=table;startSize=%d;container=1;collapsible=0;childLayout=tableLayout;'
                 'fontSize=12;fontStyle=1;fillColor=%s;strokeColor=%s;fontSize=14;whiteSpace=wrap'
                 % (ROW_H, fill, stroke))
    parts.append('<mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">'
                 '<mxGeometry x="%s" y="%s" width="%s" height="%s" as="geometry"/></mxCell>'
                 % (id, sax.escape(name), sax.escape(tbl_style, {'"': '&quot;'}), x, y, w, h))
    # Filas (atributos)
    for i, (text, is_key) in enumerate(attrs):
        style = ('shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;'
                 'strokeColor=inherit;top=0;left=0;bottom=0;right=0;collapsible=0;dropTarget=0;'
                 'fillColor=none;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=12;'
                 'fontStyle=%d;whiteSpace=wrap' % (1 if is_key else 0))
        parts.append('<mxCell id="%s_r%d" value="" style="%s" vertex="1" parent="%s">'
                     '<mxGeometry y="%d" width="%s" height="%d" as="geometry"/></mxCell>'
                     % (id, i + 1, sax.escape(style, {'"': '&quot;'}), id, i * ROW_H, w, ROW_H))
        lbl_style = ('text;strokeColor=none;fillColor=none;align=%s;verticalAlign=middle;'
                     'spacingLeft=6;spacingRight=4;overflow=hidden;rotatable=0;'
                     'points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=12;fontStyle=%d;'
                     'whiteSpace=wrap' % ('left' if not is_key else 'left', 1 if is_key else 0))
        parts.append('<mxCell id="%s_r%d_a" value="%s" style="%s" vertex="1" parent="%s_r%d">'
                     '<mxGeometry width="%s" height="%d" as="geometry"/></mxCell>'
                     % (id, i + 1, sax.escape(text), sax.escape(lbl_style, {'"': '&quot;'}),
                        id, i + 1, w, ROW_H))
    return '\n'.join(parts), h

def edge(id, src_row, tgt_row, label, source_x_dash=False):
    style = ('edgeStyle=entityRelationEdgeStyle;fontSize=12;html=1;endArrow=none;startArrow=none;'
             'rounded=0;jettySize=auto;orthogonalLoop=1;strokeWidth=2;labelBackgroundColor=#FFFFFF;'
             'whiteSpace=wrap;fontStyle=1')
    return ('<mxCell id="%s" value="%s" style="%s" edge="1" parent="1" source="%s" target="%s">'
            '<mxGeometry relative="1" as="geometry"/></mxCell>'
            % (id, sax.escape(label), style, src_row, tgt_row))


cells = []

# Título y leyenda
cells.append(cell('titulo', 'Diagrama Entidad-Relación · Base de datos «Doy Dar»',
                  'text;html=1;fontSize=24;fontStyle=1;align=left;verticalAlign=middle;', 40, 30, 700, 40))
cells.append(cell('leyenda',
                  '(PK) clave primaria · (FK) clave foránea\n'
                  'Alojamiento: Sí / No / Tal vez   ·   Estado del anuncio: Activo / Oculto',
                  'text;html=1;fontSize=12;align=left;verticalAlign=middle;fontColor=#666666;',
                  40, 70, 500, 40))

# ── USUARIO ──
u_attrs = [
    ('id_usuario (PK)', True), ('nombre', False), ('apellidos', False), ('fecha_nacimiento', False),
    ('genero', False), ('habilidades', False), ('presentacion', False),
    ('correo_electronico', False), ('contrasena', False), ('telefono', False),
    ('municipio', False), ('zona', False), ('foto_dni_frente', False), ('foto_dni_trasero', False),
    ('verificado', False), ('fecha_registro', False),
]
t, h = table('usuario', 'USUARIO', 40, 140, 230, u_attrs, '#D5E8D4', '#82B366')
cells.append(t)

# ── ANUNCIO ──
a_attrs = [
    ('id_anuncio (PK)', True), ('id_usuario (FK)', False), ('titulo', False),
    ('texto_ofrezco', False), ('texto_busco', False), ('alojamiento', False),
    ('fecha_publicacion', False), ('estado', False),
]
t, h = table('anuncio', 'ANUNCIO', 430, 140, 230, a_attrs, '#DAE8FC', '#6C8EBF')
cells.append(t)

# ── FOTO_ANUNCIO ──
f_attrs = [('id_foto (PK)', True), ('id_anuncio (FK)', False), ('archivo', False), ('orden', False)]
t, h = table('foto', 'FOTO_ANUNCIO', 430, 480, 230, f_attrs, '#FFE6CC', '#D79B00')
cells.append(t)

# ── MENSAJE ──
m_attrs = [('id_mensaje (PK)', True), ('id_conversacion (FK)', False),
           ('id_emisor (FK)', False), ('texto', False), ('fecha_hora', False), ('leido', False)]
t, h = table('mensaje', 'MENSAJE', 430, 700, 230, m_attrs, '#E1D5E7', '#9673A6')
cells.append(t)

# ── CONVERSACION ──
c_attrs = [('id_conversacion (PK)', True), ('id_usuario1 (FK)', False),
           ('id_usuario2 (FK)', False), ('fecha_inicio', False)]
t, h = table('conversacion', 'CONVERSACION', 430, 980, 230, c_attrs, '#E1D5E7', '#9673A6')
cells.append(t)

# ── CATEGORIA ──
g_attrs = [('id_categoria (PK)', True),
           ('nombre', False), ('icono', False)]
t, h = table('categoria', 'CATEGORIA', 760, 140, 230, g_attrs, '#FFF2CC', '#D6B656')
cells.append(t)

# ── TESTIMONIO ──
ts_attrs = [('id_testimonio (PK)', True), ('id_usuario (FK)', False),
            ('nombre_visible', False), ('edad', False), ('cita', False), ('fecha', False)]
t, h = table('testimonio', 'TESTIMONIO', 760, 340, 230, ts_attrs, '#F8CECC', '#B85450')
cells.append(t)

# ── Nota Free/Municipios
cells.append(cell('nota1',
                  'Nota: los municipios y zonas se guardan como texto en USUARIO y ANUNCIO\n'
                  'para mantener la BBDD sencilla. La relación ANUNCIO – CATEGORIA es N:M\n'
                  '(un anuncio puede tener varias categorías y una categoría varios anuncios).',
                  'text;html=1;fontSize=12;align=left;verticalAlign=middle;fontColor=#aa3319;',
                  760, 580, 320, 70))

# ── Relaciones ──
cells.append(edge('rel1', 'usuario_r1', 'anuncio_r2', '1 publica N'))
cells.append(edge('rel2', 'usuario_r1', 'conversacion_r2', '1 crea N'))
cells.append(edge('rel3', 'usuario_r1', 'mensaje_r3', '1 escribe N'))
cells.append(edge('rel4', 'anuncio_r1', 'foto_r2', '1 tiene N'))
cells.append(edge('rel5', 'conversacion_r1', 'mensaje_r2', '1 incluye N'))
cells.append(edge('rel6', 'anuncio_r1', 'categoria_r1', 'N clasificada M'))


xml = ('<mxfile host="app.diagrams.net">'
       '<diagram name="BBDD Doy Dar" id="bbdd-doydar">'
       '<mxGraphModel dx="1000" dy="700" grid="1" gridSize="10" guides="1" tooltips="1" connect="1"'
       ' arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="826"'
       ' math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>'
       + '\n'.join(cells) +
       '</root></mxGraphModel></diagram></mxfile>')

with open(r'C:\Users\ivans\Projecte ESDIB\Doy Dar - Entregables\diagrama-bbdd-doy-dar.drawio', 'w', encoding='utf-8') as fh:
    fh.write(xml)

print('Diagrama generado correctamente.')
print('Tamaño:', len(xml), 'caracteres')
