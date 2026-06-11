from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from apps.usuarios.decorators import perfil_required
from .models import Veiculo, TipoVeiculo
from .forms import VeiculoForm


@login_required
def lista(request):
    qs = Veiculo.objects.select_related("secretaria", "marca", "modelo", "tipo_veiculo").all()

    q         = request.GET.get("q", "").strip()
    tipo_frota = request.GET.get("tipo_frota", "")
    secretaria = request.GET.get("secretaria", "")
    status     = request.GET.get("status", "")
    tipo_v     = request.GET.get("tipo_veiculo", "")

    if q:
        qs = qs.filter(
            Q(placa__icontains=q) | Q(marca__nome__icontains=q) |
            Q(modelo__nome__icontains=q) | Q(num_patrimonio__icontains=q) |
            Q(prefixo__icontains=q)
        )
    if tipo_frota:
        qs = qs.filter(tipo_frota=tipo_frota)
    if secretaria:
        qs = qs.filter(secretaria_id=secretaria)
    if status:
        qs = qs.filter(status=status)
    if tipo_v:
        qs = qs.filter(tipo_veiculo_id=tipo_v)

    from apps.usuarios.models import Secretaria
    contexto = {
        "veiculos":       qs,
        "total":          qs.count(),
        "total_proprios": qs.filter(tipo_frota="PROPRIO").count(),
        "total_locados":  qs.filter(tipo_frota="LOCADO").count(),
        "em_manutencao":  qs.filter(status="EM_MANUTENCAO").count(),
        "secretarias":    Secretaria.objects.filter(ativa=True).order_by("nome"),
        "tipo_frota_opts":   Veiculo.TipoFrota.choices,
        "status_opts":       Veiculo.Status.choices,
        "tipo_veiculo_opts": TipoVeiculo.objects.filter(ativo=True).values_list("id", "nome"),
        "f_q":          q,
        "f_tipo_frota": tipo_frota,
        "f_secretaria": secretaria,
        "f_status":     status,
        "f_tipo_v":     tipo_v,
    }
    return render(request, "veiculos/lista.html", contexto)


@login_required
def detalhe(request, pk):
    v = get_object_or_404(Veiculo.objects.select_related("secretaria"), pk=pk)
    foto_items = [
        ("Frente",        v.foto_frente),
        ("Lateral Esq.",  v.foto_lateral_e),
        ("Lateral Dir.",  v.foto_lateral_d),
        ("Traseira",      v.foto_traseira),
        ("Hodômetro",     v.foto_hodometro),
    ]
    equipamentos = [
        ("Ar-condicionado",           v.eq_ar_condicionado),
        ("Direção hidráulica/elétrica", v.eq_direcao_hidraulica),
        ("Vidros elétricos",          v.eq_vidros_eletricos),
        ("Som / Multimídia",          v.eq_som_multimidia),
        ("Rádio comunicador",         v.eq_radio_comunicador),
        ("Rodas de liga leve",        v.eq_rodas_liga_leve),
        ("Câmera de ré",              v.eq_camera_re),
        ("Sensor de estacionamento",  v.eq_sensor_estac),
    ]
    return render(request, "veiculos/detalhe.html", {
        "veiculo": v,
        "foto_items": foto_items,
        "equipamentos": equipamentos,
    })


@login_required
@perfil_required("ADMIN", "GESTOR")
def criar(request):
    if request.method == "POST":
        form = VeiculoForm(request.POST, request.FILES)
        if form.is_valid():
            v = form.save()
            messages.success(request, f"Veículo {v.placa} cadastrado com sucesso.")
            return redirect("veiculos:detalhe", pk=v.pk)
    else:
        form = VeiculoForm()
    return render(request, "veiculos/form.html", {"form": form, "titulo": "Cadastrar Veículo"})


@login_required
@perfil_required("ADMIN", "GESTOR")
def editar(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    if request.method == "POST":
        form = VeiculoForm(request.POST, request.FILES, instance=veiculo)
        if form.is_valid():
            form.save()
            messages.success(request, f"Veículo {veiculo.placa} atualizado.")
            return redirect("veiculos:detalhe", pk=pk)
    else:
        form = VeiculoForm(instance=veiculo)
    return render(request, "veiculos/form.html", {
        "form": form, "titulo": f"Editar — {veiculo.placa}", "veiculo": veiculo,
    })


@login_required
@perfil_required("ADMIN", "GESTOR")
def inativar(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    if request.method == "POST":
        novo_status = "INATIVO" if veiculo.status != "INATIVO" else "DISPONIVEL"
        veiculo.status = novo_status
        veiculo.save(update_fields=["status", "atualizado_em"])
        label = "inativado" if novo_status == "INATIVO" else "reativado"
        messages.success(request, f"Veículo {veiculo.placa} {label}.")
        return redirect("veiculos:detalhe", pk=pk)
    return render(request, "veiculos/confirmar_inativar.html", {"veiculo": veiculo})

