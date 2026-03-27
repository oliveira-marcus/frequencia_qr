from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from aulas.models import Aula


@login_required
def registrar_presenca(request):
    aula_id = request.GET.get('id')
    token = request.GET.get('token')

    # Valida se os parâmetros existem
    if not aula_id or not token:
        return render(request, 'presencas/erro.html', {
            'mensagem': 'QR Code inválido.'
        })

    # Busca a aula e valida o token
    aula = get_object_or_404(Aula, id=aula_id, token=token)

    context = {
        'aula': aula,
    }

    return render(request, 'presencas/registrar.html', context)