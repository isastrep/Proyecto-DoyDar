# -*- coding: utf-8 -*-
"""Genera los dos informes del proyecto «Doy Dar» en formato Word (.docx)"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

VERDE = RGBColor(0x2E, 0x7D, 0x32)

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

def tabla_atributos(doc, datos, cabeceras):
    t = doc.add_table(rows=1, cols=len(cabeceras))
    t.style = 'Light Grid Accent 6'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, c in enumerate(cabeceras):
        t.rows[0].cells[i].text = c
    for fila in datos:
        for i, v in enumerate(fila):
            t.add_row().cells[i].text = v
    for row in t.rows:
        for c in row.cells:
            for par in c.paragraphs:
                for run in par.runs:
                    run.font.size = Pt(10)
    doc.add_paragraph()


# ══════════════════════ INFORME 1: DETALLE DE LA BBDD ══════════════════════
doc = base_doc()
cabecera(doc, 'Informe detallado de la Base de Datos',
         'Tipo de valor de cada atributo — Entregable 2 (diagrama asociado: diagrama-bbdd-doy-dar.drawio)')

doc.add_heading('1. Introducción', level=1)
doc.add_paragraph(
    '«Doy Dar» es una web que conecta a personas mayores que necesitan ayuda con jóvenes que buscan '
    'brindar apoyo (compania, tareas del hogar, gestiones...), proponiendo un intercambio que puede '
    'incluir o no alojamiento. La base de datos guarda las personas registradas, sus anuncios, las '
    'fotos de esos anuncios, las categorías de ayuda, las conversaciones entre usuarios y los '
    'testimonios que se muestran en la portada.')
doc.add_paragraph(
    'El diagrama completo de entidades y relaciones está hecho en Draw.io. En este documento se '
    'explica qué tipo de valor contiene cada atributo (Texto, Numérico, Fecha, Booleano...).')

doc.add_heading('2. Tipos de valor que usamos', level=1)
tabla_atributos(doc, [
    ['Texto', 'Cadenas de texto planas, como nombres, correos o descripciones.'],
    ['Número', 'Cifras numéricas: edad, orden de las fotos, identificadores.'],
    ['Fecha', 'Fechas de calendario o marcas de fecha y hora (fecha_registro, fecha_hora de un mensaje).'],
    ['Booleano', 'Valores que solo tienen dos opciones (Sí/No), o listas cerradas fijas (alojamiento: Sí/No/Tal vez; estado: Activo/Oculto).'],
    ['Imagen', 'Archivos gráficos: fotos de los anuncios y alojamiento de las dos caras del DNI. No se guardan dentro de la BBDD, se guardan como ficheros y la BBDD guarda una referencia (ruta/nombre del archivo).'],
], ['Tipo de valor', 'Qué significa'])

doc.add_heading('3. Entidades y atributos, uno a uno', level=1)

doc.add_heading('3.1. USUARIO — la persona registrada', level=2)
doc.add_paragraph('Guarda a cualquiera que se da de alta, sea mayor o joven. Los perfiles se verifican con el DNI.')
tabla_atributos(doc, [
    ['id_usuario', 'Número', 'Identificador único del usuario (clave primaria). Se lo asigna la BBDD automáticamente.'],
    ['nombre', 'Texto', 'Nombre de pila (ej.: Marta).'],
    ['apellidos', 'Texto', 'Los dos apellidos del formulario.'],
    ['fecha_nacimiento', 'Fecha', 'De donde se calcula la edad que se muestra en los anuncios (75 años, etc.).'],
    ['genero', 'Texto (lista cerrada)', 'Hombre / Mujer / Indiferente, como en los formularios.'],
    ['habilidades', 'Texto', 'Lista de etiquetas separadas por comas (Responsabilidad, Puntualidad...).'],
    ['presentacion', 'Texto largo', 'El campo «Preséntate» del formulario, redactado por el propio usuario.'],
    ['correo_electronico', 'Texto (formato email)', 'Se usa también para iniciar sesión.'],
    ['contrasena', 'Texto', 'Se guarda encriptada, nunca a la vista.'],
    ['telefono', 'Texto (numérico formateado)', 'Teléfono de contacto.'],
    ['municipio', 'Texto', 'Localidad (Huelva, Alcorcón...) para los filtros de Explora y el mapa.'],
    ['zona', 'Texto', 'Subzona dentro del municipio (p. ej. Triana).'],
    ['foto_dni_frente', 'Imagen (ruta como Texto)', 'Cara delantera del DNI, subida en el paso 3.'],
    ['foto_dni_trasero', 'Imagen (ruta como Texto)', 'Cara trasera del DNI.'],
    ['verificado', 'Booleano', 'Sí/No: indica si la entrevista y el DNI ya se han verificado.'],
    ['fecha_registro', 'Fecha', 'Momento del alta en la plataforma.'],
], ['Atributo', 'Tipo de valor', 'Qué guarda y para qué sirve'])

doc.add_heading('3.2. ANUNCIO — el anuncio de la plataforma', level=2)
doc.add_paragraph('Lo que ve el usuario en «Explora» y crea desde «Crea un anuncio».')
tabla_atributos(doc, [
    ['id_anuncio', 'Número', 'Identificador único del anuncio (clave primaria automática).'],
    ['id_usuario', 'Número (foránea)', 'A qué usuario pertenece el anuncio (clave foránea).'],
    ['titulo', 'Texto', 'Título del anuncio (máximo 80 caracteres aprox.).'],
    ['texto_ofrezco', 'Texto largo', 'Campo «Ofrezco» de Crea un anuncio.'],
    ['texto_busco', 'Texto largo', 'Campo «Busco» de Crea un anuncio.'],
    ['alojamiento', 'Texto (lista cerrada)', 'Sí / No / Tal vez, como en el formulario.'],
    ['fecha_publicacion', 'Fecha y hora', 'Momento en que se publica; sirve para ordenar la lista de Explora.'],
    ['estado', 'Texto (lista cerrada)', 'Activo / Oculto: según esté publicado o pausado el anuncio.'],
], ['Atributo', 'Tipo de valor', 'Qué guarda y para qué sirve'])

doc.add_heading('3.3. FOTO_ANUNCIO — las fotos de un anuncio', level=2)
doc.add_paragraph('Un anuncio puede tener varias fotos; por esta razón van en una tabla aparte (1 a N).')
tabla_atributos(doc, [
    ['id_foto', 'Número', 'Identificador único de la foto (clave primaria automática).'],
    ['id_anuncio', 'Número (foránea)', 'A qué anuncio pertenece (clave foránea).'],
    ['archivo', 'Imagen (ruta como Texto)', 'Archivo de la foto tal como se subió en «Crea un anuncio».'],
    ['orden', 'Número', 'Posición de la foto dentro del anuncio (la primera es la principal).'],
], ['Atributo', 'Tipo de valor', 'Qué guarda y para qué sirve'])

doc.add_heading('3.4. CATEGORIA — tipos de ayuda', level=2)
doc.add_paragraph('Las opciones que aparecen en los filtros de Explora y en Crea un anuncio.')
tabla_atributos(doc, [
    ['id_categoria', 'Número', 'Identificador único de la categoría (clave primaria automática).'],
    ['nombre', 'Texto', 'Nombre de la ayuda: Gestiones, Tareas del hogar, Recados, Tecnología, Compra, Compañía, Alojamiento.'],
    ['icono', 'Texto', 'Nombre del icono con el que se dibuja cada categoría en pantalla.'],
], ['Atributo', 'Tipo de valor', 'Qué guarda y para qué sirve'])
doc.add_paragraph(
    'Relación entre ANUNCIO y CATEGORIA: es de varios a varios (N:M). Un anuncio puede abarcar '
    'varias categorías (por ejemplo Compañía y Compra) y una categoría aparece en muchos anuncios. '
    'Para representarlo se crea una tabla intermedia «ANUNCIO_CATEGORIA» con dos claves foráneas: '
    'id_anuncio (Número foránea) e id_categoria (Número foránea).')

doc.add_heading('3.5. CONVERSACION — un chat entre dos personas', level=2)
tabla_atributos(doc, [
    ['id_conversacion', 'Número', 'Identificador único de la conversación (clave primaria automática).'],
    ['id_usuario1', 'Número (foránea)', 'El primer participante del chat (clave foránea).'],
    ['id_usuario2', 'Número (foránea)', 'El segundo participante del chat (clave foránea).'],
    ['fecha_inicio', 'Fecha y hora', 'Momento en que un usuario pulsa «Contactar» y se abre el chat.'],
], ['Atributo', 'Tipo de valor', 'Qué guarda y para qué sirve'])

doc.add_heading('3.6. MENSAJE — cada línea escrita en un chat', level=2)
tabla_atributos(doc, [
    ['id_mensaje', 'Número', 'Identificador único del mensaje (clave primaria automática).'],
    ['id_conversacion', 'Número (foránea)', 'A qué chat pertenece este mensaje (clave foránea).'],
    ['id_emisor', 'Número (foránea)', 'Quién escribió el mensaje (clave foránea a USUARIO).'],
    ['texto', 'Texto largo', 'Contenido escrito por el usuario en el campo «Escribe algo».'],
    ['fecha_hora', 'Fecha y hora', 'Momento del envío (08:12, 09:32...).'],
    ['leido', 'Booleano', 'Sí/No: si el receptor ya lo ha visto (sirve para marcar la conversación con mensajes sin leer).'],
], ['Atributo', 'Tipo de valor', 'Qué guarda y para qué sirve'])

doc.add_heading('3.7. TESTIMONIO — «Así nos lo cuentan» (portada)', level=2)
tabla_atributos(doc, [
    ['id_testimonio', 'Número', 'Identificador único del testimonio (clave primaria automática).'],
    ['id_usuario', 'Número (foránea, opcional)', 'Del testimonio a qué usuario está vinculado, si este está registrado.'],
    ['nombre_visible', 'Texto', 'Nombre que se publica (p. ej. «Mia»).'],
    ['edad', 'Número', 'Edad que se enseña debajo del nombre (23 años).'],
    ['cita', 'Texto largo', 'La frase en cursiva del testimonio.'],
    ['fecha', 'Fecha', 'Fecha en que se publicó el testimonio, para mostrar los más recientes.'],
], ['Atributo', 'Tipo de valor', 'Qué guarda y para qué sirve'])

doc.add_heading('4. Resumen de relaciones (como en el diagrama)', level=1)
tabla_atributos(doc, [
    ['USUARIO → ANUNCIO', '1 a N', 'Un usuario publica muchos anuncios; un anuncio pertenece a un solo usuario.'],
    ['ANUNCIO → FOTO_ANUNCIO', '1 a N', 'Un anuncio tiene varias fotos; cada foto pertenece a un anuncio.'],
    ['ANUNCIO ↔ CATEGORIA', 'N a M', 'Un anuncio puede cubrir varias categorías y una categoría abarca muchos anuncios (tabla intermedia ANUNCIO_CATEGORIA).'],
    ['USUARIO ↔ CONVERSACION', 'Participantes', 'Una conversación guarda dos participantes (id_usuario1 e id_usuario2), ambos foráneas a USUARIO.'],
    ['CONVERSACION → MENSAJE', '1 a N', 'Una conversación contiene muchos mensajes.'],
    ['USUARIO → MENSAJE', '1 a N', 'Un usuario escribe muchos mensajes (id_emisor).'],
    ['USUARIO → TESTIMONIO', '1 a N', 'Opcional: conexión con el usuario real, si lo hay.'],
], ['Relación', 'Tipo', 'Explicación'])

doc.save(r'C:\Users\ivans\OneDrive\Documentos\Proyecto predeterminado\Doy Dar - Entregables\informe-detalle-bbdd.docx')
print('Informe BBDD OK')


# ════════════════ INFORME 2: CONTENIDO ESTÁTICO / DINÁMICO ════════════════
doc = base_doc()
cabecera(doc, 'Informe de contenido estático y dinámico',
         'Según la estructura de la web — Entregable 3')

doc.add_heading('1. ¿Qué es contenido estático y dinámico?', level=1)
doc.add_paragraph(
    'Contenido estático es el que está escrito y maquetado a mano: no se cambia y por tanto no '
    'necesita base de datos. Incluye logos, textos fijos, navegación, recomendaciones y textos informativos.')
doc.add_paragraph(
    'Contenido dinámico es el que se saca de la base de datos cada vez que alguien abre la pantalla: '
    'listas de usuarios, anuncios, mensajes, testimonials... cambia si cambia la información guardada.')
doc.add_paragraph(
    'A continuación se repasa cada pantalla de la web y se indica qué contenido es estático y '
    'cuál viene de la BBDD.')

doc.add_heading('2. Análisis por pantallas', level=1)

doc.add_heading('2.1. INICIO (portada pública)', level=2)
tabla_atributos(doc, [
    ['«Compartir casa, tiempo y compañía...» — titular y subtítulos', 'Estático', 'Texto fijo de la maquetación.'],
    ['Bloque «¿Cómo funciona?» (3 pasos: Publica o explora / Entrevista y verificación / Acuerdo convivencia)', 'Estático', 'Explicación fija del servicio.'],
    ['Bloque testimonios «Así nos lo cuentan» (Mia, 23 años...)', 'Dinámico', 'Tabla TESTIMONIO (apellido, edad, cita).'],
    ['Banner de la Cruz Roja, Ministerio y fondos europeos', 'Estático', 'Texto e imágenes fijas del mandatario.'],
    ['«Llámanos gratis al» (número de teléfono)', 'Estático', 'Dato fijo de contacto.'],
    ['Enlace «Explora anuncios»', 'Estático', 'El botón en sí; lo que enseña al pulsarlo es dinámico.'],
    ['Menú superior y pie de página (Aviso legal, Privacidad, Accesibilidad, © 2026)', 'Estático', 'Navegación y textos legales fijos.'],
    ['Botones «Busco ayuda» / «Busco ayudar»', 'Estático', 'Botones fijos de entrada al registro.'],
], ['Contenido', 'Tipo', 'De dónde sale'])

doc.add_heading('2.2. Formularios de registro (Paso 1, 2 y 3)', level=2)
tabla_atributos(doc, [
    ['Títulos, textos de ayuda y orden de los campos', 'Estático', 'Maquetación del formulario.'],
    ['Opción «¿Prefieres dictárnoslo por teléfono? Llama...»', 'Estático', 'Texto fijo con el número.'],
    ['Lista de categorías del Paso 1 (¿Qué propones intercambiar?)', 'Dinámico', 'Tabla CATEGORIA (nombre, icono).'],
    ['Campos del Paso 2 (nombre, edad, género, habilidades, preséntate)', 'Dinámico', 'Datos que el usuario teclea y se guardan en USUARIO.'],
    ['Campos del Paso 3 (correo, teléfono, ubicación, DNI)', 'Dinámico', 'Se guardan en USUARIO (y las dos fotos del DNI como archivos).'],
], ['Contenido', 'Tipo', 'De dónde sale'])

doc.add_heading('2.3. EXPLORA', level=2)
tabla_atributos(doc, [
    ['Opciones de los filtros: categoría de ayuda', 'Dinámico', 'Tabla CATEGORIA.'],
    ['Opciones del filtro género (Hombre/Mujer/Indiferente) y alojamiento (Sí/No/Tal vez)', 'Estático', 'Valores cerrados fijados por el diseño.'],
    ['Tarjetas de anuncios (municipio, nombre y edad): «Huelva — Isabel, 75 años»...', 'Dinámico', 'Consulta a ANUNCIO + USUARIO (nombre, fecha de nacimiento, municipio).'],
    ['Selector Lista / Mapa y botón Buscar', 'Estático', 'Controles fijos de la interfaz.'],
    ['Pestañas de navegación (Explora, Tablero, Mensajes)', 'Estático', 'Cabecera fija de la app.'],
], ['Contenido', 'Tipo', 'De dónde sale'])

doc.add_heading('2.4. EXPLORA – Mapa', level=2)
tabla_atributos(doc, [
    ['Pines con un anuncio por municipio (Murcia, Huelva, Hellín...)', 'Dinámico', 'Consulta a ANUNCIO + USUARIO por municipio.'],
    ['Mapa base (calles, zoom)', 'Estático', 'Compuesto por un servicio de mapas (ej. Google Maps / OpenStreetMap).'],
], ['Contenido', 'Tipo', 'De dónde sale'])

doc.add_heading('2.5. EXPLORA – Perfil ajeno', level=2)
tabla_atributos(doc, [
    ['Municipio, nombre y edad, y los textos de los anuncios (Ofrezco / Busco)', 'Dinámico', 'Consulta a USUARIO + ANUNCIO.'],
    ['Foto del anuncio', 'Dinámico', 'Tabla FOTO_ANUNCIO.'],
    ['Botón «Contactar»', 'Estático', 'Botón fijo que crea una CONVERSACION (dinámico al usarse).'],
], ['Contenido', 'Tipo', 'De dónde sale'])

doc.add_heading('2.6. TABLERO (mis anuncios)', level=2)
tabla_atributos(doc, [
    ['Título «Tus anuncios» y navegación', 'Estático', 'Maquetación fija.'],
    ['Tarjetas de anuncios propios con su ubicación', 'Dinámico', 'Consulta a ANUNCIO filtrada por el usuario conectado.'],
    ['Botón «Crea un anuncio»', 'Estático', 'Control fijo que abre el formulario.'],
], ['Contenido', 'Tipo', 'De dónde sale'])

doc.add_heading('2.7. CREA UN ANUNCIO', level=2)
tabla_atributos(doc, [
    ['Título y etiquetas de los campos (Título, Fotos, Ofrezco, Busco, Alojamiento)', 'Estático', 'Formulario fijado.'],
    ['Campos rellenados por el usuario', 'Dinámico', 'Se guardan en ANUNCIO y las fotos en FOTO_ANUNCIO.'],
    ['Selector Alojamiento: Sí / No / Tal vez', 'Estático', 'Opciones fijas; el valor elegido se guarda en la BBDD.'],
], ['Contenido', 'Tipo', 'De dónde sale'])

doc.add_heading('2.8. INFO PERFIL (perfil personal)', level=2)
tabla_atributos(doc, [
    ['Etiquetas (Edad, Género, Habilidades, Preséntate, Actualiza)', 'Estático', 'Maquetación fija.'],
    ['Datos que se muestran (Marta, 27, mujer, habilidades, presentación)', 'Dinámico', 'Consulta a USUARIO del usuario conectado.'],
    ['Botón «Actualiza» / edición', 'Dinámico', 'Modifica los registros de USUARIO.'],
], ['Contenido', 'Tipo', 'De dónde sale'])

doc.add_heading('2.9. MENSAJES (lista) y chat', level=2)
tabla_atributos(doc, [
    ['Título «Mensajes» y campo «Escribe algo»', 'Estático', 'Maquetación fija.'],
    ['Lista de conversaciones (nombre, hora, resumen último mensaje, contador sin leer)', 'Dinámico', 'Consulta a CONVERSACION + USUARIO + MENSAJE (último por fecha_hora, campo leido).'],
    ['Historial de mensajes en el chat', 'Dinámico', 'Consulta a MENSAJE filtrada por id_conversacion.'],
    ['Estado «conectado a las 09:32»', 'Dinámico', 'Fecha y hora de entrada (fecha_inicio o similar).'],
], ['Contenido', 'Tipo', 'De dónde sale'])

doc.add_heading('3. Resumen general', level=1)
doc.add_paragraph('Como conclusión, todo lo que cambia con el tiempo o depende de cada usuario (anuncios, '
                  'perfiles, mensajes, testimonios, categorías y fotos) viene de la base de datos. '
                  'Lo que es siempre lo mismo (títulos, textos explicativos, navegación, controles y textos '
                  'legales) está como contenido fijo en la maquetación.')

doc.save(r'C:\Users\ivans\OneDrive\Documentos\Proyecto predeterminado\Doy Dar - Entregables\informe-contenido-estatico-dinamico.docx')
print('Informe estático/dinámico OK')
