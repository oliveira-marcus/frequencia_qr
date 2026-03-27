from django.contrib import admin
from .models import Disciplina, Sala, Aula


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'professor', 'semestre']
    list_filter = ['semestre']
    search_fields = ['codigo', 'nome']


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'predio', 'raio_permitido']
    search_fields = ['nome', 'predio']


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ['disciplina', 'sala', 'data', 'horario_inicio', 'horario_fim']
    list_filter = ['data', 'disciplina']
    search_fields = ['disciplina__nome']
    readonly_fields = ['token', 'qr_code']