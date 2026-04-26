from django.db import models
from usuarios.models import Aluno
from aulas.models import Aula


class RedePermitida(models.Model):
    descricao = models.CharField(max_length=100)
    cidr = models.CharField(
        max_length=50,
        help_text='Notação CIDR. Ex: 200.129.128.0/17 ou 177.20.147.50/32'
    )
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.descricao} ({self.cidr})'

    class Meta:
        verbose_name = 'Rede Permitida'
        verbose_name_plural = 'Redes Permitidas'


class Presenca(models.Model):
    STATUS_CHOICES = [
        ('presente', 'Presente'),
        ('negado', 'Negado'),
        ('fora_do_raio', 'Fora do Raio'),
        ('rede_invalida', 'Rede Inválida'),
    ]

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='presencas')
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name='presencas')
    horario_registro = models.DateTimeField(auto_now_add=True)
    ip_registrado = models.GenericIPAddressField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='presente')

    def __str__(self):
        return f'{self.aluno} — {self.aula} [{self.status}]'

    class Meta:
        verbose_name = 'Presença'
        verbose_name_plural = 'Presenças'
        # Garante que um aluno não pode ter dois registros para a mesma aula
        unique_together = [('aluno', 'aula')]
        ordering = ['-horario_registro']
