from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    """
    Extende o User padrão do Django com informações extras.
    Todo usuário do sistema terá um Perfil associado.
    """
    TIPO_CHOICES = [
        ('admin', 'Administrador'),
        ('professor', 'Professor'),
        ('aluno', 'Aluno'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} ({self.tipo})'

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'


class Aluno(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE, related_name='aluno')
    matricula = models.CharField(max_length=20, unique=True)
    curso = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.perfil.user.get_full_name()} - {self.matricula}'

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'


class Professor(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE, related_name='professor')
    departamento = models.CharField(max_length=100)

    def __str__(self):
        return f'Prof. {self.perfil.user.get_full_name()}'

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'


class LogAuditoria(models.Model):
    """
    Registra todas as ações relevantes feitas pelos usuários.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    acao = models.CharField(max_length=255)
    detalhes = models.TextField(blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.criado_em:%d/%m/%Y %H:%M}] {self.user} — {self.acao}'

    class Meta:
        verbose_name = 'Log de Auditoria'
        verbose_name_plural = 'Logs de Auditoria'
        ordering = ['-criado_em']