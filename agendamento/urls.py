from django.urls import path
from . import views
from . import views_prestador

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('agendar/', views.agendar, name='agendar'),
    path('montar-pedido/', views.montar_pedido, name='montar_pedido'),
    path('pagamento/', views.pagamento, name='pagamento'),

    path('confirmar-pedido/', views.confirmar_pedido, name='confirmar_pedido'),
    path('meus-agendamentos/', views.meus_agendamentos, name='meus_agendamentos'),

    path('agendamento/<int:agendamento_id>/editar/', views.editar_agendamento, name='editar_agendamento'),
    path('agendamento/<int:agendamento_id>/cancelar/', views.cancelar_agendamento, name='cancelar_agendamento'),

    path('prestador/dashboard/', views.prestador_dashboard, name='prestador_dashboard'),
    path('cliente/pedido/<int:pedido_id>/acompanhar/', views.cliente_acompanhamento, name='cliente_acompanhamento'),
    path('reclame-aqui/', views.reclame_aqui, name='reclame_aqui'),

    path('prestador/servicos/criar/', views_prestador.servico_criar, name='servico_criar'),
    path('prestador/servicos/<int:servico_id>/editar/', views_prestador.servico_editar, name='servico_editar'),
    path('prestador/servicos/<int:servico_id>/excluir/', views_prestador.servico_excluir, name='servico_excluir'),

    path('prestador/customizacao/salvar/', views_prestador.customizacao_salvar, name='customizacao_salvar'),
]