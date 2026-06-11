from django.db import models

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from apps.usuarios.models import Secretaria


def _foto_upload(instance, filename):
    return f"condutores/fotos/{instance.cpf}/{filename}"


def _cnh_upload(instance, filename):
    return f"condutores/cnh/{instance.cpf}/{filename}"


class Condutor(models.Model):
    """Cadastro de motoristas e condutores da frota municipal."""

    class Status(models.TextChoices):
        ATIVO     = "ATIVO",     _("Ativo")
        INATIVO   = "INATIVO",   _("Inativo")
        SUSPENSO  = "SUSPENSO",  _("Suspenso")

    class CategoriaCNH(models.TextChoices):
        A   = "A",   "A"
        B   = "B",   "B"
        C   = "C",   "C"
        D   = "D",   "D"
        E   = "E",   "E"
        AB  = "AB",  "AB"
        AC  = "AC",  "AC"
        AD  = "AD",  "AD"
        AE  = "AE",  "AE"
        ACC = "ACC", "ACC"

    # Identificação
    prontuario = models.CharField(
        _("Prontuário"), max_length=20, unique=True,
        help_text="Número de prontuário funcional do servidor na prefeitura",
    )
    foto   = models.ImageField(_("Foto"), upload_to=_foto_upload, null=True, blank=True)
    status = models.CharField(_("Status"), max_length=10, choices=Status.choices, default=Status.ATIVO)

    # Dados pessoais
    nome             = models.CharField(_("Nome completo"), max_length=160)
    data_nascimento  = models.DateField(_("Data de nascimento"))
    cpf = models.CharField(
        _("CPF"), max_length=14, unique=True,
        validators=[RegexValidator(r"^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$", "CPF inválido")],
    )
    rg             = models.CharField(_("RG"), max_length=20)
    orgao_emissor  = models.CharField(_("Órgão emissor"), max_length=30)
    cargo          = models.CharField(_("Cargo"), max_length=100)

    # Contato
    endereco = models.CharField(_("Endereço"), max_length=255, blank=True)
    telefone = models.CharField(_("Telefone"), max_length=20)
    email    = models.EmailField(_("E-mail"))

    # Lotação
    secretaria = models.ForeignKey(
        Secretaria, on_delete=models.PROTECT,
        verbose_name=_("Secretaria"), related_name="condutores",
    )
    unidade = models.CharField(_("Unidade"), max_length=100, blank=True)

    # CNH
    cnh_categoria  = models.CharField(_("Categoria CNH"), max_length=3, choices=CategoriaCNH.choices, blank=True)
    cnh_numero     = models.CharField(_("Número CNH"), max_length=11, blank=True)
    cnh_emissao    = models.DateField(_("Emissão CNH"), null=True, blank=True)
    cnh_vencimento = models.DateField(_("Vencimento CNH"), null=True, blank=True)
    cnh_orgao      = models.CharField(_("Órgão expedidor CNH"), max_length=30, blank=True)
    cnh_arquivo    = models.FileField(_("CNH digitalizada"), upload_to=_cnh_upload, null=True, blank=True)

    # Auditoria
    criado_em    = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Condutor")
        verbose_name_plural = _("Condutores")
        ordering = ["nome"]

    def __str__(self):
        return f"{self.prontuario} — {self.nome}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def cnh_vencida(self):
        from django.utils import timezone
        if not self.cnh_vencimento:
            return False
        return self.cnh_vencimento < timezone.now().date()

    @property
    def cnh_vence_em_breve(self):
        """Retorna True se a CNH vence nos próximos 30 dias."""
        from django.utils import timezone
        import datetime
        if not self.cnh_vencimento:
            return False
        hoje = timezone.now().date()
        return hoje <= self.cnh_vencimento <= (hoje + datetime.timedelta(days=30))


class Acidente(models.Model):
    condutor    = models.ForeignKey(Condutor, on_delete=models.CASCADE, related_name="acidentes")
    data        = models.DateField(_("Data"))
    descricao   = models.TextField(_("Descrição"))
    veiculo_placa = models.CharField(_("Placa do veículo"), max_length=10, blank=True)

    class Meta:
        verbose_name = _("Acidente")
        ordering = ["-data"]

    def __str__(self):
        return f"Acidente {self.data} — {self.condutor.nome}"


class Infracao(models.Model):
    condutor = models.ForeignKey(Condutor, on_delete=models.CASCADE, related_name="infracoes")
    data     = models.DateField(_("Data"))
    tipo     = models.CharField(_("Tipo de infração"), max_length=120)
    pontos   = models.PositiveSmallIntegerField(_("Pontos"), default=0)
    valor    = models.DecimalField(_("Valor (R$)"), max_digits=10, decimal_places=2, default=0)
    observacao = models.TextField(_("Observação"), blank=True)

    class Meta:
        verbose_name = _("Infração")
        verbose_name_plural = _("Infrações")
        ordering = ["-data"]

    def __str__(self):
        return f"{self.tipo} ({self.data}) — {self.condutor.nome}"


class Qualificacao(models.Model):
    condutor     = models.ForeignKey(Condutor, on_delete=models.CASCADE, related_name="qualificacoes")
    curso        = models.CharField(_("Curso"), max_length=200)
    instituicao  = models.CharField(_("Instituição"), max_length=200)
    data         = models.DateField(_("Data de conclusão"))
    carga_horaria = models.PositiveSmallIntegerField(_("Carga horária (h)"), default=0)

    class Meta:
        verbose_name = _("Qualificação")
        verbose_name_plural = _("Qualificações")
        ordering = ["-data"]

    def __str__(self):
        return f"{self.curso} — {self.condutor.nome}"


class Penalidade(models.Model):
    class Tipo(models.TextChoices):
        ADVERTENCIA  = "ADVERTENCIA",  _("Advertência")
        SUSPENSAO    = "SUSPENSAO",    _("Suspensão")
        DEMISSAO     = "DEMISSAO",     _("Demissão")
        OUTRO        = "OUTRO",        _("Outro")

    condutor    = models.ForeignKey(Condutor, on_delete=models.CASCADE, related_name="penalidades")
    tipo        = models.CharField(_("Tipo"), max_length=20, choices=Tipo.choices)
    data_inicio = models.DateField(_("Data de início"))
    data_fim    = models.DateField(_("Data de fim"), null=True, blank=True)
    observacao  = models.TextField(_("Observação"), blank=True)

    class Meta:
        verbose_name = _("Penalidade")
        ordering = ["-data_inicio"]

    def __str__(self):
        return f"{self.get_tipo_display()} ({self.data_inicio}) — {self.condutor.nome}"


class FolgaFerias(models.Model):
    class Tipo(models.TextChoices):
        FERIAS = "FERIAS", _("Férias")
        FOLGA  = "FOLGA",  _("Folga")
        LICENCA = "LICENCA", _("Licença")
        OUTRO  = "OUTRO",  _("Outro")

    condutor    = models.ForeignKey(Condutor, on_delete=models.CASCADE, related_name="folgas")
    tipo        = models.CharField(_("Tipo"), max_length=10, choices=Tipo.choices, default=Tipo.FERIAS)
    data_inicio = models.DateField(_("Início"))
    data_fim    = models.DateField(_("Fim"))
    observacao  = models.CharField(_("Observação"), max_length=255, blank=True)

    class Meta:
        verbose_name = _("Folga / Férias")
        verbose_name_plural = _("Folgas / Férias")
        ordering = ["-data_inicio"]

    def __str__(self):
        return f"{self.get_tipo_display()} {self.data_inicio}→{self.data_fim} — {self.condutor.nome}"
