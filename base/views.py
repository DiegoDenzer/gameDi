from django.shortcuts import render
from django.contrib.auth.views import logout_then_login

# Create your views here.
from django.views import View

from base.models import Jogador


def logout_view(request):
    logout_then_login(request, '')

class PersonagensView(View):

    def get(self, request):

        jogadores = Jogador.objects.filter(user=request.user)

        return render(request, 'base/personagens.html', {'personagens' : jogadores})

