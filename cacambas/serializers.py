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
    veiculo = serializers.PrimaryKeyRelatedField(queryset=Veiculo.objects.all())

    class Meta:
        model = Movimentacao
        fields = ['veiculo', 'produto', 'quantidade', 'operador', 'valor_entrega']

    def validate(self, data):
        veiculo = data.get('veiculo')
        quantidade = data.get('quantidade')
        if veiculo and quantidade:
            if quantidade > veiculo.capacidade:
                # Se a quantidade for maior, levanta um erro de validação
                raise serializers.ValidationError(
                    f"A quantidade informada ({quantidade}m³) excede a capacidade do veículo '{veiculo.placa}' ({veiculo.capacidade}m³)."
                )
        return data


class UserSerializer(serializers.ModelSerializer):
    # Campo de senha para escrita, não será retornado em requisições GET
    password = serializers.CharField(
        write_only=True, 
        required=False,  # Não obrigatório em atualizações (PATCH)
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'password']
        # Garante que o email seja enviado na criação, se desejado
        extra_kwargs = {
            'email': {'required': True, 'allow_blank': False}
        }

    def create(self, validated_data):
        """
        Cria um novo usuário usando o método create_user para hashear a senha.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_staff=validated_data.get('is_staff', False),
            password=validated_data.get('password')
        )
        return user

    def update(self, instance, validated_data):
        """
        Atualiza um usuário, tratando a senha de forma especial.
        """
        # Remove a senha do dicionário para ser tratada separadamente
        password = validated_data.pop('password', None)
        
        # Atualiza os outros campos
        instance = super().update(instance, validated_data)

        # Se uma nova senha foi fornecida, atualiza e hasheia
        if password:
            instance.set_password(password)
            instance.save()
            
        return instance

class MovimentacaoStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimentacao
        fields = ['status']
