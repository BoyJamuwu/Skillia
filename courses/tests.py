from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from .models import Course, Lesson, Module


class SeedCoursesTests(TestCase):
    def test_new_rows_after_seeding_get_free_ids(self):
        # El seed inserta con id fijo; en PostgreSQL eso deja atrás el contador
        # de ids si no se reinicia, y el siguiente create choca con un id existente.
        call_command("seed_courses", stdout=StringIO())

        course = Course.objects.create(title="Nuevo", description="d", category="x")
        module = Module.objects.create(course=course, title="Nuevo")
        lesson = Lesson.objects.create(module=module, title="Nueva")

        self.assertEqual(Course.objects.filter(pk=course.pk).count(), 1)
        self.assertGreater(module.pk, 30)
        self.assertGreater(lesson.pk, 100)
