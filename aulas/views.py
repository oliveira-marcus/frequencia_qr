from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Disciplina, Sala, Aula
from .forms import DisciplinaForm, SalaForm, AulaForm
from usuarios.models import LogAuditoria


def get_ip(request):
    return request.META.get('REMOTE_ADDR')


# ─── Disciplinas ──────────────────────────────────────────

@login_required
def disciplina_list(request):
    perfil = request.user.perfil

    if perfil.tipo == 'professor':
        try:
            disciplinas = Disciplina.objects.select_related(
                'professor__perfil__user'
            ).filter(professor=perfil.professor)
        except Exception:
            disciplinas = Disciplina.objects.none()
    else:
        disciplinas = Disciplina.objects.select_related(
            'professor__perfil__user'
        ).all()

    return render(request, 'aulas/disciplina_list.html', {'disciplinas': disciplinas})


@login_required
def disciplina_create(request):
    perfil = request.user.perfil

    # Apenas admin e professor podem criar disciplinas
    if perfil.tipo == 'aluno':
        messages.error(request, 'Você não tem permissão para criar disciplinas.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            disciplina = form.save()
            LogAuditoria.objects.create(
                user=request.user,
                acao=f'Disciplina criada: {disciplina}',
                ip=get_ip(request)
            )
            messages.success(request, 'Disciplina criada com sucesso!')
            return redirect('disciplina_list')
    else:
        form = DisciplinaForm()

    return render(request, 'aulas/disciplina_form.html', {
        'form': form,
        'titulo': 'Nova Disciplina',
        'cancelar_url': 'disciplina_list',
    })


@login_required
def disciplina_edit(request, pk):
    disciplina = get_object_or_404(Disciplina, pk=pk)
    perfil = request.user.perfil

    # Professor só pode editar suas próprias disciplinas
    if perfil.tipo == 'professor':
        try:
            if disciplina.professor != perfil.professor:
                messages.error(request, 'Você não tem permissão para editar essa disciplina.')
                return redirect('disciplina_list')
        except Exception:
            return redirect('disciplina_list')
    elif perfil.tipo == 'aluno':
        messages.error(request, 'Você não tem permissão para editar disciplinas.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            LogAuditoria.objects.create(
                user=request.user,
                acao=f'Disciplina editada: {disciplina}',
                ip=get_ip(request)
            )
            messages.success(request, 'Disciplina atualizada com sucesso!')
            return redirect('disciplina_list')
    else:
        form = DisciplinaForm(instance=disciplina)

    return render(request, 'aulas/disciplina_form.html', {
        'form': form,
        'titulo': 'Editar Disciplina',
        'cancelar_url': 'disciplina_list',
    })


@login_required
def disciplina_delete(request, pk):
    disciplina = get_object_or_404(Disciplina, pk=pk)
    perfil = request.user.perfil

    if perfil.tipo == 'professor':
        try:
            if disciplina.professor != perfil.professor:
                messages.error(request, 'Você não tem permissão para excluir essa disciplina.')
                return redirect('disciplina_list')
        except Exception:
            return redirect('disciplina_list')
    elif perfil.tipo == 'aluno':
        messages.error(request, 'Você não tem permissão para excluir disciplinas.')
        return redirect('dashboard')

    if request.method == 'POST':
        nome = str(disciplina)
        disciplina.delete()
        LogAuditoria.objects.create(
            user=request.user,
            acao=f'Disciplina removida: {nome}',
            ip=get_ip(request)
        )
        messages.success(request, 'Disciplina removida com sucesso!')
        return redirect('disciplina_list')

    return render(request, 'aulas/confirmar_exclusao.html', {
        'objeto': disciplina,
        'cancelar_url': 'disciplina_list',
    })


# ─── Salas ────────────────────────────────────────────────

@login_required
def sala_list(request):
    salas = Sala.objects.all()
    return render(request, 'aulas/sala_list.html', {'salas': salas})


@login_required
def sala_create(request):
    if request.method == 'POST':
        form = SalaForm(request.POST)
        if form.is_valid():
            sala = form.save()
            LogAuditoria.objects.create(
                user=request.user,
                acao=f'Sala criada: {sala}',
                ip=get_ip(request)
            )
            messages.success(request, 'Sala criada com sucesso!')
            return redirect('sala_list')
    else:
        form = SalaForm()

    return render(request, 'aulas/sala_form.html', {
        'form': form,
        'titulo': 'Nova Sala',
        'cancelar_url': 'sala_list',
    })


@login_required
def sala_edit(request, pk):
    sala = get_object_or_404(Sala, pk=pk)
    if request.method == 'POST':
        form = SalaForm(request.POST, instance=sala)
        if form.is_valid():
            form.save()
            LogAuditoria.objects.create(
                user=request.user,
                acao=f'Sala editada: {sala}',
                ip=get_ip(request)
            )
            messages.success(request, 'Sala atualizada com sucesso!')
            return redirect('sala_list')
    else:
        form = SalaForm(instance=sala)

    return render(request, 'aulas/sala_form.html', {
        'form': form,
        'titulo': 'Editar Sala',
        'cancelar_url': 'sala_list',
    })


@login_required
def sala_delete(request, pk):
    sala = get_object_or_404(Sala, pk=pk)
    if request.method == 'POST':
        nome = str(sala)
        sala.delete()
        LogAuditoria.objects.create(
            user=request.user,
            acao=f'Sala removida: {nome}',
            ip=get_ip(request)
        )
        messages.success(request, 'Sala removida com sucesso!')
        return redirect('sala_list')

    return render(request, 'aulas/confirmar_exclusao.html', {
        'objeto': sala,
        'cancelar_url': 'sala_list',
    })


# ─── Aulas ────────────────────────────────────────────────

@login_required
def aula_list(request):
    perfil = request.user.perfil

    # Professor vê apenas suas próprias aulas
    if perfil.tipo == 'professor':
        try:
            professor = perfil.professor
            aulas = Aula.objects.select_related('disciplina', 'sala').filter(
                disciplina__professor=professor
            )
        except Exception:
            aulas = Aula.objects.none()
    else:
        # Admin vê todas
        aulas = Aula.objects.select_related('disciplina', 'sala').all()

    return render(request, 'aulas/aula_list.html', {'aulas': aulas})


@login_required
def aula_create(request):
    perfil = request.user.perfil

    if perfil.tipo == 'aluno':
        messages.error(request, 'Você não tem permissão para criar aulas.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = AulaForm(request.POST)
        if form.is_valid():
            aula = form.save()
            LogAuditoria.objects.create(
                user=request.user,
                acao=f'Aula criada: {aula}',
                ip=get_ip(request)
            )
            messages.success(request, 'Aula criada e QR Code gerado com sucesso!')
            return redirect('aula_list')
    else:
        form = AulaForm()

    return render(request, 'aulas/aula_form.html', {
        'form': form,
        'titulo': 'Nova Aula',
        'cancelar_url': 'aula_list',
    })



@login_required
def aula_edit(request, pk):
    aula = get_object_or_404(Aula, pk=pk)
    perfil = request.user.perfil

    # Professor só pode editar aulas das suas disciplinas
    if perfil.tipo == 'professor':
        try:
            if aula.disciplina.professor != perfil.professor:
                messages.error(request, 'Você não tem permissão para editar essa aula.')
                return redirect('aula_list')
        except Exception:
            return redirect('aula_list')
    elif perfil.tipo == 'aluno':
        messages.error(request, 'Você não tem permissão para editar aulas.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = AulaForm(request.POST, instance=aula)
        if form.is_valid():
            form.save()
            LogAuditoria.objects.create(
                user=request.user,
                acao=f'Aula editada: {aula}',
                ip=get_ip(request)
            )
            messages.success(request, 'Aula atualizada com sucesso!')
            return redirect('aula_list')
    else:
        form = AulaForm(instance=aula)

    return render(request, 'aulas/aula_form.html', {
        'form': form,
        'titulo': 'Editar Aula',
        'cancelar_url': 'aula_list',
    })


@login_required
def aula_delete(request, pk):
    aula = get_object_or_404(Aula, pk=pk)
    perfil = request.user.perfil

    if perfil.tipo == 'professor':
        try:
            if aula.disciplina.professor != perfil.professor:
                messages.error(request, 'Você não tem permissão para excluir essa aula.')
                return redirect('aula_list')
        except Exception:
            return redirect('aula_list')
    elif perfil.tipo == 'aluno':
        messages.error(request, 'Você não tem permissão para excluir aulas.')
        return redirect('dashboard')

    if request.method == 'POST':
        nome = str(aula)
        aula.delete()
        LogAuditoria.objects.create(
            user=request.user,
            acao=f'Aula removida: {nome}',
            ip=get_ip(request)
        )
        messages.success(request, 'Aula removida com sucesso!')
        return redirect('aula_list')

    return render(request, 'aulas/confirmar_exclusao.html', {
        'objeto': aula,
        'cancelar_url': 'aula_list',
    })


@login_required
def aula_detail(request, pk):
    """Página de detalhes da aula com QR Code para impressão."""
    aula = get_object_or_404(Aula, pk=pk)
    presencas = aula.presencas.select_related('aluno__perfil__user').all()
    return render(request, 'aulas/aula_detail.html', {
        'aula': aula,
        'presencas': presencas,
    })