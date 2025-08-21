import csv
from django.http import HttpResponse
from django.db.models import Sum, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Movimentacao

class RelatorioMovimentacoes(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        qs = Movimentacao.objects.select_related("veiculo", "produto", "operador")
        de = request.GET.get("de")
        ate = request.GET.get("ate")
        placa = request.GET.get("placa")
        produto = request.GET.get("produto")
        if de:
            qs = qs.filter(data_hora_saida__gte=de)
        if ate:
            qs = qs.filter(data_hora_saida__lte=ate)
        if placa:
            qs = qs.filter(veiculo__placa__icontains=placa)
        if produto:
            qs = qs.filter(produto_id=produto)
        if not request.user.is_staff:
            qs = qs.filter(operador=request.user)
        return qs

    def get(self, request):
        fmt = request.GET.get("format", "json")
        qs = self.get_queryset(request)

        total_geral = qs.aggregate(total=Sum("quantidade"))["total"] or 0
        por_produto = qs.values("produto__nome").annotate(total=Sum("quantidade"), registros=Count("id")).order_by("-total")
        por_veiculo = qs.values("veiculo__placa").annotate(total=Sum("quantidade"), registros=Count("id")).order_by("-total")
        por_dia = qs.extra(select={"dia": "date(data_hora_saida)"}).values("dia").annotate(total=Sum("quantidade"), registros=Count("id")).order_by("dia")

        if fmt == "csv":
            resp = HttpResponse(content_type="text/csv")
            resp["Content-Disposition"] = 'attachment; filename="relatorio_movimentacoes.csv"'
            w = csv.writer(resp)
            w.writerow(["=== POR PRODUTO ==="])
            w.writerow(["Produto", "Total", "Registros"])
            for r in por_produto: w.writerow([r["produto__nome"], r["total"], r["registros"]])
            w.writerow([])
            w.writerow(["=== POR VEÍCULO ==="])
            w.writerow(["Placa", "Total", "Registros"])
            for r in por_veiculo: w.writerow([r["veiculo__placa"], r["total"], r["registros"]])
            w.writerow([])
            w.writerow(["=== POR DIA ==="])
            w.writerow(["Dia", "Total", "Registros"])
            for r in por_dia: w.writerow([r["dia"], r["total"], r["registros"]])
            w.writerow([])
            w.writerow(["TOTAL GERAL", total_geral])
            return resp

        return Response({
            "total_geral": total_geral,
            "por_produto": list(por_produto),
            "por_veiculo": list(por_veiculo),
            "por_dia": list(por_dia),
        })
