from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.practice_dashboard,
        name='practice_dashboard'
    ),

    path(
        'create/',
        views.create_practice_session,
        name='create_practice_session'
    ),

    path(
        'extract/<int:session_id>/',
        views.extract_practice_materials,
        name='extract_practice_materials'
    ),

    path(
        'generate/<int:session_id>/',
        views.generate_session_questions,
        name='generate_session_questions'
    ),

    path(
        'exam/<int:session_id>/',
        views.take_practice_session,
        name='take_practice_session'
    ),

    path(
        'save-answer/<int:session_id>/',
        views.save_practice_answer,
        name='save_practice_answer'
    ),

    path(
        'submit/<int:session_id>/',
        views.submit_practice_session,
        name='submit_practice_session'
    ),

    path(
        'results/<int:session_id>/',
        views.practice_results,
        name='practice_results'
    ),

    path(
        'delete/<int:session_id>/',
        views.delete_practice_session,
        name='delete_practice_session'
    ),

    path(
        'clear-history/',
        views.clear_practice_history,
        name='clear_practice_history'
    ),

]