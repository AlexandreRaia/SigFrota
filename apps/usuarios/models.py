from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Secretaria(models.Model):
    nome = models.CharField(_("Nome"), max_length=120)
    sigla = models.CharField(_("Sigla"), max_length=20)
    ativa = models.BooleanField(_("Ativa"), default=True)

    class Meta:
        verbose_name = _("Secretaria")
        verbose_name_plural = _("Secretarias")
        ordering = ["nome"]

    def __str__(self):
        return f"{self.sigla} — {self.nome}"


class Usuario(AbstractUser):
    class Perfil(models.TextChoices):
        ADMIN    = "ADMIN",    _("Administrador")
        GESTOR   = "GESTOR",   _("Gestor")
        OPERADOR = "OPERADOR", _("Operador")
        OFICINA  = "OFICINA",  _("Oficina")
        AUDITOR  = "AUDITOR",  _("Auditor")

    perfil = models.CharField(
        _("Perfil de acesso"),
        max_length=10,
        choices=Perfil.choices,
        default=Perfil.OPERADOR,
    )
    secretaria = models.ForeignKey(
        Secretaria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Secretaria"),
        related_name="usuarios",
    )
    telefone = models.CharField(_("Telefone"), max_length=20, blank=True)
    foto     = models.ImageField(_("Foto"), upload_to="usuarios/fotos/", null=True, blank=True)

    class Meta:
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_perfil_display()})"

    @property
    def is_admin(self):
        return self.perfil == self.Perfil.ADMIN or self.is_superuser

    @property
    def is_gestor(self):
        return self.perfil in (self.Perfil.ADMIN, self.Perfil.GESTOR) or self.is_superuser
