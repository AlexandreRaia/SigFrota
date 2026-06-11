from django.urls import path
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Modelo


@login_required
def modelos_por_marca(request):
    marca_id = request.GET.get("marca_id")
    if not marca_id:
        return JsonResponse([], safe=False)
    qs = Modelo.objects.filter(marca_id=marca_id, ativo=True).values("id", "nome", "tipo_veiculo_id")
    return JsonResponse(list(qs), safe=False)


urlpatterns = [
    path("modelos/", modelos_por_marca, name="api_modelos"),
]

