from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from apps.usuarios.decorators import perfil_required
from .models import Condutor, Acidente, Infracao, Qualificacao, Penalidade, FolgaFerias
from .forms import CondutorForm, AcidenteForm, InfracaoForm, QualificacaoForm, PenalidadeForm, FolgaFeriasForm
from apps.multas.models import Multa


@login_required
def lista(request):
    """Lista de condutores com filtros de busca."""
    qs = Condutor.objects.select_related("secretaria").all()

    busca      = request.GET.get("q", "").strip()
    status     = request.GET.get("status", "")
    secretaria = request.GET.get("secretaria", "")
    categoria  = request.GET.get("categoria", "")

    if busca:
        qs = qs.filter(Q(nome__icontains=busca) | Q(cpf__icontains=busca) | Q(prontuario__icontains=busca))
    if status:
        qs = qs.filter(status=status)
    if secretaria:
        qs = qs.filter(secretaria_id=secretaria)
    if categoria:
        qs = qs.filter(cnh_categoria=categoria)

    from apps.usuarios.models import Secretaria as Sec
    contexto = {
        "condutores":  qs,
        "total":       qs.count(),
        "secretarias": Sec.objects.filter(ativa=True).order_by("sigla"),
        "categorias":  Condutor.CategoriaCNH.choices,
        "status_opts": Condutor.Status.choices,
        "busca":       busca,
        "status_sel":  status,
        "sec_sel":     secretaria,
        "cat_sel":     categoria,
    }
    return render(request, "condutores/lista.html", contexto)


@login_required
def detalhe(request, pk):
    """Ficha completa do condutor com abas de histórico."""
    condutor = get_object_or_404(Condutor.objects.select_related("secretaria"), pk=pk)

    qualificacoes = list(condutor.qualificacoes.all())
    penalidades   = list(condutor.penalidades.all())
    folgas        = list(condutor.folgas.all())

    contexto = {
        "condutor":  condutor,
        "acidentes": condutor.acidentes.all(),
        "multas_condutor": Multa.objects.filter(condutor=condutor).order_by("-data_infracao"),
        # listas com formulário de edição embutido
        "qualificacoes_items": [(q, QualificacaoForm(instance=q, prefix=f"q{q.pk}")) for q in qualificacoes],
        "penalidades_items":   [(p, PenalidadeForm(instance=p, prefix=f"p{p.pk}")) for p in penalidades],
        "folgas_items":        [(f, FolgaFeriasForm(instance=f, prefix=f"f{f.pk}")) for f in folgas],
        # formulários de criação (sem prefixo)
        "form_acidente":   AcidenteForm(),
        "form_infracao":   InfracaoForm(),
        "form_qualif":     QualificacaoForm(),
        "form_penalidade": PenalidadeForm(),
        "form_folga":      FolgaFeriasForm(),
    }
    return render(request, "condutores/detalhe.html", contexto)


@login_required
@perfil_required("ADMIN", "GESTOR")
def criar(request):
    """Formulário de criação de novo condutor."""
    if request.method == "POST":
        form = CondutorForm(request.POST, request.FILES)
        if form.is_valid():
            condutor = form.save()
            messages.success(request, f"Condutor {condutor.nome} cadastrado com sucesso.")
            return redirect("condutores:detalhe", pk=condutor.pk)
    else:
        form = CondutorForm()
    return render(request, "condutores/form.html", {"form": form, "titulo": "Novo Condutor"})


@login_required
@perfil_required("ADMIN", "GESTOR")
def editar(request, pk):
    """Edição de um condutor existente."""
    condutor = get_object_or_404(Condutor, pk=pk)
    if request.method == "POST":
        form = CondutorForm(request.POST, request.FILES, instance=condutor)
        if form.is_valid():
            form.save()
            messages.success(request, "Dados atualizados com sucesso.")
            return redirect("condutores:detalhe", pk=pk)
    else:
        form = CondutorForm(instance=condutor)
    return render(request, "condutores/form.html", {
        "form": form, "titulo": f"Editar — {condutor.nome}", "condutor": condutor,
    })


@login_required
@perfil_required("ADMIN")
def inativar(request, pk):
    """Soft-delete: marca condutor como INATIVO."""
    condutor = get_object_or_404(Condutor, pk=pk)
    if request.method == "POST":
        condutor.status = Condutor.Status.INATIVO
        condutor.save(update_fields=["status"])
        messages.warning(request, f"Condutor {condutor.nome} marcado como inativo.")
        return redirect("condutores:lista")
    return render(request, "condutores/confirmar_inativar.html", {"condutor": condutor})


@login_required
@perfil_required("ADMIN")
def suspender(request, pk):
    """Suspende o condutor."""
    condutor = get_object_or_404(Condutor, pk=pk)
    if request.method == "POST":
        condutor.status = Condutor.Status.SUSPENSO
        condutor.save(update_fields=["status"])
        messages.warning(request, f"Condutor {condutor.nome} suspenso.")
    return redirect("condutores:detalhe", pk=pk)


