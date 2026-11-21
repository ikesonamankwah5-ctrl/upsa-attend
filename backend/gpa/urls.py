from django.urls import path
from . import views

urlpatterns = [
    path('', views.cgpa_dashboard, name='cgpa_dashboard'),

    path(
        'edit/<int:result_id>/',
        views.edit_semester_result,
        name='edit_semester_result'
    ),

    path(
        'delete/<int:result_id>/',
        views.delete_semester_result,
        name='delete_semester_result'
    ),
]