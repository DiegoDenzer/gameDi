from random import randint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from base.models import Personagem
from base.util.util import valida_jogador


class ListarAdversariosView(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):

        jogador = Personagem.objects.get(pk=request.session['player_id'])

        if valida_jogador(request, jogador):
            alvos = Personagem.objects.all()
            '''
            alvos = Personagem.objects.filter(
                experiencia__gte=(jogador.experiencia * 0.6)
            ).filter(
                experiencia__lte=(jogador.experiencia * 1.4)
            ).exclude(
                id=jogador.id
            ).exclude(
                experiencia=0
            ).exclude(
                hp=0
            )[:10]'''

            return render(request, 'base/alvos.html', {'personagem': jogador, 'alvos': alvos})


class AtacarView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request, alvo):
        # view da luta
        alvo_id = alvo
        # verifica se esta sendo passado um alvo valido
        alvo = get_object_or_404(Personagem, pk=alvo_id)

        # pega o nosso jogador da sessao
        jogador =get_object_or_404(Personagem, pk= request.session['player_id'])

        # verifica se o jogador e o alvo sao a mesma pessoa
        if jogador == alvo:
            return redirect('alvos')

        # verifica se a experiencia do alvo eh menor que 50% da experiencia do atacante
        if jogador.experiencia * 0.5 > alvo.experiencia:
            return redirect('alvos')

        # atualiza o alvo e o jogador
        alvo.refresh()
        jogador.refresh()

        # verifica se o nosso jogador possui raiva para atacar
        if jogador.raiva_atual == 0:
            return redirect('alvos')

        # verifica se o nosso jogador esta "morto"
        if jogador.hp <= 0:
            return redirect('alvos')

        # verifica se o alvo esta 'morto'
        if alvo.hp <= 0:
            return redirect('alvos')

        # salva o hp inicial do jogador e do alvo para fazer um pequeno relatorio no final
        jogador_hp = jogador.hp
        alvo_hp = alvo.hp

        # pega o valor da arma do jogador
        if jogador.armas is not None:
            jogador_arma = jogador.armas.poder
        else:
            jogador_arma = 1

        # pega o valor da armadura do jogador
        if jogador.armaduras is not None:
            jogador_armadura = jogador.armaduras.poder
        else:
            jogador_armadura = 1

        # pega o valor da arma do alvo
        if alvo.armas is not None:
            alvo_arma = alvo.armas.poder
        else:
            alvo_arma = 1

        # pega o valor da armadura do alvo
        if alvo.armaduras is not None:
            alvo_armadura = alvo.armaduras.poder
        else:
            alvo_armadura = 1

        dano_personagem = []
        dano_alvo = []

        # agora o bicho vai pegar!
        # a luta dura 5 turnos
        for turno in [1, 2, 3, 4, 5]:

            # primeiro o jogador ataca

            ataque = randint(int(jogador.ataque / 3), jogador.ataque)
            defesa = randint(int(alvo.defesa / 3), alvo.defesa)

            # calcula o dano
            dano = ataque * jogador_arma - defesa * alvo_armadura

            if dano > 0:
                alvo.hp = alvo.hp - dano
                dano_personagem.append(dano)
            else:
                dano_personagem.append(0)

            # agora o alvo ataca
            ataque = randint(int(alvo.ataque / 3), alvo.ataque)
            defesa = randint(int(jogador.defesa / 3), jogador.defesa)

            # calcula o dano
            dano = ataque * alvo_arma - defesa * jogador_armadura

            if dano > 0:
                jogador.hp = jogador.hp - dano
                dano_alvo.append(dano)
            else:
                dano_alvo.append(0)

            # verifica se alguem morreu no combate
            if jogador.hp == 0 or alvo.hp == 0:
                break

        # descobrindo quem perdeu
        if jogador.hp == 0:
            vitoria = False
        elif alvo.hp == 0:
            vitoria = True
        elif alvo_hp - alvo.hp > jogador_hp - jogador.hp:
            vitoria = True
        else:
            vitoria = False

        # se o jogador ganhou, tira dinheiro do alvo e da ao jogador
        if vitoria:
            grana = alvo.gold * (randint(10, 90) / 100.0)  # entre 10% e 90% do valor da carteira
            grana = round(grana)

            alvo.gold = alvo.gold - grana
            jogador.gold = jogador.gold + grana

            # ganha 10% da experiencia do adversario
            jogador.experiencia = jogador.experiencia + alvo.experiencia * 0.1
        else:
            grana = jogador.gold * (randint(10, 90) / 100.0)  # entre 10% e 90% do valor da carteira
            grana = round(grana)

            alvo.gold = alvo.gold + grana
            jogador.gold = jogador.gold - grana

            # ganha 10% da experiencia do adversario
            alvo.experiencia = alvo.experiencia + jogador.experiencia * 0.1

        # o nosso atacante perde 1 de raiva
        jogador.raiva_atual = jogador.raiva_atual - 1

        # verifica se alguem deu level up
        alvo.level_up()
        jogador.level_up()

        # salva todas as alteracoes no banco de dados
        alvo.save()
        jogador.save()

        # exibe o template com o resultado da luta
        return render(request, "base/resultado_luta.html", {"personagem": jogador,
                                                  "alvo": alvo,
                                                  "vitoria": vitoria,
                                                  "dados_p": dano_personagem,
                                                  "dados_a": dano_alvo
                                                            })