from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from base.models import Personagem
from base.util.util import valida_jogador


class ListarAdversariosView(LoginRequiredMixin, View):

    def get(self, request):

        jogador = Personagem.objects.get(pk=request.session['player_id'])

        if valida_jogador(request.user, jogador):
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
