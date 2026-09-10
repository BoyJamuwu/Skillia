from decimal import Decimal, InvalidOperation

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, ListView
from django.http import JsonResponse
from django.urls import reverse
from teachers.models import Teacher
from .models import Course, Enrollment, Lesson, Progress, parse_hours

# Tramos del filtro lateral. El valor es lo que viaja en la query string y las
# tuplas son rangos cerrados por abajo y abiertos por arriba cuando el tope es None.
DURATION_BUCKETS = {
    "corta": ("Menos de 10 horas", 0, 9),
    "media": ("Entre 10 y 15 horas", 10, 15),
    "larga": ("Más de 15 horas", 16, None),
}

PRICE_BUCKETS = {
    "baja": ("Hasta $60,000", None, Decimal("60000")),
    "media": ("$60,000 - $80,000", Decimal("60000"), Decimal("80000")),
    "alta": ("Más de $80,000", Decimal("80000"), None),
}

RATING_CHOICES = [
    ("4.9", "4.9 o más"),
    ("4.7", "4.7 o más"),
    ("4.5", "4.5 o más"),
]

SORT_OPTIONS = {
    "destacados": ("Destacados", ["id"]),
    "recientes": ("Más recientes", ["-created_at", "-id"]),
    "valoracion": ("Mejor valorados", ["-rating", "id"]),
    "precio_asc": ("Precio: menor a mayor", ["price", "id"]),
    "precio_desc": ("Precio: mayor a menor", ["-price", "id"]),
    "titulo": ("Título A-Z", ["title"]),
}

DEFAULT_SORT = "destacados"


class CourseListView(ListView):
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"

    def get_queryset(self):
        params = self.request.GET
        queryset = Course.objects.select_related("teacher")

        search = params.get("q", "").strip()
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(category__icontains=search)
                | Q(teacher__full_name__icontains=search)
            )

        categories = [value for value in params.getlist("categoria") if value]
        if categories:
            queryset = queryset.filter(category__in=categories)

        teacher_ids = [value for value in params.getlist("docente") if value.isdigit()]
        if teacher_ids:
            queryset = queryset.filter(teacher_id__in=teacher_ids)

        duration = params.get("duracion")
        if duration in DURATION_BUCKETS:
            # La duración se guarda como texto libre ("12 horas"), así que el tramo
            # se resuelve en Python sobre los pares (id, duración) y luego se filtra por id.
            queryset = queryset.filter(id__in=self.ids_in_duration_bucket(duration))

        price = params.get("precio")
        if price in PRICE_BUCKETS:
            _, minimum, maximum = PRICE_BUCKETS[price]
            if minimum is not None:
                queryset = queryset.filter(price__gt=minimum)
            if maximum is not None:
                queryset = queryset.filter(price__lte=maximum)

        rating = params.get("valoracion")
        if rating:
            try:
                queryset = queryset.filter(rating__gte=Decimal(rating))
            except (InvalidOperation, TypeError):
                pass

        ordering = SORT_OPTIONS.get(params.get("orden"), SORT_OPTIONS[DEFAULT_SORT])[1]
        return queryset.order_by(*ordering)

    @staticmethod
    def ids_in_duration_bucket(bucket):
        _, minimum, maximum = DURATION_BUCKETS[bucket]
        matches = []
        for course_id, duration in Course.objects.values_list("id", "duration"):
            hours = parse_hours(duration)
            if hours is None or hours < minimum:
                continue
            if maximum is None or hours <= maximum:
                matches.append(course_id)
        return matches

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = self.request.GET

        # Las facetas se calculan sobre el catálogo completo: las opciones no
        # desaparecen al filtrar, solo cambia el resultado.
        context["categories"] = (
            Course.objects.values("category")
            .annotate(total=Count("id"))
            .order_by("category")
        )
        context["teachers"] = (
            Teacher.objects.annotate(total=Count("courses"))
            .filter(total__gt=0)
            .order_by("full_name")
        )
        context["duration_buckets"] = [
            (key, label) for key, (label, _, _) in DURATION_BUCKETS.items()
        ]
        context["price_buckets"] = [
            (key, label) for key, (label, _, _) in PRICE_BUCKETS.items()
        ]
        context["rating_choices"] = RATING_CHOICES
        context["sort_options"] = [
            (key, label) for key, (label, _) in SORT_OPTIONS.items()
        ]

        selected_teachers = [value for value in params.getlist("docente") if value.isdigit()]
        context["selected"] = {
            "q": params.get("q", "").strip(),
            "categories": params.getlist("categoria"),
            "teachers": [int(value) for value in selected_teachers],
            "duration": params.get("duracion", ""),
            "price": params.get("precio", ""),
            "rating": params.get("valoracion", ""),
            "sort": params.get("orden") if params.get("orden") in SORT_OPTIONS else DEFAULT_SORT,
        }
        context["active_filters"] = sum(
            [
                bool(context["selected"]["q"]),
                len(context["selected"]["categories"]),
                len(context["selected"]["teachers"]),
                bool(context["selected"]["duration"]),
                bool(context["selected"]["price"]),
                bool(context["selected"]["rating"]),
            ]
        )
        context["total_courses"] = Course.objects.count()
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"

    def get_queryset(self):
        # El temario recorre módulos y lecciones: sin prefetch son 1 + N consultas.
        return Course.objects.select_related("teacher").prefetch_related("modules__lessons")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["is_enrolled"] = (
            user.is_authenticated
            and Enrollment.objects.filter(user=user, course=self.object).exists()
        )
        return context


