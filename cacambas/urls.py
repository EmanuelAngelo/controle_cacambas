from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutoViewSet, VeiculoViewSet, MovimentacaoViewSet

# Cria um roteador
router = DefaultRouter()

# Registra nossas ViewSets com o roteador
router.register(r'produtos', ProdutoViewSet)
router.register(r'veiculos', VeiculoViewSet)
router.register(r'movimentacoes', MovimentacaoViewSet)

# As URLs da API são determinadas automaticamente pelo roteador
urlpatterns = [
    path('', include(router.urls)),
]