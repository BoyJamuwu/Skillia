from django.db.models import Count
from django.views.generic import DetailView, ListView
from .models import Teacher


class TeacherListView(ListView):
    model = Teacher
    template_name = "teachers/teacher_list.html"
    context_object_name = "teachers"

    def get_queryset(self):
        return Teacher.objects.annotate(
            courses_count=Count("courses", distinct=True),
            students_count=Count("courses__enrollment", distinct=True),
        )


class TeacherDetailView(DetailView):
    model = Teacher
    template_name = "teachers/teacher_detail.html"
    context_object_name = "teacher"

    def get_queryset(self):
        return Teacher.objects.annotate(
            courses_count=Count("courses", distinct=True),
            students_count=Count("courses__enrollment", distinct=True),
            lessons_count=Count("courses__modules__lessons", distinct=True),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courses"] = self.object.courses.all()
        return context
