from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q, Count, Subquery, OuterRef, ExpressionWrapper, F, DurationField
from django.utils import timezone

from apps.usuarios.decorators import perfil_required
from apps.veiculos.models import Veiculo
from apps.chat.models import SMVMensagem, SMVMensagemLeitura
from .models import (
    SMV, SMVEtapa, SMVOrcamento, SMVAnexo,
    SMVChecklist, SMVNotaFiscal, SMVItemNF, SMVRecepcao,
    SMVDiagnosticoItem, SMVAprovacao,
)


# ── Lista ─────────────────────────────────────────────────────────────────────

@login_required
def lista(request):
    qs = SMV.objects.select_related(
        "veiculo", "veiculo__marca", "veiculo__modelo", "solicitante"
    ).order_by("-numero")

    q       = request.GET.get("q", "").strip()
    etapa   = request.GET.get("etapa", "")
    urgencia = request.GET.get("urgencia", "")

    if q:
        qs = qs.filter(
            Q(numero__icontains=q) |
            Q(veiculo__placa__icontains=q) |
            Q(veiculo__modelo__nome__icontains=q)
        )
    if etapa:
        qs = qs.filter(etapa=etapa)
    if urgencia:
        qs = qs.filter(urgencia=urgencia)

    # Badge: total de mensagens não lidas por SMV para o usuário logado
    lidas_ids = SMVMensagemLeitura.objects.filter(
        usuario=request.user, mensagem__smv=OuterRef("pk")
    ).values("mensagem")
    nao_lidas_sub = SMVMensagem.objects.filter(
        smv=OuterRef("pk")
    ).exclude(pk__in=Subquery(lidas_ids)).values("smv").annotate(c=Count("pk")).values("c")

    qs = qs.annotate(msgs_nao_lidas=Subquery(nao_lidas_sub[:1]))

    # Dias que o veículo está parado (desde a solicitação)
    agora = timezone.now()
    qs = qs.annotate(
        dias_parado=ExpressionWrapper(
            agora - F('dt_solicitacao'),
            output_field=DurationField()
        )
    )

    ctx = {
        "smvs":          qs,
        "total":         SMV.objects.count(),
        "em_aberto":     SMV.objects.exclude(etapa=SMV.Etapa.FINALIZADO).count(),
        "finalizadas":   SMV.objects.filter(etapa=SMV.Etapa.FINALIZADO).count(),
        "etapa_opts":    SMV.Etapa.choices,
        "urgencia_opts": SMV.Urgencia.choices,
        "f_q":       q,
        "f_etapa":   etapa,
        "f_urgencia": urgencia,
    }
    return render(request, "manutencao/lista.html", ctx)


# ── Detalhe ───────────────────────────────────────────────────────────────────

@login_required
def detalhe(request, pk):
    smv = get_object_or_404(
        SMV.objects.select_related(
            "veiculo", "veiculo__marca", "veiculo__modelo",
            "veiculo__secretaria", "solicitante"
        ),
        pk=pk,
    )
    historico     = smv.historico_etapas.select_related("responsavel").all()
    orcamentos    = smv.orcamentos.select_related("criado_por").all()
    notas_fiscais = smv.notas_fiscais.prefetch_related("itens").all()
    checklists    = smv.checklists.select_related("responsavel").all()
    anexos        = smv.anexos.select_related("enviado_por").all()
    mensagens     = smv.mensagens.select_related("autor").all()

    # Marcar mensagens como lidas
    ids_nao_lidas = mensagens.exclude(
        pk__in=SMVMensagemLeitura.objects.filter(usuario=request.user).values("mensagem")
    ).values_list("pk", flat=True)
    for mid in ids_nao_lidas:
        SMVMensagemLeitura.objects.get_or_create(
            mensagem_id=mid, usuario=request.user
        )

    # Próxima etapa possível
    ordem_etapas = [e[0] for e in SMV.Etapa.choices]
    idx_atual = ordem_etapas.index(smv.etapa) if smv.etapa in ordem_etapas else -1
    proxima_etapa = ordem_etapas[idx_atual + 1] if idx_atual + 1 < len(ordem_etapas) else None

    pending_aguard_aprova = orcamentos.filter(status=SMVOrcamento.Status.AGUARD_APROVA).exists()

    ctx = {
        "smv":           smv,
        "historico":     historico,
        "orcamentos":    orcamentos,
        "notas_fiscais": notas_fiscais,
        "checklists_entrada": checklists.filter(tipo=SMVChecklist.Tipo.ENTRADA),
        "checklists_saida":   checklists.filter(tipo=SMVChecklist.Tipo.SAIDA),
        "anexos":        anexos,
        "mensagens":     mensagens,
        "itens_diagnostico": smv.itens_diagnostico.all(),
        "proxima_etapa": proxima_etapa,
        "proxima_etapa_label": dict(SMV.Etapa.choices).get(proxima_etapa, ""),
        "etapas_completas": ordem_etapas[:idx_atual + 1],
        "todas_etapas":  SMV.Etapa.choices,
        "pending_aguard_aprova": pending_aguard_aprova,
    }
    return render(request, "manutencao/detalhe.html", ctx)


