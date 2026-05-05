from django.urls import path
from . import views

urlpatterns = [
    # Disciplinas
    path('disciplinas/', views.disciplina_list, name='disciplina_list'),
    path('disciplinas/nova/', views.disciplina_create, name='disciplina_create'),
    path('disciplinas/<int:pk>/editar/', views.disciplina_edit, name='disciplina_edit'),
    path('disciplinas/<int:pk>/excluir/', views.disciplina_delete, name='disciplina_delete'),

    # Salas
    path('salas/', views.sala_list, name='sala_list'),
    path('salas/nova/', views.sala_create, name='sala_create'),
    path('salas/<int:pk>/editar/', views.sala_edit, name='sala_edit'),
    path('salas/<int:pk>/excluir/', views.sala_delete, name='sala_delete'),

    # Aulas
    path('aulas/', views.aula_list, name='aula_list'),
    path('aulas/nova/', views.aula_create, name='aula_create'),
    path('aulas/<int:pk>/', views.aula_detail, name='aula_detail'),
    path('aulas/<int:pk>/editar/', views.aula_edit, name='aula_edit'),
    path('aulas/<int:pk>/excluir/', views.aula_delete, name='aula_delete'),
]