from django.db import models
from django.conf import settings

# Modelo para os tipos de produtos transportados
class Produto(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Produto")
    esta_ativo = models.BooleanField(default=True, verbose_name="Está ativo?")

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.nome

# Modelo para os veículos
class Veiculo(models.Model):
    numero_interno = models.CharField(max_length=50, unique=True, verbose_name="Número Interno") # [cite: 11, 52]
    placa = models.CharField(max_length=10, unique=True, verbose_name="Placa") # [cite: 10, 53]
    capacidade = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Capacidade (m³)") # [cite: 11, 54]
    tipo = models.CharField(max_length=50, verbose_name="Tipo") # [cite: 12, 55]
    marca = models.CharField(max_length=50, verbose_name="Marca") # [cite: 13, 56]
    esta_ativo = models.BooleanField(default=True, verbose_name="Está ativo?") # [cite: 14, 21]

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"

    def __str__(self):
        return f"{self.marca} - {self.placa}"

# Modelo principal para registrar as saídas/movimentações
class Movimentacao(models.Model):
    # Definindo status para o fluxo de cancelamento
    class Status(models.TextChoices):
        CONCLUIDO = 'CONCLUIDO', 'Concluído'
        PENDENTE_CANCELAMENTO = 'PENDENTE', 'Pendente Cancelamento'
        CANCELADO = 'CANCELADO', 'Cancelado'

    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, related_name='movimentacoes', verbose_name="Veículo")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='movimentacoes', verbose_name="Produto")
    # A forma correta de referenciar o usuário do Django é usando settings.AUTH_USER_MODEL
    operador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='movimentacoes', verbose_name="Operador")
    quantidade = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Quantidade (m³)") # [cite: 7]
    data_hora_saida = models.DateTimeField(auto_now_add=True, verbose_name="Data e Hora da Saída") # [cite: 80, 81]
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CONCLUIDO, verbose_name="Status")

    class Meta:
        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"
        ordering = ['-data_hora_saida'] # Ordena as mais recentes primeiro

    def __str__(self):
        return f"Saída de {self.veiculo.placa} ({self.produto.nome}) em {self.data_hora_saida.strftime('%d/%m/%Y %H:%M')}"