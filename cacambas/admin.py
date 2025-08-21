from django.contrib import admin
from .models import Produto, Veiculo, Movimentacao

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "esta_ativo")
    list_filter = ("esta_ativo",)
    search_fields = ("nome",)
    list_editable = ("esta_ativo",)

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ("id", "placa", "numero_interno", "capacidade", "tipo", "marca", "esta_ativo")
    list_filter = ("esta_ativo", "marca", "tipo")
    search_fields = ("placa", "numero_interno", "marca", "tipo")
    autocomplete_fields = ()
    list_editable = ("esta_ativo",)

@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ("id", "veiculo", "produto", "quantidade", "status", "operador", "data_hora_saida")
    list_filter = ("status", "produto", "veiculo__placa", "operador")
    search_fields = ("veiculo__placa", "produto__nome", "operador__username")
    date_hierarchy = "data_hora_saida"
    autocomplete_fields = ("veiculo", "produto", "operador")
