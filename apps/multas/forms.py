from django import forms
from .models import Multa, TipoMulta


class MultaForm(forms.ModelForm):
    class Meta:
        model  = Multa
        fields = [
            "placa", "condutor",
            "data_infracao", "tipo_infracao",
            "pontos", "valor",
            "status", "data_vencimento", "prazo_indicacao", "prazo_defesa",
            "arquivo", "observacao",
        ]
        widgets = {
            "placa":           forms.TextInput(attrs={"class": "form-control", "placeholder": "AAA-0000"}),
            "condutor":        forms.Select(attrs={"class": "form-control"}),
            "data_infracao":   forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "tipo_infracao":   forms.Select(attrs={"class": "form-control"}),
            "pontos":          forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "valor":           forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": 0}),
            "status":          forms.Select(attrs={"class": "form-control"}),
            "data_vencimento": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "prazo_indicacao": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "prazo_defesa":    forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "arquivo":         forms.FileInput(attrs={"class": "form-control-file", "accept": ".pdf"}),
            "observacao":      forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        condutor_inicial = kwargs.pop("condutor_inicial", None)
        super().__init__(*args, **kwargs)
        self.fields["condutor"].empty_label = "— Condutor não identificado —"
        self.fields["tipo_infracao"].empty_label = "— Selecione o tipo —"
        self.fields["tipo_infracao"].queryset = TipoMulta.objects.filter(ativo=True).order_by("codigo")
        if condutor_inicial:
            self.fields["condutor"].initial = condutor_inicial


class TipoMultaForm(forms.ModelForm):
    class Meta:
        model  = TipoMulta
        fields = ["codigo", "descricao", "natureza", "ativo"]
        widgets = {
            "codigo":    forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex: 605-01"}),
            "descricao": forms.TextInput(attrs={"class": "form-control"}),
            "natureza":  forms.Select(attrs={"class": "form-control"}),
            "ativo":     forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

