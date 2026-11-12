# -*- coding: utf-8 -*-
"""Informes v2 del proyecto «Doy Dar», basados en el diagrama simplificado de la BBDD:
ANUNCIO (con datos de la persona) + FOTO + CATEGORIA. Sin chat ni reseñas dinámicas."""
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

VERDE = RGBColor(0x2E, 0x7D, 0x32)
RUTA = r'C:\Users\ivans\Projecte ESDIB\Doy Dar - Entregables'

def base_doc():
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)
    for i, sz in ((1, 18), (2, 14), (3, 12)):
        h = doc.styles['Heading %d' % i]
        h.font.name = 'Calibri'
        h.font.color.rgb = VERDE
    return doc

def cabecera(doc, titulo, subtitulo):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('Proyecto «Doy Dar»\n')
    r.font.size = Pt(22); r.font.bold = True; r.font.color.rgb = VERDE
    r2 = p.add_run(titulo + '\n')
    r2.font.size = Pt(16); r2.font.bold = True
    r3 = p.add_run(subtitulo)
    r3.font.size = Pt(11); r3.font.italic = True
    doc.add_paragraph()

def t(doc, datos, cabeceras):
    tabla = doc.add_table(rows=1, cols=len(cabeceras))
    tabla.style = 'Light Grid Accent 6'
    tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, c in enumerate(cabeceras):
        tabla.rows[0].cells[i].text = c
    for fila in datos:
        for i, v in enumerate(fila):
            tabla.add_row().cells[i].text = v
    for row in tabla.rows:
        for c in row.cells:
            for par in c.paragraphs:
                for run in par.runs:
                    run.font.size = Pt(10)
    doc.add_paragraph()


# ════════════════ INFORME 1: DETALLE DE LA BBDD (v2) ════════════════
doc = base_doc()
cabecera(doc, 'Informe detallado de la Base de Datos',
         'Tipo de valor de cada atributo — Versión final según diagrama simplificado (Entregable 2)')

doc.add_heading('1. Introducción', level=1)
doc.add_paragraph(
    '«Doy Dar» es una web que conecta a personas mayores que necesitan ayuda con jóvenes que buscan '
    'brindar apoyo (compañía, tareas del hogar, gestiones...), proponiendo un intercambio que puede '
    'incluir o no alojamiento.')
doc.add_paragraph(
    'En esta versión del proyecto la base de datos se ha simplificado. No hay tablas de usuarios registrados '
    'ni de chats: cada anuncio de la plataforma contiene, además de la información de la ayuda, los datos de '
    'la persona que lo publica. Las reseñas de la portada se escribirán a mano (no salen de la base de datos) '
    'y el chat solo se desarrollará más adelante si hay tiempo.')
doc.add_paragraph(
    'La base de datos queda formada por tres tablas — ANUNCIO, FOTO y CATEGORIA — más una tabla intermedia '
    'para unir anuncios y categorías. Todas aparecen en el diagrama entregado hecho en Draw.io.')

doc.add_heading('2. Tipos de valor que usamos', level=1)
t(doc, [
    ['Texto', 'Cadenas de texto planas, como nombres, correos, títulos o descripciones.'],
    ['Número', 'Cifras numéricas: el orden de las fotos y los identificadores.'],
    ['Fecha', 'Marcas de calendario y hora: la fecha (y hora) de publicación del anuncio.'],
    ['Booleano', 'Valores con dos opciones (Sí/No) o listas cerradas fijas: alojamiento (Sí/No/Tal vez) y estado (Activo/Oculto).'],
    ['Imagen', 'Archivos gráficos: las fotos de los anuncios. No se guardan dentro de la base de datos, se suben como ficheros y la tabla solo guarda una referencia (ruta o nombre del archivo).'],
], ['Tipo de valor', 'Qué significa'])

doc.add_heading('3. Entidades y atributos, uno a uno', level=1)

doc.add_heading('3.1. ANUNCIO — la tabla principal', level=2)
doc.add_paragraph(
    'Guarda un registro por cada anuncio publicado. Su rasgo principal es que incluye también los datos de la '
    'persona que lo propuso (nombre, contacto, municipio...), porque no hay una tabla de usuarios aparte. '
    'Es la tabla que alimenta toda la pantalla «Explora», el mapa, el tablero y el formulario de alta.')
