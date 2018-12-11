from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.views import logout_then_login

# Create your views here.
from django.views import View

from base.forms import PersonagemForm
from base.models import  Personagem


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



            return redirect('personagens')

class Selecionar(LoginRequiredMixin, View):

    def get(self, request, player):
        request.session['player_id'] = player
        return render(request, 'base/cidade.html', {'player': Personagem.objects.get(pk=player)})