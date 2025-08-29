from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MeView,
    ProdutoViewSet,
    VeiculoViewSet,
    MovimentacaoViewSet,
    UserViewSet
)

# 1. Cria uma instância do roteador
router = DefaultRouter()

# 2. Registra os ViewSets com o roteador
# Esta linha cria as rotas para /veiculos/ (GET, POST) e /veiculos/{id}/ (GET, PUT, DELETE)
router.register(r'veiculos', VeiculoViewSet, basename='veiculo')
# (Opcional, mas recomendado) Registre seus outros ViewSets aqui também
router.register(r'produtos', ProdutoViewSet, basename='produto')
router.register(r'movimentacoes', MovimentacaoViewSet, basename='movimentacao')
router.register(r'usuarios', UserViewSet, basename='usuario')


# 3. Define os padrões de URL para o app
urlpatterns = [
    # Rota para buscar o usuário logado
    path('me/', MeView.as_view(), name='me'),
    
    # Inclui todas as URLs geradas automaticamente pelo roteador
    path('', include(router.urls)),
]