class EnrollView(LoginRequiredMixin, View):
    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        Enrollment.objects.get_or_create(user=request.user, course=course)
        return redirect("course_player", pk=course.pk)  # TODO: cambiar a course_player cuando exista

class CoursePlayerView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "courses/course_player.html"
    context_object_name = "course"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not Enrollment.objects.filter(user=request.user, course=self.object).exists():
            return redirect("course_detail", pk=self.object.pk)
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        all_lessons = list(Lesson.for_course(course).select_related("module"))
        completed_ids = set(
            Progress.objects.filter(user=self.request.user, lesson__in=all_lessons, completed=True)
            .values_list("lesson_id", flat=True)
        )

        lesson_id = self.kwargs.get("lesson_id")
        if lesson_id:
            lesson = get_object_or_404(Lesson, pk=lesson_id, module__course=course)
        else:
            lesson = next((l for l in all_lessons if l.id not in completed_ids), all_lessons[0] if all_lessons else None)

        current_index = all_lessons.index(lesson) if lesson in all_lessons else -1
        next_lesson = all_lessons[current_index + 1] if 0 <= current_index + 1 < len(all_lessons) else None

        total_lessons = len(all_lessons)
        completed_count = len(completed_ids)

        context.update({
            "all_lessons": all_lessons,
            "current_lesson": lesson,
            "current_module": lesson.module if lesson else None,
            "completed_ids": completed_ids,
            "next_lesson": next_lesson,
            "total_lessons": total_lessons,
            "completed_count": completed_count,
            "percentage": round(completed_count / total_lessons * 100) if total_lessons else 0,
        })
        return context


class CompleteLessonView(LoginRequiredMixin, View):
    def post(self, request, pk, lesson_id):
        lesson = get_object_or_404(Lesson, pk=lesson_id, module__course_id=pk)
        Progress.objects.update_or_create(user=request.user, lesson=lesson, defaults={"completed": True})

        all_lessons = list(Lesson.for_course(pk))
        current_index = all_lessons.index(lesson)
        next_lesson = all_lessons[current_index + 1] if current_index + 1 < len(all_lessons) else None

        next_url = (
            reverse("course_player_lesson", args=[pk, next_lesson.id])
            if next_lesson
            else reverse("course_detail", args=[pk])
        )
        return JsonResponse({"next_url": next_url})