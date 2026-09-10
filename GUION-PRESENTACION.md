# Guión de presentación y defensa técnica

**Proyecto:** Skillia — Plataforma de cursos en línea
**Asignatura:** Programación Back End (TI2041) — Evaluación Sumativa 1
**Equipo:** Emilio Asencio · Matias Garcia
**Duración estimada:** 15 minutos de exposición + preguntas

---

## Cómo usar este documento

La exposición vale **60% de la nota**, repartida así:

| Bloque | Puntos | Cómo se gana |
| --- | --- | --- |
| **Parte A — grupal** | 20 | Presentación (4) · Justificación y proyección (4) · **Demostración funcional (8)** · Organización y participación equilibrada (4) |
| **Parte B — individual** | 40 | Flujo de Django (8) · **Explicar tu código (8)** · Responder preguntas (8) · **Modificar código en vivo (8)** · Aporte individual e IA (8) |

Los bloques en negrita son los que más peso tienen y los que más se fallan. La Parte B se
califica **por separado a cada integrante**: uno puede sacar 40 y el otro 20.

El texto en *cursiva* es lo que dices. Lo demás son indicaciones.

---

# PARTE 1 — Exposición grupal (≈12 min)

> **Criterio A4:** la participación debe ser equilibrada. Este guión alterna a los dos
> integrantes a propósito. No lean de la pantalla: usen esto para ensayar, no para recitar.

## 1.1 Apertura y problemática — **Emilio** (1.5 min)

*"Buenas tardes. Somos Emilio Asencio y Matias Garcia, y vamos a presentar Skillia, una
plataforma web de cursos en línea desarrollada con Django 5.2.17.*

*Partimos de un problema concreto: hoy sobra formación técnica en internet, pero encontrar un
curso que realmente sirva sigue siendo difícil. Identificamos tres puntos:*

*Primero, catálogos inabarcables: miles de cursos de calidad desigual, sin ningún filtro de
calidad previo.*

*Segundo, búsqueda pobre. Los listados te obligan a recorrerlo todo porque no te dejan acotar
por lo que importa: la tecnología, cuánto tiempo tienes disponible, cuánto puedes pagar o
quién dicta el curso.*

*Y tercero, la pérdida del hilo. Cuando retomas un curso después de unos días no sabes en qué
lección quedaste ni cuánto te falta, y eso es una de las principales causas de abandono.*

*A esto se suma que la mayoría de los estudiantes compatibiliza el estudio con trabajo, así
que necesita avanzar a su ritmo y en sesiones cortas."*

## 1.2 Objetivo, usuarios y alcance — **Matias** (2 min)

*"A partir de ese problema, nuestro objetivo general fue desarrollar una plataforma que le
permita a un estudiante hacer cuatro cosas: encontrar un curso pertinente mediante búsqueda y
filtros, evaluarlo a partir de su temario, duración, valoración y docente, inscribirse, y
avanzar lección por lección con seguimiento visible de su progreso.*

*Definimos cuatro roles:*

- *El **visitante**, que explora sin cuenta: ve el inicio, recorre el catálogo, filtra y
  entra al detalle de cualquier curso.*
- *El **estudiante**, que es el foco de esta etapa: hace todo lo anterior más inscribirse,
  entrar al reproductor, marcar lecciones completadas y ver su progreso.*
- *El **administrador**, que mantiene el catálogo. En esta etapa lo hace por el admin de
  Django y por comandos de carga, no tiene un panel propio.*
- *Y el **docente**, que en esta primera versión tiene solo presencia pública: aparece con su
  ficha, su especialidad y sus cursos, pero no inicia sesión ni administra contenido.*

*Sobre el alcance, queremos ser explícitos en qué dejamos fuera a propósito: el panel de
docente, el CRUD de cursos desde la interfaz, la pasarela de pago, la emisión de certificados,
la reproducción real de video y la API REST. Todo eso está declarado en el documento de
proyecto y proyectado a las unidades siguientes."*

> **Por qué decirlo así:** el criterio A1 premia explícitamente "diferenciar de forma explícita
> lo implementado de lo proyectado". Nombrar lo que **no** hicieron suma puntos, no los resta.

## 1.3 Justificación y proyección — **Emilio** (1.5 min)

*"La solución responde al problema punto por punto: el catálogo con filtros ataca la búsqueda
pobre, la ficha con temario y docente ataca la falta de criterio para elegir, y el registro de
progreso por lección ataca la pérdida del hilo.*

