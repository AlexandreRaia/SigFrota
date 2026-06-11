from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Sum
from django.utils import timezone

from apps.usuarios.decorators import perfil_required
from .models import Multa, TipoMulta
from .forms import MultaForm, TipoMultaForm


# ── Multas ───────────────────────────────────────────────────────────────────

@login_required
def lista(request):
    qs = Multa.objects.select_related("condutor", "tipo_infracao").all()

    placa    = request.GET.get("placa", "").strip()
    condutor = request.GET.get("condutor", "").strip()
    status   = request.GET.get("status", "")
    de       = request.GET.get("de", "")
    ate      = request.GET.get("ate", "")

    if placa:
        qs = qs.filter(placa__icontains=placa)
    if condutor:
        qs = qs.filter(
            Q(condutor__nome__icontains=condutor) |
            Q(condutor__prontuario__icontains=condutor)
        )
    if status:
        qs = qs.filter(status=status)
    if de:
        qs = qs.filter(data_infracao__gte=de)
    if ate:
        qs = qs.filter(data_infracao__lte=ate)

    hoje      = timezone.now().date()
    sete_dias = hoje + timezone.timedelta(days=7)

    total_pendentes   = qs.filter(status="PENDENTE").count()
    valor_pendente    = qs.filter(status="PENDENTE").aggregate(t=Sum("valor"))["t"] or 0
    vencendo_em_breve = qs.filter(status="PENDENTE", data_vencimento__range=(hoje, sete_dias)).count()

    contexto = {
        "multas":            qs,
        "total_pendentes":   total_pendentes,
        "valor_pendente":    valor_pendente,
        "vencendo_em_breve": vencendo_em_breve,
        "status_opts":       Multa.Status.choices,
        "f_placa":    placa,
        "f_condutor": condutor,
        "f_status":   status,
        "f_de":       de,
        "f_ate":      ate,
    }
    return render(request, "multas/lista.html", contexto)


@login_required
def detalhe(request, pk):
    multa = get_object_or_404(Multa.objects.select_related("condutor", "tipo_infracao"), pk=pk)
    return render(request, "multas/detalhe.html", {"multa": multa})


@login_required
@perfil_required("ADMIN", "GESTOR")
def criar(request):
    condutor_inicial = request.GET.get("condutor")
    if request.method == "POST":
        form = MultaForm(request.POST, request.FILES)
        if form.is_valid():
            multa = form.save()
            messages.success(request, f"Multa registrada: {multa}.")
            return redirect("multas:detalhe", pk=multa.pk)
    else:
        form = MultaForm(condutor_inicial=condutor_inicial)
    return render(request, "multas/form.html", {"form": form, "titulo": "Registrar Multa"})


@login_required
@perfil_required("ADMIN", "GESTOR")
def editar(request, pk):
    multa = get_object_or_404(Multa, pk=pk)
    if request.method == "POST":
        form = MultaForm(request.POST, request.FILES, instance=multa)
        if form.is_valid():
            form.save()
            messages.success(request, "Multa atualizada.")
            return redirect("multas:detalhe", pk=pk)
    else:
        form = MultaForm(instance=multa)
    return render(request, "multas/form.html", {
        "form": form, "titulo": f"Editar Multa — {multa.placa}", "multa": multa,
    })


@login_required
@perfil_required("ADMIN")
def excluir(request, pk):
    multa = get_object_or_404(Multa, pk=pk)
    if request.method == "POST":
        desc = str(multa)
        multa.delete()
        messages.success(request, f"Multa removida: {desc}.")
        return redirect("multas:lista")
    return render(request, "multas/confirmar_excluir.html", {"multa": multa})


# ── Tipos de Multa (CRUD) ─────────────────────────────────────────────────────

@login_required
@perfil_required("ADMIN", "GESTOR")
def tipos_lista(request):
    tipos = TipoMulta.objects.all()
    form  = TipoMultaForm()
    if request.method == "POST":
        form = TipoMultaForm(request.POST)
        if form.is_valid():
            tipo = form.save()
            messages.success(request, f"Tipo '{tipo}' cadastrado.")
            return redirect("multas:tipos_lista")
    return render(request, "multas/tipos.html", {"tipos": tipos, "form": form})


