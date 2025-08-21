from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutoViewSet, VeiculoViewSet, MovimentacaoViewSet
from .views_relatorios import RelatorioMovimentacoes
from .views_admin import VeiculoImportCSV

router = DefaultRouter()
router.register("produtos", ProdutoViewSet, basename="produtos")
router.register("veiculos", VeiculoViewSet, basename="veiculos")
router.register("movimentacoes", MovimentacaoViewSet, basename="movimentacoes")

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/relatorios/movimentacoes/", RelatorioMovimentacoes.as_view()),
    path("api/v1/veiculos/import-csv/", VeiculoImportCSV.as_view()),
]