# ── Histórico ───────────────────────────────────────────────────────────────

@login_required
@perfil_required("ADMIN", "GESTOR")
def add_acidente(request, pk):
    condutor = get_object_or_404(Condutor, pk=pk)
    if request.method == "POST":
        form = AcidenteForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.condutor = condutor
            obj.save()
            messages.success(request, "Acidente registrado.")
    return redirect("condutores:detalhe", pk=pk)


@login_required
@perfil_required("ADMIN", "GESTOR")
def add_infracao(request, pk):
    condutor = get_object_or_404(Condutor, pk=pk)
    if request.method == "POST":
        form = InfracaoForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.condutor = condutor
            obj.save()
            messages.success(request, "Infração registrada.")
    return redirect("condutores:detalhe", pk=pk)


@login_required
@perfil_required("ADMIN", "GESTOR")
def add_qualificacao(request, pk):
    condutor = get_object_or_404(Condutor, pk=pk)
    if request.method == "POST":
        form = QualificacaoForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.condutor = condutor
            obj.save()
            messages.success(request, "Qualificação registrada.")
    return redirect("condutores:detalhe", pk=pk)


@login_required
@perfil_required("ADMIN", "GESTOR")
def add_penalidade(request, pk):
    condutor = get_object_or_404(Condutor, pk=pk)
    if request.method == "POST":
        form = PenalidadeForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.condutor = condutor
            obj.save()
            messages.success(request, "Penalidade registrada.")
    return redirect("condutores:detalhe", pk=pk)


@login_required
@perfil_required("ADMIN", "GESTOR")
def add_folga(request, pk):
    condutor = get_object_or_404(Condutor, pk=pk)
    if request.method == "POST":
        form = FolgaFeriasForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.condutor = condutor
            obj.save()
            messages.success(request, "Férias/Folga registrada.")
    return redirect("condutores:detalhe", pk=pk)


# ── Editar / Excluir Qualificação ────────────────────────────────────────────

@login_required
@perfil_required("ADMIN", "GESTOR")
def edit_qualificacao(request, pk, item_pk):
    condutor = get_object_or_404(Condutor, pk=pk)
    obj = get_object_or_404(Qualificacao, pk=item_pk, condutor=condutor)
    if request.method == "POST":
        form = QualificacaoForm(request.POST, instance=obj, prefix=f"q{item_pk}")
        if form.is_valid():
            form.save()
            messages.success(request, "Qualificação atualizada.")
        else:
            messages.error(request, "Erro ao atualizar qualificação.")
    return redirect("condutores:detalhe", pk=pk)


@login_required
@perfil_required("ADMIN", "GESTOR")
def del_qualificacao(request, pk, item_pk):
    condutor = get_object_or_404(Condutor, pk=pk)
    obj = get_object_or_404(Qualificacao, pk=item_pk, condutor=condutor)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Qualificação removida.")
    return redirect("condutores:detalhe", pk=pk)


# ── Editar / Excluir Penalidade ──────────────────────────────────────────────

@login_required
@perfil_required("ADMIN", "GESTOR")
def edit_penalidade(request, pk, item_pk):
    condutor = get_object_or_404(Condutor, pk=pk)
    obj = get_object_or_404(Penalidade, pk=item_pk, condutor=condutor)
    if request.method == "POST":
        form = PenalidadeForm(request.POST, instance=obj, prefix=f"p{item_pk}")
        if form.is_valid():
            form.save()
            messages.success(request, "Penalidade atualizada.")
        else:
            messages.error(request, "Erro ao atualizar penalidade.")
    return redirect("condutores:detalhe", pk=pk)


@login_required
@perfil_required("ADMIN", "GESTOR")
def del_penalidade(request, pk, item_pk):
    condutor = get_object_or_404(Condutor, pk=pk)
    obj = get_object_or_404(Penalidade, pk=item_pk, condutor=condutor)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Penalidade removida.")
    return redirect("condutores:detalhe", pk=pk)


# ── Editar / Excluir Folga/Férias ────────────────────────────────────────────

@login_required
@perfil_required("ADMIN", "GESTOR")
def edit_folga(request, pk, item_pk):
    condutor = get_object_or_404(Condutor, pk=pk)
    obj = get_object_or_404(FolgaFerias, pk=item_pk, condutor=condutor)
    if request.method == "POST":
        form = FolgaFeriasForm(request.POST, instance=obj, prefix=f"f{item_pk}")
        if form.is_valid():
            form.save()
            messages.success(request, "Férias/Folga atualizada.")
        else:
            messages.error(request, "Erro ao atualizar registro.")
    return redirect("condutores:detalhe", pk=pk)


@login_required
@perfil_required("ADMIN", "GESTOR")
def del_folga(request, pk, item_pk):
    condutor = get_object_or_404(Condutor, pk=pk)
    obj = get_object_or_404(FolgaFerias, pk=item_pk, condutor=condutor)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Registro de férias/folga removido.")
    return redirect("condutores:detalhe", pk=pk)
