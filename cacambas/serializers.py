from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Produto, Veiculo, Movimentacao
from django.contrib.auth.models import User


User = get_user_model()

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ["id", "nome", "esta_ativo"]


class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = ["id", "numero_interno", "placa", "capacidade", "tipo", "marca", "esta_ativo"]


# Serializers de leitura x escrita para Movimentacao
class MovimentacaoListSerializer(serializers.ModelSerializer):
    veiculo = serializers.CharField(source="veiculo.placa", read_only=True)
    numero_interno = serializers.CharField(source="veiculo.numero_interno", read_only=True)
    produto = serializers.CharField(source="produto.nome", read_only=True)
    operador = serializers.CharField(source="operador.username", read_only=True)
    # valor_entrega = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Movimentacao
        fields = [
            "id",
            "veiculo",
            "numero_interno",
            "produto",
            "quantidade",
            "status",
            "operador",
            "valor_entrega",
            "data_hora_saida",
        ]


class MovimentacaoCreateSerializer(serializers.ModelSerializer):
    # Altere o campo 'operador'
    # Ele agora espera um ID, mas não é obrigatório
    operador = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )

    class Meta:
        model = Movimentacao
        fields = ['veiculo', 'produto', 'quantidade', 'operador', 'valor_entrega']

    def validate(self, data):
        veiculo = data["veiculo"]
        qtd = data.get("quantidade")
        if qtd is None:
            data["quantidade"] = veiculo.capacidade
        if data["quantidade"] <= 0:
            raise serializers.ValidationError({"quantidade": "Quantidade deve ser positiva."})
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Adicione 'is_staff' à lista de campos
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff']

class MovimentacaoStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimentacao
        fields = ['status']
