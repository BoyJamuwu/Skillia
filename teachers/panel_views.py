"""Panel del Profesor: el docente gestiona sus cursos, módulos y lecciones.

Un usuario tiene el rol de Profesor cuando su cuenta está vinculada a un Teacher
(Teacher.user). Todas las vistas filtran por ese docente, así que un profesor
nunca puede ver ni tocar los cursos de otro: le responde 404.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Max
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from courses.models import Course, Lesson, Module
from .forms import CourseForm, LessonForm, ModuleForm


def get_teacher(user):
    """El Teacher vinculado a la cuenta, o None si el usuario no es profesor."""
    if not user.is_authenticated:
        return None
    return getattr(user, "teacher_profile", None)


class TeacherRequiredMixin(LoginRequiredMixin):
    """Deja pasar solo a usuarios con rol de Profesor y deja el docente en self.teacher."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.teacher = get_teacher(request.user)
        if self.teacher is None:
            raise PermissionDenied("Esta sección es solo para profesores.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teacher"] = self.teacher
        return context


class PanelFormMixin:
    """Contexto común del template genérico de formularios del panel."""

    template_name = "teachers/panel/form.html"
    page_title = ""
    success_message = ""

    def get_back_url(self):
        raise NotImplementedError

    def get_success_url(self):
        return self.get_back_url()

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["back_url"] = self.get_back_url()
        return context


def next_order(queryset):
    """Siguiente posición libre, para que lo nuevo quede al final por defecto."""
    return (queryset.aggregate(top=Max("order"))["top"] or 0) + 1


# ---------- Dashboard ----------

class PanelView(TeacherRequiredMixin, ListView):
    template_name = "teachers/panel/dashboard.html"
    context_object_name = "courses"

    def get_queryset(self):
        return self.teacher.courses.annotate(
            modules_count=Count("modules", distinct=True),
            lessons_count=Count("modules__lessons", distinct=True),
            students_count=Count("enrollment", distinct=True),
        ).order_by("-created_at", "-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = context["courses"]
        context["totals"] = {
            "courses": len(courses),
            "modules": sum(c.modules_count for c in courses),
            "lessons": sum(c.lessons_count for c in courses),
            "students": sum(c.students_count for c in courses),
        }
        return context


# ---------- Cursos ----------

class TeacherCourseMixin(TeacherRequiredMixin):
    """Restringe el queryset a los cursos del profesor logueado."""

    model = Course

    def get_queryset(self):
        return Course.objects.filter(teacher=self.teacher)


class CourseManageView(TeacherCourseMixin, DetailView):
    template_name = "teachers/panel/course_manage.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["modules"] = self.object.modules.prefetch_related("lessons")
        context["students_count"] = self.object.enrollment_set.count()
        return context


class CourseCreateView(TeacherRequiredMixin, PanelFormMixin, CreateView):
    form_class = CourseForm
    page_title = "Nuevo curso"
    success_message = "Curso creado. Ahora agrégale módulos y lecciones."

    def form_valid(self, form):
        form.instance.teacher = self.teacher
        return super().form_valid(form)

    def get_back_url(self):
        return reverse("teacher_panel")

    def get_success_url(self):
        return reverse("panel_course_manage", args=[self.object.pk])


class CourseUpdateView(TeacherCourseMixin, PanelFormMixin, UpdateView):
    form_class = CourseForm
    success_message = "Curso actualizado."

    @property
    def page_title(self):
        return f"Editar curso: {self.object.title}"

    def get_back_url(self):
        return reverse("panel_course_manage", args=[self.object.pk])


# ---------- Módulos ----------

class ModuleCreateView(TeacherRequiredMixin, PanelFormMixin, CreateView):
    form_class = ModuleForm
    success_message = "Módulo agregado."

    def get_course(self):
        if not hasattr(self, "course"):
            self.course = get_object_or_404(Course, pk=self.kwargs["pk"], teacher=self.teacher)
        return self.course

    @property
    def page_title(self):
        return f"Nuevo módulo en {self.get_course().title}"

    def get_initial(self):
        return {"order": next_order(self.get_course().modules.all())}

    def form_valid(self, form):
        form.instance.course = self.get_course()
        return super().form_valid(form)

    def get_back_url(self):
        return reverse("panel_course_manage", args=[self.get_course().pk])


class TeacherModuleMixin(TeacherRequiredMixin):
    model = Module

    def get_queryset(self):
        return Module.objects.filter(course__teacher=self.teacher).select_related("course")

    def get_back_url(self):
        return reverse("panel_course_manage", args=[self.object.course_id])


class ModuleUpdateView(TeacherModuleMixin, PanelFormMixin, UpdateView):
    form_class = ModuleForm
    success_message = "Módulo actualizado."

    @property
    def page_title(self):
        return f"Editar módulo: {self.object.title}"


class ModuleDeleteView(TeacherModuleMixin, PanelFormMixin, DeleteView):
    template_name = "teachers/panel/confirm_delete.html"
    success_message = "Módulo eliminado."

    @property
    def page_title(self):
        return f"Eliminar módulo: {self.object.title}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lessons = self.object.lessons.count()
        context["warning"] = (
            f"Se borrarán también sus {lessons} lecciones y el progreso que los "
            "estudiantes tengan registrado en ellas."
        )
        return context


# ---------- Lecciones ----------

class LessonCreateView(TeacherRequiredMixin, PanelFormMixin, CreateView):
    form_class = LessonForm
    success_message = "Lección agregada."

    def get_module(self):
        if not hasattr(self, "module"):
            self.module = get_object_or_404(
                Module.objects.select_related("course"),
                pk=self.kwargs["pk"],
                course__teacher=self.teacher,
            )
        return self.module

    @property
    def page_title(self):
        return f"Nueva lección en {self.get_module().title}"

    def get_initial(self):
        return {"order": next_order(self.get_module().lessons.all())}

    def form_valid(self, form):
        form.instance.module = self.get_module()
        return super().form_valid(form)

    def get_back_url(self):
        return reverse("panel_course_manage", args=[self.get_module().course_id])


class TeacherLessonMixin(TeacherRequiredMixin):
    model = Lesson

    def get_queryset(self):
        return Lesson.objects.filter(module__course__teacher=self.teacher).select_related(
            "module"
        )

    def get_back_url(self):
        return reverse("panel_course_manage", args=[self.object.module.course_id])


class LessonUpdateView(TeacherLessonMixin, PanelFormMixin, UpdateView):
    form_class = LessonForm
    success_message = "Lección actualizada."

    @property
    def page_title(self):
        return f"Editar lección: {self.object.title}"


class LessonDeleteView(TeacherLessonMixin, PanelFormMixin, DeleteView):
    template_name = "teachers/panel/confirm_delete.html"
    success_message = "Lección eliminada."

    @property
    def page_title(self):
        return f"Eliminar lección: {self.object.title}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["warning"] = "Se borrará también el progreso que los estudiantes tengan en esta lección."
        return context
