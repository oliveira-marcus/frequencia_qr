from celery.result import AsyncResult

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from aulas.models import Aula

from .models import Presenca
from .tasks import processar_presenca
from .validacoes import get_ip_cliente


def registrar_presenca(request):
    aula_id = request.GET.get('id')
    token = request.GET.get('token')

    if not aula_id or not token:
        return render(request, 'presencas/erro.html', {
            'mensagem': 'QR Code inválido.'
        })

    cache_key_aula = f'aula:{aula_id}_{token}'
    aula = cache.get(cache_key_aula)
    if aula is None:
        print("CACHE MISS")
        aula = get_object_or_404(Aula, id=aula_id, token=token)
        cache.set(cache_key_aula, aula, timeout=3600)

    if not request.user.is_authenticated:
        request.session['presenca_redirect'] = request.get_full_path()
        return redirect('account_login')

    try:
        aluno = request.user.perfil.aluno
    except Exception:
        return render(request, 'presencas/erro.html', {
            'mensagem': 'Apenas alunos podem registrar presença.'
        })

    cache_key_presenca = f'presenca_exists:{aluno.id}_{aula.id}'
    presenca_existe = cache.get(cache_key_presenca)
    if presenca_existe is None:
        presenca_existe = Presenca.objects.filter(aluno=aluno, aula=aula).exists()
        if presenca_existe:
            cache.set(cache_key_presenca, True, timeout=None)

    if presenca_existe:
        return redirect('dashboard')

    ip = get_ip_cliente(request)

    # --- Processamento do formulário (botão confirmar) ---
    if request.method == 'POST':
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')
        geo_erro = request.POST.get('geo_erro')

        task = processar_presenca.delay(
            aluno_id=aluno.id,
            aula_id=aula.id,
            ip=ip,
            lat=lat,
            lon=lon,
            geo_erro=geo_erro,
            user_id=request.user.id,
        )

        return render(request, 'presencas/aguardando.html', {'task_id': task.id})

    # GET — exibe a página de confirmação
    return render(request, 'presencas/registrar.html', {
        'aula': aula,
        'ip': ip,
    })


def status_presenca(request, task_id):
    result = AsyncResult(task_id)
    if not result.ready():
        return JsonResponse({'ready': False})
    return JsonResponse({'ready': True, **result.get()})