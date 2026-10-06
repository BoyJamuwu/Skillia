from django.contrib import admin
from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("full_name", "specialty", "user", "rating", "years_experience")
    search_fields = ("full_name", "specialty")
    # Vincular una cuenta aquí es lo que le da a ese usuario el rol de Profesor.
    autocomplete_fields = ("user",)
