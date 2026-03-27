from django.contrib import admin
from .models import Presenca


@admin.register(Presenca)
class PresencaAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'aula', 'horario_registro', 'status', 'ip_registrado']
    list_filter = ['status', 'aula__disciplina']
    search_fields = ['aluno__matricula', 'aluno__perfil__user__username']
    readonly_fields = ['horario_registro', 'ip_registrado', 'latitude', 'longitude']