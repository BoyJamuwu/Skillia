from django.contrib import admin
from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("full_name", "specialty", "rating", "years_experience")
    search_fields = ("full_name", "specialty")
