"""Carga el catálogo de cursos desde courses/seed_data/catalog.json.

Los cursos se actualizan por id, así que las inscripciones existentes sobreviven.
Los módulos y lecciones se regeneran completos: es la única forma de que el
catálogo del archivo sea la única fuente de verdad y no queden restos de una
carga anterior. Eso borra las filas de Progress asociadas (cascada), porque
apuntan a lecciones que dejan de existir.

    python manage.py seed_courses
    python manage.py seed_courses --prune     # además borra cursos que no estén en el archivo
"""

import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import no_style
from django.db import connection, transaction
from django.utils.dateparse import parse_datetime

from courses.models import Course, Lesson, Module, Progress
from teachers.models import Teacher

CATALOG_PATH = Path(__file__).resolve().parents[2] / "seed_data" / "catalog.json"


class Command(BaseCommand):
    help = "Crea o actualiza los cursos, módulos y lecciones del catálogo."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            default=str(CATALOG_PATH),
            help="Ruta al JSON del catálogo.",
        )
        parser.add_argument(
            "--prune",
            action="store_true",
            help="Elimina los cursos que no aparezcan en el archivo (arrastra sus inscripciones).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        path = Path(options["path"])
        if not path.exists():
            raise CommandError(f"No se encontró el catálogo en {path}")

        catalog = json.loads(path.read_text(encoding="utf-8"))

        self.load_courses(catalog["courses"])
        self.load_modules_and_lessons(catalog["modules"], catalog["lessons"])

        if options["prune"]:
            self.prune_courses({c["id"] for c in catalog["courses"]})

        self.reset_sequences()
        self.report(catalog)

    def reset_sequences(self):
        """Pone al día el contador de ids después de insertar filas con id fijo.

        PostgreSQL no lo mueve solo: sin esto, el próximo curso, módulo o lección
        creado desde el panel recibiría un id que ya existe. En SQLite no hace nada.
        """
        statements = connection.ops.sequence_reset_sql(no_style(), [Course, Module, Lesson])
        with connection.cursor() as cursor:
            for sql in statements:
                cursor.execute(sql)

    def load_courses(self, rows):
        created = updated = 0
        for row in rows:
            row = dict(row)
            course_id = row.pop("id")
            instructor = (row.pop("instructor", "") or "").strip()

            teacher = None
            if instructor:
                teacher, _ = Teacher.objects.get_or_create(full_name=instructor)

            created_at = parse_datetime(row.pop("created_at"))
            _, was_created = Course.objects.update_or_create(
                id=course_id,
                defaults={**row, "teacher": teacher, "created_at": created_at},
            )
            created += was_created
            updated += not was_created

        self.stdout.write(
            self.style.SUCCESS(f"Cursos: {created} creados, {updated} actualizados.")
        )

    def load_modules_and_lessons(self, module_rows, lesson_rows):
        # Se regeneran de cero para que el archivo mande. Progress cae por cascada.
        dropped_progress = Progress.objects.count()
        Module.objects.all().delete()

        Module.objects.bulk_create(
            Module(id=r["id"], course_id=r["course_id"], title=r["title"], order=r["order"])
            for r in module_rows
        )
        Lesson.objects.bulk_create(
            Lesson(
                id=r["id"],
                module_id=r["module_id"],
                title=r["title"],
                video_url=r["video_url"],
                duration=r["duration"],
                order=r["order"],
            )
            for r in lesson_rows
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Módulos: {len(module_rows)} · Lecciones: {len(lesson_rows)} (regenerados)."
            )
        )
        if dropped_progress:
            self.stdout.write(
                self.style.WARNING(
                    f"Se borraron {dropped_progress} registro(s) de progreso que apuntaban "
                    "a lecciones anteriores."
                )
            )

    def prune_courses(self, keep_ids):
        extra = Course.objects.exclude(id__in=keep_ids)
        titles = list(extra.values_list("title", flat=True))
        if not titles:
            self.stdout.write("No hay cursos sobrantes para eliminar.")
            return
        extra.delete()
        self.stdout.write(self.style.WARNING(f"Cursos eliminados: {', '.join(titles)}"))

    def report(self, catalog):
        """Avisa qué módulos quedaron sin lecciones, para no descubrirlo en el reproductor."""
        with_lessons = {r["module_id"] for r in catalog["lessons"]}
        empty = [r for r in catalog["modules"] if r["id"] not in with_lessons]
        if not empty:
            return

        titles = {c["id"]: c["title"] for c in catalog["courses"]}
        self.stdout.write(
            self.style.WARNING(f"\n{len(empty)} módulo(s) quedaron sin lecciones:")
        )
        for row in empty:
            self.stdout.write(f"  - {titles[row['course_id']]}: {row['title']}")
