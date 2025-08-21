from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Produto, Veiculo, Movimentacao

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
            "data_hora_saida",
        ]


class MovimentacaoCreateSerializer(serializers.ModelSerializer):
    operador = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Movimentacao
        fields = ["id", "veiculo", "produto", "quantidade", "operador"]

    def validate(self, data):
        veiculo = data["veiculo"]
        qtd = data.get("quantidade")
        if qtd is None:
            data["quantidade"] = veiculo.capacidade
        if data["quantidade"] <= 0:
            raise serializers.ValidationError({"quantidade": "Quantidade deve ser positiva."})
        return data
