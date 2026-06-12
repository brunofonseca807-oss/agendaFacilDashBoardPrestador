from django import forms
from .models import Servico


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'descricao', 'preco', 'duracao_estimada']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_preco(self):
        preco = self.cleaned_data.get('preco')
        if preco is not None and preco <= 0:
            raise forms.ValidationError('O preço deve ser maior que zero.')
        return preco

    def clean_duracao_estimada(self):
        duracao = self.cleaned_data.get('duracao_estimada')
        if duracao is not None and (duracao < 15 or duracao > 480):
            raise forms.ValidationError('A duração deve ser entre 15 e 480 minutos.')
        return duracao
