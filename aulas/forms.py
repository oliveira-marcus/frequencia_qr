from django import forms
from .models import Disciplina, Sala, Aula


class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome', 'codigo', 'professor', 'semestre']


class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['nome', 'predio', 'latitude', 'longitude', 'raio_permitido']


class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = ['disciplina', 'sala', 'data', 'horario_inicio', 'horario_fim']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'horario_fim': forms.TimeInput(attrs={'type': 'time'}),
        }