*Respecto a cómo evoluciona: en la Unidad 2 incorporamos formularios propios para el CRUD de
cursos, módulos y lecciones, el panel de docente con autenticación por rol, y el
endurecimiento de sesiones y seguridad. Eso se apoya en modelos que ya están definidos y
relacionados.*

*En la Unidad 3 sumamos la API REST con Django REST Framework: serializers para catálogo,
inscripciones y progreso, endpoints CRUD con salida JSON y autenticación por token. La lógica
de consulta ya está aislada en las vistas y en el modelo, así que se puede reutilizar desde
los serializers sin reescribirla."*

> **Prepárense para esta pregunta:** *"¿Por qué usaron base de datos si la Unidad 1 no la
> exigía?"* — Respuesta en la sección **P8** de este documento. Es la pregunta más probable de
> toda la defensa.

## 1.4 Demostración funcional — **los dos, alternando** (6 min) ⭐ 8 puntos

> Este es el bloque de mayor puntaje de la Parte A. El criterio exige "recorrer las interfaces
> principales, evidenciar navegación y datos simulados, y relacionar la demostración con el
> alcance declarado **sin depender de explicaciones no verificables**". Traducción: mostrar,
> no contar.

**Antes de empezar:** revisar la sección **Checklist previo** al final de este documento.

### Recorrido, en este orden

| # | Pantalla | Quién | Qué mostrar y decir |
| --- | --- | --- | --- |
| 1 | `/` Inicio | Matias | *"Esta es la portada. La navegación superior es un partial reutilizado en todas las páginas."* Abrir el modal "Quiénes Somos" para mostrar que es un `<dialog>` nativo, sin librerías. |
| 2 | `/courses/` Catálogo | Matias | *"Este es el catálogo completo: 6 cursos cargados desde un archivo JSON, no escritos en el HTML."* Señalar categoría, duración, valoración y precio en las tarjetas. |
| 3 | Filtros | Matias | **El momento fuerte de la demo.** Ver el guión detallado abajo. |
| 4 | `/courses/1/` Detalle | Emilio | Abrir **Master en React**. *"El temario se arma recorriendo módulos y lecciones: 5 módulos y 21 lecciones."* Mencionar que se usa `prefetch_related` para no hacer una consulta por módulo. |
| 5 | Inscripción | Emilio | Iniciar sesión con la cuenta de prueba y pulsar Inscribirme. *"La inscripción es un POST; crea el registro que da acceso al reproductor."* |
| 6 | Reproductor | Emilio | *"El reproductor abre en la primera lección no completada, no en la primera del curso."* Marcar una lección como completada y mostrar que la barra de progreso se mueve. |
| 7 | `/dashboard/` | Emilio | *"El panel calcula el porcentaje de avance por curso y recuerda la última lección vista."* |
| 8 | `/teachers/` | Matias | Listado y ficha de **Fernando Reveco**, con sus cursos asociados. |
| 9 | Ruta inexistente | Matias | Escribir una URL falsa para mostrar el 404 personalizado. *"Cerramos la navegación: no hay callejones sin salida."* |

### Guión detallado del bloque de filtros — **Matias**

Este es tu aporte principal y donde te pueden preguntar más. Hazlo en este orden, comentando
la URL en voz alta:

1. Escribe **`react`** en el buscador.
   *"Busca en título, descripción, categoría y nombre del docente, todo en la misma consulta.
   Devuelve dos cursos: Master en React y Full Stack con MERN — el segundo aparece porque
   React se menciona en su descripción."*
2. Limpia y marca la categoría **Backend**, luego suma **DevOps**.
   *"Los filtros de categoría son acumulativos: dos categorías, dos cursos."*
3. Marca duración **Menos de 10 horas**.
   *"Ahora se cruzan los dos filtros."*
4. **Señala la barra de direcciones.**
   *"Fíjense que todo el estado del filtro viaja en la URL. Es un formulario GET, así que esta
   búsqueda es enlazable y se puede recargar o compartir."*
5. Cambia el orden a **Precio: menor a mayor**.
6. Deja una combinación que no devuelva nada.
   *"Y este es el estado vacío, con un acceso directo para limpiar los filtros."*

