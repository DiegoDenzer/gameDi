import uuid
from _ast import In
from operator import inv
from random import randint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from base.models.inventario import InventarioItem, Inventario
from base.models.personagem import Personagem
from base.models.quest import Quest
from base.util.util import valida_jogador, rolar_dado, VALOR_DROP


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
                return f'{atacante.nome} Acertou critico de {dano} no {defensor.nome}.'
            else:
                dano = atacante.dano
                defensor.hp_atual -= dano
                return f'{atacante.nome} casou {dano} de dano em {defensor.nome}.'
        else:
            return f'{defensor.nome} defendeu o ataque de {atacante.nome}'
    else:
        return f'{atacante.nome} errou ataque seu ataque em {defensor.nome}'


def vivo(individuo):
    return individuo.hp_atual > 0


def ordem_ataque(jogador, inimigo, lista):
    if jogador.agilidade > inimigo.inimigo.agilidade:
        lista.append(atacar(jogador, inimigo.inimigo))
        if vivo(inimigo.inimigo):
            lista.append(atacar(inimigo.inimigo, jogador))
    else:
        lista.append(atacar(inimigo.inimigo, jogador))
        if vivo(jogador):
            lista.append(atacar(jogador, inimigo.inimigo))


def define_morte(inimigo, jogador, lista):
    inimigos_mortos = 0
    if inimigo.inimigo.hp_atual <= 0:
        lista.append(f'{inimigo.inimigo.nome} morreu')
        inimigos_mortos += 1
    if jogador.hp_atual <= 0:
        lista.append(f'{jogador.nome} morreu')
        return 99

    return inimigos_mortos;

def combate(jogador, quest):

    detalhes_combate = {}

    inimigos = list(quest.inimigos.all())

    inimigos.sort(key=lambda a: a.inimigo.agilidade, reverse=True)

    inimigos_totais = quest.inimigos.count()

    turno = 1

    while inimigos_totais > 0:
        lista = []
        for inimigo in inimigos:
            if vivo(jogador) and vivo(inimigo.inimigo):
                ordem_ataque(jogador,inimigo,lista)
                inimigos_totais = inimigos_totais - define_morte(inimigo, jogador, lista)
                detalhes_combate[turno] = lista

        turno += 1

    return detalhes_combate


def drop_item(quest, jogador):
    if quest.materialDrop is not None and quest.chance_material_drop >= randint(1, VALOR_DROP):
        inv = Inventario.objects.get(personagem=jogador)
        try:
            item = InventarioItem.objects.get(itemDrop=quest.materialDrop, inventario=inv)
            item.quantidade += 1
            item.save()
        except InventarioItem.DoesNotExist:

            item = InventarioItem.objects.create(id=uuid.uuid4(), itemDrop=quest.materialDrop,
                                                 inventario=Inventario.objects.get(personagem=jogador),
                                                 quantidade=1)
        return item


class QuestView(View, LoginRequiredMixin):
    login_url = '/'

    def get(self, request, quest):

        jogador = Personagem.objects.get(pk=request.session['player_id'])

        if valida_jogador(request, jogador) and jogador.hp_atual > 0:

            data = {}

            quest = Quest.objects.get(pk=quest)

            if jogador.energia_atual < quest.gasto_energia:
                return redirect('quests')

            data['combate'] = combate(jogador, quest)

            vitoria = False

            if jogador.hp_atual > 0:

                vitoria = True

                # adiciona ganho de gold
                ganho_de_gold = jogador.gold + (quest.ganho_gold * randint(1, 5))
                jogador.gold = jogador.gold + ganho_de_gold
                data['gold'] = ganho_de_gold

                # adiciona experiencia ao jogador
                xp_ganha = (quest.ganho_experiencia * randint(1, 3))
                jogador.experiencia = jogador.experiencia + xp_ganha
                data['xp'] = xp_ganha

                data['drop'] = drop_item(quest, jogador)

            data['vitoria'] = vitoria
            jogador.energia_atual = jogador.energia_atual - quest.gasto_energia

            # verifica se subiu de nivel
            jogador.level_up()
            jogador.save()
            data['personagem'] = jogador
            return render(request, 'base/quest/resultado_quest.html', data)
        else:
            return redirect('quests')
