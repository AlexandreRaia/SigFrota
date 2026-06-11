import json
from django import forms
from .models import Veiculo, TipoVeiculo, Marca, Modelo


_w = lambda extra="": {"class": f"form-control {extra}".strip()}
_s = lambda: {"class": "form-control"}


class VeiculoForm(forms.ModelForm):

    class Meta:
        model  = Veiculo
        fields = [
            # Identificação
            "placa", "marca", "modelo", "chassi", "renavam", "prefixo", "num_patrimonio",
            # Especificações Técnicas
            "tipo_veiculo", "ano_fabricacao", "motor_potencia", "combustivel",
            "cap_tanque", "consumo_ref", "cap_passageiros", "cor", "transmissao", "pneu_dim",
            # Histórico e Estado
            "km_entrada", "ultimo_km", "estado_conservacao", "status",
            # Informações Financeiras
            "valor_fipe", "tipo_frota", "locadora", "valor_aluguel",
            "dt_ini_contrato", "dt_fim_contrato",
            # Administrativo
            "secretaria", "centro_custo",
            # Documentação
            "crlv", "foto_frente", "foto_lateral_e", "foto_lateral_d",
            "foto_traseira", "foto_hodometro", "outros_docs",
            # Equipamentos
            "eq_ar_condicionado", "eq_direcao_hidraulica", "eq_vidros_eletricos",
            "eq_som_multimidia", "eq_radio_comunicador", "eq_rodas_liga_leve",
            "eq_camera_re", "eq_sensor_estac", "eq_outros",
        ]
        widgets = {
            "placa":           forms.TextInput(attrs={**_w(), "placeholder": "ABC-1234"}),
            "chassi":          forms.TextInput(attrs={**_w(), "maxlength": "17"}),
            "renavam":         forms.TextInput(attrs={**_w(), "maxlength": "11"}),
            "prefixo":         forms.TextInput(attrs=_w()),
            "num_patrimonio":  forms.TextInput(attrs=_w()),

            "marca":           forms.Select(attrs={**_s(), "id": "id_marca"}),
            "modelo":          forms.Select(attrs={**_s(), "id": "id_modelo"}),
            "tipo_veiculo":    forms.Select(attrs=_s()),

            "ano_fabricacao":  forms.NumberInput(attrs={**_w(), "min": "1900", "max": "2100"}),
            "motor_potencia":  forms.TextInput(attrs={**_w(), "placeholder": "Ex: 1.6 VHT 110cv"}),
            "combustivel":     forms.Select(attrs=_s()),
            "cap_tanque":      forms.NumberInput(attrs={**_w(), "step": "0.1"}),
            "consumo_ref":     forms.NumberInput(attrs={**_w(), "step": "0.01"}),
            "cap_passageiros": forms.NumberInput(attrs=_w()),
            "cor":             forms.TextInput(attrs=_w()),
            "transmissao":     forms.Select(attrs=_s()),
            "pneu_dim":        forms.TextInput(attrs={**_w(), "placeholder": "195/65 R15"}),

            "km_entrada":         forms.NumberInput(attrs=_w()),
            "ultimo_km":          forms.NumberInput(attrs=_w()),
            "estado_conservacao": forms.Select(attrs=_s()),
            "status":             forms.Select(attrs=_s()),

            "valor_fipe":      forms.NumberInput(attrs={**_w(), "step": "0.01"}),
            "tipo_frota":      forms.Select(attrs=_s()),
            "locadora":        forms.TextInput(attrs=_w()),
            "valor_aluguel":   forms.NumberInput(attrs={**_w(), "step": "0.01"}),
            "dt_ini_contrato": forms.DateInput(attrs={**_w(), "type": "date"}),
            "dt_fim_contrato": forms.DateInput(attrs={**_w(), "type": "date"}),

            "secretaria":   forms.Select(attrs=_s()),
            "centro_custo": forms.TextInput(attrs=_w()),

            "eq_outros": forms.Textarea(attrs={**_w(), "rows": "2", "placeholder": "Descreva outros equipamentos…"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apenas registros ativos nas FK lookups
        self.fields["marca"].queryset       = Marca.objects.filter(ativo=True)
        self.fields["tipo_veiculo"].queryset = TipoVeiculo.objects.filter(ativo=True)
        # Modelos: todos ativos (JS faz o filtro visual por marca)
        self.fields["modelo"].queryset      = Modelo.objects.filter(ativo=True).select_related("marca")

        # Mapa modelo_id → marca_id serializado para o JS de filtro
        self.modelo_marca_map_json = json.dumps({
            str(pk): str(marca_id)
            for pk, marca_id in Modelo.objects.filter(ativo=True).values_list("pk", "marca_id")
        }, separators=(',', ':'))

        # Empty labels
        self.fields["marca"].empty_label        = "— Selecione a marca —"
        self.fields["modelo"].empty_label       = "— Selecione o modelo —"
        self.fields["tipo_veiculo"].empty_label = "— Selecione o tipo —"

        # Campos opcionais
        for f in ("locadora", "valor_aluguel", "dt_ini_contrato", "dt_fim_contrato",
                  "motor_potencia", "consumo_ref", "cap_passageiros", "cor", "transmissao",
                  "pneu_dim", "prefixo", "num_patrimonio", "valor_fipe",
                  "crlv", "foto_frente", "foto_lateral_e", "foto_lateral_d",
                  "foto_traseira", "foto_hodometro", "outros_docs", "eq_outros", "ultimo_km"):
            self.fields[f].required = False

