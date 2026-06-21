from django.urls import path
from . import views

urlpatterns = [
    path('', views.registrar_presenca, name='registrar_presenca'),
    path('status/<str:task_id>/', views.status_presenca, name='status_presenca'),
]