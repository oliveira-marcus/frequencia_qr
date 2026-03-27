from django import forms
from django.contrib.auth.models import User
from .models import Perfil, Aluno, Professor


class UserForm(forms.ModelForm):
    """Formulário para criar/editar o User base."""
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        help_text='Deixe em branco para manter a senha atual.'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['matricula', 'curso']


class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['departamento']