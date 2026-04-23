import ipaddress

from django import forms
from django.contrib import admin

from .models import Presenca, RedePermitida


@admin.register(Presenca)
class PresencaAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'aula', 'horario_registro', 'status', 'ip_registrado']
    list_filter = ['status', 'aula__disciplina']
    search_fields = ['aluno__matricula', 'aluno__perfil__user__username']
    readonly_fields = ['horario_registro', 'ip_registrado', 'latitude', 'longitude']


class RedePermitidaForm(forms.ModelForm):
    def clean_cidr(self):
        cidr = self.cleaned_data['cidr'].strip()
        try:
            ipaddress.ip_network(cidr, strict=False)
        except ValueError:
            raise forms.ValidationError(
                'CIDR inválido. Use o formato correto: 200.129.128.0/17 ou 177.20.147.50/32'
            )
        return cidr

    class Meta:
        model = RedePermitida
        fields = '__all__'


@admin.register(RedePermitida)
class RedePermitidaAdmin(admin.ModelAdmin):
    form = RedePermitidaForm
    list_display = ['descricao', 'cidr', 'ativo']
    list_editable = ['ativo']