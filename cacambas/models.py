from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Produto(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    esta_ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Veiculo(models.Model):
    numero_interno = models.CharField(max_length=50, blank=True, default="")
    placa = models.CharField(max_length=10, unique=True)
    capacidade = models.DecimalField(max_digits=10, decimal_places=2)  # m³ ou t
    tipo = models.CharField(max_length=50, blank=True, default="")
    marca = models.CharField(max_length=50, blank=True, default="")
    esta_ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["placa"]
        indexes = [
            models.Index(fields=["placa"]),
            models.Index(fields=["numero_interno"]),
        ]

    def __str__(self):
        return f"{self.placa} ({self.numero_interno})".strip()


class Movimentacao(models.Model):
    class Status(models.TextChoices):
        CONCLUIDO = "CONCLUIDO", "Concluído"
        PENDENTE_CANCELAMENTO = "PENDENTE_CANCELAMENTO", "Pendente de Cancelamento"
        CANCELADO = "CANCELADO", "Cancelado"

    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, related_name="movimentacoes")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name="movimentacoes")
    operador = models.ForeignKey(User, on_delete=models.PROTECT, related_name="movimentacoes")
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    data_hora_saida = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.CONCLUIDO)

    class Meta:
        ordering = ["-data_hora_saida"]

    def __str__(self):
        return f"{self.veiculo} - {self.produto} - {self.quantidade}"
