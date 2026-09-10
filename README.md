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

## Puesta en marcha

```bash
# 5. Crear la base de datos local
python manage.py migrate

# 6. Cargar los datos de ejemplo
python manage.py seed_teachers
python manage.py seed_courses

# 7. Crear un usuario administrador (opcional, para /admin/)
python manage.py createsuperuser

# 8. Levantar el servidor
python manage.py runserver
```

La aplicación queda disponible en <http://127.0.0.1:8000/>.

La base de datos (`db.sqlite3`) no se versiona: se regenera con `migrate` + los comandos de
carga, que son idempotentes y pueden volver a ejecutarse sin duplicar registros.

## Comandos útiles

| Comando | Qué hace |
| --- | --- |
| `python manage.py runserver` | Levanta el servidor de desarrollo. |
| `python manage.py check` | Valida la configuración del proyecto. |
| `python manage.py migrate` | Aplica las migraciones. |
| `python manage.py seed_teachers` | Carga los docentes de ejemplo. |
| `python manage.py seed_teachers --assign-courses` | Además asocia los cursos existentes a sus docentes. |
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
├── teachers/              # Listado y ficha pública de docentes
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
| `/accounts/signup/` | `signup` | `SignUpView` | Público |
| `/accounts/login/` | `login` | `LoginView` | Público |
| `/accounts/logout/` | `logout` | `LogoutView` | Autenticado (POST) |
| `/dashboard/` | `dashboard` | `DashboardView` | Autenticado |
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
