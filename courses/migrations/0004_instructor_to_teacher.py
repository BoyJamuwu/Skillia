"""Convierte el texto libre de Course.instructor en filas reales de Teacher."""

from django.db import migrations


def instructor_to_teacher(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    Teacher = apps.get_model('teachers', 'Teacher')

    for course in Course.objects.all():
        name = (course.instructor or '').strip()
        if not name:
            continue
        teacher, _ = Teacher.objects.get_or_create(full_name=name)
        course.teacher = teacher
        course.save(update_fields=['teacher'])


def teacher_to_instructor(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')

    for course in Course.objects.exclude(teacher=None).select_related('teacher'):
        course.instructor = course.teacher.full_name
        course.save(update_fields=['instructor'])


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_teacher'),
    ]

    operations = [
        migrations.RunPython(instructor_to_teacher, teacher_to_instructor),
    ]
