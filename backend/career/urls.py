from django.urls import path
from . import views

app_name = 'career'

urlpatterns = [
    path('', views.career_dashboard, name='dashboard'),

    # Opportunities Hub
    path('opportunities/', views.opportunity_list, name='opportunity_list'),
    path('opportunities/<int:opportunity_id>/', views.opportunity_detail, name='opportunity_detail'),

    # Career Exploration
    path('careers/<slug:slug>/', views.career_detail, name='career_detail'),

    # Career Quest
    path('quest/', views.career_quest, name='quest'),
    path('quest/start/', views.start_career_quest, name='start_career_quest'),
    path('quest/<int:assessment_id>/question/', views.career_question, name='career_question'),
    path('quest/<int:assessment_id>/results/', views.career_results, name='career_results'),

    # Delete Career Quest Results
    path(
        'quest/<int:assessment_id>/delete/',
        views.delete_career_result,
        name='delete_career_result'
    ),
]