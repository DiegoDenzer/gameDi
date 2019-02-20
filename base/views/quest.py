import uuid
from random import randint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from base.models.inventario import InventarioItem, Inventario
from base.models.personagem import Personagem
from base.models.quest import Quest
from base.util.util import valida_jogador, rolar_dado


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


def atacar(atacante, defensor):
    valor_dado = rolar_dado()
    print(f'{atacante.nome} rolou: {valor_dado} ')
    critico = False
    pode_atacar = False

    if valor_dado > 2:
        pode_atacar = True
        if valor_dado == 20:
            critico = True
    if pode_atacar:
        if atacante.ataque(valor_dado) > defensor.defesa:
            if critico:
                dano = atacante.dano * 2
                atacante.hp_atual -= dano
                return f'{atacante.nome} Criticou com {dano}'
            else:
                dano = atacante.dano
                defensor.hp_atual -= dano
                return f'{atacante.nome} atacou com {dano}'
        else:
            return f'{defensor.nome} defendeu'
    else:
        return f'{atacante.nome} errou ataque'


def combate(request, jogador, quest):

    if jogador.energia_atual < quest.gasto_energia:
        return redirect('quests')

    if quest.inimigos.count() > 0:

        detalhes_combate = {}

        inimigos = list(quest.inimigos.all())

        inimigos.sort(key=lambda a: a.inimigo.agilidade, reverse=True)

        fim_combate = True

        turno = 1

        while fim_combate:

            hp_inimigos = 0

            for inimigo in inimigos:

                if jogador.agilidade > inimigo.inimigo.agilidade:
                    detalhes_combate[f'{turno} - {jogador.nome}'] = atacar(jogador, inimigo.inimigo)
                    if inimigo.inimigo.hp_atual > 0:
                        detalhes_combate[f'{turno} - {inimigo.inimigo.nome}'] = atacar(inimigo.inimigo, jogador)
                else:
                    detalhes_combate[f'{turno} - {inimigo.inimigo.nome}'] = atacar(inimigo.inimigo, jogador)
                    if jogador.hp_atual > 0:
                        detalhes_combate[f'{turno} - {jogador.nome}'] = atacar(jogador, inimigo.inimigo)

                hp_inimigos += inimigo.inimigo.hp_atual

            if jogador.hp_atual <= 0 or hp_inimigos <= 0:
                fim_combate = False

            turno += 1

        return detalhes_combate


class QuestView(View, LoginRequiredMixin):
    login_url = '/'

    def get(self, request, quest):

        jogador = Personagem.objects.get(pk=request.session['player_id'])

        if valida_jogador(request, jogador) and jogador.hp_atual > 0:

            data = {}

            quest = Quest.objects.get(pk=quest)

            data['combate'] = combate(request, jogador, quest)

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
