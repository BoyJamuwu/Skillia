from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import EmailUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from courses.models import Course, Lesson, Progress


class SignUpView(CreateView):
    form_class = EmailUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        courses = Course.objects.filter(enrollment__user=user).distinct()

        courses_data = []
        for course in courses:
            lessons = list(Lesson.for_course(course))
            total_lessons = len(lessons)
            completed_ids = set(
                Progress.objects.filter(user=user, lesson__in=lessons, completed=True)
                .values_list("lesson_id", flat=True)
            )
            completed_lessons = [l for l in lessons if l.id in completed_ids]
            courses_data.append({
                "course": course,
                "percentage": round(len(completed_lessons) / total_lessons * 100) if total_lessons else 0,
                "completed_count": len(completed_lessons),
                "total_lessons": total_lessons,
                "last_lesson": completed_lessons[-1] if completed_lessons else None,
            })

        context["courses_data"] = courses_data
        return context