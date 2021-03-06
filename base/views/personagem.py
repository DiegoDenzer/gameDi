import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import logout_then_login

# Create your views here.
from django.views import View
from rest_framework import viewsets

from base.forms import PersonagemForm
from base.models.classe import Classe
from base.models.inventario import Inventario, InventarioItem
from base.models.personagem import Personagem
from base.models.pocao import Pocao
from base.serializers import ClasseSerializer
from base.util.util import valida_jogador


def logout_view(request):
    del request.session['player_id']
    logout_then_login(request, '')


class PersonagensListView(LoginRequiredMixin, View):
    login_url = '/'
    template = 'base/personagem/personagens.html'

    def get(self, request):
        jogadores = Personagem.objects.filter(user=request.user)
        return render(request, self.template, {'personagens': jogadores})


class PersonagemCreatedView(LoginRequiredMixin, View):
    login_url = '/'
    template = 'base/personagem/novo_personagem.html'

    def get(self, request):
        form = PersonagemForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = PersonagemForm(request.POST)
        if form.is_valid():
            # Obter Classe.
            classe = get_object_or_404(Classe, pk=form.cleaned_data['classe'].pk)
            # Criar o Jogador
            personagem = Personagem()
            personagem.criar_personagem(classe, request.user, form.cleaned_data['nome'])

            # Cria Invetario para o personagem
            inv = Inventario()
            inv.criar_inventario(personagem)

            p_hp = Pocao.objects.get(pk=1)
            p_energia = Pocao.objects.get(pk=2)
            p_raiva = Pocao.objects.get(pk=3)

            InventarioItem.objects.bulk_create([
                InventarioItem(id=uuid.uuid4(), pocao=p_hp, inventario=inv),
                InventarioItem(id=uuid.uuid4(), pocao=p_energia, inventario=inv),
                InventarioItem(id=uuid.uuid4(), pocao=p_raiva, inventario=inv)]
            )

            return redirect('personagens')


class PersonagemDeleteView(LoginRequiredMixin, View):
    template = 'base/personagem/personagens.html'
    login_url = '/'

    def get(self, request, player):
        personagem_deletar = Personagem.objects.get(pk=player)
        if valida_jogador(request, personagem_deletar):
            personagem_deletar.delete()
            return redirect('personagens')


class SelecionarView(LoginRequiredMixin, View):
    login_url = '/'
    template = 'base/cidade.html'

    def get(self, request):
        jogador = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, jogador):
            jogador.refresh()
            jogador.save()

        return render(request, self.template, {'personagem': jogador})

    def post(self, request):
        player = request.POST['player']
        request.session['player_id'] = player
        jogador = Personagem.objects.get(pk=player)
        jogador.refresh()
        jogador.save()
        return render(request, self.template, {'personagem': jogador})


class PesonagemDetailView(LoginRequiredMixin, View):

    template = 'base/personagem/personagem_detail.html'

    def get(self, request):
        personagem = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, personagem):
            personagem.refresh()
            inv = Inventario.objects.get(personagem=personagem)  # Feito assim para ficar mais transparente pode não ser
            itens = list(inv.itens.all())  # a melhor forma mas é mais e de facil entendimento
            return render(request, self.template, {'personagem': personagem, 'itens': itens})


def distribuir_atributo(personagem, atributo):

    personagem.refresh()
    personagem.save()
    if personagem.pontos > 0:
        if atributo == 'ataque':
            personagem.forca += 1
        elif atributo == 'agilidade':
            personagem.agilidade += 1
        elif atributo == 'inteligencia':
            personagem.inteligencia += 1
        elif atributo == 'sabedoria':
            personagem.sabedoria += 1
        elif atributo == 'carisma':
            personagem.carisma += 1
        elif atributo == 'energia':
            personagem.energia += 1
        elif atributo == 'raiva':
            personagem.raiva += 1
        personagem.pontos -= 1
        personagem.save()


class AddAtaque(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        personagem = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, personagem):
            distribuir_atributo(personagem, 'ataque')
            return redirect('personagem_detail')


class AddAgilidade(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        personagem = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, personagem):
            distribuir_atributo(personagem, 'agilidade')
            return redirect('personagem_detail')


class AddInteligencia(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        personagem = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, personagem):
            distribuir_atributo(personagem, 'inteligencia')
            return redirect('personagem_detail')


class AddSabedoria(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        personagem = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, personagem):
            distribuir_atributo(personagem, 'sabedoria')
            return redirect('personagem_detail')


class AddCarisma(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        personagem = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, personagem):
            distribuir_atributo(personagem, 'carisma')
            return redirect('personagem_detail')


class AddEnergia(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        personagem = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, personagem):
            distribuir_atributo(personagem, 'energia')
            return redirect('personagem_detail')


class AddRaiva(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        personagem = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, personagem):
            distribuir_atributo(personagem, 'raiva')
            return redirect('personagem_detail')


class ClasseViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer