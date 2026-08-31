from django.urls import path
from .views import CourseListView, CourseDetailView, EnrollView, CoursePlayerView, CompleteLessonView

urlpatterns = [
    path("", CourseListView.as_view(), name="course_list"),
    path("<int:pk>/", CourseDetailView.as_view(), name="course_detail"),
    path("<int:pk>/enroll/", EnrollView.as_view(), name="course_enroll"),
    path("<int:pk>/player/", CoursePlayerView.as_view(), name="course_player"),
    path("<int:pk>/player/<int:lesson_id>/", CoursePlayerView.as_view(), name="course_player_lesson"),
    path("<int:pk>/lessons/<int:lesson_id>/complete/", CompleteLessonView.as_view(), name="lesson_complete"),
]