@login_required
@perfil_required("ADMIN", "GESTOR")
def tipos_editar(request, pk):
    tipo = get_object_or_404(TipoMulta, pk=pk)
    if request.method == "POST":
        form = TipoMultaForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            messages.success(request, f"Tipo '{tipo}' atualizado.")
            return redirect("multas:tipos_lista")
    else:
        form = TipoMultaForm(instance=tipo)
    return render(request, "multas/tipo_form.html", {"form": form, "tipo": tipo})


@login_required
@perfil_required("ADMIN")
def tipos_excluir(request, pk):
    tipo = get_object_or_404(TipoMulta, pk=pk)
    if request.method == "POST":
        if tipo.multas.exists():
            messages.error(request, "Não é possível excluir: existem multas vinculadas a este tipo.")
        else:
            nome = str(tipo)
            tipo.delete()
            messages.success(request, f"Tipo '{nome}' removido.")
        return redirect("multas:tipos_lista")
    return render(request, "multas/tipo_confirmar_excluir.html", {"tipo": tipo})



@login_required
def lista(request):
    qs = Multa.objects.select_related("condutor").all()

    # Filtros
    placa    = request.GET.get("placa", "").strip()
    condutor = request.GET.get("condutor", "").strip()
    status   = request.GET.get("status", "")
    de       = request.GET.get("de", "")
    ate      = request.GET.get("ate", "")

    if placa:
        qs = qs.filter(placa__icontains=placa)
    if condutor:
        qs = qs.filter(
            Q(condutor__nome__icontains=condutor) |
            Q(condutor__prontuario__icontains=condutor)
        )
    if status:
        qs = qs.filter(status=status)
    if de:
        qs = qs.filter(data_infracao__gte=de)
    if ate:
        qs = qs.filter(data_infracao__lte=ate)

    hoje = timezone.now().date()
    sete_dias = hoje + timezone.timedelta(days=7)

    # KPIs
    total_pendentes   = qs.filter(status="PENDENTE").count()
    valor_pendente    = qs.filter(status="PENDENTE").aggregate(t=Sum("valor"))["t"] or 0
    vencendo_em_breve = qs.filter(
        status="PENDENTE", data_vencimento__range=(hoje, sete_dias)
    ).count()

    contexto = {
        "multas":           qs,
        "total_pendentes":  total_pendentes,
        "valor_pendente":   valor_pendente,
        "vencendo_em_breve": vencendo_em_breve,
        "status_opts":      Multa.Status.choices,
        # filtros ativos
        "f_placa":    placa,
        "f_condutor": condutor,
        "f_status":   status,
        "f_de":       de,
        "f_ate":      ate,
    }
    return render(request, "multas/lista.html", contexto)


@login_required
def detalhe(request, pk):
    multa = get_object_or_404(Multa.objects.select_related("condutor"), pk=pk)
    return render(request, "multas/detalhe.html", {"multa": multa})


@login_required
@perfil_required("ADMIN", "GESTOR")
def criar(request):
    condutor_inicial = request.GET.get("condutor")
    if request.method == "POST":
        form = MultaForm(request.POST, request.FILES)
        if form.is_valid():
            multa = form.save()
            messages.success(request, f"Multa registrada: {multa.placa} — {multa.get_tipo_infracao_display()}.")
            return redirect("multas:detalhe", pk=multa.pk)
    else:
        form = MultaForm(condutor_inicial=condutor_inicial)
    return render(request, "multas/form.html", {"form": form, "titulo": "Registrar Multa"})


@login_required
@perfil_required("ADMIN", "GESTOR")
def editar(request, pk):
    multa = get_object_or_404(Multa, pk=pk)
    if request.method == "POST":
        form = MultaForm(request.POST, request.FILES, instance=multa)
        if form.is_valid():
            form.save()
            messages.success(request, "Multa atualizada.")
            return redirect("multas:detalhe", pk=pk)
    else:
        form = MultaForm(instance=multa)
    return render(request, "multas/form.html", {
        "form": form, "titulo": f"Editar Multa — {multa.placa}", "multa": multa,
    })


@login_required
@perfil_required("ADMIN")
def excluir(request, pk):
    multa = get_object_or_404(Multa, pk=pk)
    if request.method == "POST":
        desc = str(multa)
        multa.delete()
        messages.success(request, f"Multa removida: {desc}.")
        return redirect("multas:lista")
    return render(request, "multas/confirmar_excluir.html", {"multa": multa})

