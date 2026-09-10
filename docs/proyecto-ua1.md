# Skillia — Definición de proyecto (Unidad de Aprendizaje 1)

**Asignatura:** Programación Back End (TI2041) — Primavera 2026
**Evaluación:** Sumativa 1 — Primera etapa de proyecto web con Django
**Modalidad:** Equipo de dos integrantes
**Stack:** Django 5.2.17 · Python 3.13 · SQLite · Tailwind CSS

---

## 1. Problemática

Existe una cantidad enorme de formación técnica en línea, pero encontrar un curso que
realmente sirva sigue siendo difícil. Quien quiere aprender una habilidad nueva se enfrenta a
tres problemas concretos:

1. **Catálogos inabarcables y sin criterio.** Miles de cursos de calidad desigual, sin una
   revisión previa que permita distinguir cuáles valen el tiempo invertido.
2. **Búsqueda pobre.** Los listados obligan a recorrer todo el catálogo porque no permiten
   acotar por lo que a la persona le importa: la tecnología, cuánto tiempo tiene disponible,
   cuánto puede pagar o quién dicta el curso.
3. **Pérdida del hilo.** Al retomar un curso después de unos días, no queda claro en qué
   lección se quedó, cuánto avanzó ni cuánto le falta, lo que aumenta el abandono.

A esto se suma que la mayoría de los estudiantes compatibiliza el estudio con trabajo o
carrera, por lo que necesita avanzar a su propio ritmo y en sesiones cortas.

## 2. Objetivo general

Desarrollar una plataforma web de cursos en línea que permita a un estudiante **encontrar**
un curso pertinente mediante búsqueda y filtros, **evaluarlo** a partir de su temario,
duración, valoración y docente, **inscribirse** y **avanzar** lección por lección con
seguimiento visible de su progreso.

### Objetivos específicos

1. Publicar un catálogo navegable de cursos con búsqueda y filtros combinables.
2. Entregar, para cada curso, una ficha con temario, duración, valoración y docente.
3. Permitir el registro e inicio de sesión de estudiantes.
4. Permitir la inscripción a un curso y el acceso a su reproductor de lecciones.
5. Registrar el avance por lección y mostrarlo de forma agregada en un panel personal.
6. Exponer el cuerpo docente con fichas públicas que den respaldo a cada programa.

## 3. Usuarios y roles

| Rol | Descripción | Interacciones principales | Estado en UA1 |
| --- | --- | --- | --- |
| **Visitante** | Persona no autenticada que explora la oferta. | Ver inicio, recorrer el catálogo, filtrar y buscar cursos, abrir el detalle de un curso, revisar el cuerpo docente, registrarse. | Implementado |
| **Estudiante** | Usuario autenticado, foco principal de esta etapa. | Todo lo del visitante, más: inscribirse en un curso, ver el reproductor, marcar lecciones completadas, consultar su progreso en el dashboard. | Implementado |
| **Administrador** | Encargado de mantener el catálogo. | Alta y edición de cursos, módulos, lecciones y docentes. | Parcial: se opera vía Django Admin y comandos de carga; no existe un panel propio. |
| **Docente** | Profesional que dicta los cursos. | En esta etapa **solo tiene presencia pública**: aparece con ficha, especialidad y cursos asociados. No inicia sesión ni administra contenido. | Fuera de alcance como rol operativo (ver 4.2) |

> El sistema no distingue permisos por rol más allá de la separación
> autenticado / no autenticado y del acceso de staff al admin de Django. La gestión
> diferenciada por rol se proyecta para la UA2.

## 4. Alcance de la primera etapa

### 4.1 Incluido en esta entrega

**Configuración y arquitectura**

- Proyecto Django 5.2.17 en entorno reproducible (`requirements.txt` + `.env.example`).
- Cuatro aplicaciones propias: `pages`, `accounts`, `courses` y `teachers`.
- Flujo MVT completo: `urls.py` por aplicación incluidos desde el `urls.py` del proyecto,
  vistas basadas en clases y plantillas que heredan de `base.html`.
- Secretos fuera del código versionado, leídos desde variables de entorno.

**Interfaces (13 rutas navegables)**

- Página de inicio.
- Catálogo con búsqueda por texto y filtros combinables por categoría, docente, duración,
  precio y valoración, además de seis criterios de ordenamiento.
- Detalle de curso con temario por módulos y lecciones.
- Reproductor de lecciones con avance y marcado de lección completada.
- Registro, inicio y cierre de sesión.
- Dashboard del estudiante con porcentaje de avance por curso.
- Listado y ficha pública de docentes.
- Página 404 personalizada.

**Datos**

- Catálogo definido en `courses/seed_data/catalog.json`: 6 cursos, 30 módulos y 100 lecciones.
- Comandos de carga idempotentes (`seed_courses`, `seed_teachers`) que leen el archivo,
  lo recorren con estructuras de Python y lo llevan al sistema.
- Las vistas preparan la información y la entregan a las plantillas mediante el contexto;
  las plantillas solo presentan.