> **Truco que suma:** antes de terminar, escribe a mano en la URL `?valoracion=abc` y muestra
> que la página no se rompe. *"Validamos cada parámetro: si llega basura por la query string,
> se ignora en vez de reventar la vista."* Eso responde por adelantado a una pregunta clásica.

## 1.5 Cierre — **Matias** (1 min)

*"En resumen: cumplimos el alcance que declaramos para esta unidad — configuración de Django,
flujo de rutas, vistas y templates, las interfaces de los roles previstos, navegación completa
y datos simulados desde un archivo JSON. Dejamos fuera, de forma consciente, lo que
corresponde a las unidades siguientes, y el proyecto está estructurado para incorporarlo sin
rehacer lo que ya existe. Quedamos atentos a sus preguntas."*

---

# PARTE 2 — Defensa individual (40 puntos por persona)

> Aquí cada uno responde por su cuenta. Lo que el otro sepa no te suma.

## 2.1 Reparto: qué defiende cada uno

| Emilio Asencio | Matias Garcia |
| --- | --- |
| `django_project/settings.py` (estructura base) | `django_project/settings.py` (variables de entorno) |
| `accounts/forms.py`, `accounts/views.py` | `courses/views.py` → `CourseListView` y filtros |
| `courses/models.py` (modelos del dominio) | `courses/models.py` → `parse_hours`, `duration_hours` |
| `courses/views.py` → `CourseDetailView`, `EnrollView`, `CoursePlayerView`, `CompleteLessonView` | `courses/management/commands/seed_courses.py` |
| `templates/courses/course_player.html`, `templates/dashboard.html` | `teachers/` completa |
| `templates/base.html` | `templates/courses/course_list.html`, `templates/partials/header_landing.html` |

## 2.2 B1 — El flujo de Django (8 pts)

**Los dos tienen que saber decir esto de memoria.** Es la pregunta de entrada más probable.

*"Cuando llega una petición, Django la toma en `django_project/urls.py`, que es el URLconf
raíz. Ahí se decide qué aplicación la atiende: `/courses/` se delega al `urls.py` de la
aplicación courses con `include()`. Ese archivo hace coincidir el patrón con una vista. La
vista prepara la información — consulta los modelos y arma el contexto — y se la entrega a un
template. El template solo presenta esos datos y devuelve el HTML como respuesta."*

**Ejemplo concreto, con nuestro proyecto:**

```
GET /courses/?q=react
  → django_project/urls.py         path("courses/", include("courses.urls"))
  → courses/urls.py                path("", CourseListView.as_view(), name="course_list")
  → courses/views.py               CourseListView.get_queryset() filtra los cursos
                                   CourseListView.get_context_data() agrega las facetas
  → templates/courses/course_list.html    recorre courses y dibuja las tarjetas
  → respuesta HTML
```

**Si preguntan MVT vs MVC:** *"Es el mismo patrón con otros nombres. El 'Modelo' es el mismo;
lo que Django llama View equivale al Controlador de MVC, y lo que Django llama Template es la
Vista de MVC. El 'controlador' propiamente tal es el propio framework, que enruta la petición."*

## 2.3 B2 — Preguntas sobre el código, con respuesta

### Para Matias

**P1. ¿Cómo se acumulan los filtros?**
*"`get_queryset()` parte de un QuerySet base y le va encadenando `.filter()` solo por los
parámetros que llegaron en `request.GET`. Como los QuerySets de Django son perezosos, no se
ejecuta ninguna consulta hasta que el template los recorre: termina siendo una sola consulta
SQL con todas las condiciones, no una por filtro."*

**P2. ¿Por qué usas objetos `Q` en la búsqueda?**
*"Porque necesito un OR. Si pongo varias condiciones dentro de un mismo `.filter()`, Django
las une con AND, y yo quiero que el texto se busque en el título **o** en la descripción **o**
en la categoría **o** en el nombre del docente. Eso se escribe con `Q(...) | Q(...)`."*

**P3. ¿Por qué la duración se resuelve en Python y no en la consulta?**
*"Porque el campo `duration` es texto libre: guarda `'12 horas'`, no un número. La base de
datos no puede compararlo como entero. Entonces `ids_in_duration_bucket()` recorre los pares
id–duración, extrae las horas con `parse_hours()`, que usa una expresión regular, y devuelve
los ids que caen en el tramo. Recién ahí filtro con `id__in`."*
*"Si tuviera que rehacerlo, lo correcto sería guardar la duración como entero de minutos y
formatearla al mostrarla. Lo mantuve así porque cambiar el tipo del campo implica migración y
tocar el catálogo completo."*

