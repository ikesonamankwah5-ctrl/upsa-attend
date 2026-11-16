from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),

    path(
        'bulk-import/',
        views.bulk_import_students,
        name='bulk_import_students'
    ),
]