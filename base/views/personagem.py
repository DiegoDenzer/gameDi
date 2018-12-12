from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import logout_then_login

# Create your views here.
from django.views import View
from pip._vendor import pkg_resources

from base.forms import PersonagemForm
from base.models import Personagem, Classe


def logout_view(request):
    del request.session['player_id']
    logout_then_login(request, '')

class PersonagensListView(LoginRequiredMixin, View):
    login_url = '/'
    template = 'base/personagens.html'

    def get(self, request):
        jogadores = Personagem.objects.filter(user=request.user)
        return render(request, self.template, {'personagens' : jogadores})

class PersonagemCreatedView(LoginRequiredMixin, View):
    login_url = '/'
    template = 'base/novo_personagem.html'

    def get(self, request):
        form = PersonagemForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = PersonagemForm(request.POST)
        if form.is_valid():
            player = Personagem()
            player.user = request.user
            player.classe = form.cleaned_data['classe']
            player.nome = form.cleaned_data['nome']

            player.save()

            classe = get_object_or_404(Classe, pk=form.cleaned_data['classe'].pk)
            player.ataque += player.ataque + classe.ataque
            player.defesa += player.defesa + classe.defesa

            player.save()

            return redirect('personagens')


class PersonagemDeleteView(LoginRequiredMixin, View):
    template = 'base/personagens.html'
    login_url = '/'
    def get(self, request, player):
        personagem_deletar = Personagem.objects.get(pk=player)
        if request.user == personagem_deletar.user:
            personagem_deletar.delete()
            return redirect('personagens')


class SelecionarView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request, player):
        request.session['player_id'] = player
        jogador = Personagem.objects.get(pk=player)
        jogador.refresh()
        jogador.save()

        return render(request, 'base/cidade.html', {'personagem': jogador})