> Esa segunda frase vale oro: el criterio B2 premia **justificar** decisiones, y reconocer el
> límite de una decisión demuestra más criterio que defenderla a ciegas.

**P4. ¿Por qué los contadores de categoría no cambian al filtrar?**
*"Es a propósito. Las facetas se calculan sobre el catálogo completo con
`values('category').annotate(total=Count('id'))`, sin aplicar los filtros activos. Si las
calculara sobre el resultado filtrado, las opciones irían desapareciendo del panel a medida
que filtras y el usuario no podría volver atrás."*

**P5. ¿Por qué el formulario es GET y no POST?**
*"Porque filtrar es una consulta, no una modificación. Al ser GET, el estado queda en la URL:
la búsqueda es enlazable, se puede recargar sin reenviar nada y el navegador la guarda en el
historial. Un POST rompería las tres cosas."*

**P6. ¿Cómo funciona el comando `seed_courses`?**
*"Es un management command. Lee `catalog.json`, y recorre las listas de cursos, módulos y
lecciones. Los cursos se actualizan por id con `update_or_create`, para que las inscripciones
existentes sobrevivan a una recarga. Los módulos y lecciones, en cambio, se regeneran
completos, porque así el archivo es la única fuente de verdad y no quedan restos de una carga
anterior. Todo va dentro de una transacción: si algo falla, no queda a medias."*

**P7. ¿Qué hace `load_env()` en settings?**
*"Lee el archivo `.env` línea por línea y carga las variables con `os.environ.setdefault()`.
Uso `setdefault` a propósito: si la variable ya viene del entorno del sistema, esa gana. Así
en un despliegue real mandan las variables de la máquina y no un archivo. Y `get_env()` falla
con un mensaje explícito si falta algo obligatorio, en vez de arrancar con una configuración a
medias."*

### Para Emilio

**P8. ¿Por qué usaron base de datos si la Unidad 1 no la exigía?** ⚠️ *la más probable*
*"El requisito de la unidad es demostrar contenido dinámico con estructuras de Python, y eso
lo cumplimos: el catálogo está definido en `catalog.json` y se recorre con listas y
diccionarios en los comandos de carga. Apoyarlo en el ORM fue una decisión de alcance, no un
adelanto por adelantar: el seguimiento de progreso por estudiante y lección necesita conservar
estado entre sesiones, y eso en memoria se pierde al reiniciar el servidor. Sabemos que la
unidad no lo pide y no lo presentamos como logro de esta etapa."*

**P9. ¿Cómo se calcula el progreso del estudiante?**
*"Hay dos modelos: `Enrollment`, que une usuario y curso, y `Progress`, que une usuario y
lección con un booleano. Ambos con `unique_together`, así que no se pueden duplicar. Para
calcular el avance traigo las lecciones del curso con `Lesson.for_course()`, consulto los
`Progress` completados de ese usuario, y el porcentaje es la división entre ambos."*

**P10. ¿Por qué `Lesson.for_course()` es un classmethod del modelo y no código en la vista?**
*"Porque el orden en que se dictan las lecciones es una regla del dominio: primero por orden
de módulo, después por orden de lección. Esa regla la usan el reproductor y el dashboard. Si
la dejara escrita en cada vista, tendría la misma consulta duplicada en dos lugares y
podrían desincronizarse."*

**P11. ¿Qué pasa si alguien entra al reproductor sin estar inscrito?**
*"Lo redirijo al detalle del curso. `CoursePlayerView` sobrescribe `get()` y antes de
responder verifica que exista el `Enrollment`. Además la vista usa `LoginRequiredMixin`, así
que un usuario anónimo ni siquiera llega: lo manda al login con el `next` apuntando de vuelta."*

**P12. ¿Por qué el detalle del curso usa `prefetch_related`?**
*"Porque el temario recorre módulos y, dentro de cada módulo, sus lecciones. Sin prefetch eso
son una consulta inicial más una por cada módulo — el problema N+1. Con
`prefetch_related('modules__lessons')` Django las trae por adelantado en pocas consultas."*

**P13. ¿Por qué el registro usa un formulario propio y no el de Django?**
*"Porque queríamos que el usuario se registre e inicie sesión con su correo. `EmailUserCreationForm`
extiende el formulario estándar de Django, así que conserva la validación de contraseña que ya
trae el framework, y solo cambia lo que necesitábamos."*

