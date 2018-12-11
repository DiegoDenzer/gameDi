from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from base.models import Personagem


class ListarAdversarios(LoginRequiredMixin, View):

    def get(self, request):

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
        )[:10]
