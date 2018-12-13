from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import logout_then_login

# Create your views here.
from django.views import View
from django.views.generic import DetailView
from pip._vendor import pkg_resources

from base.forms import PersonagemForm
from base.models import Personagem, Classe
from base.util.util import valida_jogador


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
        if valida_jogador(request, personagem_deletar):
            personagem_deletar.delete()
            return redirect('personagens')


class SelecionarView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        jogador = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, jogador):
            jogador.refresh()
            jogador.save()

        return render(request, 'base/cidade.html', {'personagem': jogador})

    def post(self, request):
        player = request.POST['player']
        request.session['player_id'] = player
        jogador = Personagem.objects.get(pk=player)
        jogador.refresh()
        jogador.save()
        return render(request, 'base/cidade.html', {'personagem': jogador})


class PesonagemDetailView(LoginRequiredMixin, View):

    template = 'base/personagem_detail.html'

    def get(self, request):
        personagem = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, personagem):
            return render(request, self.template, {'personagem': personagem})


def distribuirAtributo(personagem, atributo):
    personagem.refresh()
    personagem.save()
    if personagem.pontos > 0:
        if atributo == 'ataque':
            personagem.ataque += 1
        elif atributo == 'defesa':
            personagem.defesa += 1
        elif atributo == 'vida':
            personagem.vida += 1
        elif atributo == 'energia':
            personagem.raiva += 1
        elif atributo == 'raiva':
            personagem.raiva += 1
        personagem.pontos -= 1
        personagem.save()


class AddAtaque(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        personagem = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, personagem):
            distribuirAtributo(personagem, 'ataque')
            return redirect('personagem_detail')


class AddDefesa(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        personagem = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, personagem):
            distribuirAtributo(personagem, 'defesa')
            return redirect('personagem_detail')

class AddVida(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        personagem = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, personagem):
            distribuirAtributo(personagem, 'vida')
            return redirect('personagem_detail')

class AddEnergia(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        personagem = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, personagem):
            distribuirAtributo(personagem, 'energia')
            return redirect('personagem_detail')

class AddRaiva(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        personagem = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, personagem):
            distribuirAtributo(personagem, 'raiva')
            return redirect('personagem_detail')