from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Perfil, Aluno, Professor, LogAuditoria
from .forms import UserForm, AlunoForm, ProfessorForm


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('account_login')


@login_required
def dashboard(request):
    perfil = request.user.perfil

    if perfil.tipo == 'professor':
        try:
            professor = perfil.professor
            disciplinas = professor.disciplinas.prefetch_related('aulas').all()
            from django.utils import timezone
            aulas_hoje = []
            for d in disciplinas:
                aulas_hoje += list(d.aulas.filter(data=timezone.localdate()))

            context = {
                'perfil': perfil,
                'disciplinas': disciplinas,
                'aulas_hoje': aulas_hoje,
                'total_disciplinas': disciplinas.count(),
                'total_aulas_hoje': len(aulas_hoje),
            }
        except Exception:
            context = {'perfil': perfil}
        return render(request, 'usuarios/dashboard_professor.html', context)

    elif perfil.tipo == 'aluno':
        try:
            aluno = perfil.aluno
            from presencas.models import Presenca
            presencas = Presenca.objects.filter(
                aluno=aluno, status='presente'
            ).select_related('aula__disciplina').order_by('-horario_registro')[:5]

            total_presencas = Presenca.objects.filter(aluno=aluno, status='presente').count()

            context = {
                'perfil': perfil,
                'presencas_recentes': presencas,
                'total_presencas': total_presencas,
            }
        except Exception:
            context = {'perfil': perfil}
        return render(request, 'usuarios/dashboard_aluno.html', context)

    else:
        from django.contrib.auth.models import User
        from aulas.models import Aula, Disciplina
        from presencas.models import Presenca

        context = {
            'perfil': perfil,
            'total_usuarios': User.objects.count(),
            'total_disciplinas': Disciplina.objects.count(),
            'total_aulas': Aula.objects.count(),
            'total_presencas': Presenca.objects.count(),
        }
        return render(request, 'usuarios/dashboard_admin.html', context)


# ─── Alunos ───────────────────────────────────────────────

@login_required
def aluno_list(request):
    alunos = Aluno.objects.select_related('perfil__user').all()
    return render(request, 'usuarios/aluno_list.html', {'alunos': alunos})


@login_required
def aluno_create(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        aluno_form = AlunoForm(request.POST)

        if user_form.is_valid() and aluno_form.is_valid():
            # Cria o User
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Cria o Perfil
            perfil = Perfil.objects.create(user=user, tipo='aluno')

            # Cria o Aluno
            aluno = aluno_form.save(commit=False)
            aluno.perfil = perfil
            aluno.save()

            LogAuditoria.objects.create(
                user=request.user,
                acao=f'Aluno criado: {user.username}',
                ip=request.META.get('REMOTE_ADDR')
            )

            messages.success(request, f'Aluno {user.get_full_name()} criado com sucesso!')
            return redirect('aluno_list')
    else:
        user_form = UserForm()
        aluno_form = AlunoForm()

    return render(request, 'usuarios/aluno_form.html', {
        'user_form': user_form,
        'aluno_form': aluno_form,
        'titulo': 'Novo Aluno',
    })


@login_required
def aluno_edit(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    user = aluno.perfil.user

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        aluno_form = AlunoForm(request.POST, instance=aluno)

        if user_form.is_valid() and aluno_form.is_valid():
            user = user_form.save(commit=False)
            senha = user_form.cleaned_data.get('password')
            if senha:
                user.set_password(senha)
            user.save()
            aluno_form.save()

            LogAuditoria.objects.create(
                user=request.user,
                acao=f'Aluno editado: {user.username}',
                ip=request.META.get('REMOTE_ADDR')
            )

            messages.success(request, 'Aluno atualizado com sucesso!')
            return redirect('aluno_list')
    else:
        user_form = UserForm(instance=user)
        aluno_form = AlunoForm(instance=aluno)

    return render(request, 'usuarios/aluno_form.html', {
        'user_form': user_form,
        'aluno_form': aluno_form,
        'titulo': 'Editar Aluno',
    })


@login_required
def aluno_delete(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == 'POST':
        nome = str(aluno)
        aluno.perfil.user.delete()  # Cascata: deleta perfil e aluno também
        LogAuditoria.objects.create(
            user=request.user,
            acao=f'Aluno removido: {nome}',
            ip=request.META.get('REMOTE_ADDR')
        )
        messages.success(request, 'Aluno removido com sucesso!')
        return redirect('aluno_list')

    return render(request, 'usuarios/confirmar_exclusao.html', {
        'objeto': aluno,
        'cancelar_url': 'aluno_list',
    })


# ─── Professores ──────────────────────────────────────────

@login_required
def professor_list(request):
    professores = Professor.objects.select_related('perfil__user').all()
    return render(request, 'usuarios/professor_list.html', {'professores': professores})


@login_required
def professor_create(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        professor_form = ProfessorForm(request.POST)

        if user_form.is_valid() and professor_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            perfil = Perfil.objects.create(user=user, tipo='professor')

            professor = professor_form.save(commit=False)
            professor.perfil = perfil
            professor.save()

            LogAuditoria.objects.create(
                user=request.user,
                acao=f'Professor criado: {user.username}',
                ip=request.META.get('REMOTE_ADDR')
            )

            messages.success(request, f'Professor {user.get_full_name()} criado com sucesso!')
            return redirect('professor_list')
    else:
        user_form = UserForm()
        professor_form = ProfessorForm()

    return render(request, 'usuarios/professor_form.html', {
        'user_form': user_form,
        'professor_form': professor_form,
        'titulo': 'Novo Professor',
    })


@login_required
def professor_edit(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    user = professor.perfil.user

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        professor_form = ProfessorForm(request.POST, instance=professor)

        if user_form.is_valid() and professor_form.is_valid():
            user = user_form.save(commit=False)
            senha = user_form.cleaned_data.get('password')
            if senha:
                user.set_password(senha)
            user.save()
            professor_form.save()

            LogAuditoria.objects.create(
                user=request.user,
                acao=f'Professor editado: {user.username}',
                ip=request.META.get('REMOTE_ADDR')
            )

            messages.success(request, 'Professor atualizado com sucesso!')
            return redirect('professor_list')
    else:
        user_form = UserForm(instance=user)
        professor_form = ProfessorForm(instance=professor)

    return render(request, 'usuarios/professor_form.html', {
        'user_form': user_form,
        'professor_form': professor_form,
        'titulo': 'Editar Professor',
    })


@login_required
def professor_delete(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    if request.method == 'POST':
        nome = str(professor)
        professor.perfil.user.delete()
        LogAuditoria.objects.create(
            user=request.user,
            acao=f'Professor removido: {nome}',
            ip=request.META.get('REMOTE_ADDR')
        )
        messages.success(request, 'Professor removido com sucesso!')
        return redirect('professor_list')

    return render(request, 'usuarios/confirmar_exclusao.html', {
        'objeto': professor,
        'cancelar_url': 'professor_list',
    })