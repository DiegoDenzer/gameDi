import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from base.models.inventario import InventarioItem, Inventario
from base.models.itens import Receita
from base.models.personagem import Personagem
from base.util.util import valida_jogador


class MostrarReceitasView(View, LoginRequiredMixin):
    login_url = '/'
    template = 'base/receitas.html'

    def get(self, request):
        personagem = Personagem.objects.get(pk=request.session['player_id'])
        personagem.refresh()
        return render(request, self.template, {'receitas': Receita.objects.all(), 'personagem': personagem})


class ForjaView(View, LoginRequiredMixin):
    login_url = '/'
    template = 'base/forja.html'

    def get(self, request):
        personagem = Personagem.objects.get(pk=request.session['player_id'])
        personagem.refresh()
        return render(request, self.template, {'personagem': personagem})


class CriarItem(View, LoginRequiredMixin):
    login_url = '/'

    def get(self, request, receita):
        personagem = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, personagem):
            personagem.refresh()

            receita_selecionada = Receita.objects.get(receita)

            if receita_selecionada.ingrediente_1:
                InventarioItem.objects.get(inventario=Inventario.objects.get(personagem=personagem,
                                                                             itens__itemDrop=receita.ingrediente_1))
            if receita_selecionada.ingrediente_2:
                pass
            if receita_selecionada.ingrediente_3:
                pass





