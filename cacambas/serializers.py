# Em cacambas/serializers.py

from rest_framework import serializers
from .models import Produto, Veiculo, Movimentacao
from django.contrib.auth.models import User

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__' # Inclui todos os campos do modelo

class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = '__all__'

# Serializer para LISTAR as movimentações, mostrando dados legíveis
class MovimentacaoListSerializer(serializers.ModelSerializer):
    # Usando StringRelatedField para mostrar o __str__ do modelo relacionado
    veiculo = serializers.StringRelatedField()
    produto = serializers.StringRelatedField()
    # Usando ReadOnlyField para pegar um campo específico do modelo relacionado
    operador = serializers.ReadOnlyField(source='operador.username')

    class Meta:
        model = Movimentacao
        fields = ['id', 'veiculo', 'produto', 'operador', 'quantidade', 'data_hora_saida', 'status']

# Serializer para CRIAR uma nova movimentação, aceitando os IDs dos objetos
class MovimentacaoCreateSerializer(serializers.ModelSerializer):
    # Garante que o operador seja o usuário logado, e não um campo a ser enviado
    operador = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Movimentacao
        # Excluímos os campos que serão preenchidos automaticamente
        fields = ['veiculo', 'produto', 'quantidade', 'operador']