from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Perfil, Aluno, Professor


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class AlunoSerializer(serializers.ModelSerializer):
    nome = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Aluno
        fields = ['id', 'nome', 'email', 'matricula', 'curso']

    def get_nome(self, obj):
        return obj.perfil.user.get_full_name() or obj.perfil.user.username

    def get_email(self, obj):
        return obj.perfil.user.email


class ProfessorSerializer(serializers.ModelSerializer):
    nome = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Professor
        fields = ['id', 'nome', 'email', 'departamento']

    def get_nome(self, obj):
        return obj.perfil.user.get_full_name() or obj.perfil.user.username

    def get_email(self, obj):
        return obj.perfil.user.email