t(doc, [
    ['id_anuncio', 'Número', 'Identificador único del anuncio (clave primaria). La base de datos lo asigna automáticamente.'],
    ['titulo', 'Texto', 'Título del anuncio, el que sale remarcado en la tarjeta (máx. 80 caracteres aprox.).'],
    ['texto_ofrezco', 'Texto largo', 'Campo «Ofrezco» de Crea un anuncio: qué pone la persona a disposición de la otra.'],
    ['texto_busco', 'Texto largo', 'Campo «Busco»: qué necesita a cambio (a cambio de ayuda con las tareas del hogar, compañía...).'],
    ['alojamiento', 'Texto (lista cerrada)', 'Sí / No / Tal vez, como el selector del formulario de creación.'],
    ['estado', 'Texto (lista cerrada)', 'Activo / Oculto: si el anuncio está publicado o pausado. Determina si se ve en Explora.'],
    ['fecha_publicacion', 'Fecha y hora', 'Momento en el que se publica; sirve para ordenar la lista de Explora y el mapa.'],
    ['nombre', 'Texto', 'Nombre de pila que aparece en la tarjeta («Isabel, 75 años»).'],
    ['apellidos', 'Texto', 'Apellidos de la persona que propone el anuncio.'],
    ['edad', 'Número (entero)', 'Edad que se muestra junto al nombre en las tarjetas y en el perfil («Isabel, 75 años»), «Edad 27»).'],
    ['correo_electronico', 'Texto (formato email)', 'Correo de contacto de la persona.'],
    ['telefono', 'Texto (numérico formateado)', 'Teléfono de contacto, para la opción de dar los datos por teléfono en el formulario.'],
    ['habilidades', 'Texto', 'Lista de etiquetas separadas por comas (Responsabilidad, Puntualidad, Paciencia...).'],
    ['municipio', 'Texto', 'Localidad (Huelva, Alcorcón, Murcia...). Es la pieza que ordena la lista de Explora y sitúa las marcas del mapa.'],
    ['zona', 'Texto', 'Subzona dentro del municipio (por ejemplo Triana). Completa la dirección visible en la tarjeta.'],
    ['verificado', 'Booleano', 'Sí/No: si la persona ya ha pasado la entrevista y la verificación de identidad hecha por el equipo.'],
], ['Atributo', 'Tipo de valor', 'Qué guarda y para qué sirve'])

doc.add_heading('3.2. FOTO — las imágenes de un anuncio', level=2)
doc.add_paragraph('Un anuncio puede tener varias fotos (las que se suben en «Crea un anuncio»); por eso son una tabla aparte (relación 1 a N).')
t(doc, [
    ['id_foto', 'Número', 'Identificador único de la foto (clave primaria automática).'],
    ['id_anuncio', 'Número (foránea)', 'A qué anuncio pertenece la foto (clave foránea a ANUNCIO).'],
    ['archivo', 'Imagen (ruta como Texto)', 'El archivo de la foto tal como se subió.'],
    ['orden', 'Número', 'Posición de la foto dentro del anuncio; la primera es la que se ve en la tarjeta.'],
], ['Atributo', 'Tipo de valor', 'Qué guarda y para qué sirve'])

doc.add_heading('3.3. CATEGORIA — los tipos de ayuda', level=2)
doc.add_paragraph('Las opciones que se muestran en los filtros de Explora y en el paso 1 del formulario.')
t(doc, [
    ['id_categoria', 'Número', 'Identificador único de la categoría (clave primaria automática).'],
    ['nombre', 'Texto', 'Nombre de la ayuda: Gestiones, Tareas del hogar, Recados, Tecnología, Compra, Compañía, Alojamiento.'],
], ['Atributo', 'Tipo de valor', 'Qué guarda y para qué sirve'])

doc.add_heading('3.4. ANUNCIO_CATEGORIA — la tabla que une ambas', level=2)
doc.add_paragraph(
    'La relación entre ANUNCIO y CATEGORIA es de varios a varios (N:M): un anuncio puede cubrir varias '
    'categorías (por ejemplo Compañía y Compra) y una categoría aparece en muchos anuncios. '
    'Para unirlas se usa una tabla intermedia con dos claves foráneas:')
