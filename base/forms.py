from django import forms

from base.models import Personagem


class PersonagemForm(forms.ModelForm):

    class Meta:
        model = Personagem
        fields = ['nome','classe']
