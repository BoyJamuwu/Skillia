from django.conf import settings
from django.db import models
from django.utils import timezone
from teachers.models import Teacher


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    category = models.CharField(max_length=100)
    duration = models.CharField(max_length=100, blank=True)
    teacher = models.ForeignKey(
        Teacher, related_name="courses", null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    duration = models.CharField(max_length=50, blank=True)
    video_url = models.URLField(max_length=500, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    @classmethod
    def for_course(cls, course):
        """Lecciones de un curso en el orden en que se dictan (acepta instancia o pk)."""
        return cls.objects.filter(module__course=course).order_by(
            "module__order", "module_id", "order", "id"
        )


class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "course")


class Progress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "lesson")