from django.urls import path
from . import views

urlpatterns = [
    path('', views.study_group_list, name='study_group_list'),

    path('create/', views.create_study_group, name='create_study_group'),

    path(
        'group/<int:group_id>/',
        views.study_group_detail,
        name='study_group_detail'
    ),

    path(
        'group/<int:group_id>/join/',
        views.join_study_group,
        name='join_study_group'
    ),

    path(
        'group/<int:group_id>/leave/',
        views.leave_study_group,
        name='leave_study_group'
    ),

    path(
        'group/<int:group_id>/delete/',
        views.delete_study_group,
        name='delete_study_group'
    ),

    path(
        'group/<int:group_id>/sessions/create/',
        views.create_study_session,
        name='create_study_session'
    ),

    path(
        'group/<int:group_id>/send-message/',
        views.send_group_message,
        name='send_group_message'
    ),

    path(
        'group/<int:group_id>/messages/',
        views.get_group_messages,
        name='get_group_messages'
    ),

    path(
        'membership/<int:membership_id>/approve/',
        views.approve_membership,
        name='approve_membership'
    ),

    path(
        'membership/<int:membership_id>/reject/',
        views.reject_membership,
        name='reject_membership'
    ),
]