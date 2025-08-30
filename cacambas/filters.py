import django_filters as df
from .models import Movimentacao

class MovimentacaoFilter(df.FilterSet):
    de = df.DateTimeFilter(field_name="data_hora_saida", lookup_expr="gte")
    ate = df.DateTimeFilter(field_name="data_hora_saida", lookup_expr="lte")
    placa = df.CharFilter(field_name="veiculo__placa", lookup_expr="icontains")
    produto = df.NumberFilter(field_name="produto_id")
    operador = df.NumberFilter(field_name="operador_id")
    valor_entrega = df.NumberFilter(field_name="valor_entrega", lookup_expr="exact")
    status = df.CharFilter(field_name="status", lookup_expr="exact")

    class Meta:
        model = Movimentacao
        fields = ["de", "ate", "placa", "produto", "operador", "status", "valor_entrega"]
