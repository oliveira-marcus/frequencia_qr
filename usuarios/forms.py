from django import forms
from django.contrib.auth.models import User
from .models import Perfil, Aluno, Professor


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        help_texts = {
            'username': 'Será preenchido automaticamente pelo Google no primeiro acesso.',
            'email': 'Use o email institucional do usuário.',
        }


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['matricula', 'curso']


class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['departamento']