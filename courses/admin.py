from django.contrib import admin
from .models import Course, Module, Lesson, Enrollment, Progress


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "rating")
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course")
    inlines = [LessonInline]


admin.site.register(Enrollment)
admin.site.register(Progress)