t(doc, [
    ['id_anuncio', 'Número (foránea)', 'A qué anuncio apunta (clave foránea a ANUNCIO).'],
    ['id_categoria', 'Número (foránea)', 'A qué categoría apunta (clave foránea a CATEGORIA).'],
], ['Atributo', 'Tipo de valor', 'Qué guarda y para qué sirve'])

doc.add_heading('4. Resumen de relaciones (como en el diagrama)', level=1)
t(doc, [
    ['ANUNCIO → FOTO', '1 a N', 'Un anuncio puede tener varias fotos; cada foto pertenece a un solo anuncio.'],
    ['ANUNCIO ↔ CATEGORIA', 'N a M', 'Un anuncio puede cubrir varias categorías y una categoría abarca muchos anuncios (tabla intermedia ANUNCIO_CATEGORIA).'],
], ['Relación', 'Tipo', 'Explicación'])

doc.add_heading('5. Lo que no hay en la base de datos (y por qué)', level=1)
doc.add_paragraph(
    'Con la simplificación del proyecto, fuera de la base de datos quedan tres cosas: '
    'los usuarios registrados (los datos de la persona van dentro de cada ANUNCIO), '
    'los mensajes de chat (la sección Mensajes se mostrará con datos escritos a mano y, si más adelante se '
    'quiere un chat real, se añadirían tablas de CONVERSACION y MENSAJE) y '
    'las reseñas o testimonios de la portada, que se escribirán a mano como texto fijo de la web.')

doc.save(RUTA + r'\informe-detalle-bbdd-v2.docx')
print('Informe BBDD v2 OK')


# ════════════════ INFORME 2: CONTENIDO ESTÁTICO / DINÁMICO (v2) ════════════════
doc = base_doc()
cabecera(doc, 'Informe de contenido estático y dinámico',
         'Según la estructura de la web y el diagrama simplificado — Entregable 3')

doc.add_heading('1. ¿Qué es contenido estático y dinámico?', level=1)
doc.add_paragraph(
    'Contenido estático es el que está escrito y maquetado a mano en la propia web: no se cambia con el uso '
    'y por tanto no necesita base de datos. Incluye logos, textos fijos, navegación, avisos legales y las '
    'reseñas de la portada, que en este proyecto se colocan a mano.')
doc.add_paragraph(
    'Contenido dinámico es el que se saca de la base de datos cada vez que alguien abre la página: la lista '
    'de anuncios, el mapa, el detalle de un anuncio o las fotos. Cambia automáticamente porque depende de '
    'lo que hay guardado en las tablas ANUNCIO, FOTO y CATEGORIA.')
doc.add_paragraph(
    'A continuación se repasa cada pantalla de la web y se indica qué contenido es estático y cuál viene '
    'de la BBDD.')

doc.add_heading('2. Análisis por pantallas', level=1)

doc.add_heading('2.1. INICIO (portada pública)', level=2)
t(doc, [
    ['Titular «Compartir casa, tiempo y compañía entre distintas generaciones» y subtítulos', 'Estático', 'Texto fijo de la maquetación.'],
    ['Bloque «¿Cómo funciona?» (Publica o explora / Entrevista y verificación / Acuerdo de convivencia)', 'Estático', 'Explicación fija del servicio.'],
    ['Bloque testimonios «Así nos lo cuentan» (Mia, 23 años...)', 'Estático', 'Se escriben a mano: no salen de la BBDD en esta fase del proyecto.'],
    ['Banner Cruz Roja / Ministerio / fondos europeos y teléfono «Llámanos gratis al»', 'Estático', 'Texto e imágenes fijas.'],
    ['Botones «Busco ayuda», «Busco ayudar» y «Explora anuncios»', 'Estático', 'Botones fijos; lo que muestran al pulsarlos sí es dinámico.'],
    ['Menú superior y pie de página (Aviso legal, Privacidad, Accesibilidad, © 2026)', 'Estático', 'Navegación y textos legales fijos.'],
], ['Contenido', 'Tipo', 'De dónde sale'])

