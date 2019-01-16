from random import randint


def valida_jogador(request, jogador):
    if request.user == jogador.user:
        return True
    else:
        return False


def rolar_dado(destreza):
    dado_ataque = randint(0, 21)

    chance = destreza // 20

    if dado_ataque < 6 - chance:
        return 'Erro'

    if dado_ataque >= 6 - chance or dado_ataque <= 17:
        return 'Normal'

    if dado_ataque >= 18 or dado_ataque >= 20:
        return 'Critico'
