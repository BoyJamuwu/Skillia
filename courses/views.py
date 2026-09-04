from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, ListView
from .models import Course, Enrollment
from django.http import JsonResponse
from django.urls import reverse
from .models import Course, Enrollment, Lesson, Progress

class CourseListView(ListView):
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"


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