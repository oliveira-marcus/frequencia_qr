from rest_framework import serializers
from .models import Disciplina, Sala, Aula


class DisciplinaSerializer(serializers.ModelSerializer):
    professor_nome = serializers.SerializerMethodField()

    class Meta:
        model = Disciplina
        fields = ['id', 'nome', 'codigo', 'semestre', 'professor', 'professor_nome']

    def get_professor_nome(self, obj):
        if obj.professor:
            return obj.professor.perfil.user.get_full_name()
        return None


class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ['id', 'nome', 'predio', 'latitude', 'longitude', 'raio_permitido']


class AulaSerializer(serializers.ModelSerializer):
    disciplina_nome = serializers.SerializerMethodField()
    sala_nome = serializers.SerializerMethodField()

    class Meta:
        model = Aula
        fields = [
            'id', 'disciplina', 'disciplina_nome',
            'sala', 'sala_nome',
            'data', 'horario_inicio', 'horario_fim',
        ]

    def get_disciplina_nome(self, obj):
        return str(obj.disciplina)

    def get_sala_nome(self, obj):
        return str(obj.sala) if obj.sala else None