## 2.4 B4 — Modificar código en vivo (8 pts) ⭐ el que más se falla

El profesor te va a pedir que **localices** algo y lo **cambies** delante de él. No se evalúa
que lo hagas rápido, sino que sepas **dónde** está y **qué** rompe tu cambio.

**Cómo responder siempre, en tres pasos:**

1. Di en voz alta dónde vas antes de abrir nada: *"Eso está en `courses/views.py`, en el
   método `get_queryset` de `CourseListView`."*
2. Haz el cambio.
3. Recarga y **muestra el efecto**. Luego di qué más se ve afectado.

### Cambios probables — Matias

| Si te piden… | Vas a… |
| --- | --- |
| "Agrega un tramo de duración" | `DURATION_BUCKETS` en `courses/views.py`. Agregas la clave con su etiqueta y su rango. El template lo dibuja solo, porque recorre el diccionario. |
| "Que la búsqueda no considere la descripción" | Borras el `Q(description__icontains=search)` del OR en `get_queryset()`. |
| "Cambia el orden por defecto" | La constante `DEFAULT_SORT`. |
| "Agrega una categoría nueva al catálogo" | `courses/seed_data/catalog.json` y vuelves a correr `python manage.py seed_courses`. |
| "Que el filtro de precio use otros tramos" | `PRICE_BUCKETS`, ajustando los `Decimal`. |
| "Muestra el nombre del docente en la tarjeta" | `templates/courses/course_list.html`, dentro del `{% for course in courses %}`: `{{ course.teacher.full_name }}`. Y explicas que no genera consultas extra porque la vista ya usa `select_related('teacher')`. |

### Cambios probables — Emilio

| Si te piden… | Vas a… |
| --- | --- |
| "Muestra cuántas lecciones tiene el curso en el detalle" | `CourseDetailView.get_context_data()` y luego el template. |
| "Que el reproductor abra siempre en la primera lección" | `CoursePlayerView.get_context_data()`, en la línea del `next(...)` que busca la primera no completada. |
| "Agrega un campo al registro" | `accounts/forms.py`, en `EmailUserCreationForm`. |
| "Ordena el dashboard por porcentaje de avance" | `DashboardView.get_context_data()`, ordenando `courses_data` antes de devolverlo. |
| "Agrega un curso a mano" | Por `/admin/`, o por el JSON del catálogo. |

> **Ensayen esto de verdad.** Elijan tres cambios de su tabla, háganlos cronometrados y
> devuelvan el archivo a como estaba. Es media hora y son 8 puntos.

## 2.5 B5 — Aporte individual y uso de IA (8 pts)

El instrumento dice textual que **si usaste IA y lo declaras, no hay penalización**. Lo que se
castiga es no poder explicar el código.

**Cómo plantearlo, sin rodeos:**

*"Usamos Claude Code como apoyo en dos partes, y está documentado en el anexo: el sistema de
filtros del catálogo y la configuración por variables de entorno. En ambos casos revisamos el
resultado, y hubo cosas que corregimos — por ejemplo, la instrucción original pedía filtrar
por lenguaje de programación, y al revisar los modelos vimos que ese campo no existía, así que
resolvimos la necesidad con la categoría y la búsqueda por texto en vez de agregar una columna
que el catálogo no usaba."*

Y si preguntan cuánto es tuyo: no exageres ni minimices. Di qué escribiste, qué te apoyó la
herramienta y **demuestra que lo entiendes** respondiendo P1 a P7.

> ⚠️ **Antes de la presentación:** las dos secciones "Revisión del equipo" de
> `docs/anexo-ia.md` siguen vacías. Complétenlas con lo que efectivamente revisaron. Es el
> respaldo escrito de este bloque.

---

# Checklist previo a la presentación

## El día anterior

- [ ] Completar las dos secciones **"Revisión del equipo"** de `docs/anexo-ia.md`.
- [ ] Commitear todo lo pendiente, incluida la baja de `db.sqlite3` del control de versiones.
- [ ] Verificar que la cuenta de prueba **entra**: usuario `pepito@gmail.com`, con 2 cursos
      inscritos. Si no recuerdan la contraseña, creen una cuenta nueva y déjenla lista.
- [ ] Ensayar la demo completa cronometrada, al menos dos veces.
- [ ] Cada uno: ensayar tres modificaciones en vivo de su tabla de B4.

