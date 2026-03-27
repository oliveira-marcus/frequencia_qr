from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def index(request):
    # Se já estiver logado, vai direto pro dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('account_login')


@login_required
def dashboard(request):
    perfil = request.user.perfil

    context = {
        'perfil': perfil,
    }

    # Redireciona para o template certo dependendo do tipo de usuário
    if perfil.tipo == 'professor':
        return render(request, 'usuarios/dashboard_professor.html', context)
    elif perfil.tipo == 'aluno':
        return render(request, 'usuarios/dashboard_aluno.html', context)
    else:
        return render(request, 'usuarios/dashboard_admin.html', context)