doc.add_heading('2.2. Formularios de alta (Paso 1, 2 y 3)', level=2)
doc.add_paragraph('En esta versión los formularios de registro van dirigidos a crear un ANUNCIO nuevo, '
                  'de forma que todos los datos que se piden encajan en la tabla principal.')
t(doc, [
    ['Títulos, textos de ayuda y orden de los campos', 'Estático', 'Maquetación del formulario.'],
    ['«¿Prefieres dictárnoslo por teléfono? Llama y te tomamos nota»', 'Estático', 'Texto fijo con el número de la entidad.'],
    ['Opciones del Paso 1: ¿qué propones intercambiar? (categorías y marcas de Balances)', 'Dinámico', 'Se guardan en la tabla intermedia ANUNCIO_CATEGORIA apuntando a las filas de CATEGORIA.'],
    ['Paso 2 «Sobre mí»: nombre y apellidos, habilidades, preséntate...', 'Dinámico', 'Se guardan como texto en los campos del ANUNCIO (nombre, apellidos, habilidades...).'],
    ['Paso 3 «Contacto»: correo, teléfono, ubicación, DNI', 'Dinámico', 'Correo, teléfono, municipio y zona se guardan en ANUNCIO. Las fotos del DNI no van a la BBDD: son documentación que revisa el equipo.'],
    ['Campo «verificado»', 'Dinámico', 'Se marca a mano por el equipo tras la entrevista; mientras es No, el anuncio no se publica.'],
], ['Contenido', 'Tipo', 'De dónde sale'])

doc.add_heading('2.3. EXPLORA (lista)', level=2)
t(doc, [
    ['Filtro de tipo de ayuda (las opciones que se muestran)', 'Dinámico', 'Se leen de la tabla CATEGORIA.'],
    ['Opciones fijas de otros filtros (alojamiento Sí/No/Tal vez)', 'Estático', 'Valores cerrados fijados por el diseño; el valor guardado en cada anuncio sí es dinámico.'],
    ['Selector Municipio / Zona', 'Dinámico', 'Los valores que ofrece se sacan de los campos municipio y zona de ANUNCIO.'],
    ['Tarjetas de anuncios (municipio, nombre y edad, zonas...) ej. «Huelva — Isabel»', 'Dinámico', 'Consulta a ANUNCIO filtrando solo estado = Activo, ordenando por fecha_publicacion.'],
    ['Selector Lista / Mapa y botón Buscar', 'Estático', 'Controles fijos de la interfaz.'],
    ['Pestañas de navegación (Explora, Tablero, Mensajes)', 'Estático', 'Cabecera fija de la web.'],
], ['Contenido', 'Tipo', 'De dónde sale'])

doc.add_heading('2.4. EXPLORA – Mapa', level=2)
t(doc, [
    ['Pínes de anuncios por municipio (Murcia, Huelva, Hellín...)', 'Dinámico', 'Consulta a ANUNCIO (municipio, titulo, estado).'],
    ['Mapa base (calles, nivel de zoom)', 'Estático', 'Lo aporta un servicio de mapas (Google Maps/ OpenStreetMap).'],
    ['Selector Lista / Mapa', 'Estático', 'Control fijo que cambia de vista; las dos vistas leen la misma BBDD.'],
], ['Contenido', 'Tipo', 'De dónde sale'])

doc.add_heading('2.5. EXPLORA – Perfil ajeno (detalle de un anuncio)', level=2)
t(doc, [
    ['Municipio, nombre, textos «Ofrezco» y «Busco»', 'Dinámico', 'Consulta a ANUNCIO del anuncio elegido.'],
    ['Galería de fotos del anuncio', 'Dinámico', 'Consulta a FOTO (campo archivo, ordenadas por orden).'],
    ['Categorías del anuncio (Gestiones, Compañía...)', 'Dinámico', 'Consulta a la tabla intermedia ANUNCIO_CATEGORIA + CATEGORIA.'],
    ['Botón «Contactar»', 'Estático', 'Botón fijo; en esta fase muestra los datos de contacto guardados (correo o teléfono), sin chat.'],
], ['Contenido', 'Tipo', 'De dónde sale'])

