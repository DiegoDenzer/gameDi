

def valida_jogador(request, jogador):
    if request.user == jogador.user:
        return True
    else:
        return False

