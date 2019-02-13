import uuid
from random import randint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from base.models.inventario import InventarioItem, Inventario
from base.models.personagem import Personagem
from base.models.quest import Quest
from base.util.util import valida_jogador


class QuestListView(View, LoginRequiredMixin):
    login_url = '/'

    def get(self, request):
        # Obter Jogador
        jogador = Personagem.objects.get(pk=request.session['player_id'])
        # Valida se o Jogador e Valido
        if valida_jogador(request, jogador):
            jogador.refresh()
            jogador.save()
            # Retorna as Quests
            return render(request, 'base/quest/quests.html', {'personagem': jogador, 'quests': Quest.objects.all()})


class QuestView(View, LoginRequiredMixin):
    login_url = '/'

    def get(self, request, quest):
        jogador = Personagem.objects.get(pk=request.session['player_id'])

        if valida_jogador(request, jogador):

            quest = Quest.objects.get(pk=quest)
            if jogador.energia_atual < quest.gasto_energia:
                return redirect('quests')

            if quest.inimigos.count() > 0:
                combatentes = []
                for inimigo in list(quest.inimigos.all()):
                    combatentes.append(inimigo.inimigo)
                combatentes.append(jogador)
                combatentes.sort(key=lambda a: a.agilidade, reverse=True)

                for c in combatentes:
                    print(c)


            jogador.gold = jogador.gold + (quest.ganho_gold * randint(1, 5))
            jogador.energia_atual = jogador.energia_atual - quest.gasto_energia

            # adiciona experiencia ao jogador
            jogador.experiencia = jogador.experiencia + (quest.ganho_experiencia * randint(1, 3))

            if quest.itemDrop is not None:
                InventarioItem.objects.create(id=uuid.uuid4(), itemDrop=quest.itemDrop,
                                              inventario=Inventario.objects.get(personagem=jogador)),

            # verifica se subiu de nivel
            jogador.level_up()
            jogador.save()

            return redirect('quests')
        else:
            return redirect('quests')
