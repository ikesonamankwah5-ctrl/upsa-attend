from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.classroom_list,
        name='classroom_list'
    ),

    path(
        '<int:classroom_id>/qr-code/',
        views.classroom_qr_code,
        name='classroom_qr_code'
    ),

]