# Anexo de uso de herramientas de inteligencia artificial

**Proyecto:** Skillia — Plataforma de cursos en línea
**Asignatura:** Programación Back End (TI2041) — Evaluación Sumativa 1

Este anexo se presenta según la instrucción 13 de la evaluación. Deja constancia de en qué
partes del proyecto se usó asistencia de IA, con qué instrucciones, qué tipo de apoyo se
recibió y qué se revisó o modificó después.

> **Pendiente de completar:** este anexo documenta las sesiones de trabajo con IA que
> quedaron registradas. Si algún integrante utilizó otra herramienta o en otra parte del
> proyecto, debe agregar su sesión antes de la entrega. El uso de IA no penaliza; omitirlo, sí.

---

## 1. Herramienta utilizada

| Dato | Detalle |
| --- | --- |
| Herramienta | Claude Code (Anthropic), modelo Claude Opus 5 |
| Modalidad | Asistente de línea de comandos con acceso al repositorio local |
| Integrante que la utilizó | Matías Alberto |
| Fecha | 2026-09-09 |

---

## 2. Sesión 1 — Sistema de filtros del catálogo

### Instrucción principal entregada

> "Necesito que revises la parte donde dice Filtro y desarrolles la función de poder filtrar,
> mediante el nombre, quizás lenguaje o dependiendo de la estructura de la base de datos.
> Considera el diseño igual a la página de por sí."

### Tipo de apoyo recibido

Generación de código a partir de una descripción funcional. La herramienta revisó primero los
modelos y plantillas existentes, y luego propuso e implementó:

- La lógica de filtrado en `CourseListView` (`courses/views.py`).
- El helper `parse_hours()` y la propiedad `Course.duration_hours` en `courses/models.py`.
- El panel de filtros en `templates/courses/course_list.html`.

### Observaciones y correcciones surgidas del proceso

- **No existe un campo "lenguaje" en el modelo.** La instrucción original pedía filtrar por
  lenguaje; al revisar `courses/models.py` se verificó que la tabla `Course` no tiene ese
  campo. Se resolvió cubriendo esa necesidad con el campo `category` y con la búsqueda por
  texto sobre título y descripción, en lugar de agregar una columna que el catálogo no usa.
- **La duración está guardada como texto libre** (`"12 horas"`), no como número, así que no se
  puede comparar directamente en la consulta. Se agregó `parse_hours()` para extraer el valor
  numérico y agrupar los cursos en tramos.
- **Los parámetros inválidos no deben romper la página.** Se agregó validación de cada
  parámetro de la query string (`?valoracion=abc`, `?orden=basura`, `?docente=nope`) para que
  se ignoren en lugar de provocar un error.
- Se verificó el resultado ejecutando 16 combinaciones de filtros contra la base de datos
  local y contrastando los cursos devueltos con los datos de `catalog.json`.

### Revisión del equipo

_(Completar: qué revisó cada integrante, qué se modificó a mano y qué se decidió mantener.)_

---

## 3. Sesión 2 — Documentación y configuración por entorno

### Instrucción principal entregada

> "Revisa el PDF de la evaluación y dime qué faltaría."
> "Haz el documento de proyecto, el anexo de IA, el registro de contribución, el README,
> mueve la SECRET_KEY a .env y saca db.sqlite3 del control de versiones."

### Tipo de apoyo recibido

- Lectura del instrumento de evaluación y contraste con el estado real del repositorio.
- Redacción de `README.md`, `docs/proyecto-ua1.md`, `docs/contribucion-individual.md` y de
  este anexo, a partir del código existente y del historial de Git.
- Refactor de `django_project/settings.py` para leer `SECRET_KEY`, `DEBUG` y `ALLOWED_HOSTS`
  desde variables de entorno, con la función `load_env()` y `get_env()`.
- Creación de `.env.example` y corrección de `.gitignore` para dejar de versionar
  `db.sqlite3`.

### Observaciones surgidas del proceso

- La `SECRET_KEY` original quedó expuesta en el historial de Git, por lo que se generó una
  clave nueva para `.env` en lugar de reutilizar la anterior.
- La línea `db.sqlite3` estaba comentada en `.gitignore`, de modo que la base de datos seguía
  versionada pese al commit que decía haberla quitado. Se corrigió y se ejecutó
  `git rm --cached db.sqlite3`.

### Revisión del equipo

_(Completar: confirmación de que el contenido de los documentos refleja el proyecto real.)_

---

## 4. Declaración de responsabilidad

El equipo asume la responsabilidad sobre la totalidad del código entregado, haya sido escrito
directamente o con apoyo de IA. Cada integrante puede explicar el funcionamiento de los
archivos listados en su sección de `contribucion-individual.md`, justificar las decisiones de
diseño tomadas y realizar modificaciones sobre ellos durante la defensa técnica.

### Puntos del código asistido que el equipo debe poder explicar

Para la defensa individual, conviene tener claros estos puntos del código generado con apoyo
de IA:

1. **Cómo se acumulan los filtros.** `get_queryset()` parte de un QuerySet base y le va
   encadenando `.filter()` según los parámetros presentes en `request.GET`. Como los
   QuerySets de Django son perezosos, no se ejecuta ninguna consulta hasta que la plantilla
   recorre los resultados: se arma una sola consulta SQL con todas las condiciones.
2. **Por qué la búsqueda usa objetos `Q`.** Un `.filter(a=1, b=2)` combina condiciones con
   AND. Para buscar el mismo texto en título *o* descripción *o* categoría *o* nombre del
   docente se necesita OR, y eso se expresa con `Q(...) | Q(...)`.
3. **Por qué la duración se resuelve en Python.** El campo `duration` es texto, así que la
   base de datos no puede compararlo como número. `ids_in_duration_bucket()` recorre los pares
   `(id, duration)`, extrae las horas con `parse_hours()` y devuelve los ids que caen en el
   tramo; recién entonces se filtra con `id__in`.
4. **Por qué las facetas se calculan sobre el catálogo completo.** Los contadores de categoría
   se obtienen con `values("category").annotate(total=Count("id"))` sin aplicar los filtros
   activos, para que las opciones no desaparezcan del panel al filtrar.
5. **Cómo viaja el estado del filtro.** Todo el panel es un único `<form method="get">`, así
   que los filtros quedan en la URL: la página es enlazable, recargable y no requiere POST.
6. **Qué hace `load_env()` en settings.** Lee el archivo `.env` línea por línea y usa
   `os.environ.setdefault()`, de modo que una variable ya definida en el sistema tiene
   prioridad sobre el archivo.
