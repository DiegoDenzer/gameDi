import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from base.models import Personagem, Inventario, InventarioItem
from base.util.util import valida_jogador

'''
    Poderia ter feito tudo em uma unica Classe mas separei para ficar melhor a manutenção
    e ampliação de recursos
'''

class UsarPocaoView(LoginRequiredMixin, View):
    template = 'base/personagem_detail.html'
    login_url = '/'

    def get(self, request, item):
        personagem = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, personagem):
            personagem.refresh()
            item = InventarioItem.objects.get(pk=item)
            if item.pocao is None:
                personagem.hp += item.pocao.hp
                personagem.energia += item.pocao.energia
                personagem.raiva_atual += item.pocao.raiva
                item.delete()
                personagem.save()
            return redirect('personagem_detail')

        return redirect('personagem_detail')


class UsarPocaoView(LoginRequiredMixin, View):
    template = 'base/personagem_detail.html'
    login_url = '/'

    def get(self, request, item):
        personagem = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, personagem):
            personagem.refresh()
            item = InventarioItem.objects.get(id=item)
            if item.pocao is not None:
                personagem.hp += item.pocao.hp
                personagem.energia_atual += item.pocao.energia
                personagem.raiva_atual += item.pocao.raiva
                item.delete()

                if personagem.hp > personagem.vida * 10:
                    personagem.hp = personagem.vida * 10
                if personagem.energia_atual > personagem.energia:
                    personagem.energia_atual = personagem.energia
                if personagem.raiva_atual > personagem.raiva:
                    personagem.raiva_atual = personagem.raiva

                personagem.save()
            return redirect('personagem_detail')

        return redirect('personagem_detail')


class EquiparView(LoginRequiredMixin, View):
    template = 'base/personagem_detail.html'
    login_url = '/'

    def get(self, request, item):
        personagem = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, personagem):
            personagem.refresh()
            item = InventarioItem.objects.get(pk=item)
            if item.arma is not None:
                if personagem.armas is None:
                    personagem.armas = item.arma
                    item.delete()
                else:
                    atual = personagem.armas
                    personagem.armas = item.arma
                    InventarioItem.objects.create(id=uuid.uuid4(), arma=atual,
                                                  inventario=Inventario.objects.get(personagem=personagem))
                    item.delete()

                personagem.save()

            elif item.armadura is not None:
                if personagem.armaduras is None:
                    personagem.armaduras = item.armadura
                    item.delete()
                else:
                    atual = personagem.armaduras
                    personagem.armaduras = item.armadura
                    InventarioItem.objects.create(id=uuid.uuid4(), arma=atual,
                                                  inventario=Inventario.objects.get(personagem=personagem))
                    item.delete()

                personagem.save()
            return redirect('personagem_detail')

        return redirect('personagem_detail')
