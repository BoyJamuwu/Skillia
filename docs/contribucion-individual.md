# Registro de contribución individual

**Proyecto:** Skillia — Plataforma de cursos en línea
**Asignatura:** Programación Back End (TI2041) — Evaluación Sumativa 1
**Modalidad:** Equipo de dos integrantes

---

## Integrantes

| Integrante | Usuario Git | Commits propios | Líneas aportadas (código, plantillas y datos) |
| --- | --- | --- | --- |
| Emilio Asencio | `BoyJamuwu` | 1 | +1.756 |
| Matias Garcia | `matiudev` | 5 | +2.520 / −59 |

El commit `71a3563` (rol Docente y PostgreSQL) se trabajó entre ambos y se subió desde la
cuenta de Matias; sus líneas se reparten en la tabla según lo que hizo cada uno.

---

## Integrante 1 — Emilio Asencio

**Aporte principal:** estructura base del proyecto, flujo del estudiante e interfaz del
panel docente.

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
- Interfaz del panel docente: formularios `CourseForm`, `ModuleForm` y `LessonForm`
  (`teachers/forms.py`) y las plantillas del panel (resumen de cursos, gestión de módulos y
  lecciones, formulario genérico, confirmación de borrado y mensajes).
- Separación de roles en la navegación: el docente que entra al Dashboard se redirige a su
  panel, y el header muestra "Panel Docente" en lugar de "Dashboard".

**Evidencia:** commit `9673a75` (2026-08-31) y parte del commit `71a3563` (2026-10-06).

**Archivos donde puede rendir defensa técnica:**
`accounts/forms.py`, `accounts/views.py`, `courses/models.py`, `courses/views.py`
(`CourseDetailView`, `EnrollView`, `CoursePlayerView`, `CompleteLessonView`),
`templates/courses/course_player.html`, `templates/dashboard.html`, `teachers/forms.py`,
`templates/teachers/panel/`, `accounts/views.py` (`DashboardView.get`).

---

## Integrante 2 — Matias Garcia

**Aporte principal:** cuerpo docente, navegación, carga de datos, filtros del catálogo,
lógica del rol Docente y migración a PostgreSQL.

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
- Rol Docente: campo `Teacher.user` que vincula la cuenta con su ficha (migración
  `0002_teacher_user`), vistas del panel en `teachers/panel_views.py` con el control de
  permisos (cada docente solo ve y modifica sus propios cursos, módulos y lecciones), rutas
  del panel y opción `seed_teachers --create-users` para crear una cuenta por docente.
- Migración a PostgreSQL: conexión configurable desde `.env` (`DB_NAME`, `DB_USER`, ...),
  driver `psycopg`, detección de `libpq` en Windows, reinicio de las secuencias de ids en
  `seed_courses` y retiro completo de SQLite del proyecto.
- Tests del panel docente, sus permisos y los comandos de carga.
- Documentación del proyecto: `README.md` y los documentos de esta carpeta.

**Evidencia:** commits `51d1442`, `78e9832`, `8310a9f`, `f0ca91d` (2026-09-01 a 2026-09-09)
y `71a3563` (2026-10-06).

**Archivos donde puede rendir defensa técnica:**
`courses/views.py` (`CourseListView` y la lógica de filtros), `courses/models.py`
(`parse_hours`, `Course.duration_hours`), `courses/management/commands/seed_courses.py`,
`teachers/` (aplicación completa), `templates/courses/course_list.html`,
`templates/partials/header_landing.html`, `django_project/settings.py` (base de datos),
`teachers/panel_views.py`, `teachers/tests.py`.

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
| Panel docente: formularios, plantillas y redirección por rol | Emilio Asencio |
| Panel docente: vistas, permisos y cuentas de docentes | Matias Garcia |
| Migración a PostgreSQL | Matias Garcia |