doc.add_heading('2.6. TABLERO (gestión de anuncios)', level=2)
t(doc, [
    ['Título «Tus anuncios» y navegación', 'Estático', 'Maquetación fija.'],
    ['Tarjetas de anuncios con su ubicación (Jerez, Galicia, Oviedo...)', 'Dinámico', 'Consulta a ANUNCIO; al no haber usuarios registrados, en esta fase el equipo gestiona los anuncios desde aquí.'],
    ['Botón «Crea un anuncio»', 'Estático', 'Control fijo que abre el formulario.'],
], ['Contenido', 'Tipo', 'De dónde sale'])

doc.add_heading('2.7. CREA UN ANUNCIO', level=2)
t(doc, [
    ['Título y etiquetas de los campos (Título, Fotos, Ofrezco, Busco, Alojamiento)', 'Estático', 'Formulario fijado por el diseño.'],
    ['Campos rellenados (título, fotos, Ofrezco, Busco, datos de contacto)', 'Dinámico', 'Se guardan en ANUNCIO y las fotos en FOTO.'],
    ['Selector «Alojamiento»: Sí / No / Tal vez', 'Estático', 'Opciones fijas; el valor elegido se guarda de forma dinámica en ANUNCIO.'],
    ['Selector de categorías del Paso 1', 'Dinámico', 'Se guarda la relación en ANUNCIO_CATEGORIA.'],
], ['Contenido', 'Tipo', 'De dónde sale'])

doc.add_heading('2.8. INFO PERFIL (editar anuncio)', level=2)
t(doc, [
    ['Etiquetas (Edad, Género, Habilidades, Preséntate, botón Actualiza)', 'Estático', 'Maquetación fija.'],
    ['Datos que se muestran (nombre, habilidades, presentación, contacto)', 'Dinámico', 'Consulta a ANUNCIO del anuncio que se está editando.'],
    ['Botón «Actualiza»', 'Dinámico', 'Modifica los campos de la fila de ANUNCIO guardada.'],
], ['Contenido', 'Tipo', 'De dónde sale'])

doc.add_heading('2.9. MENSAJES (lista de chats y conversación)', level=2)
doc.add_paragraph(
    'En esta fase del proyecto la sección de Mensajes NO está conectada a la base de datos: se muestra como '
    'maqueta con los textos escritos a mano (los nombres, horas y mensajes que se ven en el diseño). '
    'Es contenido estático. Si más adelante se desarrolla el chat, se añadiran las tablas CONVERSACION y '
    'MENSAJE y todo este bloque pasará a ser dinámico.')
t(doc, [
    ['Título «Mensajes», lista de conversaciones con horas «08:12»... y contador sin leer', 'Estático', 'Datos escritos a mano, con el aspecto del diseño (sin BBDD).'],
    ['Historial del chat («Mensajes Chat») y campo «Escribe algo»', 'Estático', 'Maqueta general; el envío de mensajes reales queda para una fase posterior.'],
], ['Contenido', 'Tipo', 'De dónde sale'])

doc.add_heading('2.10. Reseñas y testimonios', level=2)
t(doc, [
    ['Reseñas de la portada y cualquier comentario de las personas usuarias', 'Estático', 'Se escriben a mano y se suben con código; cuando exista la función de reseñas se estudiará una tabla propia.'],
], ['Contenido', 'Tipo', 'De dónde sale'])

doc.add_heading('3. Resumen general', level=1)
doc.add_paragraph(
    'Como conclusión: todo lo que cambia con el tiempo o depende de lo que ha publicado cada persona '
    '(anuncios, fotos, categorías de ayuda, municipios y zonas) viene de la base de datos y por tanto es '
    'contenido dinámico. Lo que es siempre lo mismo —títulos, textos explicativos, navegación, controles, '
    'textos legales- y lo que en esta fase se decide escribir a mano —las reseñas y los mensajes de la '
    'sección Mensajes— queda como contenido estático en la maquetación.')

doc.save(RUTA + r'\informe-contenido-estatico-dinamico-v2.docx')
print('Informe estático/dinámico v2 OK')
