from django.urls import path
from . import views

app_name = 'study_simplifier'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('new/', views.create_session, name='create_session'),

    path(
        '<int:session_id>/',
        views.session_detail,
        name='session_detail'
    ),

    path(
        '<int:session_id>/download/',
        views.download_material,
        name='download_material'
    ),

    path(
        '<int:session_id>/material/<int:material_id>/download/',
        views.download_study_material,
        name='download_study_material'
    ),
]