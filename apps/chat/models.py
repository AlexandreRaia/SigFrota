from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


def _mensagem_anexo_upload(instance, filename):
    return f"manutencao/smv-{instance.smv.numero}/chat/{filename}"


class SMVMensagem(models.Model):
    """Mensagem do chat vinculada a uma SMV e à etapa em que foi enviada."""

    smv     = models.ForeignKey(
        "manutencao.SMV",
        on_delete=models.CASCADE,
        related_name="mensagens",
        verbose_name=_("SMV"),
    )
    etapa   = models.CharField(
        _("Etapa ao enviar"),
        max_length=15,
        help_text=_("Etapa da SMV no momento do envio — registrado automaticamente."),
    )
    autor   = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="mensagens_smv",
        verbose_name=_("Autor"),
    )
    texto   = models.TextField(_("Mensagem"), blank=True)
    anexo   = models.FileField(_("Anexo"), upload_to=_mensagem_anexo_upload, null=True, blank=True)
    enviada_em = models.DateTimeField(_("Enviada em"), auto_now_add=True)

    class Meta:
        verbose_name        = _("Mensagem SMV")
        verbose_name_plural = _("Mensagens SMV")
        ordering            = ["enviada_em"]

    def __str__(self):
        return f"SMV {self.smv.numero} | {self.autor} @ {self.enviada_em:%d/%m/%Y %H:%M}"


class SMVMensagemLeitura(models.Model):
    """Rastreia quais usuários já leram cada mensagem (para badge de não lidas)."""

    mensagem = models.ForeignKey(SMVMensagem, on_delete=models.CASCADE, related_name="leituras")
    usuario  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="leituras_smv")
    lida_em  = models.DateTimeField(_("Lida em"), auto_now_add=True)

    class Meta:
        unique_together     = [["mensagem", "usuario"]]
        verbose_name        = _("Leitura de mensagem")
        verbose_name_plural = _("Leituras de mensagem")

    def __str__(self):
        return f"{self.usuario} leu {self.mensagem}"
