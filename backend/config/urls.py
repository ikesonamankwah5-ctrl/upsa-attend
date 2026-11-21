from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('sw.js', views.service_worker, name='service_worker'),

    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('classrooms/', include('classrooms.urls')),
    path('students/', include('students.urls')),
    path('attendance/', include('attendance.urls')),
    path('reports/', include('reports.urls')),
    path('gpa/', include('gpa.urls')),
    path('academics/', include('academics.urls')),
    path('practice/', include('practice.urls')),
    path('study-connect/', include('study_connect.urls')),
    path('career/', include('career.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('study-simplifier/', include('study_simplifier.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )