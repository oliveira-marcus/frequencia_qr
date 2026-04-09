from django.urls import path
from . import views

urlpatterns = [
    # Públicos
    path('disciplinas/', views.DisciplinaListAPI.as_view(), name='api_disciplinas'),
    path('professores/', views.ProfessorListAPI.as_view(), name='api_professores'),
    path('aulas/', views.AulaListPublicaAPI.as_view(), name='api_aulas_publico'),

    # Restritos
    path('alunos/', views.AlunoListCreateAPI.as_view(), name='api_alunos'),
    path('alunos/<int:pk>/', views.AlunoDetailAPI.as_view(), name='api_aluno_detail'),
    path('aulas/gerenciar/', views.AulaListCreateAPI.as_view(), name='api_aulas'),
    path('aulas/gerenciar/<int:pk>/', views.AulaDetailAPI.as_view(), name='api_aula_detail'),
    path('presencas/', views.PresencaListCreateAPI.as_view(), name='api_presencas'),
]