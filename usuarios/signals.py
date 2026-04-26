from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from allauth.socialaccount.signals import pre_social_login
from .models import Perfil, Aluno


@receiver(post_save, sender=User)
def criar_perfil_novo_usuario(sender, instance, created, **kwargs):
    if created:
        perfil, _ = Perfil.objects.get_or_create(user=instance, defaults={'tipo': 'aluno'})
        if perfil.tipo == 'aluno':
            Aluno.objects.get_or_create(perfil=perfil)


@receiver(pre_social_login)
def criar_perfil_social(sender, request, sociallogin, **kwargs):
    user = sociallogin.user
    if user.pk:
        perfil, _ = Perfil.objects.get_or_create(user=user, defaults={'tipo': 'aluno'})
        if perfil.tipo == 'aluno':
            Aluno.objects.get_or_create(perfil=perfil)