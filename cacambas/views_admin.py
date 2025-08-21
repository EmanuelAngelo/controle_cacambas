from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .permissions import IsAdmin
from .models import Veiculo

import csv, io

class VeiculoImportCSV(APIView):
    permission_classes = [IsAdmin]
    parser_classes = [MultiPartParser]

    def post(self, request):
        if "file" not in request.FILES:
            return Response({"detail": "Envie um arquivo CSV em 'file'."}, status=400)
        f = request.FILES["file"]
        data = io.TextIOWrapper(f.file, encoding="utf-8")
        reader = csv.DictReader(data)
        created, updated = 0, 0
        for row in reader:
            placa = row.get("placa", "").strip().upper()
            if not placa:
                continue
            obj, exists = Veiculo.objects.update_or_create(
                placa=placa,
                defaults={
                    "numero_interno": (row.get("numero_interno") or "").strip(),
                    "capacidade": row.get("capacidade") or 0,
                    "tipo": (row.get("tipo") or "").strip(),
                    "marca": (row.get("marca") or "").strip(),
                    "esta_ativo": str(row.get("esta_ativo", "true")).lower() in ("1", "true", "t", "yes", "y"),
                },
            )
            created += 0 if exists else 1
            updated += 1 if exists else 0
        return Response({"importados": created, "atualizados": updated})
