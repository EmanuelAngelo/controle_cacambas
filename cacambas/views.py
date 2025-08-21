from rest_framework import viewsets, permissions
from .models import Produto, Veiculo, Movimentacao
from .serializers import (
    ProdutoSerializer,
    VeiculoSerializer,
    MovimentacaoListSerializer,
    MovimentacaoCreateSerializer
)

class ProdutoViewSet(viewsets.ModelViewSet):
    """
    Endpoint da API que permite que os produtos sejam vistos ou editados.
    """
    queryset = Produto.objects.all().order_by('nome')
    serializer_class = ProdutoSerializer
    permission_classes = [permissions.IsAuthenticated]

class VeiculoViewSet(viewsets.ModelViewSet):
    """
    Endpoint da API que permite que os veículos sejam vistos ou editados.
    """
    queryset = Veiculo.objects.all().order_by('placa')
    serializer_class = VeiculoSerializer
    permission_classes = [permissions.IsAuthenticated]

class MovimentacaoViewSet(viewsets.ModelViewSet):
    """
    Endpoint da API para listar e criar movimentações.
    """
    queryset = Movimentacao.objects.all()
    # A permissão IsAuthenticated garante que apenas usuários logados possam acessar
    permission_classes = [permissions.IsAuthenticated]

    # Este método escolhe qual serializer usar dependendo da ação (listar vs. criar)
    def get_serializer_class(self):
        if self.action == 'create':
            return MovimentacaoCreateSerializer
        return MovimentacaoListSerializer