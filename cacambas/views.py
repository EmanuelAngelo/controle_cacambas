from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, views
from rest_framework import status
from django.utils.timezone import now

from rest_framework import filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Produto, Veiculo, Movimentacao
from .serializers import (
    ProdutoSerializer,
    VeiculoSerializer,
    MovimentacaoListSerializer,
    MovimentacaoCreateSerializer, UserSerializer,
)
from .permissions import IsAdmin, IsAuthenticatedAny
from .filters import MovimentacaoFilter


class MeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class ProdutoViewSet(ModelViewSet):
    queryset = Produto.class_.objects if hasattr(Produto, "class_") else Produto.objects  # proteção caso IDE marque
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [IsAuthenticatedAny]
    filter_backends = [DjangoFilterBackend, drf_filters.OrderingFilter, drf_filters.SearchFilter]
    search_fields = ["nome"]
    ordering_fields = ["nome", "id"]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.query_params.get("incluir_inativos") != "1":
            qs = qs.filter(esta_ativo=True)
        return qs

    @action(detail=True, methods=["patch"], permission_classes=[IsAdmin])
    def toggle(self, request, pk=None):
        obj = self.get_object()
        obj.esta_ativo = not obj.esta_ativo
        obj.save(update_fields=["esta_ativo"])
        return Response({"id": obj.id, "esta_ativo": obj.esta_ativo})


class VeiculoViewSet(ModelViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    permission_classes = [IsAuthenticatedAny]
    filter_backends = [DjangoFilterBackend, drf_filters.OrderingFilter, drf_filters.SearchFilter]
    search_fields = ["placa", "numero_interno", "marca", "tipo"]
    ordering_fields = ["placa", "capacidade", "id"]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.query_params.get("incluir_inativos") != "1":
            qs = qs.filter(esta_ativo=True)
        return qs

    @action(detail=True, methods=["patch"], permission_classes=[IsAdmin])
    def toggle(self, request, pk=None):
        obj = self.get_object()
        obj.esta_ativo = not obj.esta_ativo
        obj.save(update_fields=["esta_ativo"])
        return Response({"id": obj.id, "esta_ativo": obj.esta_ativo})


class MovimentacaoViewSet(ModelViewSet):
    queryset = Movimentacao.objects.select_related("veiculo", "produto", "operador").all()
    permission_classes = [IsAuthenticatedAny]
    filter_backends = [DjangoFilterBackend, drf_filters.OrderingFilter, drf_filters.SearchFilter]
    filterset_class = MovimentacaoFilter
    ordering_fields = ["data_hora_saida", "quantidade"]
    search_fields = ["veiculo__placa", "produto__nome", "operador__username"]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(operador=self.request.user)
        return qs

    def get_serializer_class(self):
        if self.action in ["list", "retrieve", "hoje"]:
            return MovimentacaoListSerializer
        return MovimentacaoCreateSerializer

    @action(detail=False, methods=["get"])
    def hoje(self, request):
        today = now().date()
        qs = self.get_queryset().filter(data_hora_saida__date=today)
        page = self.paginate_queryset(qs)
        ser = MovimentacaoListSerializer(page or qs, many=True)
        if page is not None:
            return self.get_paginated_response(ser.data)
        return Response(ser.data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticatedAny])
    def solicitar_cancelamento(self, request, pk=None):
        mov = self.get_object()
        if mov.status == Movimentacao.Status.CANCELADO:
            return Response({"detail": "Movimentação já cancelada."}, status=status.HTTP_400_BAD_REQUEST)
        mov.status = Movimentacao.Status.PENDENTE_CANCELAMENTO
        mov.save(update_fields=["status"])
        return Response({"id": mov.id, "status": mov.status})

    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def aprovar_cancelamento(self, request, pk=None):
        mov = self.get_object()
        mov.status = Movimentacao.Status.CANCELADO
        mov.save(update_fields=["status"])
        return Response({"id": mov.id, "status": mov.status})

    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def rejeitar_cancelamento(self, request, pk=None):
        mov = self.get_object()
        mov.status = Movimentacao.Status.CONCLUIDO
        mov.save(update_fields=["status"])
        return Response({"id": mov.id, "status": mov.status})
