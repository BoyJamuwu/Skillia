from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from courses.models import Course, Lesson, Module
from .models import Teacher


class TeacherPanelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("profe@skillia.com", password="pass12345")
        self.teacher = Teacher.objects.create(full_name="Profe Uno", user=self.user)
        self.course = Course.objects.create(
            title="Curso propio", description="d", category="Programacion", teacher=self.teacher
        )
        self.module = Module.objects.create(course=self.course, title="Intro", order=1)
        self.lesson = Lesson.objects.create(module=self.module, title="Hola", order=1)

        self.other = Teacher.objects.create(full_name="Profe Dos")
        self.other_course = Course.objects.create(
            title="Curso ajeno", description="d", category="Datos", teacher=self.other
        )
        self.other_module = Module.objects.create(course=self.other_course, title="Ajeno")

    def login(self):
        self.client.login(username="profe@skillia.com", password="pass12345")

    def test_anonymous_is_sent_to_login(self):
        response = self.client.get(reverse("teacher_panel"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('teacher_panel')}")

    def test_student_gets_403(self):
        User.objects.create_user("alumno@skillia.com", password="pass12345")
        self.client.login(username="alumno@skillia.com", password="pass12345")
        self.assertEqual(self.client.get(reverse("teacher_panel")).status_code, 403)

    def test_panel_lists_only_own_courses(self):
        self.login()
        response = self.client.get(reverse("teacher_panel"))
        self.assertContains(response, "Curso propio")
        self.assertNotContains(response, "Curso ajeno")
        self.assertEqual(response.context["totals"]["lessons"], 1)

    def test_cannot_touch_other_teachers_content(self):
        self.login()
        urls = [
            reverse("panel_course_manage", args=[self.other_course.pk]),
            reverse("panel_course_edit", args=[self.other_course.pk]),
            reverse("panel_module_create", args=[self.other_course.pk]),
            reverse("panel_module_edit", args=[self.other_module.pk]),
            reverse("panel_lesson_create", args=[self.other_module.pk]),
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 404)
        response = self.client.post(reverse("panel_module_delete", args=[self.other_module.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Module.objects.filter(pk=self.other_module.pk).exists())

    def test_create_course_assigns_teacher(self):
        self.login()
        response = self.client.post(reverse("panel_course_create"), {
            "title": "Nuevo", "description": "desc", "category": "Programacion",
            "duration": "10 horas", "price": "50000", "image_url": "",
        })
        course = Course.objects.get(title="Nuevo")
        self.assertEqual(course.teacher, self.teacher)
        self.assertRedirects(response, reverse("panel_course_manage", args=[course.pk]))

    def test_add_module_and_lesson(self):
        self.login()
        response = self.client.get(reverse("panel_module_create", args=[self.course.pk]))
        self.assertEqual(response.context["form"].initial["order"], 2)

        self.client.post(reverse("panel_module_create", args=[self.course.pk]),
                         {"title": "Avanzado", "order": 2})
        module = self.course.modules.get(title="Avanzado")

        self.client.post(reverse("panel_lesson_create", args=[module.pk]),
                         {"title": "Clase 1", "duration": "10:00", "video_url": "", "order": 1})
        self.assertTrue(module.lessons.filter(title="Clase 1").exists())

    def test_edit_and_delete_lesson(self):
        self.login()
        self.client.post(reverse("panel_lesson_edit", args=[self.lesson.pk]),
                         {"title": "Renombrada", "duration": "", "video_url": "", "order": 1})
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Renombrada")

        response = self.client.post(reverse("panel_lesson_delete", args=[self.lesson.pk]))
        self.assertRedirects(response, reverse("panel_course_manage", args=[self.course.pk]))
        self.assertFalse(Lesson.objects.filter(pk=self.lesson.pk).exists())

    def test_header_swaps_dashboard_for_panel(self):
        self.login()
        response = self.client.get(reverse("home"))
        self.assertContains(response, reverse("teacher_panel"))
        self.assertNotContains(response, f'href="{reverse("dashboard")}"')

        User.objects.create_user("alumno@skillia.com", password="pass12345")
        self.client.login(username="alumno@skillia.com", password="pass12345")
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, reverse("teacher_panel"))
        self.assertContains(response, f'href="{reverse("dashboard")}"')

    def test_dashboard_redirects_teachers_to_panel(self):
        self.login()
        self.assertRedirects(self.client.get(reverse("dashboard")), reverse("teacher_panel"))
