from random import randint


def valida_jogador(request, jogador):
    if request.user == jogador.user:
        return True
    else:
        return False


def rolar_dado():
    return randint(0, 20)

