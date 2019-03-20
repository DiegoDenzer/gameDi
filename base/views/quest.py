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
                return f'{atacante.nome} Acertou critico com {dano} de dano.'
            else:
                dano = atacante.dano
                defensor.hp_atual -= dano
                return f'{atacante.nome} casou {dano} de dano.'
        else:
            return f'{defensor.nome} defendeu'
    else:
        return f'{atacante.nome} errou ataque'


def combate(jogador, quest):

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

            lista = []

            for inimigo in inimigos:
                # Refatrado diminuir a complexidade cognitiva.
                if jogador.agilidade > inimigo.inimigo.agilidade:
                    # Jogador ataca primeiro.
                    lista.append(atacar(jogador, inimigo.inimigo))
                    atacou = True

                elif inimigo.inimigo.hp_atual > 0:
                    # inimigo ataca
                    lista.append(atacar(inimigo.inimigo, jogador))
                    # se jogador nao morreu ele ataca.

                elif jogador.hp_atual > 0 and not atacou:
                    lista.append(atacar(jogador, inimigo.inimigo))

                hp_inimigos += inimigo.inimigo.hp_atual

                detalhes_combate[turno] = lista

            fim_combate = jogador.hp_atual > 0 and hp_inimigos > 0

            turno += 1

        return detalhes_combate


class QuestView(View, LoginRequiredMixin):
    login_url = '/'

    def get(self, request, quest):

        jogador = Personagem.objects.get(pk=request.session['player_id'])

        if valida_jogador(request, jogador) and jogador.hp_atual > 0:

            data = {}

            quest = Quest.objects.get(pk=quest)

            data['combate'] = combate(jogador, quest)
            vitoria = False
            if jogador.hp_atual > 0:
                vitoria = True
                data['vitoria'] = vitoria
                # adiciona ganho de gold
                ganho_de_gold = jogador.gold + (quest.ganho_gold * randint(1, 5))
                jogador.gold = jogador.gold + ganho_de_gold
                data['gold'] = ganho_de_gold

                # adiciona experiencia ao jogador
                xp_ganha = (quest.ganho_experiencia * randint(1, 3))
                jogador.experiencia = jogador.experiencia + xp_ganha
                data['xp'] = xp_ganha

                # drop
                if quest.itemDrop is not None:
                    item = InventarioItem.objects.create(id=uuid.uuid4(), itemDrop=quest.itemDrop,
                                                  inventario=Inventario.objects.get(personagem=jogador)),
                    data['drop'] = item


            jogador.energia_atual = jogador.energia_atual - quest.gasto_energia

            # verifica se subiu de nivel
            jogador.level_up()
            jogador.save()
            data['personagem'] = jogador
            return render(request, 'base/quest/resultado_quest.html', data)
        else:
            return redirect('quests')
