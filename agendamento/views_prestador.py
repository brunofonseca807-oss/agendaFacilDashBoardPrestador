from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .models import Servico
from .forms_servico import ServicoForm


@login_required
@require_POST
def servico_criar(request):
    form = ServicoForm(request.POST)
    if form.is_valid():
        servico = form.save(commit=False)
        servico.prestador = request.user
        servico.save()
        return JsonResponse({
            'success': True,
            'servico': {
                'id': servico.id,
                'nome': servico.nome,
                'descricao': servico.descricao,
                'preco': str(servico.preco),
                'duracao_estimada': servico.duracao_estimada,
            },
        })
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@login_required
@require_POST
def servico_editar(request, servico_id):
    # get_object_or_404 com prestador=request.user garante ownership:
    # retorna 404 se o servico pertencer a outro usuario
    servico = get_object_or_404(Servico, id=servico_id, prestador=request.user)
    form = ServicoForm(request.POST, instance=servico)
    if form.is_valid():
        form.save()
        return JsonResponse({
            'success': True,
            'servico': {
                'id': servico.id,
                'nome': servico.nome,
                'descricao': servico.descricao,
                'preco': str(servico.preco),
                'duracao_estimada': servico.duracao_estimada,
            },
        })
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@login_required
@require_POST
def servico_excluir(request, servico_id):
    # get_object_or_404 com prestador=request.user garante ownership
    servico = get_object_or_404(Servico, id=servico_id, prestador=request.user)
    servico.delete()
    return JsonResponse({'success': True})