## Dos horas antes

- [ ] Probar el proyecto **desde cero** en otra carpeta: clonar, crear el `.env`, `migrate`,
      `seed_teachers`, `seed_courses`, `runserver`. Si algo falla, es mejor descubrirlo ahora.
- [ ] `python manage.py check` sin errores.
- [ ] Levantar el servidor y recorrer las 9 pantallas de la demo.

## Cinco minutos antes

- [ ] Servidor corriendo en `http://127.0.0.1:8000/`.
- [ ] Sesión **cerrada** en el navegador (la demo empieza como visitante).
- [ ] Pestañas abiertas y en orden: inicio · catálogo · detalle del curso 1 · docentes.
- [ ] Editor abierto con `courses/views.py`, `courses/models.py` y
      `templates/courses/course_list.html` ya cargados, para B4.
- [ ] Zoom del navegador al 110–125% y del editor a un tamaño legible desde el fondo de la sala.
- [ ] Cerrar notificaciones, chats y todo lo que pueda aparecer encima.

---

# Problemas conocidos — léanlo antes de improvisar en la demo

Estas son cosas reales del proyecto que pueden aparecer si se salen del guión:

1. **No demuestren el curso "Introducción a DevOps" (id 6).** Tiene sus 5 módulos pero
   **ninguna lección** en el catálogo. No se cae — el reproductor responde correctamente —
   pero se ve vacío y no luce. Usen **Master en React** (5 módulos, 21 lecciones).
   *Si el profesor lo abre por su cuenta y lo nota:* *"Es un curso del catálogo de ejemplo al
   que le falta cargar el detalle de lecciones; los módulos están definidos y el reproductor
   responde sin error, solo que sin contenido que listar."*

2. **Los 6 cursos tienen el mismo docente.** Fernando Reveco dicta todo, y los otros 5
   docentes aparecen en `/teachers/` con 0 cursos. Por eso el **filtro por docente no se
   muestra en el catálogo**: la vista solo lo dibuja si hay más de un docente con cursos.
   *Si lo preguntan:* *"El panel de filtros se arma desde los datos: la sección de docente
   solo aparece cuando hay más de uno con cursos asignados. Con el catálogo de ejemplo actual
   hay uno solo, así que la ocultamos en vez de mostrar un filtro inútil."*
   *Si quieren evitar la pregunta:* repartan los cursos entre docentes desde `/admin/` antes
   de presentar; el filtro aparece solo.

3. **La `SECRET_KEY` vieja sigue en el historial de Git.** El código actual no expone
   secretos, pero si el profesor revisa commits antiguos, la va a ver.
   *Respuesta:* *"La detectamos y la sacamos del código: ahora se lee desde `.env`, que no se
   versiona, y generamos una clave nueva porque la anterior quedó comprometida. Limpiar el
   historial completo implicaba reescribirlo y romper el repositorio para el equipo."*

4. **Si el profesor clona el proyecto y no crea el `.env`, no arranca.** Falla con un mensaje
   explícito que dice qué hacer, y está documentado en el README, pero conviene advertirlo
   antes de que lo intente: *"Necesita copiar `.env.example` como `.env` y generar una clave;
   está en el README, primera sección."*

---

# Resumen de una página — para llevar impreso

**Qué es:** plataforma de cursos en línea. Django 5.2.17, 4 aplicaciones propias, 14 rutas.

**Problema:** catálogos inabarcables · búsqueda pobre · se pierde el hilo del avance.

**Objetivo:** encontrar → evaluar → inscribirse → avanzar con progreso visible.

**Roles:** visitante · estudiante (foco) · administrador (vía admin) · docente (solo público).

**Fuera de alcance, a propósito:** panel de docente · CRUD por interfaz · pagos · certificados
· video real · API REST.

**Proyección:** UA2 = CRUD, formularios, roles, sesiones. UA3 = API REST con DRF.

**Datos simulados:** `catalog.json` → 6 cursos, 30 módulos, 100 lecciones, cargados por
comandos idempotentes.

**El flujo, en una frase:** *URL raíz → include de la app → vista que arma el contexto →
template que presenta → respuesta.*

**Si te bloqueas:** describe lo que ves en pantalla y conéctalo con el archivo donde vive. Es
mejor decir *"eso está en `courses/views.py`, déjeme abrirlo"* que quedarse en silencio.
