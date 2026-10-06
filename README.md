# Skillia

Plataforma web de cursos en línea desarrollada con Django 5.2.17 como proyecto de la
asignatura **Programación Back End (TI2041)**.

El catálogo permite explorar cursos con filtros, revisar el detalle de cada programa,
inscribirse y avanzar lección por lección desde un reproductor con seguimiento de progreso.

La definición del proyecto (problemática, objetivo, usuarios, alcance y proyección) está en
[`docs/proyecto-ua1.md`](docs/proyecto-ua1.md).

---

## Requisitos

- Python 3.10 – 3.14 (el proyecto se desarrolló con 3.13)
- pip
- Git
- PostgreSQL 14 o superior (ver [Base de datos](#base-de-datos-postgresql)). Para probar
  sin instalarlo se puede usar SQLite con `DB_ENGINE=sqlite`.

## Instalación

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd backend-Skillia

# 2. Crear y activar el entorno virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar las variables de entorno
copy .env.example .env        # Windows
cp .env.example .env          # macOS / Linux
```

Luego edita `.env` y genera una `DJANGO_SECRET_KEY` propia:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

El archivo `.env` no se versiona: el repositorio no contiene secretos. Si falta la variable,
Django se detiene con un mensaje que indica exactamente qué completar.

| Variable | Descripción | Valor por defecto |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Clave criptográfica de Django. Obligatoria. | — |
| `DJANGO_DEBUG` | Modo depuración. `False` en producción. | `False` |
| `DJANGO_ALLOWED_HOSTS` | Hosts autorizados, separados por coma. | `127.0.0.1,localhost` |
| `DB_ENGINE` | `postgres` o `sqlite`. | `postgres` |
| `DB_NAME` | Nombre de la base. Obligatoria con Postgres. | — |
| `DB_USER` | Usuario de la base. Obligatoria con Postgres. | — |
| `DB_PASSWORD` | Contraseña del usuario. Obligatoria con Postgres. | — |
| `DB_HOST` | Servidor de la base. | `localhost` |
| `DB_PORT` | Puerto de la base. | `5432` |
| `PG_BIN_DIR` | Solo Windows: carpeta `bin` de PostgreSQL. Se detecta sola si está en Program Files. | — |
| `DB_CONN_MAX_AGE` | Segundos que se reutiliza una conexión (`0` = una por request). | `60` |

## Base de datos (PostgreSQL)

El proyecto usa PostgreSQL. Los modelos y las migraciones no dependen del motor: todo pasa
por el ORM de Django, así que lo único que cambia entre bases es la conexión en `.env`.

**1. Instalar PostgreSQL.** En Windows, con el instalador de
<https://www.postgresql.org/download/windows/> (incluye pgAdmin). Anota la contraseña que
le pongas al usuario `postgres` durante la instalación.

**2. Crear el usuario y la base del proyecto.** Desde *SQL Shell (psql)* o la herramienta
de consultas de pgAdmin, conectado como `postgres`:

```sql
CREATE USER skillia WITH PASSWORD 'una-clave-segura';
CREATE DATABASE skillia OWNER skillia;
ALTER USER skillia CREATEDB;  -- necesario para que `manage.py test` cree su base de pruebas
```

**3. Completar `.env`** con esos datos (`DB_ENGINE=postgres`, `DB_NAME=skillia`,
`DB_USER=skillia`, `DB_PASSWORD=una-clave-segura`) y seguir con la
[Puesta en marcha](#puesta-en-marcha).

Para comprobar la conexión: `python manage.py dbshell` abre la consola de la base.

### Pasar los datos de SQLite a PostgreSQL

Todo el catálogo sale de los comandos `seed_*`, así que basta con correrlos sobre la base
nueva. Si además quieres conservar las cuentas e inscripciones creadas a mano:

```bash
# Con DB_ENGINE=sqlite en .env
python manage.py dumpdata --natural-foreign --exclude contenttypes --exclude auth.permission --exclude admin.logentry --exclude sessions -o datos.json

# Cambiar a DB_ENGINE=postgres y crear las tablas vacías
python manage.py migrate
python manage.py loaddata datos.json
```

### Problemas frecuentes

| Error | Causa y solución |
| --- | --- |
| `Error loading psycopg2 or psycopg module` | Falta el driver: `pip install -r requirements.txt`. En Windows, si además aparece *"Una directiva de Control de aplicaciones bloqueó este archivo"*, es Smart App Control bloqueando la librería del driver. `settings.py` ya lo resuelve usando la `libpq` que trae PostgreSQL desde `C:\Program Files\PostgreSQL\<versión>\bin`; si lo instalaste en otra carpeta, indícala en `PG_BIN_DIR` dentro de `.env`. |
| `password authentication failed for user "skillia"` | La clave de `DB_PASSWORD` no coincide con la del `CREATE USER`. |
| `database "skillia" does not exist` | Falta el `CREATE DATABASE` del paso 2. |
| `connection refused` / `could not connect to server` | El servicio de PostgreSQL no está corriendo, o `DB_HOST`/`DB_PORT` no coinciden. |
| `permission denied to create database` al correr tests | Falta el `ALTER USER skillia CREATEDB`. |

## Puesta en marcha

```bash
# 5. Crear la base de datos local
python manage.py migrate

# 6. Cargar los datos de ejemplo
python manage.py seed_teachers --create-users
python manage.py seed_courses

# 7. Crear un usuario administrador (opcional, para /admin/)
python manage.py createsuperuser

# 8. Levantar el servidor
python manage.py runserver
```

La aplicación queda disponible en <http://127.0.0.1:8000/>.

La base de datos no se versiona: se regenera con `migrate` + los comandos de
carga, que son idempotentes y pueden volver a ejecutarse sin duplicar registros.

## Roles

| Rol | Cómo se obtiene | Qué puede hacer |
| --- | --- | --- |
| Estudiante | Registrándose en `/accounts/signup/` | Inscribirse en cursos, verlos en el reproductor y seguir su progreso en `/dashboard/`. |
| Docente | Su cuenta está vinculada a un docente (`Teacher.user`) | Usa el **Panel Docente** en `/teachers/panel/` en lugar del Dashboard: crea y edita sus cursos, y agrega, edita y elimina módulos y lecciones. Solo ve y modifica los cursos que dicta. |
| Administrador | `createsuperuser` | Todo, desde `/admin/`. |

Para convertir a un usuario en Profesor, en `/admin/` se abre el docente y se le asigna la
cuenta en el campo **User**. Con los datos de ejemplo, `seed_teachers --create-users` crea
una cuenta por docente: el usuario es su email (por ejemplo `fernando.reveco@skillia.com`) y
la contraseña es `profesor123`, o la que se pase con `--password`.

## Comandos útiles

| Comando | Qué hace |
| --- | --- |
| `python manage.py runserver` | Levanta el servidor de desarrollo. |
| `python manage.py check` | Valida la configuración del proyecto. |
| `python manage.py migrate` | Aplica las migraciones. |
| `python manage.py seed_teachers` | Carga los docentes de ejemplo. |
| `python manage.py seed_teachers --assign-courses` | Además asocia los cursos existentes a sus docentes. |
| `python manage.py seed_teachers --create-users` | Además crea una cuenta de Profesor por docente (contraseña `profesor123`, cambiable con `--password`). |
| `python manage.py test` | Corre los tests (incluye los permisos del Panel Docente). |
| `python manage.py seed_courses` | Carga cursos, módulos y lecciones desde `courses/seed_data/catalog.json`. |
| `python manage.py seed_courses --prune` | Además elimina los cursos que ya no estén en el archivo. |

## Estructura del proyecto

```
backend-Skillia/
├── django_project/        # Configuración del proyecto (settings, urls, wsgi)
├── pages/                 # Página de inicio
├── accounts/              # Registro, inicio de sesión y dashboard del estudiante
├── courses/               # Catálogo, detalle, inscripción, reproductor y progreso
│   ├── management/commands/   # Comandos de carga de datos
│   └── seed_data/             # catalog.json: 6 cursos, 30 módulos, 100 lecciones
├── teachers/              # Listado y ficha pública de docentes + Panel Docente (panel_views.py)
├── templates/             # Plantillas HTML (base + una carpeta por app)
│   └── partials/          # Header y footer reutilizables
├── static/icons/          # Íconos SVG
├── .env.example           # Plantilla de configuración
└── requirements.txt       # Dependencias
```

## Mapa de rutas

| Ruta | Nombre | Vista | Acceso |
| --- | --- | --- | --- |
| `/` | `home` | `HomePageView` | Público |
| `/courses/` | `course_list` | `CourseListView` | Público |
| `/courses/<pk>/` | `course_detail` | `CourseDetailView` | Público |
| `/courses/<pk>/enroll/` | `course_enroll` | `EnrollView` | Autenticado (POST) |
| `/courses/<pk>/player/` | `course_player` | `CoursePlayerView` | Inscrito |
| `/courses/<pk>/player/<lesson_id>/` | `course_player_lesson` | `CoursePlayerView` | Inscrito |
| `/courses/<pk>/lessons/<lesson_id>/complete/` | `lesson_complete` | `CompleteLessonView` | Inscrito (POST, JSON) |
| `/teachers/` | `teacher_list` | `TeacherListView` | Público |
| `/teachers/<pk>/` | `teacher_detail` | `TeacherDetailView` | Público |
| `/teachers/panel/` | `teacher_panel` | `PanelView` | Profesor |
| `/teachers/panel/courses/new/` | `panel_course_create` | `CourseCreateView` | Profesor |
| `/teachers/panel/courses/<pk>/` | `panel_course_manage` | `CourseManageView` | Profesor (dueño) |
| `/teachers/panel/courses/<pk>/edit/` | `panel_course_edit` | `CourseUpdateView` | Profesor (dueño) |
| `/teachers/panel/courses/<pk>/modules/new/` | `panel_module_create` | `ModuleCreateView` | Profesor (dueño) |
| `/teachers/panel/modules/<pk>/edit/` | `panel_module_edit` | `ModuleUpdateView` | Profesor (dueño) |
| `/teachers/panel/modules/<pk>/delete/` | `panel_module_delete` | `ModuleDeleteView` | Profesor (dueño) |
| `/teachers/panel/modules/<pk>/lessons/new/` | `panel_lesson_create` | `LessonCreateView` | Profesor (dueño) |
| `/teachers/panel/lessons/<pk>/edit/` | `panel_lesson_edit` | `LessonUpdateView` | Profesor (dueño) |
| `/teachers/panel/lessons/<pk>/delete/` | `panel_lesson_delete` | `LessonDeleteView` | Profesor (dueño) |
| `/accounts/signup/` | `signup` | `SignUpView` | Público |
| `/accounts/login/` | `login` | `LoginView` | Público |
| `/accounts/logout/` | `logout` | `LogoutView` | Autenticado (POST) |
| `/dashboard/` | `dashboard` | `DashboardView` | Autenticado (los docentes se redirigen a su panel) |
| `/admin/` | — | Django Admin | Staff |

## Filtros del catálogo

`/courses/` acepta estos parámetros por query string, combinables entre sí:

| Parámetro | Valores | Efecto |
| --- | --- | --- |
| `q` | texto libre | Busca en título, descripción, categoría y nombre del docente. |
| `categoria` | múltiple | Filtra por categoría exacta. |
| `docente` | múltiple (id) | Filtra por docente. |
| `duracion` | `corta`, `media`, `larga` | Menos de 10 h / 10–15 h / más de 15 h. |
| `precio` | `baja`, `media`, `alta` | Hasta $60.000 / $60.000–$80.000 / más de $80.000. |
| `valoracion` | `4.5`, `4.7`, `4.9` | Valoración mínima. |
| `orden` | `destacados`, `recientes`, `valoracion`, `precio_asc`, `precio_desc`, `titulo` | Criterio de ordenamiento. |

Los valores inválidos se ignoran sin interrumpir la navegación.

## Documentación del proyecto

- [`docs/proyecto-ua1.md`](docs/proyecto-ua1.md) — problemática, objetivo, usuarios, alcance y proyección.
- [`docs/contribucion-individual.md`](docs/contribucion-individual.md) — aporte de cada integrante.
- [`docs/anexo-ia.md`](docs/anexo-ia.md) — anexo de uso de herramientas de inteligencia artificial.
