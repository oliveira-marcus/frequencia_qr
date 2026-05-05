from rest_framework import serializers
from .models import Presenca


class PresencaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.SerializerMethodField()
    disciplina_nome = serializers.SerializerMethodField()

    class Meta:
        model = Presenca
        fields = [
            'id', 'aluno', 'aluno_nome',
            'aula', 'disciplina_nome',
            'horario_registro', 'status',
            'ip_registrado', 'latitude', 'longitude',
        ]
        read_only_fields = ['horario_registro', 'ip_registrado']

    def get_aluno_nome(self, obj):
        return str(obj.aluno)

    def get_disciplina_nome(self, obj):
        return str(obj.aula.disciplina)