from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from usuarios.models import Aluno, Professor
from aulas.models import Disciplina, Aula
from presencas.models import Presenca

from usuarios.serializers import AlunoSerializer, ProfessorSerializer
from aulas.serializers import DisciplinaSerializer, AulaSerializer
from presencas.serializers import PresencaSerializer


# ─── Endpoints Públicos ───────────────────────────────────

class DisciplinaListAPI(generics.ListAPIView):
    """Lista todas as disciplinas — público."""
    queryset = Disciplina.objects.select_related('professor__perfil__user').all()
    serializer_class = DisciplinaSerializer
    permission_classes = [permissions.AllowAny]


class ProfessorListAPI(generics.ListAPIView):
    """Lista todos os professores — público."""
    queryset = Professor.objects.select_related('perfil__user').all()
    serializer_class = ProfessorSerializer
    permission_classes = [permissions.AllowAny]


class AulaListPublicaAPI(generics.ListAPIView):
    """Lista todas as aulas — público."""
    queryset = Aula.objects.select_related('disciplina', 'sala').all()
    serializer_class = AulaSerializer
    permission_classes = [permissions.AllowAny]


# ─── Endpoints Restritos ──────────────────────────────────

class AlunoListCreateAPI(generics.ListCreateAPIView):
    """Lista e cria alunos — autenticado."""
    queryset = Aluno.objects.select_related('perfil__user').all()
    serializer_class = AlunoSerializer
    permission_classes = [permissions.IsAuthenticated]


class AlunoDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """Detalhe, edição e exclusão de aluno — autenticado."""
    queryset = Aluno.objects.select_related('perfil__user').all()
    serializer_class = AlunoSerializer
    permission_classes = [permissions.IsAuthenticated]


class AulaListCreateAPI(generics.ListCreateAPIView):
    """Lista e cria aulas — autenticado."""
    queryset = Aula.objects.select_related('disciplina', 'sala').all()
    serializer_class = AulaSerializer
    permission_classes = [permissions.IsAuthenticated]


class AulaDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """Detalhe, edição e exclusão de aula — autenticado."""
    queryset = Aula.objects.select_related('disciplina', 'sala').all()
    serializer_class = AulaSerializer
    permission_classes = [permissions.IsAuthenticated]


class PresencaListCreateAPI(generics.ListCreateAPIView):
    """Lista e cria presenças — autenticado."""
    serializer_class = PresencaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        perfil = self.request.user.perfil

        # Aluno vê apenas suas próprias presenças
        if perfil.tipo == 'aluno':
            return Presenca.objects.filter(
                aluno=perfil.aluno
            ).select_related('aluno', 'aula__disciplina')

        # Professor vê presenças das suas disciplinas
        if perfil.tipo == 'professor':
            return Presenca.objects.filter(
                aula__disciplina__professor=perfil.professor
            ).select_related('aluno', 'aula__disciplina')

        # Admin vê tudo
        return Presenca.objects.select_related('aluno', 'aula__disciplina').all()