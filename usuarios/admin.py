from django.contrib import admin
from .models import Perfil, Aluno, Professor, LogAuditoria


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'tipo', 'criado_em']
    list_filter = ['tipo']
    search_fields = ['user__username', 'user__email']


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ['get_nome', 'matricula', 'curso']
    search_fields = ['perfil__user__username', 'matricula']

    def get_nome(self, obj):
        return obj.perfil.user.get_full_name() or obj.perfil.user.username
    get_nome.short_description = 'Nome'


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['get_nome', 'departamento']
    search_fields = ['perfil__user__username']

    def get_nome(self, obj):
        return obj.perfil.user.get_full_name() or obj.perfil.user.username
    get_nome.short_description = 'Nome'


@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    list_display = ['criado_em', 'user', 'acao', 'ip']
    list_filter = ['criado_em']
    search_fields = ['user__username', 'acao']
    readonly_fields = ['user', 'acao', 'detalhes', 'ip', 'criado_em']

    # Logs não devem ser editados nem criados manualmente
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False