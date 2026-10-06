from django.urls import path
from .views import TeacherListView, TeacherDetailView
from . import panel_views as panel

urlpatterns = [
    path("", TeacherListView.as_view(), name="teacher_list"),
    path("<int:pk>/", TeacherDetailView.as_view(), name="teacher_detail"),

    # Panel del Profesor
    path("panel/", panel.PanelView.as_view(), name="teacher_panel"),
    path("panel/courses/new/", panel.CourseCreateView.as_view(), name="panel_course_create"),
    path("panel/courses/<int:pk>/", panel.CourseManageView.as_view(), name="panel_course_manage"),
    path("panel/courses/<int:pk>/edit/", panel.CourseUpdateView.as_view(), name="panel_course_edit"),
    path("panel/courses/<int:pk>/modules/new/", panel.ModuleCreateView.as_view(), name="panel_module_create"),
    path("panel/modules/<int:pk>/edit/", panel.ModuleUpdateView.as_view(), name="panel_module_edit"),
    path("panel/modules/<int:pk>/delete/", panel.ModuleDeleteView.as_view(), name="panel_module_delete"),
    path("panel/modules/<int:pk>/lessons/new/", panel.LessonCreateView.as_view(), name="panel_lesson_create"),
    path("panel/lessons/<int:pk>/edit/", panel.LessonUpdateView.as_view(), name="panel_lesson_edit"),
    path("panel/lessons/<int:pk>/delete/", panel.LessonDeleteView.as_view(), name="panel_lesson_delete"),
]
