from django.db import models
from django.conf import settings
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
    # --- MUDANÇA AQUI: NOVOS STATUS ---
    class Status(models.TextChoices):
        A_ENTREGAR = 'A ENTREGAR', 'A entregar'
        EM_ROTA = 'EM ROTA', 'Em rota'
        CONCLUIDO = 'CONCLUIDO', 'Concluído'
        PENDENTE_CANCELAMENTO = 'PENDENTE', 'Pendente Cancelamento'
        CANCELADO = 'CANCELADO', 'Cancelado'

    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, related_name='movimentacoes', verbose_name="Veículo")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='movimentacoes', verbose_name="Produto")
    operador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='movimentacoes', verbose_name="Operador")
    quantidade = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Quantidade (m³)")
    data_hora_saida = models.DateTimeField(auto_now_add=True, verbose_name="Data e Hora da Saída")
    
    # --- MUDANÇA AQUI: NOVO STATUS PADRÃO ---
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.A_ENTREGAR, # O padrão agora é 'A entregar'
        verbose_name="Status"
    )

    class Meta:
        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"
        ordering = ['-data_hora_saida']

    def __str__(self):
        return f"Saída de {self.veiculo.placa} ({self.produto.nome}) em {self.data_hora_saida.strftime('%d/%m/%Y %H:%M')}"
