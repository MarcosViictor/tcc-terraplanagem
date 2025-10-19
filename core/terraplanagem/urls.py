from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PerfilViewSet, ObraViewSet, FornecedorViewSet, ContratoViewSet,
    EquipamentoViewSet, FuncionarioViewSet, AtividadeViewSet,
    MotivoManutencaoViewSet, ImportacaoViewSet
)

router = DefaultRouter()
router.register(r'perfis', PerfilViewSet, basename='perfil')
router.register(r'obras', ObraViewSet, basename='obra')
router.register(r'fornecedores', FornecedorViewSet, basename='fornecedor')
router.register(r'contratos', ContratoViewSet, basename='contrato')
router.register(r'equipamentos', EquipamentoViewSet, basename='equipamento')
router.register(r'funcionarios', FuncionarioViewSet, basename='funcionario')
router.register(r'atividades', AtividadeViewSet, basename='atividade')
router.register(r'motivos-manutencao', MotivoManutencaoViewSet, basename='motivo-manutencao')
router.register(r'importacoes', ImportacaoViewSet, basename='importacao')

urlpatterns = [
    path('', include(router.urls)),
]
