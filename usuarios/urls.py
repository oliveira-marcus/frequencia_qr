from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Alunos
    path('alunos/', views.aluno_list, name='aluno_list'),
    path('alunos/novo/', views.aluno_create, name='aluno_create'),
    path('alunos/<int:pk>/editar/', views.aluno_edit, name='aluno_edit'),
    path('alunos/<int:pk>/excluir/', views.aluno_delete, name='aluno_delete'),

    # Professores
    path('professores/', views.professor_list, name='professor_list'),
    path('professores/novo/', views.professor_create, name='professor_create'),
    path('professores/<int:pk>/editar/', views.professor_edit, name='professor_edit'),
    path('professores/<int:pk>/excluir/', views.professor_delete, name='professor_delete'),
]