# Registro de contribución individual

**Proyecto:** Skillia — Plataforma de cursos en línea
**Asignatura:** Programación Back End (TI2041) — Evaluación Sumativa 1
**Modalidad:** Equipo de dos integrantes

---

## Integrantes

| Integrante | Usuario Git | Commits | Líneas aportadas (código, plantillas y datos) |
| --- | --- | --- | --- |
| _(completar nombre)_ | `BoyJamuwu` | 1 | +1.412 |
| Matías Alberto | `matiudev` | 4 | +1.955 / −46 |

---

## Integrante 1 — _(completar nombre)_

**Aporte principal:** estructura base del proyecto y flujo del estudiante.

**Trabajo realizado**

- Creación y configuración inicial del proyecto Django 5.2.17 (`django_project/`: settings,
  urls, wsgi) y de la estructura de plantillas con `base.html`.
- Aplicación `pages` con la página de inicio.
- Aplicación `accounts`: formularios de registro e inicio de sesión por correo
  (`EmailUserCreationForm`, `EmailAuthenticationForm`), vista de registro, rutas de
  autenticación y vista del dashboard del estudiante con el cálculo de progreso por curso.
- Aplicación `courses` en su versión inicial: modelos `Course`, `Module`, `Lesson`,
  `Enrollment` y `Progress`; vistas de catálogo, detalle, inscripción y reproductor de
  lecciones; marcado de lección completada con respuesta JSON.
- Plantillas de inicio, catálogo, detalle de curso, reproductor, dashboard, login, registro
  y página 404.

**Evidencia:** commit `9673a75` (2026-08-31).

**Archivos donde puede rendir defensa técnica:**
`accounts/forms.py`, `accounts/views.py`, `courses/models.py`, `courses/views.py`
(`CourseDetailView`, `EnrollView`, `CoursePlayerView`, `CompleteLessonView`),
`templates/courses/course_player.html`, `templates/dashboard.html`.

---

## Integrante 2 — Matías Alberto

**Aporte principal:** cuerpo docente, navegación, carga de datos y filtros del catálogo.

**Trabajo realizado**

- Higiene del repositorio: `.gitignore` y limpieza de archivos generados del control de
  versiones.
- Footer del sitio y modales institucionales reutilizables (`templates/partials/footer.html`).
- Barra de navegación con menú responsive y modales "Quiénes Somos" e "Institución"
  (`templates/partials/header_landing.html`).
- Aplicación `teachers` completa: modelo `Teacher`, vistas de listado y ficha pública,
  rutas y plantillas; migración del campo `instructor` (texto) a una relación real con
  `Teacher`.
- Comandos de carga de datos: `seed_courses`, que lee `courses/seed_data/catalog.json`
  (6 cursos, 30 módulos, 100 lecciones) y lo sincroniza de forma idempotente, y
  `seed_teachers`, que carga el cuerpo docente.
- Sistema de filtros del catálogo: búsqueda por texto, filtros combinables por categoría,
  docente, duración, precio y valoración, seis criterios de ordenamiento y panel lateral
  responsive (`courses/views.py`, `templates/courses/course_list.html`).
- Configuración por variables de entorno para sacar los secretos del código versionado.
- Documentación del proyecto: `README.md` y los documentos de esta carpeta.

**Evidencia:** commits `51d1442`, `78e9832`, `8310a9f`, `f0ca91d` (2026-09-01 a 2026-09-09).

**Archivos donde puede rendir defensa técnica:**
`courses/views.py` (`CourseListView` y la lógica de filtros), `courses/models.py`
(`parse_hours`, `Course.duration_hours`), `courses/management/commands/seed_courses.py`,
`teachers/` (aplicación completa), `templates/courses/course_list.html`,
`templates/partials/header_landing.html`, `django_project/settings.py`.

---

## Distribución del trabajo

El reparto se organizó por área funcional, no por tipo de archivo: cada integrante trabajó
sus vistas, sus modelos y sus plantillas de extremo a extremo. Eso evitó bloqueos entre
ambos y permite que cada uno defienda un flujo completo de Django.

| Área | Responsable |
| --- | --- |
| Configuración del proyecto y base de plantillas | Emilio Asencio |
| Autenticación y dashboard | Emilio Asencio |
| Modelos del dominio de cursos | Emilio Asencio |
| Detalle de curso y reproductor | Emilio Asencio |
| Cuerpo docente | Matias Garcia |
| Navegación (header y footer) | Matias Garcia |
| Carga de datos y catálogo de ejemplo | Matias Garcia |
| Filtros y ordenamiento del catálogo | Matias Garcia |
| Configuración por entorno y documentación | Matias Garcia |
