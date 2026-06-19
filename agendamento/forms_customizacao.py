from django import forms
from .models import CustomizacaoHeader


class CustomizacaoHeaderForm(forms.ModelForm):
    class Meta:
        model = CustomizacaoHeader
        fields = ['titulo', 'subtitulo', 'exibir_titulo_subtitulo', 'cor_header', 'logo', 'logo_posicao']

    def clean_cor_header(self):
        cor = self.cleaned_data.get('cor_header')
        if cor and not cor.startswith('#'):
            cor = '#' + cor
        return cor
