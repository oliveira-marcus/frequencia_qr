import uuid
from django.db import models
from usuarios.models import Professor


class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, related_name='disciplinas')
    semestre = models.CharField(max_length=10)  # Ex: "2025.1"

    def __str__(self):
        return f'{self.codigo} - {self.nome}'

    class Meta:
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'


class Sala(models.Model):
    nome = models.CharField(max_length=50)
    predio = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    raio_permitido = models.IntegerField(default=50, help_text='Raio em metros')

    def __str__(self):
        return f'{self.nome} — {self.predio}'

    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'


class Aula(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='aulas')
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, null=True, related_name='aulas')
    data = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Verifica se a aula é nova (ainda não tem ID)
        is_nova = self.pk is None
        super().save(*args, **kwargs)
        # Só gera o QR Code na criação, não em cada edição
        if is_nova and not self.qr_code:
            from .utils import gerar_qr_code
            gerar_qr_code(self)

    def __str__(self):
        return f'{self.disciplina} — {self.data}'

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['-data', 'horario_inicio']