from django.contrib import admin
from .models import Produto, Veiculo, Movimentacao

# O decorator @admin.register é a forma moderna de registrar um model
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'esta_ativo')
    search_fields = ('nome',)
    list_filter = ('esta_ativo',)

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'marca', 'numero_interno', 'capacidade', 'esta_ativo')
    search_fields = ('placa', 'marca', 'numero_interno')
    list_filter = ('esta_ativo', 'marca', 'tipo')

@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'produto', 'quantidade', 'operador', 'data_hora_saida', 'status')
    search_fields = ('veiculo__placa', 'produto__nome', 'operador__username')
    list_filter = ('status', 'produto', 'data_hora_saida')
    # Para campos de data, o Django oferece uma hierarquia de navegação especial
    date_hierarchy = 'data_hora_saida'
    # Torna campos de chave estrangeira mais rápidos de carregar e pesquisar
    autocomplete_fields = ['veiculo', 'produto', 'operador']