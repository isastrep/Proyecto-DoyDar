# -*- coding: utf-8 -*-
"""Diagrama ER estilo clásico (texto de clase) para «Doy Dar»:
   - Entidades: rectángulos
   - Atributos: ELIPSES dibujadas alrededor de cada entidad (la clave primaria va subrayada)
   - Relaciones: rombos con cardinalidades 1,1 / 0,N en las líneas
   - Estilo blanco/black como el ejemplo del profesor."""
import xml.sax.saxutils as sax

EW = 170   # ancho elipse atributo
EH = 55    # alto elipse

def rect(id, name, cx, cy, w=200, h=60):
    style = ('rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;'
             'fontColor=#000000;fontSize=14;fontStyle=1;fontFamily=Calibri;')
    return ('<mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">'
            '<mxGeometry x="%s" y="%s" width="%s" height="%s" as="geometry"/></mxCell>'
            % (id, sax.escape(name), sax.escape(style, {'"': '&quot;'}),
               cx - w / 2, cy - h / 2, w, h))

def rombo(id, name, cx, cy, w=120, h=70):
    style = ('shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;'
             'fontColor=#000000;fontSize=13;fontStyle=1;fontFamily=Calibri;')
    return ('<mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">'
            '<mxGeometry x="%s" y="%s" width="%s" height="%s" as="geometry"/></mxCell>'
            % (id, sax.escape(name), sax.escape(style, {'"': '&quot;'}),
               cx - w / 2, cy - h / 2, w, h))

def elipse(id, name, cx, cy, pk=False):
    fs = 4 if pk else 0   # fontStyle 4 = subrayado (clave primaria)
    style = ('shape=ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;'
             'fontColor=#000000;fontSize=12;fontStyle=%d;fontFamily=Calibri;' % fs)
    return ('<mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">'
            '<mxGeometry x="%s" y="%s" width="%s" height="%s" as="geometry"/></mxCell>'
            % (id, sax.escape(name), sax.escape(style, {'"': '&quot;'}),
               cx - EW / 2, cy - EH / 2, EW, EH))

def edge(id, src, tgt):
    style = ('edgeStyle=none;html=1;endArrow=none;startArrow=none;rounded=0;'
             'strokeColor=#000000;strokeWidth=1.5;')
    return ('<mxCell id="%s" style="%s" edge="1" parent="1" source="%s" target="%s">'
            '<mxGeometry relative="1" as="geometry"/></mxCell>' % (id, style, src, tgt))

def tag(id, parent_edge, text, pos):
    style = ('edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];'
             'fontColor=#000000;fontSize=11;fontFamily=Calibri;background=#FFFFFF;')
    return ('<mxCell id="%s" value="%s" style="%s" vertex="1" connectable="0" parent="%s">'
            '<mxGeometry x="%s" relative="1" as="geometry"/></mxCell>'
            % (id, sax.escape(text), style, parent_edge, pos))


C = []
E = []   # contador de ids

def atributos(ent_id, lista_pk, posiciones, prefijo):
    """Crea elipses de atributos y sus líneas hacia la entidad.
    posiciones: lista de (cx, cy). lista_pk: atributos que son clave primaria."""
    for i, (nombre, (cx, cy)) in enumerate(zip(atributos_actuales, posiciones)):
        eid = 'attr_%s_%d' % (prefijo, i + 1)
        C.append(elipse(eid, nombre, cx, cy, pk=(nombre in lista_pk)))
        C.append(edge('eattr_%s_%d' % (prefijo, i + 1), eid, ent_id))


# ── ENTIDADES ──
C.append(rect('usuario', 'USUARIO', 430, 1000))
C.append(rect('anuncio', 'ANUNCIO', 1300, 1000))
C.append(rect('categoria', 'CATEGORIA', 2150, 480))
C.append(rect('foto', 'FOTO', 1300, 1720))
C.append(rect('conversacion', 'CONVERSACION', 2000, 1400, w=210))
C.append(rect('mensaje', 'MENSAJE', 2650, 1400))
C.append(rect('testimonio', 'TESTIMONIO', 430, 1650))