### 4.2 Explícitamente fuera de esta entrega

- **Panel de docente.** El docente no inicia sesión ni publica contenido; su presencia es
  únicamente informativa. Se proyecta para la UA2.
- **CRUD de cursos desde la interfaz.** El mantenimiento se hace por Django Admin o por los
  comandos de carga, no con formularios propios.
- **Pasarela de pago.** Los precios se muestran, pero la inscripción no cobra: todos los
  cursos quedan liberados en esta etapa.
- **Certificados.** Se describen en la propuesta institucional, pero no se emiten.
- **Reproducción real de video.** El reproductor muestra la estructura y el avance; las
  lecciones apuntan a URLs de ejemplo.
- **API REST.** No hay endpoints JSON públicos; la única respuesta JSON es la interna del
  marcado de lección completada.
- **Valoraciones y comentarios de estudiantes.** Las valoraciones son un dato del catálogo,
  no son ingresadas por usuarios.
- **Recuperación de contraseña y verificación de correo.**

### 4.3 Nota sobre el uso de base de datos

La UA1 no exige persistencia y admite datos simulados en memoria. En este proyecto, el
catálogo **sí se define como dato simulado**: vive en `courses/seed_data/catalog.json` y se
recorre con estructuras de Python (listas y diccionarios) dentro de los comandos de carga.

La decisión de apoyar ese catálogo en el ORM desde esta etapa fue deliberada y responde al
alcance del propio proyecto: el seguimiento de progreso por estudiante y lección requiere
conservar estado entre sesiones. La estructura de datos ya está pensada para la UA2 y no
reemplaza ninguno de los aprendizajes de esta unidad — el flujo URL → View → Template, el uso
del contexto y la organización de las plantillas se mantienen como eje del trabajo.

## 5. Proyección del proyecto

| Unidad | Qué se incorpora | Sobre qué base del trabajo actual |
| --- | --- | --- |
| **UA1** (esta entrega) | Problema, objetivo y alcance. Django 5.2.17. URLs, Views, Templates e interfaces. Navegación y datos simulados. | — |
| **UA2** | Formularios propios para el CRUD de cursos, módulos y lecciones. Panel de docente con autenticación por rol. Django Admin personalizado. Sesiones y endurecimiento de seguridad. Recuperación de contraseña. | Los modelos `Course`, `Module`, `Lesson`, `Teacher`, `Enrollment` y `Progress` ya están definidos y relacionados. Las interfaces de estudiante ya existen y sirven de referencia visual para el panel de docente. |
| **UA3** | API REST con Django REST Framework: serializers para catálogo, inscripciones y progreso; endpoints CRUD con salida JSON; autenticación por token/JWT para consumo desde un cliente externo. | La lógica de consulta del catálogo y de cálculo de progreso ya está aislada en las vistas y en el modelo (`Lesson.for_course`, `Course.duration_hours`), lista para reutilizarse desde serializers. |

## 6. Modelo de datos

| Modelo | Aplicación | Campos principales | Relaciones |
| --- | --- | --- | --- |
| `Teacher` | `teachers` | `full_name`, `headline`, `specialty`, `bio`, `photo_url`, `rating`, `years_experience`, `email`, `linkedin_url` | Un docente dicta muchos cursos. |
| `Course` | `courses` | `title`, `description`, `image_url`, `price`, `rating`, `category`, `duration`, `created_at` | FK a `Teacher`. Contiene módulos. |
| `Module` | `courses` | `title`, `order` | FK a `Course`. Contiene lecciones. |
| `Lesson` | `courses` | `title`, `duration`, `video_url`, `order` | FK a `Module`. |
| `Enrollment` | `courses` | — | Une usuario y curso. Único por par. |
| `Progress` | `courses` | `completed` | Une usuario y lección. Único por par. |

## 7. Evidencias de la entrega

| Evidencia solicitada | Dónde está |
| --- | --- |
| Código fuente completo del proyecto Django 5.2.17 | Repositorio completo; versión fijada en `requirements.txt`. |
| Proyecto ejecutable y al menos una aplicación propia | Cuatro aplicaciones propias; instalación y ejecución en `README.md`. |
| Rutas, Views y Templates para la navegación principal | `django_project/urls.py` y los `urls.py`, `views.py` y `templates/` de cada aplicación. Mapa completo en `README.md`. |
| Interfaces del alcance declarado y de los roles previstos | 13 rutas navegables, detalladas en la sección 4.1. |
| Datos simulados mediante estructuras de Python | `courses/seed_data/catalog.json` y los comandos en `courses/management/commands/` y `teachers/management/commands/`. |
| Documento con problemática, objetivo, usuarios/roles, alcance y proyección | Este documento. |
| Registro de contribución individual | [`contribucion-individual.md`](contribucion-individual.md) |
| Anexo de uso de IA | [`anexo-ia.md`](anexo-ia.md) |
| Exposición, demostración funcional y defensa técnica | A realizar en la fecha que indique el docente. |
