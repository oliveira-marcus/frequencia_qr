from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from aulas.models import Aula
from usuarios.models import LogAuditoria
from .models import Presenca
from .validacoes import (
    get_ip_cliente,
    validar_rede,
    validar_geolocalizacao,
    validar_horario,
)


def registrar_presenca(request):
    aula_id = request.GET.get('id')
    token = request.GET.get('token')

    # Valida parâmetros do QR Code
    if not aula_id or not token:
        return render(request, 'presencas/erro.html', {
            'mensagem': 'QR Code inválido.'
        })

    aula = get_object_or_404(Aula, id=aula_id, token=token)

    # Se não estiver logado, salva a URL atual e redireciona para login
    if not request.user.is_authenticated:
        request.session['presenca_redirect'] = request.get_full_path()
        from django.shortcuts import redirect
        return redirect('account_login')

    # Verifica se o usuário tem perfil de aluno
    try:
        aluno = request.user.perfil.aluno
    except Exception:
        return render(request, 'presencas/erro.html', {
            'mensagem': 'Apenas alunos podem registrar presença.'
        })

    # Verifica se já registrou presença nessa aula
    if Presenca.objects.filter(aluno=aluno, aula=aula).exists():
        return render(request, 'presencas/erro.html', {
            'mensagem': 'Você já registrou presença nessa aula.'
        })

    ip = get_ip_cliente(request)

    # --- Processamento do formulário (botão confirmar) ---
    if request.method == 'POST':
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')
        geo_erro = request.POST.get('geo_erro')

        # 1. Valida horário
        horario_ok, msg_horario = validar_horario(aula)
        if not horario_ok:
            presenca = Presenca.objects.create(
                aluno=aluno, aula=aula,
                ip_registrado=ip, status='negado'
            )
            _registrar_log(request, f'Presença negada (horário): {msg_horario}')
            return render(request, 'presencas/erro.html', {'mensagem': msg_horario})

        # 2. Valida rede institucional
        if not validar_rede(ip):
            Presenca.objects.create(
                aluno=aluno, aula=aula,
                ip_registrado=ip, status='rede_invalida'
            )
            _registrar_log(request, f'Presença negada (rede inválida): IP {ip}')
            return render(request, 'presencas/erro.html', {
                'mensagem': f'Você não está conectado à rede da universidade. (IP: {ip})'
            })

        # 3. Valida geolocalização
        if geo_erro or not lat or not lon:
            Presenca.objects.create(
                aluno=aluno, aula=aula,
                ip_registrado=ip, status='fora_do_raio'
            )
            _registrar_log(request, 'Presença negada (geolocalização não disponível)')
            return render(request, 'presencas/erro.html', {
                'mensagem': 'Não foi possível obter sua localização. Verifique as permissões do navegador.'
            })

        geo_ok, distancia = validar_geolocalizacao(lat, lon, aula.sala)
        if not geo_ok:
            Presenca.objects.create(
                aluno=aluno, aula=aula,
                ip_registrado=ip,
                latitude=lat, longitude=lon,
                status='fora_do_raio'
            )
            _registrar_log(request, f'Presença negada (fora do raio): {distancia:.0f}m da sala')
            return render(request, 'presencas/erro.html', {
                'mensagem': f'Você está a {distancia:.0f}m da sala. O limite é {aula.sala.raio_permitido}m.'
            })

        # ✅ Tudo válido — registra presença
        Presenca.objects.create(
            aluno=aluno, aula=aula,
            ip_registrado=ip,
            latitude=lat, longitude=lon,
            status='presente'
        )
        _registrar_log(request, f'Presença registrada: aula {aula.id}')

        return render(request, 'presencas/sucesso.html', {'aula': aula})

    # GET — exibe a página de confirmação
    return render(request, 'presencas/registrar.html', {
        'aula': aula,
        'ip': ip,
    })


def _registrar_log(request, acao):
    """Função auxiliar para gravar log de auditoria."""
    from .validacoes import get_ip_cliente
    LogAuditoria.objects.create(
        user=request.user,
        acao=acao,
        ip=get_ip_cliente(request)
    )