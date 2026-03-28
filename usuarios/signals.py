from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from allauth.socialaccount.signals import pre_social_login
from .models import Perfil


@receiver(post_save, sender=User)
def criar_perfil_novo_usuario(sender, instance, created, **kwargs):
    """
    Cria um Perfil sempre que um novo User é criado,
    independente de ser via Google ou cadastro tradicional.
    """
    if created:
        Perfil.objects.get_or_create(user=instance, defaults={'tipo': 'aluno'})


@receiver(pre_social_login)
def criar_perfil_social(sender, request, sociallogin, **kwargs):
    """
    Garante que usuários que já existem no banco também tenham perfil
    ao fazer login pelo Google.
    """
    user = sociallogin.user
    if user.pk:
        Perfil.objects.get_or_create(user=user, defaults={'tipo': 'aluno'})