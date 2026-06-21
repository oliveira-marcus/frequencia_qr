import time

from celery import shared_task
from django.core.cache import cache


@shared_task
def processar_presenca(aluno_id, aula_id, ip, lat, lon, geo_erro, user_id):
    from aulas.models import Aula
    from usuarios.models import LogAuditoria
    from .models import Presenca
    from .validacoes import validar_horario, validar_rede, validar_geolocalizacao

    time.sleep(3)

    cache_key_presenca = f'presenca_exists:{aluno_id}_{aula_id}'

    try:
        aluno = Presenca._meta.get_field('aluno').related_model.objects.get(id=aluno_id)
        aula = Aula.objects.get(id=aula_id)
    except Exception:
        return {'sucesso': False, 'mensagem': 'Aula ou aluno não encontrado.'}

    def registrar_log(acao):
        from django.contrib.auth import get_user_model
        try:
            user = get_user_model().objects.get(id=user_id)
            LogAuditoria.objects.create(user=user, acao=acao, ip=ip)
        except Exception:
            pass

    horario_ok, msg_horario = validar_horario(aula)
    if not horario_ok:
        Presenca.objects.create(aluno=aluno, aula=aula, ip_registrado=ip, status='negado')
        cache.set(cache_key_presenca, True, timeout=None)
        registrar_log(f'Presença negada (horário): {msg_horario}')
        return {'sucesso': False, 'mensagem': msg_horario}

    if not validar_rede(ip):
        Presenca.objects.create(aluno=aluno, aula=aula, ip_registrado=ip, status='rede_invalida')
        cache.set(cache_key_presenca, True, timeout=None)
        registrar_log(f'Presença negada (rede inválida): IP {ip}')
        return {'sucesso': False, 'mensagem': f'Você não está conectado à rede da universidade. (IP: {ip})'}

    if geo_erro or not lat or not lon:
        msgs_geo = {
            'sem_https': 'O registro de presença requer conexão HTTPS. Use o link seguro da instituição.',
            'nao_suportado': 'Seu navegador não suporta geolocalização.',
            'geo_1': 'Permissão de localização negada. Habilite nas configurações do navegador.',
            'geo_2': 'Não foi possível determinar sua posição. Verifique o GPS/Wi-Fi.',
            'geo_3': 'Tempo esgotado ao obter localização. Tente novamente.',
        }
        mensagem = msgs_geo.get(geo_erro, 'Não foi possível obter sua localização.')
        Presenca.objects.create(aluno=aluno, aula=aula, ip_registrado=ip, status='fora_do_raio')
        cache.set(cache_key_presenca, True, timeout=None)
        registrar_log(f'Presença negada (geo indisponível): {geo_erro}')
        return {'sucesso': False, 'mensagem': mensagem}

    geo_ok, distancia = validar_geolocalizacao(lat, lon, aula.sala)
    if not geo_ok:
        Presenca.objects.create(
            aluno=aluno, aula=aula, ip_registrado=ip,
            latitude=lat, longitude=lon, status='fora_do_raio'
        )
        cache.set(cache_key_presenca, True, timeout=None)
        registrar_log(f'Presença negada (fora do raio): {distancia:.0f}m da sala')
        return {'sucesso': False, 'mensagem': f'Você está a {distancia:.0f}m da sala. O limite é {aula.sala.raio_permitido}m.'}

    Presenca.objects.create(
        aluno=aluno, aula=aula, ip_registrado=ip,
        latitude=lat, longitude=lon, status='presente'
    )
    cache.set(cache_key_presenca, True, timeout=None)
    registrar_log(f'Presença registrada: aula {aula.id}')
    return {
        'sucesso': True,
        'disciplina': str(aula.disciplina),
        'data': str(aula.data),
        'horario_inicio': str(aula.horario_inicio),
        'horario_fim': str(aula.horario_fim),
    }