# ── RELACIONES ──
C.append(rombo('publica_d', 'Publica', 865, 1000))
C.append(edge('publica_e1', 'usuario', 'publica_d'))
C.append(edge('publica_e2', 'publica_d', 'anuncio'))
C.append(tag('publica_l1', 'publica_e1', '1,1', -0.6))
C.append(tag('publica_l2', 'publica_e2', '0,N', 0.6))

C.append(rombo('tiene_d', 'Tiene', 1300, 1365))
C.append(edge('tiene_e1', 'anuncio', 'tiene_d'))
C.append(edge('tiene_e2', 'tiene_d', 'foto'))
C.append(tag('tiene_l1', 'tiene_e1', '1,1', -0.6))
C.append(tag('tiene_l2', 'tiene_e2', '0,N', 0.6))

C.append(rombo('clasifica_d', 'Clasifica', 1690, 760))
C.append(edge('clasifica_e1', 'anuncio', 'clasifica_d'))
C.append(edge('clasifica_e2', 'clasifica_d', 'categoria'))
C.append(tag('clasifica_l1', 'clasifica_e1', '0,N', -0.6))
C.append(tag('clasifica_l2', 'clasifica_e2', '1,M', 0.6))

C.append(rombo('abre_d', 'Abre', 1660, 1230))
C.append(edge('abre_e1', 'anuncio', 'abre_d'))
C.append(edge('abre_e2', 'abre_d', 'conversacion'))
C.append(tag('abre_l1', 'abre_e1', '1,1', -0.6))
C.append(tag('abre_l2', 'abre_e2', '0,N', 0.6))

C.append(rombo('incluye_d', 'Incluye', 2320, 1400))
C.append(edge('incluye_e1', 'conversacion', 'incluye_d'))
C.append(edge('incluye_e2', 'incluye_d', 'mensaje'))
C.append(tag('incluye_l1', 'incluye_e1', '1,1', -0.6))
C.append(tag('incluye_l2', 'incluye_e2', '1,N', 0.6))

C.append(rombo('cuenta_d', 'Cuenta', 430, 1370))
C.append(edge('cuenta_e1', 'usuario', 'cuenta_d'))
C.append(edge('cuenta_e2', 'cuenta_d', 'testimonio'))
C.append(tag('cuenta_l1', 'cuenta_e1', '0,1', -0.6))
C.append(tag('cuenta_l2', 'cuenta_e2', '0,N', 0.6))

# ── ATRIBUTOS EN ELIPSES ──
# USUARIO: 16 en dos columnas a la izquierda-encima
for i, (n, (cx, cy)) in enumerate([
        ('id_usuario', (150, 170)), ('nombre', (340, 250)), ('apellidos', (150, 260)),
        ('fecha_nacimiento', (340, 340)), ('genero', (150, 350)), ('habilidades', (340, 430)),
        ('presentacion', (150, 440)), ('correo_electronico', (340, 520)),
        ('contrasena', (150, 530)), ('telefono', (340, 610)), ('municipio', (150, 620)),
        ('zona', (340, 700)), ('dni_frente', (150, 710)), ('dni_trasero', (340, 790)),
        ('verificado', (150, 800)), ('fecha_registro', (340, 880)),
]):
    C.append(elipse('u_a%d' % i, n, cx, cy, pk=(n == 'id_usuario')))
    C.append(edge('u_e%d' % i, 'u_a%d' % i, 'usuario'))

# ANUNCIO: 8 encima, dos columnas
for i, (n, (cx, cy)) in enumerate([
        ('id_anuncio', (1000, 200)), ('id_usuario (FK)', (1340, 200)),
        ('titulo', (1000, 290)), ('texto_ofrezco', (1340, 290)),
        ('texto_busco', (1000, 380)), ('alojamiento', (1340, 380)),
        ('fecha_publicacion', (1000, 470)), ('estado', (1340, 470)),
]):
    C.append(elipse('a_a%d' % i, n, cx, cy, pk=(n == 'id_anuncio')))
    C.append(edge('a_e%d' % i, 'a_a%d' % i, 'anuncio'))

# CATEGORIA: 3 a la derecha
for i, (n, (cx, cy)) in enumerate([
        ('id_categoria', (2450, 380)), ('nombre', (2450, 490)), ('icono', (2450, 600)),
]):
    C.append(elipse('c_a%d' % i, n, cx, cy, pk=(n == 'id_categoria')))
    C.append(edge('c_e%d' % i, 'c_a%d' % i, 'categoria'))

# FOTO: 4 debajo en fila
for i, (n, (cx, cy)) in enumerate([
        ('id_foto', (1080, 1900)), ('id_anuncio (FK)', (1265, 1900)),
        ('archivo', (1450, 1900)), ('orden', (1635, 1900)),
]):
    C.append(elipse('f_a%d' % i, n, cx, cy, pk=(n == 'id_foto')))
    C.append(edge('f_e%d' % i, 'f_a%d' % i, 'foto'))

# CONVERSACION: 4 debajo en cuadrícula 2x2
for i, (n, (cx, cy)) in enumerate([
        ('id_conversacion', (1880, 1610)), ('id_usuario1 (FK)', (2130, 1610)),
        ('id_usuario2 (FK)', (1880, 1720)), ('fecha_inicio', (2130, 1720)),
]):
    C.append(elipse('cv_a%d' % i, n, cx, cy, pk=(n == 'id_conversacion')))
    C.append(edge('cv_e%d' % i, 'cv_a%d' % i, 'conversacion'))

# MENSAJE: 6 encima en dos columnas (a la derecha del lienzo)
for i, (n, (cx, cy)) in enumerate([
        ('id_mensaje', (2680, 1000)), ('id_conversacion (FK)', (2450, 1055)),
        ('id_emisor (FK)', (2680, 1110)), ('texto', (2450, 1165)),
        ('fecha_hora', (2680, 1220)), ('leido', (2450, 1275)),
]):
    C.append(elipse('m_a%d' % i, n, cx, cy, pk=(n == 'id_mensaje')))
    C.append(edge('m_e%d' % i, 'm_a%d' % i, 'mensaje'))

# TESTIMONIO: 1 a la izquierda + 4 debajo
for i, (n, (cx, cy)) in enumerate([
        ('id_testimonio', (130, 1560)), ('nombre_visible', (130, 1830)),
        ('edad', (330, 1830)), ('cita', (530, 1830)), ('fecha', (730, 1830)),
]):
    C.append(elipse('t_a%d' % i, n, cx, cy, pk=(n == 'id_testimonio')))
    C.append(edge('t_e%d' % i, 't_a%d' % i, 'testimonio'))

# ── NOTA ──
C.append('<mxCell id="nota" value="Atributo subrayado = clave primaria (PK).  '
         'FK = clave foránea." style="text;html=1;fontSize=13;fontColor=#000000;'
         'fontFamily=Calibri;align=left;" vertex="1" parent="1">'
         '<mxGeometry x="40" y="30" width="600" height="30" as="geometry"/></mxCell>')


xml = ('<mxfile host="app.diagrams.net">'
       '<diagram name="ER clásico con elipses Doy Dar" id="er-clasico-doydar">'
       '<mxGraphModel dx="1200" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1"'
       ' arrows="1" fold="1" page="1" pageScale="1" pageWidth="2900" pageHeight="2050"'
       ' math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>'
       + '\n'.join(C) +
       '</root></mxGraphModel></diagram></mxfile>')

with open(r'C:\Users\ivans\Projecte ESDIB\Doy Dar - Entregables\diagrama-er-clasico-elipses.drawio', 'w', encoding='utf-8') as fh:
    fh.write(xml)

print('OK. Tamaño:', len(xml))
