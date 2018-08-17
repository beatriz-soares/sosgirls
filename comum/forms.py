# -*- coding: utf-8 -*-
from django import forms
from comum.models import *

class NovoDepoimentoForm(forms.ModelForm):
    class Meta:
        model = Depoimentos
        fields = ('titulo', 'conteudo', 'tipo')
        labels = {
            'titulo': u"Título",
            'conteudo': u"Conteúdo",
            'tipo': u"Tipo"
        }
