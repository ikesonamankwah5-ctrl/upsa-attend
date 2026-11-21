from django.urls import path
from . import views


urlpatterns = [
    path(
        'past-questions/',
        views.past_questions_library,
        name='past_questions_library'
    ),

    path(
        'past-questions/<int:question_id>/view/',
        views.view_past_question,
        name='view_past_question'
    ),

    path(
        'calendar/',
        views.academic_calendar,
        name='academic_calendar'
    ),
]