from django import forms
from .models import Condutor, Acidente, Infracao, Qualificacao, Penalidade, FolgaFerias


class CondutorForm(forms.ModelForm):
    class Meta:
        model = Condutor
        fields = [
            "prontuario", "foto", "status",
            "nome", "data_nascimento", "cpf", "rg", "orgao_emissor", "cargo",
            "telefone", "email", "endereco",
            "secretaria", "unidade",
            "cnh_categoria", "cnh_numero", "cnh_emissao", "cnh_vencimento",
            "cnh_orgao", "cnh_arquivo",
        ]
        widgets = {
            "data_nascimento": forms.DateInput(attrs={"type": "date"}),
            "cnh_emissao":     forms.DateInput(attrs={"type": "date"}),
            "cnh_vencimento":  forms.DateInput(attrs={"type": "date"}),
            "endereco":        forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput,
                                         forms.Select, forms.DateInput,
                                         forms.NumberInput)):
                field.widget.attrs.setdefault("class", "form-control")
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.setdefault("class", "form-control-file")


class AcidenteForm(forms.ModelForm):
    class Meta:
        model  = Acidente
        fields = ["data", "descricao", "veiculo_placa"]
        widgets = {"data": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
                   "descricao": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
                   "veiculo_placa": forms.TextInput(attrs={"class": "form-control"})}


class InfracaoForm(forms.ModelForm):
    class Meta:
        model  = Infracao
        fields = ["data", "tipo", "pontos", "valor", "observacao"]
        widgets = {"data": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
                   "tipo": forms.TextInput(attrs={"class": "form-control"}),
                   "pontos": forms.NumberInput(attrs={"class": "form-control"}),
                   "valor":  forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
                   "observacao": forms.Textarea(attrs={"rows": 2, "class": "form-control"})}


class QualificacaoForm(forms.ModelForm):
    class Meta:
        model  = Qualificacao
        fields = ["curso", "instituicao", "data", "carga_horaria"]
        widgets = {"data": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
                   "curso": forms.TextInput(attrs={"class": "form-control"}),
                   "instituicao": forms.TextInput(attrs={"class": "form-control"}),
                   "carga_horaria": forms.NumberInput(attrs={"class": "form-control"})}


class PenalidadeForm(forms.ModelForm):
    class Meta:
        model  = Penalidade
        fields = ["tipo", "data_inicio", "data_fim", "observacao"]
        widgets = {
            "tipo":        forms.Select(attrs={"class": "form-control"}),
            "data_inicio": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "data_fim":    forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "observacao":  forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
        }


class FolgaFeriasForm(forms.ModelForm):
    class Meta:
        model  = FolgaFerias
        fields = ["tipo", "data_inicio", "data_fim", "observacao"]
        widgets = {
            "tipo":        forms.Select(attrs={"class": "form-control"}),
            "data_inicio": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "data_fim":    forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "observacao":  forms.TextInput(attrs={"class": "form-control"}),
        }