# ── Criar SMV ─────────────────────────────────────────────────────────────────

@login_required
@perfil_required("ADMIN", "GESTOR")
def criar(request):
    veiculos = Veiculo.objects.select_related("marca", "modelo").filter(
        status=Veiculo.Status.DISPONIVEL
    ).order_by("placa")

    if request.method == "POST":
        veiculo_id = request.POST.get("veiculo")
        descricao  = request.POST.get("descricao_problema", "").strip()
        km_entrada = request.POST.get("km_entrada") or None

        if not veiculo_id or not descricao:
            messages.error(request, "Veículo e descrição são obrigatórios.")
        else:
            veiculo = get_object_or_404(Veiculo, pk=veiculo_id)
            smv = SMV.objects.create(
                veiculo=veiculo,
                solicitante=request.user,
                descricao_problema=descricao,
                km_entrada=km_entrada,
            )
            # Registra etapa inicial
            SMVEtapa.objects.create(
                smv=smv,
                etapa_de="",
                etapa_para=SMV.Etapa.SOLICITACAO,
                responsavel=request.user,
                observacao="SMV aberta.",
            )
            # Atualiza status do veículo
            veiculo.status = Veiculo.Status.EM_MANUTENCAO
            veiculo.save(update_fields=["status"])

            messages.success(request, f"SMV {smv.numero} criada com sucesso.")
            return redirect("manutencao:detalhe", pk=smv.pk)

    return render(request, "manutencao/form.html", {"veiculos": veiculos, "urgencia_opts": SMV.Urgencia.choices})


# ── Avançar etapa ─────────────────────────────────────────────────────────────

@login_required
@perfil_required("ADMIN", "GESTOR", "OFICINA", "AUDITOR")
def avancar_etapa(request, pk):
    smv = get_object_or_404(SMV, pk=pk)

    if request.method == "POST":
        nova_etapa  = request.POST.get("nova_etapa")
        observacao  = request.POST.get("observacao", "").strip()
        etapa_atual = smv.etapa

        SMVEtapa.objects.create(
            smv=smv,
            etapa_de=etapa_atual,
            etapa_para=nova_etapa,
            responsavel=request.user,
            observacao=observacao,
        )
        smv.etapa = nova_etapa

        # Timestamps automáticos
        agora = timezone.now()
        if nova_etapa == SMV.Etapa.RECEPCAO:
            smv.dt_recepcao = agora
        elif nova_etapa == SMV.Etapa.DIAGNOSTICO:
            smv.dt_diagnostico = agora
        elif nova_etapa == SMV.Etapa.EXECUCAO:
            smv.dt_inicio_exec = agora
        elif nova_etapa == SMV.Etapa.RETIRADA:
            smv.dt_retirada = agora
        elif nova_etapa == SMV.Etapa.FINALIZADO:
            smv.dt_finalizacao = agora
            smv.veiculo.status = Veiculo.Status.DISPONIVEL
            smv.veiculo.save(update_fields=["status"])

        smv.save()
        messages.success(request, f"Etapa avançada para {smv.get_etapa_display()}.")

    return redirect("manutencao:detalhe", pk=smv.pk)


# ── Enviar mensagem (chat) ─────────────────────────────────────────────────────

@login_required
def enviar_mensagem(request, pk):
    smv = get_object_or_404(SMV, pk=pk)

    if request.method == "POST":
        texto = request.POST.get("texto", "").strip()
        anexo = request.FILES.get("anexo")

        if texto or anexo:
            msg = SMVMensagem.objects.create(
                smv=smv,
                etapa=smv.etapa,
                autor=request.user,
                texto=texto,
                anexo=anexo,
            )
            SMVMensagemLeitura.objects.get_or_create(mensagem=msg, usuario=request.user)

    return redirect("manutencao:detalhe", pk=smv.pk)

# ── Recepção do veículo ──────────────────────────────────────────────────────────────────

# Itens padrão do checklist de entrada
# tipo "ok"  → checkbox pré-marcado (presente / ausente)
# tipo "pneu" → radio Bom / Regular / Ruim
CHECKLIST_ENTRADA = [
    {"nome": "Macaco",               "key": "macaco",         "tipo": "ok"},
    {"nome": "Chave de roda",        "key": "chave_de_roda",  "tipo": "ok"},
    {"nome": "Triângulo",            "key": "triangulo",      "tipo": "ok"},
    {"nome": "Step / Estepe",        "key": "step_estepe",    "tipo": "ok"},
    {"nome": "Extintor",             "key": "extintor",       "tipo": "ok"},
    {"nome": "Lanternas / Faróis",   "key": "lanternas",      "tipo": "ok"},
    {"nome": "Retrovisores",         "key": "retrovisores",   "tipo": "ok"},
    {"nome": "Documentos no veículo","key": "documentos",     "tipo": "ok"},
    {"nome": "Pneu dianteiro esq.",  "key": "pneu_diant_esq", "tipo": "pneu"},
    {"nome": "Pneu dianteiro dir.",  "key": "pneu_diant_dir", "tipo": "pneu"},
    {"nome": "Pneu traseiro esq.",   "key": "pneu_tras_esq",  "tipo": "pneu"},
    {"nome": "Pneu traseiro dir.",   "key": "pneu_tras_dir",  "tipo": "pneu"},
]

@login_required
@perfil_required("ADMIN", "GESTOR", "OFICINA")
def recepcao(request, pk):
    smv = get_object_or_404(SMV, pk=pk)

    # Impede dupla recepção
    ja_recepcionado = hasattr(smv, 'recepcao')

    if request.method == "POST" and not ja_recepcionado:
        km      = request.POST.get("km_entrada") or smv.km_entrada
        nivel   = request.POST.get("nivel_combustivel")
        obs     = request.POST.get("observacoes", "").strip()

        # Salva recepção
        SMVRecepcao.objects.create(
            smv=smv,
            km_entrada=km,
            nivel_combustivel=nivel,
            observacoes=obs,
            responsavel=request.user,
        )
        # Atualiza km_entrada na SMV
        smv.km_entrada = km
        smv.save(update_fields=["km_entrada"])

        # Salva checklist
        for item in CHECKLIST_ENTRADA:
            key      = item["key"]
            obs_item = request.POST.get(f"obs_{key}", "")

            if item["tipo"] == "ok":
                # Checkbox: marcado → OK, desmarcado → RUIM
                condicao = (SMVChecklist.Condicao.OK
                            if request.POST.get(f"item_{key}")
                            else SMVChecklist.Condicao.RUIM)
            else:
                # Radio Bom/Regular/Ruim → mapeia para choices do modelo
                val_map = {"BOM": SMVChecklist.Condicao.OK,
                           "REGULAR": SMVChecklist.Condicao.REGULAR,
                           "RUIM": SMVChecklist.Condicao.RUIM}
                condicao = val_map.get(request.POST.get(f"item_{key}", "BOM"),
                                       SMVChecklist.Condicao.OK)

            SMVChecklist.objects.create(
                smv=smv,
                tipo=SMVChecklist.Tipo.ENTRADA,
                item=item["nome"],
                condicao=condicao,
                observacao=obs_item,
                responsavel=request.user,
            )

        # Avança etapa para Recepção se ainda estiver em Solicitação
        if smv.etapa == SMV.Etapa.SOLICITACAO:
            SMVEtapa.objects.create(
                smv=smv, etapa_de=SMV.Etapa.SOLICITACAO,
                etapa_para=SMV.Etapa.RECEPCAO,
                responsavel=request.user,
                observacao="Veículo recepcionado na oficina.",
            )
            smv.etapa = SMV.Etapa.RECEPCAO
            smv.dt_recepcao = timezone.now()
            smv.save()

        messages.success(request, "Recepção registrada com sucesso.")
        return redirect("manutencao:detalhe", pk=smv.pk)

    ctx = {
        "smv": smv,
        "ja_recepcionado": ja_recepcionado,
        "acessorios": [i for i in CHECKLIST_ENTRADA if i["tipo"] == "ok"],
        "pneus":      [i for i in CHECKLIST_ENTRADA if i["tipo"] == "pneu"],
        "nivel_opts": SMVRecepcao.NivelCombustivel.choices,
    }
    return render(request, "manutencao/recepcao.html", ctx)


# ── Diagnóstico ───────────────────────────────────────────────────────────────

TIPOS_SERVICO_CHOICES = [
    ("MECANICA",    "Mecânica"),
    ("ELETRICA",    "Elétrica"),
    ("FUNILARIA",   "Funilaria / Lataria"),
    ("HIDRAULICA",  "Hidráulica"),
    ("PNEUS",       "Pneus"),
    ("AR_COND",     "Ar-condicionado"),
    ("VIDROS",      "Vidros / Borrachas"),
    ("REVISAO",     "Revisão periódica"),
    ("OUTRO",       "Outro"),
]

@login_required
@perfil_required("ADMIN", "GESTOR", "OFICINA")
def diagnostico(request, pk):
    smv = get_object_or_404(SMV, pk=pk)

    if request.method == "POST":
        texto_diag  = request.POST.get("diagnostico", "").strip()
        tipos       = request.POST.getlist("tipos_servico")
        concluir    = request.POST.get("concluir") == "1"

        smv.diagnostico   = texto_diag
        smv.tipos_servico = ",".join(tipos)

        agora = timezone.now()

        # Avança para DIAGNOSTICO se ainda estiver em RECEPCAO
        if smv.etapa == SMV.Etapa.RECEPCAO:
            SMVEtapa.objects.create(
                smv=smv, etapa_de=SMV.Etapa.RECEPCAO,
                etapa_para=SMV.Etapa.DIAGNOSTICO,
                responsavel=request.user,
                observacao="Diagnóstico iniciado.",
            )
            smv.etapa = SMV.Etapa.DIAGNOSTICO
            smv.dt_diagnostico = agora

        # Se clicar em "Concluir → Solicitar Orçamento", avança para ORCAMENTO
        if concluir and smv.etapa == SMV.Etapa.DIAGNOSTICO:
            SMVEtapa.objects.create(
                smv=smv, etapa_de=SMV.Etapa.DIAGNOSTICO,
                etapa_para=SMV.Etapa.ORCAMENTO,
                responsavel=request.user,
                observacao="Diagnóstico concluído. Aguardando orçamento.",
            )
            smv.etapa = SMV.Etapa.ORCAMENTO

        smv.save()

        # ── Salva itens de diagnóstico (peças e serviços) ────────────────
        # O formulário envia listas paralelas: item_tipo[], item_desc[], item_qtd[], item_un[], item_obs[]
        # Apaga itens anteriores e recria (substituição completa na edição)
        smv.itens_diagnostico.all().delete()
        tipos_item = request.POST.getlist("item_tipo")
        descs      = request.POST.getlist("item_desc")
        qtds       = request.POST.getlist("item_qtd")
        uns        = request.POST.getlist("item_un")
        obs_items  = request.POST.getlist("item_obs")

        for i, desc in enumerate(descs):
            desc = desc.strip()
            if not desc:
                continue
            SMVDiagnosticoItem.objects.create(
                smv=smv,
                tipo=tipos_item[i] if i < len(tipos_item) else SMVDiagnosticoItem.Tipo.PECA,
                descricao=desc,
                quantidade=qtds[i] if i < len(qtds) and qtds[i] else 1,
                unidade=uns[i] if i < len(uns) and uns[i] else "pç",
                observacao=obs_items[i] if i < len(obs_items) else "",
                criado_por=request.user,
            )

        # ── Salva fotos/laudos ───────────────────────────────────────────
        for arquivo in request.FILES.getlist("fotos"):
            SMVAnexo.objects.create(
                smv=smv,
                etapa=smv.etapa,
                tipo=SMVAnexo.TipoAnexo.LAUDO,
                descricao="Foto/laudo do diagnóstico",
                arquivo=arquivo,
                enviado_por=request.user,
            )

        msg = "Diagnóstico concluído e SMV avançada para Orçamento." if concluir else "Diagnóstico salvo."
        messages.success(request, msg)
        return redirect("manutencao:detalhe", pk=smv.pk)

    tipos_atuais = smv.tipos_servico.split(",") if smv.tipos_servico else []
    ctx = {
        "smv":              smv,
        "tipos_choices":    TIPOS_SERVICO_CHOICES,
        "tipos_atuais":     tipos_atuais,
        "pode_concluir":    smv.etapa in (SMV.Etapa.RECEPCAO, SMV.Etapa.DIAGNOSTICO),
        "anexos_diag":      smv.anexos.filter(etapa=SMV.Etapa.DIAGNOSTICO),
        "itens_diagnostico": smv.itens_diagnostico.all(),
    }
    return render(request, "manutencao/diagnostico.html", ctx)


# ── Orçamento ─────────────────────────────────────────────────────────────────

@login_required
@perfil_required("ADMIN", "GESTOR", "OFICINA")
def orcamento(request, pk):
    smv = get_object_or_404(SMV, pk=pk)
    # Permite adicionar nova versão mesmo quando em APROVACAO (renegociação após recusa)
    orcamentos = smv.orcamentos.order_by("versao")

    if request.method == "POST":
        fornecedor      = request.POST.get("fornecedor", "").strip()
        cnpj            = request.POST.get("cnpj_fornecedor", "").strip()
        from decimal import Decimal, InvalidOperation
        try:
            valor_pecas = Decimal(request.POST.get("valor_pecas") or "0")
        except InvalidOperation:
            valor_pecas = Decimal("0")
        try:
            valor_mo = Decimal(request.POST.get("valor_mo") or "0")
        except InvalidOperation:
            valor_mo = Decimal("0")
        observacoes     = request.POST.get("observacoes", "").strip()
        arquivo_pdf     = request.FILES.get("arquivo_pdf")
        submeter        = request.POST.get("submeter") == "1"   # botão "Submeter para aprovação"

        if not fornecedor:
            messages.error(request, "Informe o nome do fornecedor.")
        else:
            orc = SMVOrcamento.objects.create(
                smv=smv,
                fornecedor=fornecedor,
                cnpj_fornecedor=cnpj,
                valor_pecas=valor_pecas,
                valor_mo=valor_mo,
                arquivo_pdf=arquivo_pdf,
                observacoes=observacoes,
                status=SMVOrcamento.Status.AGUARD_APROVA if submeter else SMVOrcamento.Status.EM_NEGOCIACAO,
                criado_por=request.user,
            )

            if submeter:
                # Avança SMV para APROVACAO (seja vindo de ORCAMENTO ou voltando de APROVACAO após recusa)
                if smv.etapa in (SMV.Etapa.ORCAMENTO, SMV.Etapa.APROVACAO):
                    SMVEtapa.objects.create(
                        smv=smv, etapa_de=smv.etapa,
                        etapa_para=SMV.Etapa.APROVACAO,
                        responsavel=request.user,
                        observacao=f"Orçamento v{orc.versao} submetido para aprovação. Fornecedor: {fornecedor}. Total: R$ {orc.valor_total:.2f}",
                    )
                    smv.etapa = SMV.Etapa.APROVACAO
                    smv.save()
                messages.success(request, f"Orçamento v{orc.versao} submetido para aprovação.")
            else:
                messages.success(request, f"Orçamento v{orc.versao} salvo como rascunho.")

            return redirect("manutencao:detalhe", pk=smv.pk)

    ctx = {
        "smv":             smv,
        "orcamentos":      orcamentos,
        "ultimo_orcamento": orcamentos.last(),
        "itens_diag":      smv.itens_diagnostico.all(),
    }
    return render(request, "manutencao/orcamento.html", ctx)


# ── Recusar orçamento e retornar para negociação ──────────────────────────────

@login_required
@perfil_required("ADMIN", "GESTOR")
def recusar_orcamento(request, pk, orc_pk):
    smv = get_object_or_404(SMV, pk=pk)
    orc = get_object_or_404(SMVOrcamento, pk=orc_pk, smv=smv)

    if request.method == "POST":
        motivo = request.POST.get("motivo", "").strip() or "Sem motivo informado."

        # Marca este orçamento como recusado
        orc.status = SMVOrcamento.Status.RECUSADO
        orc.observacoes = (orc.observacoes + f"\n\n❌ Recusado em {timezone.now().strftime('%d/%m/%Y %H:%M')}: {motivo}").strip()
        orc.save()

        # Retorna SMV para etapa ORCAMENTO (renegociação)
        SMVEtapa.objects.create(
            smv=smv,
            etapa_de=smv.etapa,
            etapa_para=SMV.Etapa.ORCAMENTO,
            responsavel=request.user,
            observacao=f"Orçamento v{orc.versao} recusado. Motivo: {motivo}",
        )
        smv.etapa = SMV.Etapa.ORCAMENTO
        smv.save()

        messages.warning(request, f"Orçamento v{orc.versao} recusado. SMV retornada para negociação.")

    return redirect("manutencao:detalhe", pk=smv.pk)


# ── Aprovar orçamento e avançar para execução ───────────────────────────────


@login_required
@perfil_required("ADMIN", "GESTOR")
def aprovar_orcamento(request, pk, orc_pk):
    smv = get_object_or_404(SMV, pk=pk)
    orc = get_object_or_404(SMVOrcamento, pk=orc_pk, smv=smv)

    if request.method == "POST":
        # Marca orçamento como aprovado
        orc.status = SMVOrcamento.Status.APROVADO
        orc.observacoes = (orc.observacoes + f"\n\n✅ Aprovado em {timezone.now().strftime('%d/%m/%Y %H:%M')}: {request.user.get_full_name() or request.user.username}").strip()
        orc.save()

        # Cria/atualiza registro de aprovação (documentação física / assinatura final)
        try:
            aprov = orc.aprovacao
            aprov.fiscal_contrato = request.user
            aprov.dt_aprovacao_final = timezone.now()
            aprov.observacoes = (aprov.observacoes + "\nAprovação registrada via sistema.").strip()
            aprov.save()
        except SMVAprovacao.DoesNotExist:
            SMVAprovacao.objects.create(
                orcamento=orc,
                fiscal_contrato=request.user,
                dt_aprovacao_final=timezone.now(),
                observacoes="Aprovação registrada via sistema.",
            )

        # Avança SMV para Execução
        SMVEtapa.objects.create(
            smv=smv,
            etapa_de=smv.etapa,
            etapa_para=SMV.Etapa.EXECUCAO,
            responsavel=request.user,
            observacao=f"Orçamento v{orc.versao} aprovado. Fornecedor: {orc.fornecedor}. Total: R$ {orc.valor_total:.2f}",
        )
        smv.etapa = SMV.Etapa.EXECUCAO
        smv.dt_inicio_exec = timezone.now()
        smv.save()

        messages.success(request, f"Orçamento v{orc.versao} aprovado. SMV avançada para Execução.")

    return redirect("manutencao:detalhe", pk=smv.pk)


# ── Upload de anexo ───────────────────────────────────────────────────────────

@login_required
def upload_anexo(request, pk):
    smv = get_object_or_404(SMV, pk=pk)

    if request.method == "POST":
        arquivo    = request.FILES.get("arquivo")
        tipo       = request.POST.get("tipo", SMVAnexo.TipoAnexo.OUTRO)
        descricao  = request.POST.get("descricao", "").strip()

        if arquivo:
            SMVAnexo.objects.create(
                smv=smv,
                etapa=smv.etapa,
                tipo=tipo,
                descricao=descricao,
                arquivo=arquivo,
                enviado_por=request.user,
            )
            messages.success(request, "Anexo enviado.")

    return redirect("manutencao:detalhe", pk=smv.pk)
