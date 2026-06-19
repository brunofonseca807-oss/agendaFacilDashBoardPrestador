from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .models import Servico, CustomizacaoHeader
from .forms_servico import ServicoForm
from .forms_customizacao import CustomizacaoHeaderForm


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


@login_required
@require_POST
def customizacao_salvar(request):
    customizacao = CustomizacaoHeader.get_solo()
    form = CustomizacaoHeaderForm(request.POST, request.FILES, instance=customizacao)
    if form.is_valid():
        if request.POST.get('remover_logo') and not request.FILES.get('logo'):
            customizacao.logo.delete(save=False)
            form.instance.logo = None
        customizacao = form.save()
        return JsonResponse({
            'success': True,
            'customizacao': {
                'titulo': customizacao.titulo,
                'subtitulo': customizacao.subtitulo,
                'exibir_titulo_subtitulo': customizacao.exibir_titulo_subtitulo,
                'cor_header': customizacao.cor_header,
                'logo_url': customizacao.logo.url if customizacao.logo else None,
                'logo_posicao': customizacao.logo_posicao,
            },
        })
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)
